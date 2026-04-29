import random
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_, or_
from bot.database.models import (
    User, Vocabulary, UserProgress, Lesson,
    SubscriptionTier, ArabicLevel, PaymentRequest, PaymentStatus
)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_id: int, username: Optional[str] = None) -> User:
        user = User(user_id=user_id, username=username)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_or_create(self, user_id: int, username: Optional[str] = None) -> tuple[User, bool]:
        user = await self.get(user_id)
        if user:
            return user, False
        user = await self.create(user_id, username)
        return user, True

    async def update(self, user_id: int, **kwargs) -> None:
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(**kwargs)
        )

    async def list_users(self, offset: int = 0, limit: int = 10) -> List[User]:
        result = await self.session.execute(
            select(User).order_by(User.join_date.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def search_users(self, query: str, limit: int = 10) -> List[User]:
        result = await self.session.execute(
            select(User).where(
                or_(
                    User.full_name.ilike(f"%{query}%"),
                    User.username.ilike(f"%{query}%"),
                )
            ).limit(limit)
        )
        return list(result.scalars().all())

    async def count_total(self) -> int:
        result = await self.session.execute(select(func.count(User.user_id)))
        return result.scalar() or 0

    async def count_new_since(self, since: datetime) -> int:
        result = await self.session.execute(
            select(func.count(User.user_id)).where(User.join_date >= since)
        )
        return result.scalar() or 0

    async def count_active_since(self, since: datetime) -> int:
        result = await self.session.execute(
            select(func.count(User.user_id)).where(User.last_active_date >= since)
        )
        return result.scalar() or 0

    async def count_by_tier(self, tier: SubscriptionTier) -> int:
        result = await self.session.execute(
            select(func.count(User.user_id)).where(User.subscription_tier == tier)
        )
        return result.scalar() or 0

    async def get_users_for_notification(self) -> List[User]:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await self.session.execute(
            select(User).where(
                and_(
                    User.is_notification_enabled == True,
                    User.is_registered == True,
                    User.is_banned == False,
                    or_(User.last_active_date < today, User.last_active_date == None),
                )
            )
        )
        return list(result.scalars().all())

    async def get_all_registered(self) -> List[User]:
        result = await self.session.execute(
            select(User).where(
                and_(User.is_registered == True, User.is_banned == False)
            )
        )
        return list(result.scalars().all())


class VocabularyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_level(self, level_id: int) -> List[Vocabulary]:
        result = await self.session.execute(
            select(Vocabulary).where(
                and_(Vocabulary.level_id == level_id, Vocabulary.is_active == True)
            )
        )
        return list(result.scalars().all())

    async def get_for_lesson(self, user_id: int, level_id: int, total: int = 15) -> List[Vocabulary]:
        new_count = int(total * 0.75)
        review_count = total - new_count
        now = datetime.utcnow()

        # Overdue review words
        review_result = await self.session.execute(
            select(Vocabulary)
            .join(UserProgress, and_(
                UserProgress.word_id == Vocabulary.word_id,
                UserProgress.user_id == user_id,
                UserProgress.next_review_date <= now,
            ))
            .where(Vocabulary.is_active == True)
            .limit(review_count)
        )
        review_words = list(review_result.scalars().all())

        # New / low-mastery words
        needed_new = new_count + max(0, review_count - len(review_words))
        new_result = await self.session.execute(
            select(Vocabulary)
            .outerjoin(UserProgress, and_(
                UserProgress.word_id == Vocabulary.word_id,
                UserProgress.user_id == user_id,
            ))
            .where(
                and_(
                    Vocabulary.level_id == level_id,
                    Vocabulary.is_active == True,
                    or_(UserProgress.id == None, UserProgress.mastery_level < 3),
                )
            )
            .limit(needed_new)
        )
        new_words = list(new_result.scalars().all())

        all_words = review_words + new_words
        # If still not enough, fill with any words from the level
        if len(all_words) < total:
            existing_ids = {w.word_id for w in all_words}
            fill_result = await self.session.execute(
                select(Vocabulary).where(
                    and_(
                        Vocabulary.level_id == level_id,
                        Vocabulary.is_active == True,
                        ~Vocabulary.word_id.in_(list(existing_ids)),
                    )
                ).limit(total - len(all_words))
            )
            all_words += list(fill_result.scalars().all())

        random.shuffle(all_words)
        return all_words[:total]

    async def get_random_wrong_translations(self, correct_word_id: int, count: int = 2) -> List[str]:
        result = await self.session.execute(
            select(Vocabulary.uzbek_translation)
            .where(Vocabulary.word_id != correct_word_id)
            .order_by(func.random())
            .limit(count)
        )
        return [row[0] for row in result.fetchall()]

    async def count_total(self) -> int:
        result = await self.session.execute(select(func.count(Vocabulary.word_id)))
        return result.scalar() or 0

    async def add_word(self, **kwargs) -> Vocabulary:
        word = Vocabulary(**kwargs)
        self.session.add(word)
        await self.session.flush()
        return word


class ProgressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, user_id: int, word_id: int) -> UserProgress:
        result = await self.session.execute(
            select(UserProgress).where(
                and_(UserProgress.user_id == user_id, UserProgress.word_id == word_id)
            )
        )
        prog = result.scalar_one_or_none()
        if not prog:
            prog = UserProgress(user_id=user_id, word_id=word_id)
            self.session.add(prog)
            await self.session.flush()
        return prog

    async def record_answer(self, user_id: int, word_id: int, is_correct: bool) -> None:
        prog = await self.get_or_create(user_id, word_id)
        now = datetime.utcnow()
        srs_intervals = [1, 3, 7, 14, 30]

        if is_correct:
            prog.times_correct += 1
            if prog.mastery_level < 5:
                prog.mastery_level += 1
            prog.next_review_date = now + timedelta(days=srs_intervals[prog.mastery_level - 1])
        else:
            prog.times_incorrect += 1
            prog.mastery_level = max(1, prog.mastery_level - 1)
            prog.next_review_date = now + timedelta(hours=4)

        prog.last_reviewed = now

    async def count_mastered(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count(UserProgress.id)).where(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.mastery_level >= 4,
                )
            )
        )
        return result.scalar() or 0

    async def get_progress_by_level(self, user_id: int) -> dict:
        """Returns {level_id: {"total": n, "seen": s, "mastered": m}}."""
        from sqlalchemy import case as sa_case
        # Total words per level
        totals_result = await self.session.execute(
            select(Vocabulary.level_id, func.count(Vocabulary.word_id))
            .where(Vocabulary.is_active == True)
            .group_by(Vocabulary.level_id)
        )
        totals = {row[0]: row[1] for row in totals_result.fetchall()}

        # Seen / mastered per level for this user
        progress_result = await self.session.execute(
            select(
                Vocabulary.level_id,
                func.count(UserProgress.id).label("seen"),
                func.sum(sa_case((UserProgress.mastery_level >= 4, 1), else_=0)).label("mastered"),
            )
            .join(UserProgress, and_(
                UserProgress.word_id == Vocabulary.word_id,
                UserProgress.user_id == user_id,
            ))
            .where(Vocabulary.is_active == True)
            .group_by(Vocabulary.level_id)
        )
        user_prog = {row[0]: {"seen": row[1], "mastered": int(row[2] or 0)} for row in progress_result.fetchall()}

        return {
            lvl: {
                "total": total,
                "seen": user_prog.get(lvl, {}).get("seen", 0),
                "mastered": user_prog.get(lvl, {}).get("mastered", 0),
            }
            for lvl, total in sorted(totals.items())
        }


class LessonRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, level_id: int) -> Lesson:
        lesson = Lesson(user_id=user_id, level_id=level_id)
        self.session.add(lesson)
        await self.session.flush()
        return lesson

    async def complete(self, lesson_id: int, correct_answers: int, xp_earned: int) -> None:
        await self.session.execute(
            update(Lesson).where(Lesson.id == lesson_id).values(
                completed_at=datetime.utcnow(),
                correct_answers=correct_answers,
                xp_earned=xp_earned,
                is_completed=True,
            )
        )

    async def count_completed_since(self, since: datetime) -> int:
        result = await self.session.execute(
            select(func.count(Lesson.id)).where(
                and_(Lesson.is_completed == True, Lesson.completed_at >= since)
            )
        )
        return result.scalar() or 0

    async def count_good_lessons_at_level(self, user_id: int, level_id: int, min_accuracy: float = 0.7) -> int:
        """Count completed lessons at a specific level meeting the minimum accuracy threshold."""
        result = await self.session.execute(
            select(Lesson).where(
                and_(
                    Lesson.user_id == user_id,
                    Lesson.level_id == level_id,
                    Lesson.is_completed == True,
                )
            )
        )
        lessons = result.scalars().all()
        return sum(
            1 for l in lessons
            if l.total_questions > 0 and (l.correct_answers / l.total_questions) >= min_accuracy
        )

    async def count_by_user_today(self, user_id: int) -> int:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await self.session.execute(
            select(func.count(Lesson.id)).where(
                and_(
                    Lesson.user_id == user_id,
                    Lesson.is_completed == True,
                    Lesson.completed_at >= today,
                )
            )
        )
        return result.scalar() or 0

    async def total_xp_by_user(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.sum(Lesson.xp_earned)).where(
                and_(Lesson.user_id == user_id, Lesson.is_completed == True)
            )
        )
        return result.scalar() or 0


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        tier: SubscriptionTier,
        amount: int,
        photo_file_id: str,
    ) -> PaymentRequest:
        req = PaymentRequest(
            user_id=user_id,
            tier=tier,
            amount=amount,
            photo_file_id=photo_file_id,
        )
        self.session.add(req)
        await self.session.flush()
        return req

    async def get(self, request_id: int) -> Optional[PaymentRequest]:
        result = await self.session.execute(
            select(PaymentRequest).where(PaymentRequest.id == request_id)
        )
        return result.scalar_one_or_none()

    async def set_admin_message_id(self, request_id: int, message_id: int) -> None:
        await self.session.execute(
            update(PaymentRequest)
            .where(PaymentRequest.id == request_id)
            .values(admin_message_id=message_id)
        )

    async def approve(self, request_id: int) -> None:
        await self.session.execute(
            update(PaymentRequest)
            .where(PaymentRequest.id == request_id)
            .values(status=PaymentStatus.APPROVED, processed_at=datetime.utcnow())
        )

    async def decline(self, request_id: int, reason: str = "") -> None:
        await self.session.execute(
            update(PaymentRequest)
            .where(PaymentRequest.id == request_id)
            .values(
                status=PaymentStatus.DECLINED,
                processed_at=datetime.utcnow(),
                decline_reason=reason,
            )
        )

    async def count_pending(self) -> int:
        result = await self.session.execute(
            select(func.count(PaymentRequest.id)).where(
                PaymentRequest.status == PaymentStatus.PENDING
            )
        )
        return result.scalar() or 0

    async def list_pending(self, limit: int = 20) -> List[PaymentRequest]:
        result = await self.session.execute(
            select(PaymentRequest)
            .where(PaymentRequest.status == PaymentStatus.PENDING)
            .order_by(PaymentRequest.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_users_with_expired_subscriptions(self) -> List[User]:
        now = datetime.utcnow()
        result = await self.session.execute(
            select(User).where(
                and_(
                    User.subscription_expires <= now,
                    User.subscription_tier != SubscriptionTier.FREE,
                    User.is_registered == True,
                    User.is_banned == False,
                )
            )
        )
        return list(result.scalars().all())

    async def get_users_for_trial(self) -> List[User]:
        """Users who registered yesterday, are free, and haven't got trial yet."""
        now = datetime.utcnow()
        yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59)
        result = await self.session.execute(
            select(User).where(
                and_(
                    User.join_date >= yesterday_start,
                    User.join_date <= yesterday_end,
                    User.subscription_tier == SubscriptionTier.FREE,
                    User.trial_given == False,
                    User.is_registered == True,
                    User.is_banned == False,
                )
            )
        )
        return list(result.scalars().all())

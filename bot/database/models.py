import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean,
    Enum as SAEnum, ForeignKey, Text, Index
)
from sqlalchemy.orm import relationship
from bot.database.base import Base


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    UNLIMITED = "unlimited"


class ArabicLevel(str, enum.Enum):
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False, default="")
    age = Column(Integer, nullable=True)
    arabic_level = Column(SAEnum(ArabicLevel), default=ArabicLevel.BEGINNER, nullable=False)
    current_level = Column(Integer, default=1, nullable=False)
    current_xp = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=0, nullable=False)
    last_active_date = Column(DateTime, nullable=True)
    subscription_tier = Column(SAEnum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    shijoat_points = Column(Integer, default=100, nullable=False)
    last_shijoat_reset = Column(DateTime, default=datetime.utcnow, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_registered = Column(Boolean, default=False, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    is_notification_enabled = Column(Boolean, default=True, nullable=False)
    subscription_expires = Column(DateTime, nullable=True)
    trial_given = Column(Boolean, default=False, nullable=False)
    achievements_earned = Column(Text, nullable=True, default="")
    shijoat_pin_id = Column(Integer, nullable=True)

    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="user", cascade="all, delete-orphan")
    payment_requests = relationship("PaymentRequest", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_join_date", "join_date"),
        Index("idx_users_last_active", "last_active_date"),
    )


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    word_id = Column(Integer, primary_key=True, autoincrement=True)
    arabic_word = Column(String(255), nullable=False)
    uzbek_translation = Column(String(255), nullable=False)
    transliteration = Column(String(255), nullable=True)
    example_sentence_arabic = Column(Text, nullable=True)
    example_sentence_uzbek = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    level_id = Column(Integer, nullable=False, default=1)
    telegram_audio_file_id = Column(String(500), nullable=True)
    telegram_photo_file_id = Column(String(500), nullable=True)
    difficulty = Column(Integer, default=1)
    is_active = Column(Boolean, default=True, nullable=False)

    progress = relationship("UserProgress", back_populates="vocabulary")

    __table_args__ = (
        Index("idx_vocab_level", "level_id"),
    )


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("vocabulary.word_id", ondelete="CASCADE"), nullable=False)
    mastery_level = Column(Integer, default=1, nullable=False)
    next_review_date = Column(DateTime, nullable=True)
    times_correct = Column(Integer, default=0, nullable=False)
    times_incorrect = Column(Integer, default=0, nullable=False)
    last_reviewed = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
    vocabulary = relationship("Vocabulary", back_populates="progress")

    __table_args__ = (
        Index("idx_progress_user_word", "user_id", "word_id", unique=True),
        Index("idx_progress_review_date", "next_review_date"),
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    total_questions = Column(Integer, default=15, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    shijoat_used = Column(Integer, default=10, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    level_id = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="lessons")

    __table_args__ = (
        Index("idx_lessons_user_date", "user_id", "started_at"),
        Index("idx_lessons_date", "started_at"),
    )


class PaymentRequest(Base):
    __tablename__ = "payment_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    tier = Column(SAEnum(SubscriptionTier), nullable=False)
    amount = Column(Integer, nullable=False)
    photo_file_id = Column(String(500), nullable=False)
    status = Column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    admin_message_id = Column(Integer, nullable=True)
    decline_reason = Column(String(500), nullable=True)

    user = relationship("User", back_populates="payment_requests")

    __table_args__ = (
        Index("idx_payment_status", "status"),
        Index("idx_payment_user", "user_id"),
    )

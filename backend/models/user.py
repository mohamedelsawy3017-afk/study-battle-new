# models/user.py - User database model
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Gamification
    study_score = Column(Float, default=0.0)  # Total minutes studied
    level = Column(Integer, default=1)
    badge = Column(String(50), default="Rookie")  # Current badge/rank title

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username} | Score: {self.study_score}>"


# Level thresholds and badge names
LEVEL_THRESHOLDS = [
    (0, 1, "Rookie 🐣"),
    (30, 2, "Warming Up 🔥"),
    (120, 3, "Focused 🎯"),
    (300, 4, "Grinder 💪"),
    (600, 5, "Scholar 📚"),
    (1200, 6, "Beast Mode 🦁"),
    (2400, 7, "Legend 👑"),
]


def compute_level_and_badge(score: float) -> tuple[int, str]:
    """Compute level and badge from study score (minutes)."""
    current_level, current_badge = 1, "Rookie 🐣"
    for threshold, level, badge in LEVEL_THRESHOLDS:
        if score >= threshold:
            current_level, current_badge = level, badge
    return current_level, current_badge

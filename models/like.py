from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP
from database import Base

class Like(Base):
    __tablename__ = "likes"
    
    __table_args__ = (
        UniqueConstraint("user_id", "blog_id", name="uq_user_blog_like"),
        Index("ix_like_user_blog", "user_id", "blog_id"),
        {"comment": "Tracks user likes for blog posts"}
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),  
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True,
        comment="UTC timestamp when like was created"
    )
    
    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id", ondelete="CASCADE"),
        index=True,
        comment="Reference to blog post"
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        comment="Reference to liking user"
    )
    
    user: Mapped["User"] = relationship(
        back_populates="likes",
        lazy="selectin",
        innerjoin=True
    )
    
    blog: Mapped["Blog"] = relationship(
        back_populates="likes",
        lazy="selectin",
        innerjoin=True
    )

    def __repr__(self):
        return f"<Like(id={self.id}, user={self.user_id}, blog={self.blog_id}, created={self.created_at.isoformat()})>"

    @property
    def created_at_utc(self) -> datetime:
        return self.created_at if self.created_at.tzinfo else self.created_at.replace(tzinfo=timezone.utc)

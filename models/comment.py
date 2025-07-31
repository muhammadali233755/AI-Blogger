from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))

    user: Mapped["User"] = relationship("User", back_populates="comments")
    blog: Mapped["Blog"] = relationship("Blog", back_populates="comments")

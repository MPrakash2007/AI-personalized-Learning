from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    subject = Column(String(100), nullable=True, index=True)  # Subject context name or slug (DBMS, OS, etc.)
    title = Column(String(200), default="Study Session")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")

    __table_args__ = (
        Index("ix_chat_sessions_user_updated", "user_id", "updated_at"),
    )

    @property
    def conversation_id(self) -> int:
        return self.id

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(String(20), nullable=False)  # "user" / "student", "assistant" / "ai"
    message = Column(Text, nullable=False)
    quick_check_json = Column(Text, nullable=True)  # JSON with interactive question: {question, options, correct, explanation}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    session = relationship("ChatSession", back_populates="messages")

    __table_args__ = (
        Index("ix_chat_messages_session_created", "session_id", "created_at"),
    )

    @property
    def conversation_id(self) -> int:
        return self.session_id

    @property
    def role(self) -> str:
        return "user" if self.sender in ("student", "user") else "assistant"

    @property
    def content(self) -> str:
        return self.message

# Aliases for explicit AI terminology
AIConversation = ChatSession
AIMessage = ChatMessage

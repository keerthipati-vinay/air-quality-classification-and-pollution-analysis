from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    relationship
)

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )
    role = Column(
        String,
        default="user"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    history = relationship(
    "PredictionHistory",
    back_populates="user"
   )
    
class PredictionHistory(Base):

    __tablename__ = (
        "prediction_history"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        )
    )


    AQI = Column(Float)

    predicted_category = Column(
        String
    )

    confidence = Column(
        Float
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="history"
    )
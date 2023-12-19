from uuid import uuid4
import datetime
from sqlalchemy import Column, String, Boolean, Enum, Text, TIMESTAMP, Index, Integer, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class BaseModel:
    """Base Model class"""
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class User(BaseModel, Base):
    """User class"""
    __tablename__ = 'users'
    user_id = Column(String(60), nullable=False,
                     primary_key=True, default=lambda: str(uuid4()))
    fullname = Column(String(30), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String(225), nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    phone1 = Column(String(15), nullable=False)
    phone2 = Column(String(15))
    about = Column(Text)
    address = Column(String(50), nullable=False)
    town = Column(String(30), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(20), nullable=False)
    items = relationship('Item', back_populates='user')
    ratings = relationship('Rating', back_populates='user')
    likes = relationship('Like', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    # Define the sent_messages relationship
    sent_messages = relationship('Chat', foreign_keys='Chat.sender_id',
                                 back_populates='sender', cascade='all, delete-orphan')

    # Define the received_messages relationship
    received_messages = relationship(
        'Chat', foreign_keys='Chat.receiver_id', back_populates='receiver', cascade='all, delete-orphan')

    __table_args__ = (Index('idx_users_user_id', 'user_id'),)

    def to_dict(self):
        """Convert user object to dictionary"""
        user_dict = {
            'user_id': self.user_id,
            'fullname': self.fullname,
            'verified': self.verified,
            'email': self.email,
            'gender': self.gender,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'about': self.about,
            'address': self.address,
            'town': self.town,
            'city': self.city,
            'state': self.state,
        }
        return user_dict


class Item(BaseModel, Base):
    """Item class"""
    __tablename__ = 'items'
    item_id = Column(String(36), nullable=False, primary_key=True,
                     default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id', ondelete='CASCADE'),
                     nullable=False)
    item_name = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(200), nullable=False)
    photo1 = Column(String(225), nullable=False)
    photo2 = Column(String(225))
    photo3 = Column(String(225))
    sold = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Define a relationship with the User class
    user = relationship('User', back_populates='items')
    likes = relationship('Like', back_populates='items')
    comments = relationship('Comment', back_populates='items')

    __table_args__ = (Index('idx_items_item_id', 'item_id'),)

    def to_dict(self):
        """Convert item object to dictionary"""
        user_dict = {
            'user_id': self.user_id,
            'item_name': self.item_name,
            'description': self.description,
            'price': self.price,
            'photo1': self.photo1,
            'photo2': self.photo2,
            'photo3': self.photo3,
            'sold': self.sold,
        }
        return user_dict


class Comment(BaseModel, Base):
    """Comment class"""
    __tablename__ = 'comments'
    comment_id = Column(String(36), nullable=False, primary_key=True,
                        default=lambda: str(uuid4()))
    commenter = Column(String(36), ForeignKey(
        'users.user_id', ondelete='CASCADE'), nullable=False)
    item_id = Column(String(36), ForeignKey(
        'items.item_id', ondelete='CASCADE'),  nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Define relationships with User and Item classes
    user = relationship('User', back_populates='comments')
    items = relationship('Item', back_populates='comments')

    def to_dict(self):
        """Convert rating object to dictionary"""
        comment_dict = {
            'comment_id': self.comment_id,
            'item_id': self.item_id,
            'commenter': self.commenter,
            'comment': self.comment,
            'created_at': self.created_at,
        }
        return comment_dict


class Chat(BaseModel, Base):
    """Chat class"""
    __tablename__ = 'chats'
    message_id = Column(String(36), nullable=False, primary_key=True,
                        default=lambda: str(uuid4()))
    sender_id = Column(String(36), ForeignKey('users.user_id', ondelete='CASCADE'),
                       nullable=False)
    receiver_id = Column(String(36), ForeignKey(
        'users.user_id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Define relationships with User classes
    sender = relationship('User', foreign_keys=[
                          sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[
                            receiver_id], back_populates='received_messages')

    def to_dict(self):
        """
        - Convert chat object to dictionary
        """
        chat_data = {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message': self.message,
            'created_at': self.created_at,
        }
        return chat_data


class Like(BaseModel, Base):
    """Like class"""
    __tablename__ = 'likes'

    item_id = Column(String(36), ForeignKey('items.item_id', ondelete='CASCADE'),
                     nullable=False, primary_key=True)
    user_id = Column(String(36), ForeignKey('users.user_id', ondelete='CASCADE'),
                     nullable=False, primary_key=True)
    liked = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Define relationships with User and Item class
    user = relationship('User', back_populates='likes')
    items = relationship('Item', back_populates='likes')

    def to_dict(self):
        """Convert rating object to dictionary"""
        like_dict = {
            'user_id': self.user_id,
            'item_id': self.item_id,
            'liked': self.liked,
            'created_at': self.created_at,
        }
        return like_dict


class Rating(Base):
    """Rating class"""
    __tablename__ = 'ratings'

    rating_id = Column(String(36), primary_key=True,
                       default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey(
        'users.user_id', ondelete='CASCADE'), nullable=False)
    rating = Column(Enum('1', '2', '3', '4', '5'), nullable=False)
    comment = Column(String(225))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    # Define a relationship with the User class
    user = relationship('User', back_populates='ratings')

    def to_dict(self):
        """Convert rating object to dictionary"""
        user_dict = {
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
        }
        return user_dict


class UserSession(Base):
    """
    UserSession model class
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

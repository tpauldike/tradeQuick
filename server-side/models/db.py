from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.tables import Base
from sqlalchemy.pool import QueuePool
from sqlalchemy import inspect

load_dotenv()

database = getenv("dbName")
user = getenv("dbUser")
host = getenv("dbHost")
password = getenv("dbPasswd")
port = getenv("dbPort")


def create_engine_with_session():
    """Create SQLAlchemy engine and scoped session."""
    engine = create_engine(
        f'mysql+mysqldb://{user}:{password}@{host}:{port}/{database}', pool_pre_ping=True, poolclass=QueuePool, pool_size=5, max_overflow=10)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    Session = scoped_session(session_factory)
    return engine, Session


class DBStorage:
    def __init__(self):
        """Initialize the DBStorage instance."""
        self.__engine, self.__session = create_engine_with_session()
        Base.metadata.create_all(self.__engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def all(self, cls=None):
        """Return a dictionary of all objects of a given class."""
        objects = {}
        for name, class_ in inspect.getmembers(Base.classes):
            if cls is None or cls == class_:
                objs = self.__session.query(class_).all()
                for obj in objs:
                    key = f'{type(obj).__name__}.{obj.id}'
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add a new object to the session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit changes to the database."""
        try:
            self.__session.commit()
        except Exception as e:
            print(f"Error during save: {e}")
            self.__session.rollback()
            raise e

    def delete(self, obj=None):
        """Delete an object from the session."""
        try:
            if obj:
                self.__session.delete(obj)
        except Exception as e:
            print(f"Error during delete: {e}")
            self.__session.rollback()
            raise e

    def reload(self):
        """Create all tables and reset the session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Close the session."""
        self.__session.close()

    def find_user_by_email(self, email):
        """Find a user by email."""
        from models.tables import User
        try:
            return self.__session.query(User).filter_by(email=email).first()
        except Exception as e:
            print(f"Error during find_user_by_email: {e}")
            return None

    def find_user_by_id(self, user_id):
        """Find a user by id."""
        from models.tables import User
        try:
            return self.__session.query(User).filter_by(user_id=user_id).first()
        except Exception as e:
            print(f"Error during find_user_by_id: {e}")
            return None

    def find_all_users(self):
        """Find all users."""
        from models.tables import User
        try:
            return self.__session.query(User).all()
        except Exception as e:
            print(f"Error during find_all_users: {e}")
            return None

    def create_user(self, user_data):
        """Create a user."""
        from models.tables import User
        try:
            user = User(**user_data)
            self.new(user)
            self.save()
            return user
        except Exception as e:
            print(f"Error during create_user: {e}")
            return None

    def create_session(self, session_data):
        """Create a session."""
        from models.tables import UserSession
        try:
            session = UserSession(**session_data)
            self.new(session)
            self.save()
            return session
        except Exception as e:
            print(f"Error during create_session: {e}")
            return None

    def find_session_by_id(self, session_id):
        """Find a session by id."""
        from models.tables import UserSession
        try:
            return self.__session.query(UserSession).filter_by(session_id=session_id).first()
        except Exception as e:
            print(f"Error during find_session_by_id: {e}")
            return None
        
    def find_session_by_id_by_user_id(self, user_id):
        """Find a session by user_id."""
        from models.tables import UserSession
        try:
            return self.__session.query(UserSession).filter_by(user_id=user_id).first()
        except Exception as e:
            print(f"Error during find_session_by_id: {e}")
            return None

    def delete_session(self, session):
        """Delete a session."""
        from models.tables import UserSession
        try:
            self.delete(session)
            self.save()
        except Exception as e:
            print(f"Error during delete_session: {e}")

    def delete_user(self, user):
        """Delete a user."""
        from models.tables import User
        try:
            self.delete(user)
            self.save()
        except Exception as e:
            print(f"Error during delete_user: {e}")

    def create_item(self, item_data):
        """Create an item."""
        from models.tables import Item
        try:
            item = Item(**item_data)
            self.new(item)
            self.save()
            return item
        except Exception as e:
            print(f"Error during create_item: {e}")
            return None

    def get_items(self):
        """Get all items."""
        from models.tables import Item
        try:
            return self.__session.query(Item).all()
        except Exception as e:
            print(f"Error during get_items: {e}")
            return None

    def get_items_by_user_id(self, user_id):
        """
        -  Retreive all items by user_id
        """
        from models.tables import Item
        try:
            return self.__session.query(Item).filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error during get_items_by_user_id: {e}")
            return None

    def item_by_item_id(self, item_id):
        """
        -  Retreive an item by item_id
        """
        from models.tables import Item
        try:
            return self.__session.query(Item).filter_by(item_id=item_id).first()
        except Exception as e:
            print(f"Error during get_item_by_item_id: {e}")
            return None
        
    def find_items_by_item_id(self, item_id):
        """
        -  Retreive an item by item_id
        """
        from models.tables import Item
        try:
            return self.__session.query(Item).filter_by(item_id=item_id).first()
        except Exception as e:
            print(f"Error during get_item_by_item_id: {e}")
            return None

    def update_item_by_item_id(self, item_id, item_data):
        """
        -  Update an item by item_id
        """
        from models.tables import Item
        try:
            item = self.__session.query(
                Item).filter_by(item_id=item_id).first()
            for key, value in item_data.items():
                setattr(item, key, value)
            self.save()
            return item
        except Exception as e:
            print(f"Error during update_item_by_item_id: {e}")
            return None

    def delete_item_by_item_id(self, item_id):
        """
        -  Delete an item by item_id
        """
        from models.tables import Item
        try:
            item = self.__session.query(
                Item).filter_by(item_id=item_id).first()
            self.delete(item)
            self.save()
        except Exception as e:
            print(f"Error during delete_item_by_item_id: {e}")
            return None

    def create_rating(self, rating_data):
        """
        -  Create a rating
        """
        from models.tables import Rating
        try:
            rating = Rating(**rating_data)
            self.new(rating)
            self.save()
            return rating
        except Exception as e:
            print(f"Error during create_rating: {e}")
            return None

    def get_all_ratings(self):
        """
        - Retreive all ratings
        """
        from models.tables import Rating
        try:
            return self.__session.query(Rating).all()
        except Exception as e:
            print(f"Error during get_all_ratings: {e}")
            return None
    
    def get_ratings_by_user_id(self, user_id):
        """
        - Retrieve ratings based on user_id
        """
        from models.tables import Rating
        try:
            return self.__session.query(Rating).filter_by(user_id=user_id).first()
        except Exception as e:
            print(f"Error during retriving ratings: {e}")
            return None

    def create_like(self, like_data):
        """
        -  Create a like
        """
        from models.tables import Like
        try:
            like = Like(**like_data)
            self.new(like)
            self.save()
            return like
        except Exception as e:
            print(f"Error during create_like: {e}")
            return None

    def get_like_by_item_id(self, item_id):
        """
        - Retrieve like by item_id
        """
        from models.tables import Like
        try:
            return self.__session.query(Like).filter_by(item_id=item_id).first()
        except Exception as e:
            print(f"Error during get_like_by_user_id: {e}")
            return None

    def get_like_by_item_id_all(self, item_id):
        """
        - Retrieve like by item_id
        """
        from models.tables import Like
        try:
            return self.__session.query(Like).filter_by(item_id=item_id).all()
        except Exception as e:
            print(f"Error during get_like_by_user_id: {e}")
            return None

    def create_comment(self, comment_data):
        """
        -  Create a comment
        """
        from models.tables import Comment
        try:
            comment = Comment(**comment_data)
            self.new(comment)
            self.save()
            return comment
        except Exception as e:
            print(f"Error during create_comment: {e}")
            return None

    def get_comments_by_comment_id(self, comment_id):
        """
        - Retrieve comment by comment_id
        """
        from models.tables import Comment
        try:
            return self.__session.query(Comment).filter_by(comment_id=comment_id).first()
        except Exception as e:
            print(f"Error during get_comment: {e}")
            return None

    def get_comments_by_item_id(self, item_id):
        """
        - Retrieve comment by item_id
        """
        from models.tables import Comment
        try:
            return self.__session.query(Comment).filter_by(item_id=item_id).all()
        except Exception as e:
            print(f"Error during get_comment: {e}")
            return None

    def create_message(self, message_data):
        """
        - Create new message
        """
        from models.tables import Chat
        try:
            message = Chat(**message_data)
            self.new(message)
            self.save()
            return message
        except Exception as e:
            print(f"Error during create_message: {e}")
            return None

    def get_messages_by_message_id(self, message_id):
        """
        - Retreive a message based on their messsage_id
        """
        from models.tables import Chat
        try:
            return self.__session.query(Chat).filter_by(message_id=message_id).first()
        except Exception as e:
            print(f"Error during get_messages: {e}")
            return None

    def get_messages_by_user_id(self, sender_id):
        """
        - Retreive all messages based on their user_id
        """
        from models.tables import Chat
        try:
            return self.__session.query(Chat).filter_by(sender_id=sender_id).all()
        except Exception as e:
            print(f"Error during get_messages: {e}")
            return None

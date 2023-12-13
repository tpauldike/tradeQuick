from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.tables import Base
from sqlalchemy import inspect

load_dotenv()

database = getenv("dbName")
user = getenv("dbUser")
host = getenv("dbHost")
password = getenv("dbPasswd")


def create_engine_with_session():
    """Create SQLAlchemy engine and scoped session."""
    engine = create_engine(
        f'mysql+mysqldb://{user}:{password}@{host}/{database}', pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    Session = scoped_session(session_factory)
    return engine, Session


class DBStorage:
    def __init__(self):
        """Initialize the DBStorage instance."""
        self.__engine, self.__session = create_engine_with_session()

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
        if obj:
            self.__session.delete(obj)

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

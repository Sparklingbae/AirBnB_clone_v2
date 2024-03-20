#!/usr/bin/python3
"""Database storage"""
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database storage class
    Attributes: __engine, __session
    """
    __engine = None
    __session = None
    __allowed_cls = [User, State, City, Place, Amenity, Review]

    def __init__(self):
        """Creates the engine"""

        self.__url = URL.create("mysql+mysqldb",
                                username=getenv('HBNB_MYSQL_USER'),
                                password=getenv('HBNB_MYSQL_PWD'),
                                host=getenv('HBNB_MYSQL_HOST'),
                                database=getenv('HBNB_MYSQL_DB'))
        self.__engine = create_engine(self.__url, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None) -> dict:

        cls_objs = {}
        obj_list = []
        if cls:
            if type(cls) is str:
                cls = eval(cls)
                if cls in self.__allowed_cls:
                    obj_list = self.__session.query(cls).all()
        else:
            for clss in self.__allowed_cls:
                obj_list.extend(self.__session.query(clss).all())

        for obj in obj_list:
            key = f"{type(obj).__name__}.{obj.id}"
            cls_objs.update({key: obj})
        return cls_objs

    def new(self, obj):
        """Method that adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Method that commits all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Method that deletes from the current database
        session obj if not None"""

        if obj:
            self.__session.delete(obj)

    def reload(self) -> None:
        """Method that creates all tables in the database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Method that closes the session"""
        self.__session.close()

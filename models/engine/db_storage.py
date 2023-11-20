#!/usr/bin/python3
""" A module that dedines the database storage """

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage():
    """ A class that interacts with the database """
    __engine = None
    __session = None


    def __init__(self):
        _user = ""
        _psswd = ""
        _host = ""
        _db = ""

        self.__engine = create_engine(
            f"mysql+mysqldb://{_user}:{_psswd}@{_host}/{_db}",
            pool_pre_ping=True
            )

    def all(self, cls=None):
        """ Query the database session """
        if cls:
            res = self.__session.query(cls).all()
        else:
            res = self.__session.query(State).all()
            res.extend(self.__session.query(User).all())

        return {f"{type(obj).__name__}.{obj.id}": obj for obj in res}

    def new(self, obj):
        """ Add obj to the current database session """
        self.__session.add(obj)


    def save(self):
        """ Commits all changes to current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete obj from the current database session if ! None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database
            Creates the current database session(self.__session)
                from self.__engine
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False
            )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ call remove() method on the private session attribute
            (self.__session) tips or close()
            on the class Session tips
        """
        self.__session.close()

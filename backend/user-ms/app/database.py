from sqlalchemy import create_engine
import sqlalchemy.ext.declarative as declarative
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy.orm as orm
import pymysql

DATABASE_URL = "mysql+pymysql://root:1111@user-db:3306/users"

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
	create_database(engine.url)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
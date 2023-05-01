from sqlalchemy import create_engine, MetaData
import sqlalchemy.ext.declarative as declarative
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy.orm as orm
import pymysql

DB_URL = "mysql+pymysql://root:1111@user-db:3306/db"

engine = create_engine(DB_URL)
if not database_exists(engine.url):
	create_database(engine.url)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False,\
								bind=engine)
Base = declarative.declarative_base()

Base.metadata.drop_all(bind=engine)

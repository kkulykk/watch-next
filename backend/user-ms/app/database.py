from sqlalchemy import create_engine, MetaData
import sqlalchemy.ext.declarative as declarative
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy.orm as orm
import pymysql
import os

password = os.getenv('ROOTPASS')
DB_URL = f"mysql+pymysql://root:{password}@user-db:3306/db"

engine = create_engine(DB_URL)
if not database_exists(engine.url):
	create_database(engine.url)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False,\
								bind=engine)
Base = declarative.declarative_base()

Base.metadata.drop_all(bind=engine)

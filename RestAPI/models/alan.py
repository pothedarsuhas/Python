from sqlalchemy import *
import sqlite3

db = create_engine("sqlite:///C:\\Users\\1338826\\PycharmProjects\\Flask\\project\\Django.db", echo = True)

meta = MetaData(db)

alan = Table(
    'alan', meta,
    Column('name', String),
    Column('price', Integer),
)

meta.create_all(db)
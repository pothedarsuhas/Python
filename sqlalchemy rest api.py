# basic api bundle for a single path, backed up with the
# inbuilt database, all in one

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import *
import sqlite3

# con = sqlite3.connect('Django.db')
# sql = "create table if not exists alan(name varchar2(150), price number)"
# cur = con.cursor()
# cur.execute(sql)
# con.close()

db = create_engine("sqlite:///C:\\Users\\1338826\\PycharmProjects\\Flask\\Django.db", echo = True)

meta = MetaData(db)

alan = Table(
    'alan', meta,
    Column('name', String),
    Column('price', Integer),
)

meta.create_all(db)
app = Flask(__name__)
api = Api(app)


class ItemList(Resource):
    def get(self): #tested
        con = db.connect()
        result = alan.select()
        rows=con.execute(result)
        return {"result": str(rows.fetchall())}


class Item(Resource):

    def get(self, name): #tested
        con = db.connect()
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required=True)
        con.execute(alan.select().where(alan.c.name == name))
        return {"result": "{} found".format(name)}

    def post(self, name): #tested
        con = db.connect()
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required=True)
        data = request.get_json()
        price = data['price']
        con.execute(alan.insert().values(name = name, price = price))
        return {"result": str(name) + " created"}

    def put(self, name): #tested
        con = db.connect()
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required=True)
        data = request.get_json()
        price = data['price']
        result = con.execute(alan.select().where(alan.c.name == name))
        if result.fetchone() == None:
            result = con.execute(alan.insert().values(name = name, price = price))
            return {"message": "{} created".format(name)}
        else:
            result = con.execute(alan.update().where(alan.c.name == name).values(price = price))
            return {"message": "{} updated".format(name)}

    def delete(self, name): #tested
        con = db.connect()
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required=True)
        result = con.execute(alan.delete().where(alan.c.name == name))
        result = con.execute(alan.select().where(alan.c.name == name))
        result = result.fetchall()

        return {"message": "{} deleted".format(name)}


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == "__main__":
    app.run(port=5553, debug=True)  # any port can be used here

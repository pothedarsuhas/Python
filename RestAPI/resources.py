from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models import *

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
        result = con.execute(alan.select().where(alan.c.name == name))
        return {"result": str(result.fetchall())}

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
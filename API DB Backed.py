#basic api bundle for a single path, backed up with the
#inbuilt database, all in one

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3

con = sqlite3.connect('Django.db')
sql = "create table if not exists alan(name varchar2(150), price number)"
cur = con.cursor()
cur.execute(sql)
con.close()

app = Flask(__name__)
api = Api(app)

class ItemList(Resource):
    
    def get(self):
        con = sqlite3.connect('Django.db')
        sql = "select * from alan"
        cur = con.cursor()
        result = cur.execute(sql)
        result = result.fetchall()
        con.close()
        return { "result" : str(result) }

    
class Item(Resource):
    
    def get(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required = True )
        con = sqlite3.connect('Django.db')
        sql = "select * from alan where name = ?"
        cur = con.cursor()
        result = cur.execute(sql,(name,))
        result = result.fetchall()
        cur.execute("commit")
        con.close()
        return { "result" : "{} created".format(name) }

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required = True )
        data = request.get_json()
        price = data['price']
        con = sqlite3.connect('Django.db')
        sql = "insert into alan values(?,?)"
        cur = con.cursor()
        result = cur.execute(sql, (name, price))
        cur.execute("commit")
        result = result.fetchall()
        con.close()
        return { "result" : str(result)+" created" }

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required = True )
        data = request.get_json()
        price = data['price']
        con = sqlite3.connect('Django.db')
        sql = "select * from alan where name = ?"
        cur = con.cursor()
        result = cur.execute(sql, (name, ))
        if result.fetchone() == None:
            sql = "insert into alan values(?,?)"
            cur = con.cursor()
            result = cur.execute(sql, (name, price))
            cur.execute("commit")
            con.close()
            return {"message" : "{} created".format(name)}
        else:
            sql = "update alan set price = ? where name = ?"
            cur = con.cursor()
            result = cur.execute(sql, (price, name))
            cur.execute("commit")
            con.close()
            return {"message" : "{} updated".format(name)}

    def delete(self, name):
        parser =reqparse.RequestParser()
        parser.add_argument(name, help="pass name", required = True )
        con = sqlite3.connect('Django.db')
        sql = "delete from alan where name = ?"
        cur = con.cursor()
        result = cur.execute(sql, (name,))
        cur.execute("commit")
        result = result.fetchall()
        return {"message" : "{} deleted".format(name)}

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__=="__main__":
  app.run(port = 5052, debug = True) #any port can be used here



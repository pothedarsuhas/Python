from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, ForeignKey, select, and_, or_, asc, desc, between, func, join
from sqlalchemy.sql import select
import sqlite3

def prints(rows):
   for row in rows:
      print(row)

engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()

students = Table(
   'students', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String),
   Column('lastname', String),
)

addresses = Table(
   'addresses', meta,
   Column('id', Integer, primary_key = True),
   Column('st_id', Integer, ForeignKey('students.id')),
   Column('postal_add', String),
   Column('email_add', String))


meta.create_all(engine) # this is idempotent

con = engine.connect()



ins = students.insert().values(name='shazam',lastname='pothedar')  #this is insert
con = engine.connect()
result = con.execute(ins)
print(result)



con.execute(students.insert(), [
   {'name':'Rajiv', 'lastname' : 'Khanna'},
   {'name':'Komal','lastname' : 'Bhandari'},
   {'name':'Abdul','lastname' : 'Sattar'},
   {'name':'Priya','lastname' : 'Rajhans'},
])

con.execute(addresses.insert(), [ #inserting with the corresponding id in students table
   {'st_id':1, 'postal_add':'Shivajinagar Pune', 'email_add':'ravi@gmail.com'},
   {'st_id':1, 'postal_add':'ChurchGate Mumbai', 'email_add':'kapoor@gmail.com'},
   {'st_id':3, 'postal_add':'Jubilee Hills Hyderabad', 'email_add':'komal@gmail.com'},
   {'st_id':5, 'postal_add':'MG Road Bangaluru', 'email_add':'as@yahoo.com'},
   {'st_id':2, 'postal_add':'Cannought Place new Delhi', 'email_add':'admin@khanna.com'},
])

updat = students.update().where(students.c.id <= 3).values(lastname = 'POTHEDAR') #this is update
con.execute(updat)

dele = students.delete().where(students.c.id > 0) #this is delete
con.execute(dele)

dele = addresses.delete().where(addresses.c.id > 5) #this is delete
con.execute(dele)

select = students.select().where(students.c.id > 0) # c is alias for column #this is select
result = con.execute(select)
for row in result:
   print(row)

select = addresses.select()
rows = con.execute(select)
for row in rows:
   print(row)

# join = select([students, addresses]).where(students.c.id == addresses.c.st_id) #performing a join
# rows = con.execute(join)
# prints(rows)

# stmt = students.update().values({
#    students.c.name:'xyz',
#    addresses.c.email_add:'abc@xyz.com'
# }).where(students.c.id == addresses.c.id) #update using join
# rows = con.execute(stmt)
# prints(rows)
# sqlite3 gives the forllowing error
# NotImplementedError: This backend does not support multiple-table criteria within UPDATE

rows = con.execute(text("select * from students"))

for row in rows:
   print(row)

# stmt = table1.update(preserve_parameter_order = True).\
#    values([(table1.c.y, 20), (table1.c.x, table1.c.y + 10)])
# con.execute(stmt)
# usage of set statement in sql in sqlalchemy for "UPDATE table1 SET y = 20, x = y + 10"

# stmt = users.delete().\
#    where(users.c.id == addresses.c.id).\
#    where(addresses.c.email_address.startswith('xyz%'))
# con.execute(stmt)
# DELETE FROM users USING addresses
# WHERE users.id = addresses.id
# AND (addresses.email_address LIKE %(email_address_1)s || '%%')

a = students.select()
b = addresses.select()
prints(con.execute(a))
prints(con.execute(b))
j = students.join(addresses, students.c.id == addresses.c.st_id)
stmt = select([students]).select_from(j)
result = con.execute(stmt)
prints(result)

con = sqlite3.connect("college.db")
cur = con.cursor()
sql = "select * from students"
cur.execute(sql)
result = cur.fetchall()
print(result)
con.commit()

stmt = select([students]).where(and_(students.c.name == 'Rajiv', students.c.id > 0))
#stmt = select([students]).where(or_(students.c.name == 'Ravi', students.c.id == 1))
rows = con.execute(stmt)
print(rows.fetchall())


stmt = select([students]).order_by(asc(students.c.id))
stmt = select([students]).order_by(desc(students.c.id))
stmt = select([students]).where(between(students.c.id,2,3))
prints(con.execute(stmt))

result = con.execute(select([func.now()]))
print (result.fetchone())


result = con.execute(select([func.count(students.c.id)]))
result = con.execute(select([func.max(students.c.id)]))
result = con.execute(select([func.min(students.c.id)]))
result = con.execute(select([func.avg(students.c.id).label('avg')]))
print (result.fetchone())

from sqlalchemy import union, union_all, except_, intersect
# u = union(addresses.select().where(addresses.c.email_add.like('%@gmail.com addresses.select().where(addresses.c.email_add.like('%@yahoo.com'))))
u = union_all(addresses.select().where(addresses.c.email_add.like('%@gmail.com')), addresses.select().where(addresses.c.email_add.like('%@yahoo.com')))
u = except_(addresses.select().where(addresses.c.email_add.like('%@gmail.com')), addresses.select().where(addresses.c.postal_add.like('%Pune')))
u = intersect(addresses.select().where(addresses.c.email_add.like('%@gmail.com')), addresses.select().where(addresses.c.postal_add.like('%Pune')))
prints(con.execute(u))

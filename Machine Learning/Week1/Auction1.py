import sqlalchemy
from sqlalchemy.orm import relationship

# 1 Version check
#print(sqlalchemy.__version__)

# 2 Connecting
# Đối với hướng dẫn này chúng ta sẽ sử dụng cơ sở dữ liệu SQLite trong bộ nhớ. Để kết nối chúng ta sử dụng create_engine ():
from sqlalchemy import create_engine
engine= create_engine('sqlite:///:memory:',echo=True)
#print(type(engine),'\n')
'''The echo flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python’s
standard logging module. With it enabled, we’ll see all the generated SQL produced.
If you are working through this tutorial and want less output generated, set it to False.
This tutorial will format the SQL behind a popup window so it doesn’t get in our way;
 just click the “SQL” links to see what’s being generated.
The return value of create_engine() is an instance of Engine, and it represents the core interface to
 the database, adapted through a dialect that handles the details of the database and DBAPI in use.
  In this case the SQLite dialect will interpret instructions to the Python built-in sqlite3 module.

'''
# 3 Declare a Mapping

'''Classes mapped using the Declarative system are defined in terms of a base class which maintains
a catalog of classes and tables relative to that base - this is known as the declarative base class.
Our application will usually have just one instance of this base in a commonly imported module.
We create the base class using the declarative_base() function, as follows:
'''
from sqlalchemy.ext.declarative import  declarative_base
Base=declarative_base()
'''Now that we have a “base”, we can define any number of mapped classes in terms of it.
We will start with just a single table called users, which will store records for the end-users
using our application. A new class called User will be the class to which we map this table.
Within the class, we define details about the table to which we’ll be mapping, primarily the table name,
and names and datatypes of columns:
'''
from sqlalchemy import Column,Integer,String,ForeignKey
'''The items model should contain four columns:
o An integer id, which is the primary key
o A name string, which cannot be null
o A description string, which cannot be null
o A start_time DateTime'''
import datetime
class Item(Base):
    __tablename__='Items'
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    start_time = Column(sqlalchemy.types.DateTime,default=datetime.datetime.utcnow())
    user_id = Column(Integer,ForeignKey('User.id'))
    def __init__(self,id,name,description,start_time):
        self.id=id
        self.name=name
        self.description=description
    def __repr__(self):
        return ("Items(id=%d,name='%s',description='%s'" % (self.id,self.name,self.description))


class Bid(Base):
    __tablename__='Bid'
    id=Column(Integer,primary_key=True)
    price=Column(sqlalchemy.types.Float,nullable=False)
    user_id = Column(Integer,ForeignKey('User.id'))
    def __init__(self,id,price):
        self.id=id
        self.price=price
    def __repr__(self):
        return ("Bid(id=%d,price=%f)"%(self.id,self.price))

class User(Base):
    __tablename__='User'
    id = Column(Integer,primary_key=True)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    user_item = relationship("Item")
    user_bid  = relationship("Bid")
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password
    def __repr__(self):
        return ("User(id=%d,username='%s',password='%s')" % (self.id,self.username,self.password))

# Creating a session

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# Adding objects
item1=Item(id=1,name='phuc',description='aint',start_time=datetime.datetime.utcnow())
user1=User(id=1,username='phuc',password='123456')
bid1=Bid(id=1,price=75.96)
# session.add(user1)
# session.add_all([User(id=1,username='phuc',password='123456'),
#                  User(id=2, username='ngoc', password='123456'),
#                  User(id=3, username='nam', password='123456')])

#our_items=session.query(User).first()
session.query(User).all()

# Querying objects

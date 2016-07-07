from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey, MetaData, func, desc
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    
    id= Column(Integer, primary_key=True)
    name= Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    
    bids=relationship("Bid", backref="item")
    owner_id = Column(Integer, ForeignKey('users.id'),nullable = False)
    
class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    
    item= relationship("Item", backref="owner")
    bid = relationship('Bid', uselist= False, backref = 'bidder')
    
    
class Bid(Base):
    __tablename__ = "bids"
    id=Column(Integer, primary_key=True)
    price=Column(Float,nullable=False)
    
    
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    



    
Base.metadata.create_all(engine)
m=MetaData()
m.reflect(engine)

#Creates 3 users

spencer=User( username='spencer', password='cheng')
joey = User(username='joey', password = 'password')
bob = User( username = 'bob', password = 'bob')

#1 item for auction owned by spencer
baseball = Item( name = 'baseball', owner = spencer)

#setting up inital auction for baseball of $100
sbid = Bid(price = 100, item = baseball, bidder = spencer)

# Other bets 
jbid = Bid(price = 150, item = baseball, bidder = joey)
Bbid = Bid(price = 200, item = baseball, bidder = bob)

session.add_all([spencer,joey, bob, baseball, sbid, jbid, Bbid])
session.commit()

print(jbid.price)
print(Bbid.price)

#Updating the bets with a query and update function
session.query(Bid).filter(Bid.price == 150).\
    update({Bid.price: Bid.price + 150}, synchronize_session = False)
session.query(Bid).filter(Bid.price == 200).\
    update({Bid.price: Bid.price + 300}, synchronize_session = False)
session.commit()

print(jbid.price)
print(Bbid.price)

highest_bidder= session.query(Bid).order_by(desc(Bid.price)).first()
#prints the highest bidder
print(highest_bidder.bidder.username)
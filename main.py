from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column,  select, Float, DateTime
from datetime import datetime

#create your database in postgres for assignment
#This project uses mydb_auction databace
app = Flask(__name__)
#config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:binanh1511@localhost/mydb_auction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)


#Create models
#User model
class User(db.Model):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=False, nullable=False)
    user_password = Column(String, unique=False, nullable=False)
    '''
    def __init__(self,id, name, password):
        self.user_id = id
        self.user_name = name
        self.user_password = password
    '''
    #create new user
    def add_new_user(self,id, name, password):
        new_user = User()
        new_user.user_id = id
        new_user.user_name = name
        new_user.user_password = password
        db.session.add(new_user)
        db.session.commit()

#Item model
class Item(db.Model):
    __tablename__ = 'Item'
    item_id = Column(Integer,primary_key = True)
    item_name = Column(String, nullable=False)
    item_descr = Column(String, nullable=False)
    item_start_time= Column(DateTime, default= datetime.utcnow, nullable=False)

    #create new item
    def add_new_item(self,id,name, descr):
        new_item = Item()
        new_item.item_id = id
        new_item.item_name = name
        new_item.item_descr = descr
        #new_item.item_start_time = start_time
        db.session.add(new_item)
        db.session.commit()
#Bid model
class Bid(db.Model):
    __tablename__ = 'Bid'
    bid_id = Column(Integer,primary_key =True,)
    bid_price = Column(Float, nullable=False)
    #place a bid on item
    def place_a_bid(self,id, price):
        new_a_bid = Bid()
        new_a_bid.bid_id = id
        new_a_bid.bid_price = price
        db.session.add(new_a_bid)
        db.session.commit()
#Auction model contain infor user_id auction and item_id be auctioned
class Auction(db.Model):
    __tablename__ = 'Auction'
    auction_id = Column(Integer,primary_key =True, autoincrement= True)
    auction_sellerid = Column(Integer,ForeignKey("User.user_id"), nullable =False)
    auction_iid = Column(Integer,ForeignKey("Item.item_id"), nullable =False)
    #creat an aution when user want to sell item
    def create_auction(self,uid, iid):
        new_auction = Auction()
        new_auction.auction_sellerid = uid
        new_auction.auction_iid = iid
        db.session.add(new_auction)
        db.session.commit()
#Transaction model represent Relationship of USER, ITEM and BID
class Transaction(db.Model):
    __tablename__ = 'Transaction'
    trans_id = Column (Integer,primary_key =True, autoincrement=True)
    trans_uid = Column (Integer,ForeignKey("User.user_id"))
    trans_iid = Column (Integer, ForeignKey("Item.item_id"))
    trans_bid = Column (Integer, ForeignKey("Bid.bid_id"))

    def create_transaction(self,uid, iid, bid):
        new_transaction = Transaction()
        new_transaction.trans_uid = uid
        new_transaction.trans_iid = iid
        new_transaction.trans_bid = bid
        db.session.add(new_transaction)
        db.session.commit()
#Input user data
def input_User():
    u = User()
    print("How many users will you add?")
    n = int(input("n: "))
    for i in range(0, n):
        print("User id " + str(i + 1) + "?")
        id = input("id: ")
        print("User name " + str(i + 1) + "?")
        name = input("name: ")
        print("User pass " + str(i + 1) + "?")
        password = input("pass: ")
        u.add_new_user(id,name, password)
#input item data
def input_Item():
    I = Item()
    A = Auction()
    print("How many items will you add?")
    n = int(input("n: "))
    for i in range(0, n):
        print("Item id " + str(i + 1) + "?")
        id = input("id: ")
        print("Item name " + str(i + 1) + "?")
        name = input("name: ")
        print("Item description " + str(i + 1) + "?")
        descr = input("desription: ")

        #print("Time start to buy item " + str(i + 1) + "?")
        #start_time = input("start_time: ")
        I.add_new_item(id,name,descr)
        print("Who sells item " +str(i+1)+"?")
        seller_id = input("user_id: ")
        A.create_auction(seller_id,id)
#input bid data
def input_Bid():
    B = Bid()
    T = Transaction()
    print("How many bids will you add?")
    n = int(input("n: "))
    for i in range(0, n):
        print("Bid id " + str(i + 1) + "?")
        id = input("id: ")
        print("Price " + str(i + 1) + "?")
        price = input("price: ")
        B.place_a_bid(id,price)
        print("What is this item ?")
        item_id = input("item_id: ")
        print("Who places a bid on this item?")
        buyer_id = input("user_id: ")
        T.create_transaction(buyer_id,item_id,id)
#query to find out which user which user placed the highest bid
def query_highest_price(item_name):
    query_item = db.session.query(Item).filter(Item.item_name == item_name).first()
    query_trans = db.session.query(Transaction).filter(Transaction.trans_iid == query_item.item_id).all()
    max_price = 0
    id_max_price = 0
    for i in range(len(query_trans)):
        query_bid = db.session.query(Bid).filter(Bid.bid_id == query_trans[i].trans_bid).first()
        if (query_bid.bid_price >= max_price):
            max_price = query_bid.bid_price
            id_max_price = query_bid.bid_id
    query_trans2 = db.session.query(Transaction).filter(Transaction.trans_bid == id_max_price).first()
    query_user = db.session.query(User).filter(User.user_id == query_trans2.trans_uid).first()
    print(query_user.user_id, query_user.user_name, query_user.user_password)
#main to run program
if __name__ == '__main__':
    #reset data
    #db.drop_all()

    #create database
    #db.create_all()

    #inout User data from keyboard
    #input_User()

    #input Item data from keyboard
    #input_Item()

    #input Bid data from keyboard
    #input_Bid()

    #query
    query_highest_price('baseball')

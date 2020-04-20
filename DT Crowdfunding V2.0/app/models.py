from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Identify database structure model
# Refer to store-schema.sql

# Define customer framework
class Customer(Base):
    __tablename__ = 'customers'
    id = Column('id', String(20), primary_key=True)
    name = Column('name', String(50), nullable=False)
    password = Column('password', String(20), nullable=False)
    address = Column('address', String(100))
    phone = Column('phone', String(20))
    birthday = Column('birthday', String(20))


# Define goods framework
class Goods(Base):
    __tablename__ = 'goods'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', String(200))
    brand = Column('brand', String(30))
    series = Column('series', String(30))
    asset = Column('asset_class', String(30))
    fundtype = Column('fund_type', String(30))
    maturity = Column('maturity', String(30))
    domicile = Column('domicile', String(30))
    manager = Column('manager', String(30))
    image = Column('image', String(100))
    redem_amount = Column('redem_amount', Float)  
    # One to many relationship（Goods->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  # OrderLineItem model


# Define orders framework
class Orders(Base):
    __tablename__ = 'orders'
    id = Column('id', String(20), primary_key=True)
    orderdate = Column('order_date', String(20))
    status = Column('status', Integer)  # 1= pending payment 0= paid already
    total = Column('total', Float)
    # One to many relationship（Orders->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  # OrderLineItem model


# Define OrderLineItem framework
class OrderLineItem(Base):
    __tablename__ = 'orderLineItems'
    id = Column('id', Integer, primary_key=True)
    quantity = Column('quantity', Integer)
    subtotal = Column('sub_total', Float)
    goodsid = Column('goodsid', ForeignKey('goods.id'))  
    orderid = Column('orderid', ForeignKey('orders.id')) 
    orders = relationship('Orders', backref='OrderLineItem')  
    goods = relationship('Goods', backref='OrderLineItem')  

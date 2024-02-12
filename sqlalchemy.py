import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="book")
    stocks = relationship("Stock", back_populates="book")

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="publisher")

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    book = relationship("Book", back_populates="stock")
    id_shop = Column(Integer, ForeignKey('shop.id'))
    shop = relationship("Shop", back_populates="stock")
    count = Column(Integer)
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    book = relationship("Stock", back_populates="sale")
    count = Column(Integer)
    price = Column(Float)
    date_sale = Column(Date)


database_name = "dbname"
user = "user"
password = "password"
host = "host"
port = "port"
engine_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(engine_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_shops(publisher_id_or_name):
    query = session.query(
        Book.name, Shop.name, Sale.price, Sale.date_sale
    ).join(Book).join(Shop).join(Publisher).join(Stock).join(Sale)

    if publisher_id_or_name.isdigit():
        query = query.filter(Publisher.id == int(publisher_id_or_name)).all()
    else:
        query = query.filter(Publisher.name.lower() == publisher_id_or_name.lower()).all()

    for book_name, shop_name, sale_price, date_sale in query:
        print(f"{book_name: <40} | {shop_name: <10} | {sale_price: <8} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    publisher_id_or_name = input("Введите имя или идентификатор издателя: ")
    get_shops(publisher_id_or_name)
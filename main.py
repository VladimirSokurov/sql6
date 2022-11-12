import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:r3l0ATprogef3w_+@localhost:5432/sql6"
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', encoding="utf_8") as fd:
    data = json.load(fd)

for record in data:
    if record['model'] == 'publisher':
        publisher = Publisher(id=record['pk'], name=record['fields']['name'])
        session.add(publisher)

    elif record['model'] == 'shop':
        shop = Shop(id=record['pk'], name=record['fields']['name'])
        session.add(shop)

    elif record['model'] == 'book':
        book = Book(id=record['pk'], title=record['fields']['title'], id_publisher=record['fields']['publisher'])
        session.add(book)

    elif record['model'] == 'stock':
        stock = Stock(id=record['pk'], id_book=record['fields']['book'], id_shop=record['fields']['shop'],
                      count=record['fields']['count'])
        session.add(stock)

    elif record['model'] == 'sale':
        sale = Sale(id=record['pk'], price=record['fields']['price'], date_sale=record['fields']['date_sale'],
                    id_stock=record['fields']['stock'], count=record['fields']['count'])
        session.add(sale)

    session.commit()


publisher_id_input = int(input())
publisher_query = session.query(Publisher).filter(Publisher.id == publisher_id_input).all()
shop_query = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == publisher_id_input).all()


for i in publisher_query:
    print(i)

for i in shop_query:
    print(i)


session.close()

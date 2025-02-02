# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declared_attr, declarative_base, Session


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)   


Base = declarative_base(cls=PreBase)

class Quote(Base):
    text = Column(Text)
    author = Column(String(200))
    tags = Column(String(400))


class TrainingScrapyPipeline:
    def process_item(self, item, spider):
        return item


class QuotesToDBPipeline:

    def open_spider(self, spider):

        engine = create_engine('sqlite:///sqlite.db', echo=True)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine) 
        self.session = Session(engine)

    def process_item(self, item, spider):
        # Создание объекта цитаты.
        quote = Quote(
            text=item['text'],
            author=item['author'],
            tags=', '.join(item['tags']),
        )
        # Добавление объекта в сессию и коммит сессии.
        self.session.add(quote)
        self.session.commit()
        # Возвращаем item, чтобы обработка данных не прерывалась.
        return item 

    def close_spider(self, spider):
        self.session.close()

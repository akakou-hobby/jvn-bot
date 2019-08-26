import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, Float, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker


ENGINE = create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()

session = scoped_session(
    sessionmaker(
        bind = ENGINE,
        autocommit=False,
    )
)


class Condition(Base):
    '''デバイスの設定情報'''
    __tablename__ = 'conditions'

    _id = Column('id', Integer, primary_key = True)
    channel = Column('channel', Text)
    vendor = Column('vendor', Text)
    product = Column('product', Text)
    cvss = Column('cvss', Float)

    def hit(self, vuln):
        is_same_vendor = True
        is_same_product = True
        is_cvss_higher = True

        vendor = vuln.vendor.replace(' ', '')
        product = vuln.product.replace(' ', '')

        if self.vendor:
            is_same_vendor = self.vendor in vendor

        if self.product:
            is_same_product = self.product in product

        if self.cvss:
            is_cvss_higher = self.cvss <= vuln.cvss

        return is_same_vendor \
            and is_same_product \
            and is_cvss_higher


Base.metadata.create_all(ENGINE)


if __name__=='__main__':
    condition = Condition()
    condition.channel = 'じぇねらる'
    condition.vendor = 'アドビ'
    condition.product = ''
    condition.cvss = 1

    session.add(condition)
    session.commit()

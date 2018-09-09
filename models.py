import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///database.sqlite', echo=False)

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=True)
    company_inn = Column(String, nullable=True)
    company_manager = Column(String, nullable=True)
    company_address = Column(String, nullable=True)
    company_tel = Column(String, nullable=True)
    company_link = Column(String, nullable=True)
    sro_belongs = Column(String, nullable=True)
    member_status = Column(String, nullable=True)
    updated_at = Column(Date, onupdate=datetime.datetime.now())

    def __init__(self, company_name, company_inn, company_manager,
                 company_address, company_tel, company_link,
                 sro_belongs, member_status, updated_at):
        self.company_name = company_name
        self.company_inn = company_inn
        self.company_manager = company_manager
        self.company_address = company_address
        self.company_tel = company_tel
        self.company_link = company_link
        self.sro_belongs = sro_belongs
        self.member_status = member_status
        self.updated_at = updated_at


# Database initialize
Base.metadata.create_all(engine)


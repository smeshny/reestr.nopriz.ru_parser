from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///database.sqlite', echo=True)

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

    def __init__(self, company_name, company_inn, company_manager,
                 company_address, company_tel, company_link,
                 sro_belongs, member_status):
        self.company_name = company_name
        self.company_inn = company_inn
        self.company_manager = company_manager
        self.company_address = company_address
        self.company_tel = company_tel
        self.company_link = company_link
        self.sro_belongs = sro_belongs
        self.member_status = member_status


# Database initialize
Base.metadata.create_all(engine)

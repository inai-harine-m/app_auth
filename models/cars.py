from config.db import Base
from sqlalchemy import Column, false
from sqlalchemy.sql.sqltypes import Integer,String



class Car(Base):
    __tablename__ = 'cars'
    
    registration_no = Column(String, primary_key=True)
    car_name = Column(String,nullable=false)
    model = Column(String,nullable=false)
    price = Column(Integer,nullable=false)
    
    

    
    
    
    
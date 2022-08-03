from pydantic import BaseModel


class Data(BaseModel):
    registration_no:str
    car_name:str
    model:str
    price:int
    
    class Config:
        orm_mode=True           #ORM Mode (aka Arbitrary Class Instances)
        
# class Auth(BaseModel):
#     car_name:str
#     registration_no:str
    
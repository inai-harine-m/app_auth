from fastapi import FastAPI, Depends,status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db
from models.cars import Car
from schemas.schema_car import Data
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer



app = FastAPI()

@app.get('/')
def root():
    return "{message:'car_details'}"
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login"
)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


reg_no="reg_no"
@app.post('/login')
def login(form_data:OAuth2PasswordRequestForm  = Depends(),db: Session = Depends(get_db)):
    data = db.query(Car).filter(Car.registration_no == form_data.username).first()
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid input"
        )
    hashed_pass = data.car_name
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,    
            detail="invalid input"
        )
    
    global reg_no
    reg_no=data.registration_no
    #return data.car_name
    return "logged in"

@app.get("/api/cars")
def display(db: Session = Depends(get_db),data: Data = Depends(reuseable_oauth)):
    return db.query(Car).filter(Car.registration_no == reg_no).first()


@app.post('/api/cars')
def insert( val:Data,db: Session = Depends(get_db)):


     data = db.query(Car).filter(Car.registration_no == val.registration_no).first()

     if data is not None:
         return "registration_no already found!!!"

    

     data1 = Car(
        registration_no=val.registration_no,
        car_name=get_hashed_password(val.car_name),
        model=val.model,
        price=val.price
        )

     db.add(data1)
     
     db.commit()

     return "data inserted"


@app.put('/api/cars/{registration_no}')
def update(registration_no:str,val:Data,db: Session = Depends(get_db),data: Data = Depends(reuseable_oauth)):
    data1=db.query(Car).filter(Car.registration_no == registration_no).first()

    if data1 is None:
        return "no details with this registration number"

    data1.car_name=val.car_name
    data1.price=val.price

    db.commit()
    #return db.query(Car).filter(Car.registration_no == reg_no).first()
    # return db.query(Car).all()
    return "updated "


@app.delete('/api/cars/{registration_no}')
def delete(registration_no: str,data: Data = Depends(reuseable_oauth),db: Session = Depends(get_db)):
    data1 = db.query(Car).filter(Car.registration_no == registration_no).first()

    if data1 is None:
        return "no details with this registration number"

    db.delete(data1)
    db.commit()
    return "deleted "
    #return db.query(Car).filter(Car.registration_no == reg_no).first()
    # return db.query(Car).all()

    #   val.registration_no,
    #     val.car_name,
    #     val.model,
    #     val.price














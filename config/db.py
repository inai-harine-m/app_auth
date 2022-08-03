from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="postgresql://xzkqbdblddvspd:c1dbaa1d6de257a85056b20dfe5435cc04028c482d4a3ec33dca8525e699764a@ec2-44-206-137-96.compute-1.amazonaws.com:5432/d6mvkad1agse2d"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
      
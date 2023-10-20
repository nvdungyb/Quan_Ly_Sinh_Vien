# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from fastapi import Depends
# import mysql.connector

# app = FastAPI()


# DATABASE_URL = "mysql+mysqlconnector://root:Dung3032003_135709@localhost:3306/testing"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     userName = Column(String(50), unique=False, index=True)
#     # password = Column(String(50), index=True)

# Base.metadata.create_all(bind=engine) 


# # db_config = {
# #     "host": "localhost",
# #     "user": "root",
# #     "password": "Dung3032003_135709",
# #     "database": "testing"
# # }


# # con = mysql.connector.connect(**db_config)

# # @app.get("/")
# # def read_root():
# #     cursor = con.cursor()
# #     cursor.execute("SELECT * FROM pythonWeb")
# #     result = cursor.fetchall()
# #     cursor.close()
# #     return {'data': result};

# class UserNameInput(BaseModel):
#     userName: str
     

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("index.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content = html_content)

# # db: SessionLocal = Depends()

# @app.post("/save_userName")
# async def save_userName(username_input: UserNameInput, db: SessionLocal = Depends()):
#     username = username_input.username
#     user = User(username=username)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"Message": "Username saved successfully"}


from fastapi import FastAPI, Response, Request, Depends
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel




app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Dung3032003_135709",
    "database": "testing"
}

con = mysql.connector.connect(**db_config)

# @app.post("/save_userName")
# async def read_root(request: Request):
#     cursor = con.cursor()

#     data = await request.json()
#     username = data.get('username')
#     print(username)
#     # cursor.execute("insert into testing.people values (null, 'Dung')")
#     # con.commit()

#     # result = cursor.fetchall()
#     # cursor.close()
#     return {'data': request.json()};

@app.post("/save_userName")
async def save_userName(request: Request, bodyreq:dict):
    try:
        cursor = con.cursor()
       
        print("bodyreq: ", bodyreq)
        maSv = bodyreq.get('maSv')
        name = bodyreq.get('fullName')
        lopHanhChinh = bodyreq.get('lopHanhChinh')
        email = bodyreq.get('email')
        soDt = bodyreq.get('soDt')
        diaChi = bodyreq.get('diaChi')
        gioiTinh = 'Nam'
        print(maSv, name, lopHanhChinh, email, soDt, diaChi, gioiTinh) 
        
        cursor.execute("INSERT INTO sinhvien VALUES (%s,%s, %s, %s, %s, %s, %s)", (maSv, name, lopHanhChinh, soDt, email, diaChi, gioiTinh))
        con.commit()
        
        cursor.close()


        return {"message": "Username saved successfully"}
    except Exception as e:
        return {"error": str(e)}
    

engine = create_engine("mysql+mysqlconnector://root:Dung3032003_135709@localhost:3306/testing")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index(db: Session = Depends(get_db)):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM testing.users")
    result = cursor.fetchall()
    cursor.close()
    print('hello')
    
    return {'data':result}


@app.get("/getStudents")
async def index(db: Session = Depends(get_db)):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sinhvien")
    result = cursor.fetchall()
    cursor.close()
    print("hello")
    return {'data': result}
 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
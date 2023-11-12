
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
        gioiTinh = bodyreq.get('gioiTinh')
        note = bodyreq.get('note')
        print(maSv, name, lopHanhChinh, email, soDt, diaChi, gioiTinh, note) 
        
        cursor.execute("INSERT INTO sinhvien VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", (maSv, name, lopHanhChinh, soDt, email, diaChi, gioiTinh, note))
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


@app.delete("/deleteStudent/{maSv}")
async def deleteStudent(maSv: str, db: Session = Depends(get_db)):
    cursor = con.cursor()
    print(maSv + " da thuc hien")
    print(maSv)
    try:
        cursor.execute("DELETE FROM sinhvien WHERE maSv = %s", (maSv,))
        con.commit()
    except Exception as e:
        con.rollback()
    finally:
        cursor.close()


@app.post("/changeStudent")
async def changeStudent(request: Request, bodyreq:dict):
    try:
        cursor = con.cursor()
       
        print("bodyreq: ", bodyreq)
        maSv = bodyreq.get('maSv')
        name = bodyreq.get('fullName')
        lopHanhChinh = bodyreq.get('lopHanhChinh')
        email = bodyreq.get('email')
        soDt = bodyreq.get('soDt')
        diaChi = bodyreq.get('diaChi')
        gioiTinh = bodyreq.get('gioiTinh')
        note = bodyreq.get('note')
        print(maSv, name, lopHanhChinh, email, soDt, diaChi, gioiTinh, note) 
        
        cursor.execute("UPDATE sinhvien SET hoTen = %s, lopHanhChinh = %s, soDt = %s,  email = %s, diaChi = %s, gioiTinh = %s, ghiChu = %s WHERE maSv = %s", (name, lopHanhChinh, soDt, email, diaChi, gioiTinh, note, maSv))
        con.commit()
        
        cursor.close()


        return {"message": "Username saved successfully"}
    except Exception as e:
        return {"error": str(e)}

 
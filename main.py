
from fastapi import FastAPI, Response, Request, Depends 
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


# FastAPI là một web framwork hiện đại, nhanh chóng, dễ sử dụng để xây dụng các ứng dụng và API trên Python 3.6+.
# Một số đặc điểm nổi bật của framework này.
#   +) dễ sử dụng: cú pháp đơn giản, dễ hiểu dựa trên chuẩn OpenAPI
#   +) nhanh chóng: sử dụng ASGI (Asynchronous Server Gateway Inteface), tận dụng được hiệu năng của các Server async như Uvicorn, Gunicorn.
#   +) Tự động generate ra OpenAPI schema cho API, có thể tương tác với API ngay trên docs.
#   +) Validate dữ liệu: Sử dụng Pydantic để validate các dữ liệu đầu vào, đầu ra.
#   +) ORM (Object-Relational Mapping) tích hợp sẵn: hỗ trợ tích hợp với SQLAlchemy => giúp thao tác với cơ sở dữ liệu một cách dễ dàng thông qua đối tượng.
# => dễ học, dễ sử dụng, nhanh chóng và hiệu năng cao.


# Khởi tạo app FastAPI
app = FastAPI()

# Khai báo danh sách các origin được phép, các origin này được client (truy nhập từ domain/ port này) cho phép truy cập vào API.
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


# CORS middlware này cho phép mọi origin, phương thức, headers được truy cập từ client.
# Thiết lập CORS giúp client có thể gọi API được một cách dễ dàng.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # dấu * là cho phép mọi origin được phép truy cập API.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Kết nối đến cơ sở dữ liệu Mysql sử dụng thư viên mysql.connector.

db_config = {
    "host": "localhost",                    # tên máy chủ.
    "user": "root",                         # tên người dùng.
    "password": "Dung3032003_135709",       # mk người dùng.
    "database": "testing"                   # tên cơ sở dữ liệu
}

# tạo kết nối đến Mysql, con lưu kết nối sau khi kết nối thành công.
con = mysql.connector.connect(**db_config)

 
# Đường dẫn /save_userName trong FastAPI để lưu thông tin vào database.
@app.post("/save_userName")                                     # Khai báo POST request, url là /save_userName.
async def save_userName(request: Request, bodyreq:dict):
    try:
        cursor = con.cursor()                                   # Khởi tạo cursor để thực thi câu lệnh truy vấn.
       
        print("bodyreq: ", bodyreq)                             # Thực hiện câu lệnh lấy dữ liệu từ bodyreq gồm các trường thông tin sinh viên.
        maSv = bodyreq.get('maSv')
        name = bodyreq.get('fullName')
        lopHanhChinh = bodyreq.get('lopHanhChinh')
        email = bodyreq.get('email')
        soDt = bodyreq.get('soDt')
        diaChi = bodyreq.get('diaChi')
        gioiTinh = bodyreq.get('gioiTinh')
        note = bodyreq.get('note')
        print(maSv, name, lopHanhChinh, email, soDt, diaChi, gioiTinh, note) 
        
        # Thực thi câu lệnh Insert sử dụng cursor với dữ liệu đã lấy được
        cursor.execute("INSERT INTO sinhvien VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", (maSv, name, lopHanhChinh, soDt, email, diaChi, gioiTinh, note))
        con.commit()    # Để lưu lại thay đổi vào cơ sở dữ liệu.
        
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

 
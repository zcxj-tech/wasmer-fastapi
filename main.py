from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
# 前端路由和静态文件服务
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
import platform
import sys
import os


name = os.getenv("DB_NAME", "todos")
user = os.getenv("DB_USERNAME", "root")
password = os.getenv("DB_PASSWORD", "")
host = os.getenv("DB_HOST", "127.0.0.1")
port = os.getenv("DB_PORT", "3306")
db_url = f"mysql+pymysql://{user}{':' + quote_plus(password) if password else ''}@{host}:{port}/{name}"

# 创建数据库引擎
# 注意：请根据实际情况修改数据库连接信息
#engine = create_engine('mysql+pymysql://7f15cb037e488000736360c22b98:069a7f15-cb03-7f73-8000-544e52597658@db.fr-pari1.bengt.wasmernet.com:10272/wasmer_fastapi')
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 创建用户模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# Pydantic 模型
class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建 FastAPI 应用
app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 系统信息端点
@app.get("/api/system")
def get_system_info():
    return {
        "platform": platform.platform(),
        "python_version": sys.version,
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

# 用户 CRUD 端点

# 获取所有用户
@app.get("/api/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 获取单个用户
@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 创建用户
@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 检查邮箱是否已存在
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 更新用户
@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 检查邮箱是否已被其他用户使用
    existing_user = db.query(User).filter(User.email == user.email, User.id != user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered by another user")
    
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 删除用户
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# 配置静态文件服务，设置 html=True 以支持 SPA 应用
app.mount("", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

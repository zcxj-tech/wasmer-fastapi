# FastAPI + Vue 用户管理系统

这是一个使用 FastAPI 和 Vue 构建的用户管理系统，用于管理用户信息并提供系统信息查询功能。

## 技术栈

- **后端**: FastAPI + Python 3.9+ + SQLAlchemy + MySQL
- **前端**: Vue 3 + Vite
- **部署**: 本地服务器

## 功能特性

1. **系统信息**：显示 Python 系统信息、操作系统版本等
2. **用户管理**：
   - 添加用户（支持邮箱唯一性检查）
   - 查看用户列表
   - 更新用户信息
   - 删除用户
3. **界面优化**：
   - 响应式布局
   - 现代化 UI 设计

## 安装和运行

### 后端

1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

2. 配置数据库
   - 确保 MySQL 服务已启动
   - 创建名为 `wasmer` 的数据库
   - 修改 `main.py` 中的数据库连接信息（用户名、密码等）

3. 运行后端服务
   ```bash
   python main.py
   ```
   或
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 前端

1. 安装依赖
   ```bash
   cd frontend
   npm install
   ```

2. 构建前端
   ```bash
   npm run build
   ```
   构建产物会自动生成到 `static` 目录

## API 接口

### 系统信息
- `GET /api/system` - 获取系统信息

### 用户管理
- `GET /api/users` - 获取所有用户
- `GET /api/users/{user_id}` - 获取单个用户
- `POST /api/users` - 创建新用户（参数：name, email, age）
- `PUT /api/users/{user_id}` - 更新用户信息（参数：name, email, age）
- `DELETE /api/users/{user_id}` - 删除用户

## 前端功能

1. **系统信息展示**：显示后端返回的系统信息
2. **用户管理**：
   - 添加新用户
   - 查看用户列表
   - 编辑用户信息
   - 删除用户
3. **响应式设计**：适配不同屏幕尺寸

## 项目结构

```
wasmer/
├── frontend/          # 前端代码
│   ├── src/           # 前端源码
│   ├── public/        # 静态资源
│   ├── package.json   # 前端依赖
│   └── vite.config.js # Vite 配置
├── static/            # 前端构建产物
├── main.py            # 后端主文件
├── requirements.txt   # 后端依赖
├── test_api.py        # API 测试脚本
└── README.md          # 项目说明
```

## 运行命令

1. **安装后端依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **安装前端依赖**：
   ```bash
   cd frontend
   npm install
   ```

3. **构建前端**：
   ```bash
   cd frontend
   npm run build
   ```

4. **启动后端服务**：
   ```bash
   python main.py
   ```

5. **访问应用**：
   打开浏览器访问 `http://localhost:8000`

-- 创建user表
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- 插入测试数据
INSERT INTO user (username, password) VALUES
('admin', 'admin123'),
('user1', 'user123'),
('user2', 'user456');

<script setup>
import { ref, onMounted } from 'vue';

// 状态管理
const systemInfo = ref(null);
const users = ref([]);
const loading = ref(false);
const showAddUserForm = ref(false);
const showEditUserForm = ref(false);

// 新用户表单数据
const newUser = ref({
  name: '',
  email: '',
  age: ''
});

// 编辑用户表单数据
const editUser = ref({
  id: '',
  name: '',
  email: '',
  age: ''
});

// 获取系统信息
async function fetchSystemInfo() {
  loading.value = true;
  try {
    const response = await fetch('/api/system');
    systemInfo.value = await response.json();
  } catch (error) {
    console.error('Error fetching system info:', error);
  } finally {
    loading.value = false;
  }
}

// 获取所有用户
async function fetchUsers() {
  try {
    const response = await fetch('/api/users');
    users.value = await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
  }
}

// 添加用户
async function addUser() {
  if (!newUser.value.name || !newUser.value.email || !newUser.value.age) return;
  
  try {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newUser.value)
    });
    
    if (response.ok) {
      await fetchUsers();
      // 重置表单
      newUser.value = {
        name: '',
        email: '',
        age: ''
      };
      showAddUserForm.value = false;
    } else {
      const error = await response.json();
      alert(error.detail);
    }
  } catch (error) {
    console.error('Error adding user:', error);
  }
}

// 编辑用户
async function updateUser() {
  if (!editUser.value.name || !editUser.value.email || !editUser.value.age) return;
  
  try {
    const response = await fetch(`/api/users/${editUser.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editUser.value)
    });
    
    if (response.ok) {
      await fetchUsers();
      showEditUserForm.value = false;
    } else {
      const error = await response.json();
      alert(error.detail);
    }
  } catch (error) {
    console.error('Error updating user:', error);
  }
}

// 删除用户
async function deleteUser(userId) {
  if (!confirm('确定要删除这个用户吗？')) return;
  
  try {
    const response = await fetch(`/api/users/${userId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      await fetchUsers();
    }
  } catch (error) {
    console.error('Error deleting user:', error);
  }
}

// 打开编辑表单
function openEditForm(user) {
  editUser.value = {
    id: user.id,
    name: user.name,
    email: user.email,
    age: user.age
  };
  showEditUserForm.value = true;
}

// 初始化
onMounted(() => {
  fetchSystemInfo();
  fetchUsers();
});
</script>

<template>
  <div class="container">
    <h1>FastAPI + Vue 前后端分离项目</h1>
    
    <!-- 系统信息 -->
    <section class="section">
      <h2>系统信息</h2>
      <button @click="fetchSystemInfo" :disabled="loading">
        {{ loading ? '加载中...' : '刷新系统信息' }}
      </button>
      <div v-if="systemInfo" class="result">
        <h3>系统信息:</h3>
        <p>平台: {{ systemInfo.platform }}</p>
        <p>Python版本: {{ systemInfo.python_version }}</p>
        <p>系统: {{ systemInfo.system }}</p>
        <p>系统版本: {{ systemInfo.release }}</p>
        <p>机器: {{ systemInfo.machine }}</p>
        <p>处理器: {{ systemInfo.processor }}</p>
      </div>
    </section>
    
    <!-- 用户管理 -->
    <section class="section">
      <h2>用户管理</h2>
      
      <!-- 添加用户按钮 -->
      <div class="add-user-btn">
        <button @click="showAddUserForm = true">添加用户</button>
        <button @click="fetchUsers">刷新用户列表</button>
      </div>
      
      <!-- 添加用户表单 -->
      <div v-if="showAddUserForm" class="add-user-form">
        <h3>添加新用户</h3>
        <div class="form-group">
          <label>姓名:</label>
          <input v-model="newUser.name" type="text" placeholder="输入姓名" required />
        </div>
        <div class="form-group">
          <label>邮箱:</label>
          <input v-model="newUser.email" type="email" placeholder="输入邮箱" required />
        </div>
        <div class="form-group">
          <label>年龄:</label>
          <input v-model.number="newUser.age" type="number" min="0" placeholder="输入年龄" required />
        </div>
        <div class="form-actions">
          <button @click="addUser">保存</button>
          <button @click="showAddUserForm = false">取消</button>
        </div>
      </div>
      
      <!-- 编辑用户表单 -->
      <div v-if="showEditUserForm" class="edit-user-form">
        <h3>编辑用户</h3>
        <div class="form-group">
          <label>姓名:</label>
          <input v-model="editUser.name" type="text" placeholder="输入姓名" required />
        </div>
        <div class="form-group">
          <label>邮箱:</label>
          <input v-model="editUser.email" type="email" placeholder="输入邮箱" required />
        </div>
        <div class="form-group">
          <label>年龄:</label>
          <input v-model.number="editUser.age" type="number" min="0" placeholder="输入年龄" required />
        </div>
        <div class="form-actions">
          <button @click="updateUser">保存</button>
          <button @click="showEditUserForm = false">取消</button>
        </div>
      </div>
      
      <!-- 用户列表 -->
      <div class="users-list">
        <h3>用户列表</h3>
        <table v-if="users.length > 0">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>年龄</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.age }}</td>
              <td>
                <button @click="openEditForm(user)">编辑</button>
                <button @click="deleteUser(user.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>暂无用户</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

h1, h2, h3 {
  color: #333;
}

button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f8ff;
  border-radius: 4px;
}

.add-user-btn {
  margin-bottom: 20px;
}

.add-user-form,
.edit-user-form {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: inline-block;
  width: 80px;
  font-weight: 600;
  margin-right: 10px;
}

.form-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 300px;
}

.form-actions {
  margin-top: 20px;
}

.users-list {
  margin-top: 30px;
}

.users-list table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.users-list th {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
  background-color: #e9e9e9;
  font-weight: 600;
  color: #333;
}

.users-list td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.users-list tr:hover {
  background-color: #f0f0f0;
}

.users-list tr:last-child td {
  border-bottom: none;
}

.users-list td button {
  padding: 6px 12px;
  font-size: 14px;
  margin-right: 5px;
}

.users-list td button:nth-child(2) {
  background-color: #f44336;
}

.users-list td button:nth-child(2):hover {
  background-color: #da190b;
}
</style>

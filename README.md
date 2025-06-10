
# 周童玥的网站

这是一个为应援小周童玥而开发的 Vue 3 网站项目，展示内容包括：小周百科、微博跳转、趣事集锦、人物关系、团内大事件等。

---

##  项目结构

```
vue-web/
├── backend/              # 后端
├── public/               # 公共资源：avatar.jpg, bg.jpg 等
├── src/
│   ├── views/            # 页面组件：Home.vue, Weibo.vue 等
│   ├── router/           # 路由配置：index.js
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── vite.config.js        # 构建配置
└── package.json          # 项目信息与依赖管理
```

---

## 一、 本地运行方法

### ✅ 环境准备

- Node.js ≥ 16.x（推荐使用最新版）
- Python ≥ 3.11
- Git
- sqlite3
- 推荐使用 VS Code 编辑器

### ✅ 克隆项目并安装依赖（仅适用于macOS/Linux）

```bash
git clone https://github.com/shenjian-gaocheng/vue-web.git
cd vue-web
npm install
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
cd ..
```

### ✅ 启动开发服务器

```bash
npm run dev
```

### ✅ 启动后端

```bash
cd backend
source venv/bin/activate
python3 app.py
```

打开浏览器访问：

```
http://localhost:5173
```

---

## 二、 云服务器部署（以华为云为例）

### ✅ 1. 构建生产版本

```bash
npm run build
```

生成的静态文件会输出到 `dist/` 目录。

### ✅ 2. 上传到服务器

使用以下任意方式上传：

- WinSCP / FileZilla 图形工具
- 或命令行：

```bash
scp -r dist root@your-server-ip:/root/vue-web/
```

### ✅ 3. 安装并启动 HTTP 静态服务器

在云服务器终端执行：

```bash
npm install -g http-server
cd /root/vue-web/dist
nohup http-server -p 80 -a 0.0.0.0 > vue.log 2>&1 &
```

> 🔒 建议改用 `pm2` 或 `systemd` 管理服务防止断连关闭

### ✅ 4. 确保安全组已开放 80 端口

在华为云控制台 ➝ 安全组 ➝ 出入规则 ➝ 添加端口 80（HTTP）访问权限。

---

## 三、服务器部署进程开机自启动



```bash
npm install -g pm2
```

---

### 1. 启动服务（以 http-server 为例）

```bash
pm2 start node_modules/.bin/http-server --name vue-web -- dist -p 80 -a 0.0.0.0
```

- `--name vue-web`：服务名称
- `dist`：要部署的目录
- `-p 80`：使用的端口号
- `-a 0.0.0.0`：监听所有 IP（可外网访问）

### 2. 配置开机启动

```bash
pm2 startup
```

执行命令后，终端会输出类似如下内容，请复制执行：

```bash
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u root --hp /root
```

### 3. 保存当前进程列表（确保重启后可恢复）

```bash
pm2 save
```

---

### 4. 关闭开机自启动

```bash
pm2 unstartup
```

```bash
pm2 stop vue-web
pm2 delete vue-web
```

---

## 📖 常用命令速查表

| 命令                             | 功能说明                   |
|----------------------------------|----------------------------|
| `pm2 start <命令>`              | 启动服务                   |
| `pm2 list`                      | 查看所有 PM2 管理的进程     |
| `pm2 stop <服务名>`             | 停止指定服务               |
| `pm2 restart <服务名>`          | 重启指定服务               |
| `pm2 delete <服务名>`           | 删除服务                   |
| `pm2 save`                      | 保存当前进程快照           |
| `pm2 startup`                   | 设置系统服务自启动         |
| `pm2 unstartup`                 | 取消系统服务自启动         |
| `pm2 logs <服务名>`             | 查看日志输出               |
| `npm run dev`   | 启动本地开发服务器           |
| `npm run build` | 构建生产部署包（输出到 dist）|
| `npm run preview` | 预览打包后的静态站点       |

---

## 四、 说明与致谢

- 本项目未使用 TailwindCSS，仅使用原生 CSS 编写样式
- 所有素材来源于公开渠道，仅作学习使用
- 网站非商业用途
- 特别感谢vue团队，小周应援会热心人士

---

## 📄 License

MIT License  
© 2025 shenjian-gaocheng & 小周的网站

# 网易云音乐自动签到

每日自动签到网易云音乐，获取积分。

## 功能特性

- ✅ 自动登录网易云音乐
- ✅ 每日自动签到
- ✅ 获取签到积分
- ✅ 详细日志记录
- ✅ 本地定时运行

## 环境要求

- Python 3.6+
- pip

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/aa1530382609-sudo/hengheng.git
cd hengheng
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置账号

编辑 `schedule.py` 文件，修改以下内容：

```python
PHONE = "your_phone_number"      # 修改为你的手机号
PASSWORD = "your_password"        # 修改为你的密码
```

## 使用方法

### 方式一：单次签到（测试）

```bash
python main.py
```

### 方式二：定时自动签到（推荐）

```bash
python schedule.py
```

默认每天早上 **08:00** 自动签到。修改 `schedule.py` 中的时间：

```python
schedule.every().day.at("08:00").do(job)  # 改为你想要的时间
```

## 常见问题

### Q: 如何修改签到时间？
A: 编辑 `schedule.py`，修改这一行：
```python
schedule.every().day.at("08:00").do(job)  # 改为你想要的时间，如 "09:30"
```

### Q: 账号密码安全吗？
A: 密码保存在本地文件中，请确保：
- 不要上传到公开仓库
- 定期修改密码
- 仅在个人电脑上运行

### Q: 如何在后台运行？

**Windows（使用任务计划程序）：**
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发时间和脚本位置

**Linux/Mac（使用 cron）：**
```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天 8:00 执行）
0 8 * * * cd /path/to/hengheng && python schedule.py
```

## 日志文件

- `checkin.log` - 签到日志
- `schedule.log` - 定时任务日志

## 许可证

MIT

## ⚠️ 免责声明

本项目仅供学习交流使用，使用本工具产生的一切后果由用户自负。

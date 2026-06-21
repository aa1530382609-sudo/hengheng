#!/usr/bin/env python3
"""定时运行签到脚本"""

import schedule
import time
import logging
from main import NeteaseCheckin
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('schedule.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ⚠️ 请修改为你的账号信息
PHONE = "your_phone_number"
PASSWORD = "your_password"


def job():
    """签到任务"""
    logger.info(f"[定时任务] 执行签到 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    checkin = NeteaseCheckin(PHONE, PASSWORD)
    checkin.run()
    logger.info("[定时任务] 签到完成\n")


def start_scheduler():
    """启动定时器"""
    # 每天早上 8:00 执行一次
    schedule.every().day.at("08:00").do(job)
    
    logger.info("=" * 60)
    logger.info("定时签到已启动")
    logger.info("计划时间：每天早上 08:00")
    logger.info("=" * 60)
    
    # 保持运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    if PHONE == "your_phone_number" or PASSWORD == "your_password":
        logger.error("❌ 错误：请先在 schedule.py 中配置账号和密码！")
        exit(1)
    
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logger.info("定时任务已停止")

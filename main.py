#!/usr/bin/env python3
"""网易云音乐自动签到脚本"""

import requests
import json
import time
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('checkin.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NeteaseCheckin:
    """网易云音乐签到"""
    
    def __init__(self, phone, password):
        """初始化
        
        Args:
            phone: 网易云账号手机号
            password: 网易云账号密码
        """
        self.phone = phone
        self.password = password
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.logged_in = False
    
    def login(self):
        """登录网易云音乐"""
        try:
            logger.info("开始登录...")
            
            # 登录接口
            login_url = "https://music.163.com/api/login/cellphone"
            
            params = {
                "phone": self.phone,
                "password": self.password,
                "rememberLogin": "true"
            }
            
            response = self.session.post(login_url, params=params, headers=self.headers)
            data = response.json()
            
            if data.get('code') == 200:
                logger.info(f"✓ 登录成功，用户ID: {data['account']['id']}")
                self.logged_in = True
                return True
            else:
                logger.error(f"✗ 登录失败: {data.get('msg', '未知错误')}")
                return False
        except Exception as e:
            logger.error(f"✗ 登录异常: {str(e)}")
            return False
    
    def checkin(self):
        """执行签到"""
        if not self.logged_in:
            logger.warning("未登录，尝试重新登录...")
            if not self.login():
                return False
        
        try:
            logger.info("开始签到...")
            
            # 签到接口
            checkin_url = "https://music.163.com/api/point/dailyTask"
            
            response = self.session.post(checkin_url, headers=self.headers)
            data = response.json()
            
            if data.get('code') == 200:
                points = data.get('dailyPoints', 0)
                logger.info(f"✓ 签到成功！获得 {points} 积分")
                return True
            else:
                logger.warning(f"⚠ 签到返回: {data.get('msg', '未知响应')}")
                return False
        except Exception as e:
            logger.error(f"✗ 签到异常: {str(e)}")
            return False
    
    def run(self):
        """执行登录和签到"""
        if not self.logged_in:
            self.login()
        
        if self.logged_in:
            self.checkin()
        
        return self.logged_in


def main():
    """主函数"""
    # ⚠️ 重要：请在下面填入您的网易云账号
    PHONE = "your_phone_number"  # 修改为你的手机号
    PASSWORD = "your_password"    # 修改为你的密码
    
    if PHONE == "your_phone_number" or PASSWORD == "your_password":
        logger.error("❌ 错误：请先在 main.py 中配置账号和密码！")
        return
    
    logger.info("=" * 50)
    logger.info(f"开始执行网易云音乐签到 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    
    checkin = NeteaseCheckin(PHONE, PASSWORD)
    checkin.run()
    
    logger.info("=" * 50)
    logger.info("签到流程完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()

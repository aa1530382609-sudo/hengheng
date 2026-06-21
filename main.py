#!/usr/bin/env python3
"""网易云音乐自动签到脚本 - 改进版"""

import requests
import time
import json
from datetime import datetime
import logging
from hashlib import md5

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('checkin.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NeteaseCheckin:
    """网易云音乐签到 - 改进版"""
    
    def __init__(self, phone, password):
        """初始化
        
        Args:
            phone: 网易云账号手机号
            password: 网易云账号密码
        """
        self.phone = phone
        self.password = password
        self.session = requests.Session()
        
        # 禁用自动解压，我们手动处理
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate'
        })
        self.logged_in = False
        self.uid = None
    
    def _get_md5(self, text):
        """获取MD5哈希"""
        return md5(text.encode('utf-8')).hexdigest()
    
    def login(self):
        """登录网易云音乐"""
        try:
            logger.info("开始登录...")
            
            # 先访问主页获取基本 cookies
            try:
                self.session.get('https://music.163.com/', timeout=10)
                time.sleep(0.5)
            except:
                pass
            
            # 使用登录接口
            login_url = "https://music.163.com/api/login/cellphone"
            
            # 密码需要 MD5
            password_md5 = self._get_md5(self.password)
            
            params = {
                "phone": self.phone,
                "password": password_md5,
                "rememberLogin": "true",
                "countrycode": "86"
            }
            
            response = self.session.post(login_url, data=params, timeout=10)
            response.encoding = 'utf-8'
            
            logger.info(f"登录响应状态码: {response.status_code}")
            
            # 尝试解析 JSON
            try:
                data = response.json()
            except Exception as e:
                logger.error(f"✗ 无法解析登录响应: {str(e)}")
                logger.error(f"原始响应（前200字符）: {response.text[:200]}")
                return False
            
            if data.get('code') == 200:
                # 获取用户ID
                account = data.get('account', {})
                self.uid = account.get('id')
                profile = data.get('profile', {})
                nickname = profile.get('nickname', '用户')
                
                logger.info(f"✓ 登录成功！用户: {nickname} (ID: {self.uid})")
                self.logged_in = True
                return True
            elif data.get('code') == 408:
                logger.error("✗ 登录失败: 账号或密码错误")
                return False
            elif data.get('code') == 509:
                logger.error("✗ 登录失败: 访问过于频繁，请稍后再试")
                return False
            else:
                msg = data.get('msg', data.get('message', '未知错误'))
                logger.error(f"✗ 登录失败: {msg} (code: {data.get('code')})")
                return False
        except Exception as e:
            logger.error(f"✗ 登录异常: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
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
            checkin_url = "https://music.163.com/weapi/point/dailyTask"
            
            params = {
                "type": 0  # 0: 网页签到, 1: 手机签到
            }
            
            response = self.session.post(checkin_url, data=params, timeout=10)
            response.encoding = 'utf-8'
            
            logger.info(f"签到响应状态码: {response.status_code}")
            
            try:
                data = response.json()
            except Exception as e:
                logger.error(f"✗ 签到响应无法解析为 JSON: {str(e)}")
                return False
            
            if data.get('code') == 200:
                result = data.get('data', {})
                points = result.get('point', 0)
                msg = result.get('msg', '签到成功')
                
                logger.info(f"✓ {msg}！获得 {points} 积分")
                return True
            elif data.get('code') == -1:
                logger.warning("⚠ 可能已经签到过了")
                return False
            else:
                msg = data.get('msg', data.get('message', '未知错误'))
                logger.warning(f"⚠ 签到返回: {msg} (code: {data.get('code')})")
                return False
        except Exception as e:
            logger.error(f"✗ 签到异常: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
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
    # ⚠️ 账号配置
    PHONE = "15218225254"
    PASSWORD = "Aa1530382609"
    
    if PHONE == "your_phone_number" or PASSWORD == "your_password":
        logger.error("❌ 错误：请先在 main.py 中配置账号和密码！")
        return
    
    logger.info("=" * 60)
    logger.info(f"开始执行网易云音乐签到 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    checkin = NeteaseCheckin(PHONE, PASSWORD)
    checkin.run()
    
    logger.info("=" * 60)
    logger.info("签到流程完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

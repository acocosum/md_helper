#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杭州电子科技大学校园网自动登录程序
HDU Campus Network Auto-Login System

Author: Campus Network Helper
Date: 2024
Description: 自动检测网络状态并登录校园网，支持Windows系统集成
"""

import json
import hashlib
import logging
import os
import socket
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime
from typing import Dict, Optional, Tuple

try:
    import requests
except ImportError:
    print("Error: requests module is required. Please install it with: pip install requests")
    sys.exit(1)


class CampusNetworkLogin:
    """校园网自动登录类"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化校园网登录器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 设置日志
        self._setup_logging()
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "username": "",
            "password": "",
            "login_url": "https://login.hdu.edu.cn/cgi-bin/srun_portal",
            "test_urls": [
                "http://www.baidu.com",
                "http://www.qq.com",
                "http://www.163.com"
            ],
            "timeout": 10,
            "retry_times": 3,
            "retry_interval": 30,
            "log_level": "INFO",
            "log_file": "campus_login.log"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"配置文件读取错误: {e}")
                print("使用默认配置...")
        else:
            # 创建默认配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"已创建默认配置文件: {self.config_file}")
            print("请编辑配置文件填入用户名和密码")
        
        return default_config
    
    def _setup_logging(self):
        """设置日志系统"""
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        log_file = self.config.get('log_file', 'campus_login.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _md5_encrypt(self, text: str) -> str:
        """MD5加密"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _get_local_ip(self) -> str:
        """获取本地IP地址"""
        try:
            # 创建UDP socket连接来获取本地IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception as e:
            self.logger.warning(f"无法获取本地IP: {e}")
            return "127.0.0.1"
    
    def _generate_chksum(self, username: str, password: str, ip: str, timestamp: str) -> str:
        """生成校验和"""
        # 这里需要根据实际的校验和算法来实现
        # 从cURL命令中可以看到chksum的值，但具体算法需要逆向工程
        # 暂时使用固定值或简单算法
        data = f"{username}{password}{ip}{timestamp}"
        return hashlib.sha1(data.encode('utf-8')).hexdigest()
    
    def _generate_info(self, username: str, password: str) -> str:
        """生成info参数"""
        # 这里需要根据实际的info参数生成算法来实现
        # 从cURL命令中可以看到info的值，但具体算法需要逆向工程
        # 暂时返回固定值
        return "{SRBX1}PqKChxi2njY7G0733T2sBA8mG6RCBXVDlw%2BrqkICFO6RIqCPEylDLYhtBNA7c7YuZyw3VFf2mr6CAVSy0OveKigCi66LmbOu9eabCljk5rLFb%2B9Kzvmf%2BO5iErEQDoPv3fhsRnQmjsGXBKQL"
    
    def check_network_connectivity(self) -> bool:
        """检查网络连通性"""
        test_urls = self.config.get('test_urls', ['http://www.baidu.com'])
        timeout = self.config.get('timeout', 10)
        
        for url in test_urls:
            try:
                response = self.session.get(url, timeout=timeout)
                if response.status_code == 200:
                    self.logger.info(f"网络连通正常: {url}")
                    return True
            except requests.exceptions.RequestException as e:
                self.logger.debug(f"网络连接测试失败 {url}: {e}")
                continue
        
        self.logger.warning("网络连通性检查失败")
        return False
    
    def is_logged_in(self) -> bool:
        """检查是否已登录校园网"""
        # 通过访问外网来判断是否已登录
        return self.check_network_connectivity()
    
    def login(self) -> Tuple[bool, str]:
        """
        执行登录操作
        
        Returns:
            Tuple[bool, str]: (是否成功, 结果信息)
        """
        username = self.config.get('username')
        password = self.config.get('password')
        
        if not username or not password:
            return False, "用户名或密码未配置"
        
        # 获取当前时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 获取本地IP
        local_ip = self._get_local_ip()
        
        # 生成MD5加密密码
        md5_password = self._md5_encrypt(password)
        
        # 生成校验和
        chksum = self._generate_chksum(username, md5_password, local_ip, timestamp)
        
        # 生成info参数
        info = self._generate_info(username, password)
        
        # 生成callback函数名
        callback = f"jQuery{timestamp}_{timestamp}"
        
        # 构建请求参数
        params = {
            'callback': callback,
            'action': 'login',
            'username': username,
            'password': f'{{MD5}}{md5_password}',
            'os': 'Windows 10',
            'name': 'Windows',
            'double_stack': '0',
            'chksum': chksum,
            'info': info,
            'ac_id': '0',
            'ip': local_ip,
            'n': '200',
            'type': '1',
            '_': timestamp
        }
        
        try:
            login_url = self.config.get('login_url')
            self.logger.info(f"尝试登录校园网: {username}")
            
            # 发送登录请求
            response = self.session.get(
                login_url,
                params=params,
                timeout=self.config.get('timeout', 10)
            )
            
            self.logger.debug(f"登录请求URL: {response.url}")
            self.logger.debug(f"响应状态码: {response.status_code}")
            self.logger.debug(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                # 解析JSONP响应
                response_text = response.text
                if callback in response_text and response_text.startswith(callback):
                    # 提取JSON部分
                    json_start = response_text.find('(') + 1
                    json_end = response_text.rfind(')')
                    json_str = response_text[json_start:json_end]
                    
                    try:
                        result = json.loads(json_str)
                        
                        # 检查登录结果
                        if result.get('error') == 'ok':
                            self.logger.info("校园网登录成功")
                            return True, "登录成功"
                        else:
                            error_msg = result.get('error_msg', '未知错误')
                            self.logger.error(f"登录失败: {error_msg}")
                            return False, f"登录失败: {error_msg}"
                    except json.JSONDecodeError:
                        self.logger.error("无法解析登录响应")
                        return False, "响应解析失败"
                else:
                    # 如果不是JSONP格式，尝试直接解析
                    try:
                        result = json.loads(response_text)
                        if result.get('error') == 'ok':
                            self.logger.info("校园网登录成功")
                            return True, "登录成功"
                        else:
                            error_msg = result.get('error_msg', '未知错误')
                            self.logger.error(f"登录失败: {error_msg}")
                            return False, f"登录失败: {error_msg}"
                    except json.JSONDecodeError:
                        self.logger.error("响应格式不正确")
                        return False, "响应格式错误"
            else:
                self.logger.error(f"登录请求失败: HTTP {response.status_code}")
                return False, f"请求失败: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"登录请求异常: {e}")
            return False, f"请求异常: {e}"
    
    def auto_login(self) -> bool:
        """
        自动登录流程
        
        Returns:
            bool: 是否成功
        """
        self.logger.info("开始校园网自动登录检查")
        
        # 检查是否已登录
        if self.is_logged_in():
            self.logger.info("校园网已登录，无需重复登录")
            return True
        
        # 尝试登录
        retry_times = self.config.get('retry_times', 3)
        retry_interval = self.config.get('retry_interval', 30)
        
        for i in range(retry_times):
            self.logger.info(f"第 {i + 1} 次登录尝试")
            
            success, message = self.login()
            if success:
                # 验证登录是否成功
                time.sleep(5)  # 等待网络稳定
                if self.is_logged_in():
                    self.logger.info("校园网登录成功且网络连通")
                    return True
                else:
                    self.logger.warning("登录响应成功但网络仍不通")
            else:
                self.logger.error(f"登录失败: {message}")
            
            # 如果不是最后一次尝试，等待后重试
            if i < retry_times - 1:
                self.logger.info(f"等待 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)
        
        self.logger.error("校园网登录失败，已达到最大重试次数")
        return False


def main():
    """主函数"""
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 创建登录器实例
    login_manager = CampusNetworkLogin()
    
    # 执行自动登录
    success = login_manager.auto_login()
    
    # 返回适当的退出代码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
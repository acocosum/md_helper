#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试校园网自动登录程序
Test script for campus network auto-login system
"""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import campus_login


class TestCampusNetworkLogin(unittest.TestCase):
    """测试校园网登录功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        test_config = {
            "username": "test_user",
            "password": "test_password",
            "login_url": "https://login.hdu.edu.cn/cgi-bin/srun_portal",
            "test_urls": ["http://www.baidu.com"],
            "timeout": 10,
            "retry_times": 2,
            "retry_interval": 1,
            "log_level": "ERROR"  # 减少测试时的日志输出
        }
        json.dump(test_config, self.temp_config)
        self.temp_config.close()
        
        # 创建登录器实例
        self.login_manager = campus_login.CampusNetworkLogin(self.temp_config.name)
    
    def tearDown(self):
        """测试后清理"""
        os.unlink(self.temp_config.name)
    
    def test_config_loading(self):
        """测试配置文件加载"""
        self.assertEqual(self.login_manager.config['username'], 'test_user')
        self.assertEqual(self.login_manager.config['password'], 'test_password')
        self.assertEqual(self.login_manager.config['retry_times'], 2)
    
    def test_md5_encrypt(self):
        """测试MD5加密"""
        result = self.login_manager._md5_encrypt("test_password")
        expected = "16ec1ebb01fe02ded9b7d5447d3dfc65"  # MD5 of "test_password"
        self.assertEqual(result, expected)
    
    def test_get_local_ip(self):
        """测试获取本地IP"""
        ip = self.login_manager._get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertTrue(len(ip) > 0)
    
    def test_generate_chksum(self):
        """测试校验和生成"""
        chksum = self.login_manager._generate_chksum("user", "pass", "127.0.0.1", "123456")
        self.assertIsInstance(chksum, str)
        self.assertEqual(len(chksum), 40)  # SHA1 hash length
    
    def test_generate_info(self):
        """测试info参数生成"""
        info = self.login_manager._generate_info("user", "pass")
        self.assertIsInstance(info, str)
        self.assertTrue(len(info) > 0)
    
    @patch('campus_login.requests.Session.get')
    def test_check_network_connectivity_success(self, mock_get):
        """测试网络连通性检查 - 成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.login_manager.check_network_connectivity()
        self.assertTrue(result)
    
    @patch('campus_login.requests.Session.get')
    def test_check_network_connectivity_failure(self, mock_get):
        """测试网络连通性检查 - 失败"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        result = self.login_manager.check_network_connectivity()
        self.assertFalse(result)
    
    @patch('campus_login.requests.Session.get')
    def test_login_success(self, mock_get):
        """测试登录成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        # 使用正确的JSONP格式
        mock_response.text = '{"error":"ok","message":"Login successful"}'
        mock_get.return_value = mock_response
        
        success, message = self.login_manager.login()
        self.assertTrue(success)
        self.assertEqual(message, "登录成功")
    
    @patch('campus_login.requests.Session.get')
    def test_login_failure(self, mock_get):
        """测试登录失败"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        # 使用正确的JSON格式
        mock_response.text = '{"error":"error","error_msg":"Invalid credentials"}'
        mock_get.return_value = mock_response
        
        success, message = self.login_manager.login()
        self.assertFalse(success)
        self.assertIn("Invalid credentials", message)
    
    @patch('campus_login.requests.Session.get')
    def test_auto_login_already_connected(self, mock_get):
        """测试自动登录 - 已连接"""
        # Mock网络连通性检查返回True
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.login_manager.auto_login()
        self.assertTrue(result)


def main():
    """主函数"""
    print("开始测试校园网自动登录程序...")
    print("=" * 50)
    
    # 运行单元测试
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    print("测试完成！")
    
    # 简单功能演示
    print("\n功能演示:")
    print("-" * 30)
    
    # 创建实例
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            login_manager = campus_login.CampusNetworkLogin(config_file)
            print(f"✓ 配置文件加载成功")
            print(f"  用户名: {login_manager.config.get('username', 'N/A')}")
            print(f"  登录URL: {login_manager.config.get('login_url', 'N/A')}")
            
            # 测试MD5加密
            test_password = "test123"
            encrypted = login_manager._md5_encrypt(test_password)
            print(f"✓ MD5加密测试: {test_password} -> {encrypted}")
            
            # 测试IP获取
            local_ip = login_manager._get_local_ip()
            print(f"✓ 本地IP获取: {local_ip}")
            
            # 测试校验和生成
            chksum = login_manager._generate_chksum("user", "pass", local_ip, "123456")
            print(f"✓ 校验和生成: {chksum[:20]}...")
            
            print("\n注意: 完整的网络连接和登录功能需要在校园网环境中测试")
            
        except Exception as e:
            print(f"✗ 程序测试失败: {e}")
    else:
        print(f"✗ 配置文件不存在: {config_file}")


if __name__ == "__main__":
    main()
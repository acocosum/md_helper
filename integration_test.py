#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园网自动登录系统集成测试
Campus Network Auto-Login System Integration Test
"""

import os
import sys
import json
import subprocess
import platform
from datetime import datetime

def check_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("系统环境检查")
    print("=" * 60)
    
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python版本过低，需要Python 3.7或更高版本")
        return False
    else:
        print("✅ Python版本满足要求")
        return True

def check_dependencies():
    """检查依赖包"""
    print("\n依赖包检查:")
    
    dependencies = ['requests', 'json', 'hashlib', 'logging', 'socket']
    all_ok = True
    
    for dep in dependencies:
        try:
            if dep == 'requests':
                import requests
                print(f"✅ {dep} - 版本: {requests.__version__}")
            else:
                __import__(dep)
                print(f"✅ {dep} - 已安装")
        except ImportError:
            print(f"❌ {dep} - 未安装")
            all_ok = False
    
    return all_ok

def check_config_file():
    """检查配置文件"""
    print("\n配置文件检查:")
    
    config_file = "config.json"
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_fields = ['username', 'password', 'login_url']
        missing_fields = []
        
        for field in required_fields:
            if field not in config or not config[field]:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ 配置文件缺少必要字段: {', '.join(missing_fields)}")
            return False
        
        print("✅ 配置文件格式正确")
        print(f"   用户名: {config['username']}")
        print(f"   登录URL: {config['login_url']}")
        return True
        
    except json.JSONDecodeError:
        print("❌ 配置文件格式错误")
        return False
    except Exception as e:
        print(f"❌ 配置文件读取错误: {e}")
        return False

def test_main_program():
    """测试主程序"""
    print("\n主程序测试:")
    
    if not os.path.exists("campus_login.py"):
        print("❌ 主程序文件不存在: campus_login.py")
        return False
    
    try:
        # 导入主程序
        import campus_login
        
        # 创建实例
        login_manager = campus_login.CampusNetworkLogin()
        
        # 测试基本功能
        print("✅ 主程序导入成功")
        print("✅ 类实例创建成功")
        
        # 测试配置加载
        username = login_manager.config.get('username', 'N/A')
        print(f"✅ 配置加载成功 - 用户名: {username}")
        
        # 测试MD5加密
        test_password = "test123"
        encrypted = login_manager._md5_encrypt(test_password)
        print(f"✅ MD5加密功能正常 - {test_password} -> {encrypted[:16]}...")
        
        # 测试IP获取
        local_ip = login_manager._get_local_ip()
        print(f"✅ IP获取功能正常 - 本地IP: {local_ip}")
        
        return True
        
    except Exception as e:
        print(f"❌ 主程序测试失败: {e}")
        return False

def check_windows_integration():
    """检查Windows集成功能"""
    print("\nWindows集成检查:")
    
    system = platform.system()
    print(f"当前系统: {system}")
    
    if system != "Windows":
        print("⚠️  当前不是Windows系统，无法测试Windows集成功能")
        return True
    
    # 检查安装脚本
    install_files = ["install.bat", "uninstall.bat", "task_schedule.xml"]
    all_exist = True
    
    for file in install_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")
            all_exist = False
    
    # 检查任务计划（如果在Windows上）
    if system == "Windows":
        try:
            result = subprocess.run(['schtasks', '/query', '/tn', 'HDU_Campus_Login'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Windows任务计划已配置")
            else:
                print("ℹ️  Windows任务计划未配置（这是正常的，需要运行install.bat）")
        except Exception as e:
            print(f"ℹ️  无法检查任务计划: {e}")
    
    return all_exist

def run_unit_tests():
    """运行单元测试"""
    print("\n单元测试:")
    
    if not os.path.exists("test_campus_login.py"):
        print("❌ 测试文件不存在: test_campus_login.py")
        return False
    
    try:
        # 运行测试
        result = subprocess.run([sys.executable, "test_campus_login.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 所有单元测试通过")
            return True
        else:
            print("❌ 部分单元测试失败")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 单元测试运行失败: {e}")
        return False

def generate_report():
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("校园网自动登录系统 - 集成测试报告")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print()
    
    # 执行所有测试
    tests = [
        ("Python版本检查", check_python_version),
        ("依赖包检查", check_dependencies),
        ("配置文件检查", check_config_file),
        ("主程序测试", test_main_program),
        ("Windows集成检查", check_windows_integration),
        ("单元测试", run_unit_tests),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}执行异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统已就绪。")
    else:
        print("⚠️  部分测试失败，请检查相关问题。")
    
    return passed == total

def main():
    """主函数"""
    print("校园网自动登录系统集成测试")
    print("HDU Campus Network Auto-Login System Integration Test")
    
    success = generate_report()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 系统集成测试完成 - 所有功能正常")
        print("\n后续步骤:")
        print("1. 编辑config.json填入正确的用户名和密码")
        print("2. 在Windows上运行install.bat进行系统集成")
        print("3. 重启计算机测试自动启动功能")
    else:
        print("❌ 系统集成测试失败 - 请修复相关问题")
        print("\n请检查:")
        print("1. Python环境是否正确配置")
        print("2. 依赖包是否正确安装")
        print("3. 配置文件是否正确填写")
        print("4. 程序文件是否完整")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
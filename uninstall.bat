@echo off
chcp 65001 > nul
title 杭州电子科技大学校园网自动登录程序 - 卸载
echo ========================================
echo 杭州电子科技大学校园网自动登录程序
echo HDU Campus Network Auto-Login System
echo 卸载程序
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 需要管理员权限才能卸载
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 正在卸载校园网自动登录程序...
echo.

:: 删除任务计划
echo 正在删除任务计划...
schtasks /delete /tn "HDU_Campus_Login" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo 任务计划删除成功！
) else (
    echo 任务计划删除失败或不存在
)

:: 删除启动项
echo 正在删除启动项...
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "HDU_Campus_Login" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo 启动项删除成功！
) else (
    echo 启动项删除失败或不存在
)

:: 删除临时文件
echo 正在清理临时文件...
if exist "task_schedule.xml" (
    del "task_schedule.xml" >nul 2>&1
    echo 临时文件已清理
)

echo.
echo ========================================
echo 卸载完成！
echo ========================================
echo.
echo 已完成以下操作:
echo - 删除Windows任务计划
echo - 删除启动项
echo - 清理临时文件
echo.
echo 注意: 以下文件需要手动删除:
echo - campus_login.py (主程序)
echo - config.json (配置文件)
echo - campus_login.log (日志文件)
echo - install.bat (安装脚本)
echo - uninstall.bat (本卸载脚本)
echo.
echo 这些文件保留是为了防止意外删除重要数据
echo 如需完全清理，请手动删除整个程序目录
echo.
pause
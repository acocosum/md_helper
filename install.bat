@echo off
chcp 65001 > nul
title 杭州电子科技大学校园网自动登录程序 - 安装
echo ========================================
echo 杭州电子科技大学校园网自动登录程序
echo HDU Campus Network Auto-Login System
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 需要管理员权限才能安装
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo 当前安装目录: %SCRIPT_DIR%
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 检测到Python版本:
python --version

:: 检查pip是否可用
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 未找到pip，请检查Python安装
    pause
    exit /b 1
)

echo.
echo 正在安装Python依赖包...
pip install requests

if %errorLevel% neq 0 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo 正在创建Windows任务计划...

:: 创建任务计划XML文件
set "TASK_XML=%SCRIPT_DIR%\task_schedule.xml"
echo ^<?xml version="1.0" encoding="UTF-16"?^> > "%TASK_XML%"
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> "%TASK_XML%"
echo   ^<RegistrationInfo^> >> "%TASK_XML%"
echo     ^<Date^>%DATE%T%TIME%^</Date^> >> "%TASK_XML%"
echo     ^<Author^>HDU Campus Network Auto-Login^</Author^> >> "%TASK_XML%"
echo     ^<Description^>杭州电子科技大学校园网自动登录程序^</Description^> >> "%TASK_XML%"
echo   ^</RegistrationInfo^> >> "%TASK_XML%"
echo   ^<Triggers^> >> "%TASK_XML%"
echo     ^<LogonTrigger^> >> "%TASK_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo       ^<Delay^>PT1M^</Delay^> >> "%TASK_XML%"
echo     ^</LogonTrigger^> >> "%TASK_XML%"
echo     ^<TimeTrigger^> >> "%TASK_XML%"
echo       ^<Repetition^> >> "%TASK_XML%"
echo         ^<Interval^>PT30M^</Interval^> >> "%TASK_XML%"
echo         ^<StopAtDurationEnd^>false^</StopAtDurationEnd^> >> "%TASK_XML%"
echo       ^</Repetition^> >> "%TASK_XML%"
echo       ^<StartBoundary^>2024-01-01T00:00:00^</StartBoundary^> >> "%TASK_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo     ^</TimeTrigger^> >> "%TASK_XML%"
echo   ^</Triggers^> >> "%TASK_XML%"
echo   ^<Principals^> >> "%TASK_XML%"
echo     ^<Principal id="Author"^> >> "%TASK_XML%"
echo       ^<LogonType^>InteractiveToken^</LogonType^> >> "%TASK_XML%"
echo       ^<RunLevel^>LeastPrivilege^</RunLevel^> >> "%TASK_XML%"
echo     ^</Principal^> >> "%TASK_XML%"
echo   ^</Principals^> >> "%TASK_XML%"
echo   ^<Settings^> >> "%TASK_XML%"
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> "%TASK_XML%"
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> "%TASK_XML%"
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> "%TASK_XML%"
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^> >> "%TASK_XML%"
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> "%TASK_XML%"
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^> >> "%TASK_XML%"
echo     ^<IdleSettings^> >> "%TASK_XML%"
echo       ^<StopOnIdleEnd^>false^</StopOnIdleEnd^> >> "%TASK_XML%"
echo       ^<RestartOnIdle^>false^</RestartOnIdle^> >> "%TASK_XML%"
echo     ^</IdleSettings^> >> "%TASK_XML%"
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^> >> "%TASK_XML%"
echo     ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo     ^<Hidden^>false^</Hidden^> >> "%TASK_XML%"
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^> >> "%TASK_XML%"
echo     ^<DisallowStartOnRemoteAppSession^>false^</DisallowStartOnRemoteAppSession^> >> "%TASK_XML%"
echo     ^<UseUnifiedSchedulingEngine^>true^</UseUnifiedSchedulingEngine^> >> "%TASK_XML%"
echo     ^<WakeToRun^>false^</WakeToRun^> >> "%TASK_XML%"
echo     ^<ExecutionTimeLimit^>PT1H^</ExecutionTimeLimit^> >> "%TASK_XML%"
echo     ^<Priority^>7^</Priority^> >> "%TASK_XML%"
echo   ^</Settings^> >> "%TASK_XML%"
echo   ^<Actions Context="Author"^> >> "%TASK_XML%"
echo     ^<Exec^> >> "%TASK_XML%"
echo       ^<Command^>python^</Command^> >> "%TASK_XML%"
echo       ^<Arguments^>"%SCRIPT_DIR%\campus_login.py"^</Arguments^> >> "%TASK_XML%"
echo       ^<WorkingDirectory^>%SCRIPT_DIR%^</WorkingDirectory^> >> "%TASK_XML%"
echo     ^</Exec^> >> "%TASK_XML%"
echo   ^</Actions^> >> "%TASK_XML%"
echo ^</Task^> >> "%TASK_XML%"

:: 导入任务计划
schtasks /create /tn "HDU_Campus_Login" /xml "%TASK_XML%" /f >nul 2>&1

if %errorLevel% neq 0 (
    echo 错误: 任务计划创建失败
    pause
    exit /b 1
)

echo 任务计划创建成功！

:: 添加到启动项（注册表方式）
echo.
echo 正在添加到Windows启动项...
set "STARTUP_CMD=python \"%SCRIPT_DIR%\campus_login.py\""
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "HDU_Campus_Login" /t REG_SZ /d "%STARTUP_CMD%" /f >nul 2>&1

if %errorLevel% neq 0 (
    echo 警告: 启动项添加失败，但不影响任务计划功能
) else (
    echo 启动项添加成功！
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 程序功能:
echo - 开机自动启动（延迟1分钟）
echo - 每30分钟自动检测并登录
echo - 静默运行，不打扰用户
echo.
echo 配置文件: %SCRIPT_DIR%\config.json
echo 日志文件: %SCRIPT_DIR%\campus_login.log
echo.
echo 请编辑 config.json 文件，填入正确的用户名和密码
echo 然后重启计算机或手动运行一次测试
echo.
echo 手动测试命令: python "%SCRIPT_DIR%\campus_login.py"
echo.
pause
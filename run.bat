@echo off
IF EXIST main.py (
py main.py
) else (
echo main.py file missing !!! Please check files...
)
timeout /t 10
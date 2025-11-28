@echo off

set "script_dir=%~dp0"

cd "%script_dir%"

start "main" python .\init.py


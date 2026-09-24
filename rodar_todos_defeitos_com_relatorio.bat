@echo off
.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito
set ROBOT_RC=%ERRORLEVEL%
.venv\Scripts\python.exe tools\reporting\gerar_relatorios_checks.py
start reports\relatorio_consolidado.html
exit /b %ROBOT_RC%

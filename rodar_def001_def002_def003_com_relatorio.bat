@echo off
.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito\HOT-INV-DEF-001.robot tests\hot\inventario\defeito\HOT-INV-DEF-002.robot tests\hot\inventario\defeito\HOT-INV-DEF-003.robot
.venv\Scripts\python.exe tools\reporting\gerar_relatorio_def001.py && .venv\Scripts\python.exe tools\reporting\gerar_relatorio_def002.py && .venv\Scripts\python.exe tools\reporting\gerar_relatorio_def003.py && .venv\Scripts\python.exe tools\reporting\gerar_relatorio_consolidado.py && start reports\relatorio_consolidado.html

@echo off
setlocal

where python >nul 2>nul || (echo ERRO: Python nao encontrado no PATH. & exit /b 1)
where node >nul 2>nul || (echo ERRO: Node.js nao encontrado no PATH. & exit /b 1)
where git >nul 2>nul || (echo ERRO: Git nao encontrado no PATH. & exit /b 1)

if not exist .venv (
    echo Criando ambiente virtual com o Python disponivel no PATH...
    python -m venv .venv || exit /b 1
)

call .venv\Scripts\activate || exit /b 1
python -m pip install --upgrade pip || exit /b 1
python -m pip install -r requirements.txt || exit /b 1
rfbrowser init || exit /b 1

echo.
echo Validando ambiente...
python --version || exit /b 1
robot --version || exit /b 1
rfbrowser --version || exit /b 1

echo.
echo Ambiente preparado com sucesso.
endlocal

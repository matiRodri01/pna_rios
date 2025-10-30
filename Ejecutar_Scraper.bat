@echo off
REM EJECUTOR SCRAPER PNA RIOS v1.2 - AUTOMÁTICO (doble clic)
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Detectar venv en la raiz o en PNA_Rios_Portable
set "VENV_DIR=%SCRIPT_DIR%venv_pna_rios"
if not exist "%VENV_DIR%" (
    if exist "%SCRIPT_DIR%PNA_Rios_Portable\venv_pna_rios" (
        set "VENV_DIR=%SCRIPT_DIR%PNA_Rios_Portable\venv_pna_rios"
    )
)

if not exist "%VENV_DIR%" (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Entorno virtual no encontrado. Ejecute Instalar_PNA_Rios.bat primero.','PNA Rios - Error','OK','Error')"
    exit /b 1
)

set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

REM Verificar archivos principales
if not exist "%SCRIPT_DIR%scraper.py" (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('scraper.py no encontrado en la carpeta. Asegurese de tener los archivos del proyecto aqui.','PNA Rios - Error','OK','Error')"
    exit /b 1
)
if not exist "%SCRIPT_DIR%config.py" (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('config.py no encontrado en la carpeta. Asegurese de tener los archivos del proyecto aqui.','PNA Rios - Error','OK','Error')"
    exit /b 1
)

REM Verificar que dependencias principales esten instaladas (usando python del venv)
"%VENV_PY%" -c "import requests, bs4, pandas, selenium, pywhatkit, colorama" >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Faltan dependencias en el entorno. Ejecute Instalar_PNA_Rios.bat.','PNA Rios - Error','OK','Error')"
    exit /b 1
)

REM Ejecutar el scraper con el python del venv (aislado)
echo [INFO] Ejecutando con Python aislado del venv...
echo [INFO] Python utilizado: %VENV_PY%
"%VENV_PY%" "%SCRIPT_DIR%scraper.py"
set "RET=%ERRORLEVEL%"

REM Limpiar variables de entorno para evitar conflictos
set "VENV_PY="
set "VENV_DIR="

REM Resultado: informar por ventana y salir
if "%RET%"=="0" (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Ejecucion completada correctamente. Revise la carpeta datos/ y logs/.','PNA Rios','OK','Information')"
    exit /b 0
) else (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('La ejecucion finalizo con errores. Revise el archivo de logs en la carpeta logs/.','PNA Rios - Error','OK','Error')"
    exit /b %RET%
)

endlocal
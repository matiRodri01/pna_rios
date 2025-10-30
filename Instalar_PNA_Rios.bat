@echo off
REM INSTALADOR SCRAPER PNA RIOS v1.3 - AUTOMÁTICO (doble clic)
setlocal

echo =========================================
echo   INSTALADOR SCRAPER PNA RIOS v1.3
echo =========================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Python no esta instalado en este equipo. Instale Python 3.8+ y marque \"Add to PATH\" durante la instalación.','Instalador PNA Rios','OK','Error')"
    exit /b 1
)

REM Directorio del script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Por defecto crear entorno virtual en la carpeta actual (raíz)
set "VENV_DIR=%SCRIPT_DIR%venv_pna_rios"

REM Soporte para /portable si se desea (mantener compatibilidad)
if "%1"=="/portable" (
    if not exist "%SCRIPT_DIR%PNA_Rios_Portable" mkdir "%SCRIPT_DIR%PNA_Rios_Portable"
    set "VENV_DIR=%SCRIPT_DIR%PNA_Rios_Portable\venv_pna_rios"
)

echo [INFO] Entorno virtual destino: %VENV_DIR%

REM Crear entorno virtual si no existe
if exist "%VENV_DIR%" (
    echo [INFO] Entorno virtual ya existe: %VENV_DIR%
) else (
    echo [INFO] Creando entorno virtual Python...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('No se pudo crear el entorno virtual. Revise permisos o la instalacion de Python.','Instalador PNA Rios','OK','Error')"
        exit /b 1
    )
)

REM Usar el python del venv para instalar (no necesitamos activar)
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

REM Actualizar pip/wheel/setuptools
"%VENV_PY%" -m pip install --upgrade pip wheel setuptools >nul 2>&1

REM Intentar instalar desde requirements.txt
if exist "%SCRIPT_DIR%requirements.txt" (
    "%VENV_PY%" -m pip install -r "%SCRIPT_DIR%requirements.txt"
    if %errorlevel% neq 0 (
        echo [WARN] Instalacion desde requirements.txt fallo. Intentando paquetes individuales...
        REM Lista de paquetes críticos
        set PACKS=requests==2.32.5 beautifulsoup4==4.12.3 lxml==5.3.0 selenium==4.25.0 pandas==2.3.3 openpyxl==3.1.5 numpy==2.3.4 pywhatkit==5.4 pyautogui==0.9.54 Pillow==11.0.0 python-dateutil==2.9.0.post0 schedule==1.2.2 colorama==0.4.6 python-dotenv==1.0.1 webdriver-manager==4.0.2
        for %%P in (%PACKS%) do (
            echo [INFO] Instalando %%P ...
            "%VENV_PY%" -m pip install %%P
            if errorlevel 1 (
                echo [WARN] Reintentando %%P ...
                "%VENV_PY%" -m pip install %%P
            )
        )
    ) else (
        echo [INFO] Dependencias instaladas desde requirements.txt
    )
) else (
    echo [WARN] requirements.txt no encontrado. Instalando paquetes criticos individualmente...
    "%VENV_PY%" -m pip install requests beautifulsoup4 lxml selenium pandas openpyxl numpy pywhatkit pyautogui Pillow python-dateutil schedule colorama python-dotenv webdriver-manager
)

REM Asegurar que lxml esté instalado (es crítico)
"%VENV_PY%" -m pip show lxml >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] lxml no encontrado. Intentando instalar lxml explicitamente...
    "%VENV_PY%" -m pip install lxml
    if %errorlevel% neq 0 (
        echo [WARN] Intentando instalar rueda binaria de lxml...
        "%VENV_PY%" -m pip install --only-binary=:all: lxml
        if %errorlevel% neq 0 (
            echo [ERROR] No se pudo instalar lxml automaticamente.
            powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('ATENCION: No se pudo instalar la dependencia lxml automaticamente. El instalador continuo pero el parser lxml puede faltar.','Instalador PNA Rios','OK','Warning')"
        ) else (
            echo [INFO] lxml instalado correctamente (rueda).
        )
    ) else (
        echo [INFO] lxml instalado correctamente.
    )
) else (
    echo [INFO] lxml ya instalado.
)

REM Crear carpetas datos y logs si no existen
if not exist "%SCRIPT_DIR%datos" mkdir "%SCRIPT_DIR%datos"
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

REM Mensaje final al usuario (ventana)
powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Instalacion completada correctamente.\n\nPara ejecutar el sistema haga DOBLE-CLICK en Ejecutar_Scraper.bat.','Instalador PNA Rios','OK','Information')"

endlocal
exit /b 0
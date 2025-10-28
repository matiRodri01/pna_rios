@echo off
echo =========================================
echo   INSTALADOR SCRAPER PNA RIOS v1.0
echo =========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado en este sistema.
    echo.
    echo Por favor:
    echo 1. Descarga Python desde https://python.org
    echo 2. Instala Python marcando "Add to PATH"
    echo 3. Ejecuta este instalador nuevamente
    echo.
    pause
    exit /b 1
)

echo [INFO] Python encontrado correctamente
python --version

REM Crear directorio de trabajo si no existe
if not exist "PNA_Rios_Portable" (
    echo [INFO] Creando directorio PNA_Rios_Portable...
    mkdir PNA_Rios_Portable
)

cd PNA_Rios_Portable

REM Crear entorno virtual
echo [INFO] Creando entorno virtual Python...
python -m venv venv_pna_rios
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv_pna_rios\Scripts\activate.bat

REM Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install requests==2.32.5
pip install beautifulsoup4==4.12.3
pip install lxml==5.3.0
pip install selenium==4.25.0
pip install pandas==2.3.3
pip install openpyxl==3.1.5
pip install numpy==2.3.4
pip install pywhatkit==5.4
pip install pyautogui==0.9.54
pip install Pillow==11.0.0
pip install python-dateutil==2.9.0.post0
pip install schedule==1.2.2
pip install colorama==0.4.6
pip install python-dotenv==1.0.1
pip install webdriver-manager==4.0.2

if %errorlevel% neq 0 (
    echo [ERROR] Error instalando dependencias
    pause
    exit /b 1
)

REM Crear directorios necesarios
echo [INFO] Creando estructura de directorios...
if not exist "datos" mkdir datos
if not exist "logs" mkdir logs

echo [INFO] Instalacion completada exitosamente!
echo.
echo =========================================
echo   INSTALACION COMPLETADA
echo =========================================
echo.
echo El sistema se ha instalado en: %cd%
echo.
echo PROXIMOS PASOS:
echo 1. Copia los archivos del proyecto (config.py, scraper.py) a esta carpeta
echo 2. Ejecuta "Ejecutar_Scraper.bat" para iniciar el sistema
echo.
echo Archivos necesarios:
echo - config.py (configuracion del sistema)
echo - scraper.py (programa principal)
echo.
pause
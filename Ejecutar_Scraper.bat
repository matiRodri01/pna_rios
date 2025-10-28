@echo off
echo =========================================
echo     SCRAPER PNA RIOS - EJECUTOR v1.0
echo =========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "venv_pna_rios" (
    echo [ERROR] Entorno virtual no encontrado.
    echo.
    echo Este ejecutor debe estar en la carpeta donde se instalo el sistema.
    echo Si no has instalado el sistema, ejecuta primero "Instalar_PNA_Rios.bat"
    echo.
    pause
    exit /b 1
)

if not exist "scraper.py" (
    echo [ERROR] scraper.py no encontrado.
    echo.
    echo Asegurate de que los archivos del proyecto esten en esta carpeta:
    echo - scraper.py
    echo - config.py
    echo.
    pause
    exit /b 1
)

if not exist "config.py" (
    echo [ERROR] config.py no encontrado.
    echo.
    echo Asegurate de que los archivos del proyecto esten en esta carpeta:
    echo - scraper.py  
    echo - config.py
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv_pna_rios\Scripts\activate.bat

REM Verificar que las dependencias estén instaladas
echo [INFO] Verificando dependencias...
python -c "import requests, bs4, pandas, selenium, pywhatkit, colorama" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Dependencias no instaladas correctamente.
    echo Ejecuta "Instalar_PNA_Rios.bat" para reinstalar.
    pause
    exit /b 1
)

echo [INFO] Sistema listo para ejecutar
echo.
echo =========================================
echo     INICIANDO SCRAPER PNA RIOS
echo =========================================
echo.

REM Ejecutar el scraper
python scraper.py

REM Mostrar resultado
if %errorlevel% equ 0 (
    echo.
    echo =========================================
    echo     EJECUCION COMPLETADA EXITOSAMENTE
    echo =========================================
    echo.
    echo Revisa la carpeta 'datos' para ver los archivos generados.
    echo Revisa la carpeta 'logs' para ver los registros del sistema.
) else (
    echo.
    echo =========================================
    echo     ERROR EN LA EJECUCION
    echo =========================================
    echo.
    echo Revisa los logs para mas informacion.
)

echo.
pause
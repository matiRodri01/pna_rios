@echo off
echo ================================================================
echo         VERIFICADOR DE SISTEMA - SCRAPER PNA RIOS
echo ================================================================
echo.
echo Este script verificara que todos los componentes esten listos.
echo.

REM Verificar Python
echo [1/8] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python NO esta instalado
    echo    Descargar desde: https://python.org
) else (
    echo ✅ Python esta instalado
    python --version
)
echo.

REM Verificar entorno virtual
echo [2/8] Verificando entorno virtual...
if exist venv_pna_rios (
    echo ✅ Entorno virtual venv_pna_rios existe
) else (
    echo ❌ Entorno virtual NO existe
    echo    Ejecutar: Instalar_PNA_Rios.bat
)
echo.

REM Verificar dependencias criticas
echo [3/8] Verificando dependencias Python...
if exist venv_pna_rios (
    venv_pna_rios\Scripts\python.exe -c "import requests, bs4, selenium, pandas, pywhatkit, colorama; print('✅ Todas las dependencias criticas instaladas')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Faltan dependencias Python
        echo    Ejecutar: Instalar_PNA_Rios.bat
        echo    Dependencias requeridas: requests, beautifulsoup4, selenium, pandas, pywhatkit, colorama
    )
) else (
    echo ⏭️  Saltando verificacion (no hay entorno virtual)
)
echo.

REM Verificar WebDriver Manager
echo [4/8] Verificando WebDriver Manager...
if exist venv_pna_rios (
    venv_pna_rios\Scripts\python.exe -c "from webdriver_manager.chrome import ChromeDriverManager; print('✅ WebDriver Manager disponible')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ WebDriver Manager no disponible
        echo    Necesario para automatizacion SUA
    )
) else (
    echo ⏭️  Saltando verificacion (no hay entorno virtual)
)
echo.

REM Verificar archivos principales
echo [5/8] Verificando archivos del sistema...
if exist scraper.py (
    echo ✅ scraper.py existe
) else (
    echo ❌ scraper.py NO existe - Archivo principal faltante
)

if exist config.py (
    echo ✅ config.py existe
) else (
    echo ❌ config.py NO existe - Configuracion faltante
)

if exist requirements.txt (
    echo ✅ requirements.txt existe
) else (
    echo ❌ requirements.txt NO existe - Lista de dependencias faltante
)
echo.

REM Verificar estructura de carpetas
echo [6/8] Verificando estructura de carpetas...
if exist datos (
    echo ✅ Carpeta datos/ existe
) else (
    echo ⚠️  Carpeta datos/ NO existe - Se creara automaticamente
)

if exist logs (
    echo ✅ Carpeta logs/ existe
) else (
    echo ⚠️  Carpeta logs/ NO existe - Se creara automaticamente  
)
echo.

REM Verificar conectividad a PNA
echo [7/8] Verificando conectividad web PNA...
if exist venv_pna_rios (
    venv_pna_rios\Scripts\python.exe -c "import requests; r=requests.get('https://contenidosweb.prefecturanaval.gob.ar/alturas/index.php', timeout=10); print('✅ Conexion a PNA exitosa') if r.status_code==200 else print('❌ Error de conexion a PNA')" 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  No se pudo verificar conectividad a PNA
        echo    Verificar conexion a internet
    )
) else (
    echo ⏭️  Saltando verificacion (no hay entorno virtual)
)
echo.

REM Verificar configuracion WhatsApp
echo [8/8] Verificando configuracion WhatsApp...
if exist venv_pna_rios (
    venv_pna_rios\Scripts\python.exe -c "try: from config import NUMERO_WHATSAPP, ESTACIONES_WHATSAPP; print('✅ Configuracion WhatsApp correcta' if NUMERO_WHATSAPP and ESTACIONES_WHATSAPP else '⚠️  Configuracion WhatsApp incompleta'); except ImportError: print('❌ Error al leer configuracion')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Error en configuracion WhatsApp
        echo    Verificar config.py
    )
) else (
    echo ⏭️  Saltando verificacion (no hay entorno virtual)
)
echo.

echo ================================================================
echo                    VERIFICACION COMPLETADA
echo ================================================================
echo.
echo LEYENDA:
echo ✅ = Componente funcionando correctamente
echo ⚠️  = Componente opcional o se crea automaticamente
echo ❌ = Componente con problemas - requiere atencion
echo.
echo Si todos los elementos criticos estan marcados con ✅,
echo el sistema esta listo para ejecutar el scraper.
echo.
echo Para ejecutar el sistema: doble clic en Ejecutar_Scraper.bat
echo.
pause
@echo off
echo =========================================
echo   CREADOR DE PAQUETE PORTABLE v1.0
echo =========================================
echo.

REM Crear carpeta del paquete portable
set PACKAGE_NAME=PNA_Rios_Portable_%date:~-4,4%%date:~-7,2%%date:~-10,2%
echo [INFO] Creando paquete: %PACKAGE_NAME%

if exist "%PACKAGE_NAME%" (
    echo [INFO] Eliminando paquete anterior...
    rmdir /s /q "%PACKAGE_NAME%"
)

mkdir "%PACKAGE_NAME%"

REM Copiar archivos esenciales
echo [INFO] Copiando archivos del sistema...
copy "config.py" "%PACKAGE_NAME%\"
copy "scraper.py" "%PACKAGE_NAME%\"
copy "requirements.txt" "%PACKAGE_NAME%\"
copy "README.md" "%PACKAGE_NAME%\"
copy "Instalar_PNA_Rios.bat" "%PACKAGE_NAME%\"
copy "Ejecutar_Scraper.bat" "%PACKAGE_NAME%\"

REM Crear directorios
mkdir "%PACKAGE_NAME%\datos"
mkdir "%PACKAGE_NAME%\logs"

REM Crear archivo de instrucciones
echo [INFO] Creando instrucciones...
(
echo =========================================
echo   INSTRUCCIONES DE USO - PNA RIOS
echo =========================================
echo.
echo PASO 1: INSTALACION
echo   1. Ejecuta "Instalar_PNA_Rios.bat"
echo   2. Espera a que termine la instalacion
echo.
echo PASO 2: CONFIGURACION
echo   1. Edita "config.py" si necesitas cambiar configuraciones
echo   2. El numero de WhatsApp ya esta configurado
echo   3. Las credenciales SUA se pediran al ejecutar
echo.
echo PASO 3: EJECUCION
echo   1. Ejecuta "Ejecutar_Scraper.bat"
echo   2. Sigue las instrucciones en pantalla
echo   3. Ingresa credenciales SUA cuando se solicite
echo.
echo ARCHIVOS GENERADOS:
echo   - datos\: Archivos Excel y CSV con datos
echo   - logs\: Registros del sistema
echo.
echo NOTA: Este sistema requiere Google Chrome instalado
echo.
echo Para soporte tecnico, revisa README.md
echo.
) > "%PACKAGE_NAME%\INSTRUCCIONES.txt"

REM Crear configuración de ejemplo
echo [INFO] Creando configuracion de ejemplo...
(
echo # EJEMPLO DE CONFIGURACION - PNA RIOS
echo # ===================================
echo.
echo # Para cambiar el numero de WhatsApp, edita esta linea:
echo NUMERO_WHATSAPP = "+5493415704962"
echo.
echo # Para cambiar las estaciones del WhatsApp, edita esta lista:
echo ESTACIONES_WHATSAPP = ["ANDRESITO", "IGUAZU", "ROSARIO"]
echo.
echo # Para deshabilitar SUA, cambia True por False:
echo SUA_ENABLED = True
echo.
echo # Las credenciales SUA se pediran al ejecutar el programa
echo # No es necesario configurarlas aqui por seguridad
echo.
echo # Todas las demas configuraciones estan optimizadas
echo # No es necesario modificarlas a menos que sepas lo que haces
) > "%PACKAGE_NAME%\CONFIGURACION_EJEMPLO.txt"

echo [INFO] Paquete portable creado exitosamente!
echo.
echo =========================================
echo   PAQUETE PORTABLE CREADO
echo =========================================
echo.
echo Ubicacion: %cd%\%PACKAGE_NAME%
echo.
echo CONTENIDO DEL PAQUETE:
echo - Instalar_PNA_Rios.bat (instalador)
echo - Ejecutar_Scraper.bat (ejecutor)
echo - scraper.py (programa principal)
echo - config.py (configuracion)
echo - requirements.txt (dependencias)
echo - README.md (documentacion)
echo - INSTRUCCIONES.txt (guia rapida)
echo - CONFIGURACION_EJEMPLO.txt (ayuda configuracion)
echo - datos\ (carpeta para archivos generados)
echo - logs\ (carpeta para registros)
echo.
echo LISTO PARA DISTRIBUIR!
echo.
pause
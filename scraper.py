#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRAPER DE ALTURAS DE RÍOS - PREFECTURA NAVAL ARGENTINA
=======================================================

Este script extrae datos de alturas de ríos de la página oficial de la PNA
y procesa únicamente las 36 estaciones específicas requeridas.

Autor: Sistema de Monitoreo PNA
Fecha: 2025-10-27
URL: https://contenidosweb.prefecturanaval.gob.ar/alturas/index.php
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
import time
import re
import os
import sys
from colorama import init, Fore, Back, Style
import pywhatkit as pwk
import config
import getpass

# Selenium para automatización web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Inicializar colorama para colores en Windows
init(autoreset=True)

class ScraperPNA:
    def __init__(self):
        """Inicializar el scraper con configuraciones"""
        self.url = config.URL_PNA
        self.estaciones_objetivo = config.ESTACIONES_OBJETIVO
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
        self.datos_extraidos = []
        self.timestamp = datetime.now()
        
        # Crear directorios si no existen
        os.makedirs(config.CARPETA_DATOS, exist_ok=True)
        os.makedirs(config.CARPETA_LOGS, exist_ok=True)
        
        # Configurar logging
        self.setup_logging()
        
        # Mostrar banner inicial
        self.mostrar_banner()
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        fecha_str = self.timestamp.strftime("%Y%m%d")
        log_file = config.ARCHIVO_LOG.format(fecha_str)
        
        logging.basicConfig(
            level=logging.INFO if config.DEBUG_MODE else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def mostrar_banner(self):
        """Mostrar banner inicial del sistema"""
        banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}    SCRAPER PNA RÍOS - SISTEMA DE MONITOREO HIDROLÓGICO
{Fore.CYAN}{'='*60}
{Fore.GREEN}📍 URL: {self.url}
{Fore.GREEN}🎯 Estaciones objetivo: {len(self.estaciones_objetivo)}
{Fore.GREEN}⏰ Timestamp: {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
{Fore.CYAN}{'='*60}{Style.RESET_ALL}
        """
        print(banner)
        self.logger.info("Scraper PNA iniciado")
    
    def obtener_datos_web(self):
        """Obtener datos de la página web de la PNA"""
        print(f"{Fore.BLUE}[1/4] Obteniendo datos de la web...{Style.RESET_ALL}")
        
        for intento in range(config.REINTENTOS_MAX):
            try:
                self.logger.info(f"Intento {intento + 1} de obtener datos web")
                
                response = self.session.get(
                    self.url, 
                    timeout=config.TIMEOUT_REQUEST
                )
                response.raise_for_status()
                response.encoding = 'utf-8'
                
                print(f"{Fore.GREEN}✓ Datos obtenidos exitosamente ({len(response.text)} caracteres){Style.RESET_ALL}")
                self.logger.info(f"Datos web obtenidos: {len(response.text)} caracteres")
                
                return response.text
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error en intento {intento + 1}: {e}")
                if intento < config.REINTENTOS_MAX - 1:
                    print(f"{Fore.YELLOW}⚠ Error en intento {intento + 1}, reintentando en {config.DELAY_ENTRE_REINTENTOS}s...{Style.RESET_ALL}")
                    time.sleep(config.DELAY_ENTRE_REINTENTOS)
                else:
                    print(f"{Fore.RED}✗ Error fatal al obtener datos web{Style.RESET_ALL}")
                    raise
        
        return None
    
    def parsear_html(self, html_content):
        """Parsear HTML y extraer solo Puerto, Ult. registro y Estado"""
        print(f"{Fore.BLUE}[2/4] Parseando datos HTML (Puerto, Altura, Estado)...{Style.RESET_ALL}")
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Buscar todas las filas de tabla
        filas = soup.find_all('tr')
        self.logger.info(f"Encontradas {len(filas)} filas en la página")
        
        datos_encontrados = []
        
        for fila in filas:
            celdas = fila.find_all(['td', 'th'])
            
            # Verificar que tiene suficientes columnas (mínimo para puerto, altura, estado)
            if len(celdas) >= 6:
                try:
                    # Obtener texto de cada celda
                    textos = [celda.get_text(strip=True) for celda in celdas]
                    
                    # Según el análisis correcto de la página PNA:
                    # Columna 0: Puerto/Estación
                    # Columna 2: Altura actual (Ult. registro)  
                    # Columna 6: Estado/Tendencia
                    
                    puerto = textos[0] if len(textos) > 0 else ""
                    altura = textos[2] if len(textos) > 2 else ""
                    estado = textos[6] if len(textos) > 6 else ""
                    
                    # Filtrar filas válidas
                    if (puerto and 
                        puerto not in ["RIO", "DETALLE", "", "FUENTES", "Prefectura", "Puerto"] and
                        not puerto.startswith("FUENTES") and
                        not puerto.startswith("Los datos") and
                        altura and 
                        altura not in ["", "-", "ALTURA", "Ult. registro"] and
                        estado and
                        estado not in ["", "Estado"]):
                        
                        datos_encontrados.append({
                            'puerto': puerto,
                            'altura': altura,
                            'estado': estado
                        })
                        
                        # Debug: mostrar primeros registros encontrados
                        if config.DEBUG_MODE and len(datos_encontrados) <= 5:
                            self.logger.debug(f"Registro {len(datos_encontrados)}: {puerto} - {altura}m - {estado}")
                            
                except Exception as e:
                    self.logger.debug(f"Error procesando fila: {e}")
                    continue
        
        self.logger.info(f"Datos extraídos de HTML: {len(datos_encontrados)} registros")
        print(f"{Fore.GREEN}✓ Parseado completado: {len(datos_encontrados)} registros encontrados{Style.RESET_ALL}")
        
        # Mostrar muestra de datos encontrados
        if config.DEBUG_MODE and datos_encontrados:
            print(f"{Fore.CYAN}🔍 MUESTRA DE DATOS PARSEADOS (primeros 5):{Style.RESET_ALL}")
            for i, dato in enumerate(datos_encontrados[:5]):
                print(f"   {i+1}. {dato['puerto']} - {dato['altura']} - {dato['estado']}")
        
        return datos_encontrados
    
    def filtrar_estaciones_objetivo(self, datos_brutos):
        """Filtrar solo las 36 estaciones que necesitamos"""
        print(f"{Fore.BLUE}[3/4] Filtrando 36 estaciones objetivo...{Style.RESET_ALL}")
        
        datos_filtrados = []
        estaciones_encontradas = set()
        
        for dato in datos_brutos:
            puerto = dato['puerto'].upper().strip()
            
            # Buscar coincidencias exactas con nuestras estaciones objetivo
            for estacion_objetivo in self.estaciones_objetivo:
                if puerto == estacion_objetivo.upper():
                    # Crear registro limpio con solo los 3 campos necesarios
                    altura_limpia = self.limpiar_numero(dato['altura'])
                    
                    datos_filtrados.append({
                        'estacion': estacion_objetivo,
                        'puerto_original': dato['puerto'],
                        'altura': altura_limpia,
                        'tendencia': dato['estado'],
                        'timestamp_scraping': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    estaciones_encontradas.add(estacion_objetivo)
                    break
        
        # Mostrar resumen
        print(f"{Fore.GREEN}✓ Estaciones encontradas: {len(estaciones_encontradas)}/{len(self.estaciones_objetivo)}{Style.RESET_ALL}")
        
        # Mostrar estaciones no encontradas
        estaciones_faltantes = set(self.estaciones_objetivo) - estaciones_encontradas
        if estaciones_faltantes:
            print(f"{Fore.YELLOW}⚠ Estaciones no encontradas: {', '.join(sorted(estaciones_faltantes))}{Style.RESET_ALL}")
            self.logger.warning(f"Estaciones faltantes: {estaciones_faltantes}")
        
        # Mostrar datos encontrados en formato solicitado
        if config.DEBUG_MODE and datos_filtrados:
            print(f"\n{Fore.CYAN}📊 DATOS EN FORMATO SOLICITADO:{Style.RESET_ALL}")
            for dato in datos_filtrados:
                altura_str = f"{dato['altura']}m" if dato['altura'] != 'S/E' else 'Sin datos'
                tendencia = dato['tendencia']
                print(f"   {Fore.WHITE}{dato['estacion']:<20} (Altura - Tendencia): {altura_str} - {tendencia}{Style.RESET_ALL}")
        
        self.datos_extraidos = datos_filtrados
        return datos_filtrados
    
    def limpiar_numero(self, valor):
        """Limpiar y convertir valores numéricos"""
        if not valor or valor.strip() in ['S/E', '-', '']:
            return 'S/E'
        
        # Remover caracteres no numéricos excepto punto y signo negativo
        valor_limpio = re.sub(r'[^\d\.\-]', '', str(valor).strip())
        
        try:
            return float(valor_limpio)
        except (ValueError, TypeError):
            return 'S/E'
    
    def guardar_datos(self):
        """Guardar datos en Excel y CSV"""
        print(f"{Fore.BLUE}[4/4] Guardando datos...{Style.RESET_ALL}")
        
        if not self.datos_extraidos:
            print(f"{Fore.RED}✗ No hay datos para guardar{Style.RESET_ALL}")
            return False
        
        # Crear DataFrame
        df = pd.DataFrame(self.datos_extraidos)
        
        # Generar nombres de archivo con timestamp
        fecha_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        archivo_excel = config.ARCHIVO_DATOS_EXCEL.format(fecha_str)
        archivo_csv = config.ARCHIVO_DATOS_CSV.format(fecha_str)
        
        try:
            # Guardar en Excel
            df.to_excel(archivo_excel, index=False, engine='openpyxl')
            print(f"{Fore.GREEN}✓ Datos guardados en Excel: {archivo_excel}{Style.RESET_ALL}")
            
            # Guardar en CSV
            df.to_csv(archivo_csv, index=False, encoding='utf-8')
            print(f"{Fore.GREEN}✓ Datos guardados en CSV: {archivo_csv}{Style.RESET_ALL}")
            
            self.logger.info(f"Datos guardados: {len(self.datos_extraidos)} registros")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error al guardar datos: {e}{Style.RESET_ALL}")
            self.logger.error(f"Error guardando datos: {e}")
            return False
    
    def detectar_alertas(self):
        """Detectar niveles críticos y generar alertas"""
        alertas = []
        
        for dato in self.datos_extraidos:
            estacion = dato['estacion']
            altura = dato['altura']
            
            if altura == 'S/E' or not isinstance(altura, (int, float)):
                continue
            
            # Obtener niveles críticos para esta estación
            if estacion in config.NIVELES_CRITICOS:
                nivel_alerta = config.NIVELES_CRITICOS[estacion]['alerta']
                nivel_evacuacion = config.NIVELES_CRITICOS[estacion]['evacuacion']
            else:
                nivel_alerta = config.NIVEL_ALERTA_DEFECTO
                nivel_evacuacion = config.NIVEL_EVACUACION_DEFECTO
            
            # Verificar alertas
            if altura >= nivel_evacuacion:
                alertas.append({
                    'estacion': estacion,
                    'altura': altura,
                    'tipo': 'EVACUACIÓN',
                    'nivel_critico': nivel_evacuacion,
                    'tendencia': dato['tendencia']
                })
            elif altura >= nivel_alerta:
                alertas.append({
                    'estacion': estacion,
                    'altura': altura,
                    'tipo': 'ALERTA',
                    'nivel_critico': nivel_alerta,
                    'tendencia': dato['tendencia']
                })
        
        return alertas
    
    def enviar_whatsapp(self, mensaje):
        """Enviar mensaje por WhatsApp"""
        try:
            print(f"{Fore.BLUE}📱 Enviando mensaje por WhatsApp...{Style.RESET_ALL}")
            
            # Enviar mensaje inmediatamente
            pwk.sendwhatmsg_instantly(
                config.NUMERO_WHATSAPP,
                mensaje,
                wait_time=config.DELAY_WHATSAPP,
                tab_close=True
            )
            
            print(f"{Fore.GREEN}✓ Mensaje enviado por WhatsApp{Style.RESET_ALL}")
            self.logger.info("Mensaje WhatsApp enviado exitosamente")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error enviando WhatsApp: {e}{Style.RESET_ALL}")
            self.logger.error(f"Error WhatsApp: {e}")
    
    def generar_mensaje_whatsapp(self):
        """Generar mensaje específico para WhatsApp con las 3 estaciones"""
        
        # Filtrar solo las 3 estaciones específicas para WhatsApp
        datos_whatsapp = []
        
        for dato in self.datos_extraidos:
            if dato['estacion'] in config.ESTACIONES_WHATSAPP:
                datos_whatsapp.append(dato)
        
        if not datos_whatsapp:
            return None
        
        # Obtener fecha de la página (usar la fecha de scraping)
        fecha_str = self.timestamp.strftime("%d/%m/%y")
        
        # Construir mensaje en el formato solicitado
        mensaje = "Buenos días\n"
        mensaje += "Altura de los ríos\n"
        mensaje += f"{fecha_str}\n\n\n"
        
        # Ordenar datos según el orden solicitado: ANDRESITO, IGUAZU, ROSARIO
        orden_estaciones = ["ANDRESITO", "IGUAZU", "ROSARIO"]
        
        for estacion_nombre in orden_estaciones:
            # Buscar la estación en los datos
            for dato in datos_whatsapp:
                if dato['estacion'] == estacion_nombre:
                    altura = dato['altura'] if dato['altura'] != 'S/E' else 'Sin datos'
                    tendencia = dato['tendencia']
                    
                    # Formatear tendencia con emojis
                    if tendencia == "CRECE":
                        tendencia_emoji = "CRECE ⬆️"
                    elif tendencia == "BAJA":
                        tendencia_emoji = "BAJA ⬇️"
                    elif tendencia == "ESTAC.":
                        tendencia_emoji = "ESTACIONADO ➡️"
                    else:
                        tendencia_emoji = tendencia  # Para casos como S/E.
                    
                    # Formatear nombre de estación
                    nombre_mostrar = estacion_nombre
                    if estacion_nombre == "IGUAZU":
                        nombre_mostrar = "Iguazú"
                    elif estacion_nombre == "ANDRESITO":
                        nombre_mostrar = "Andresito"
                    elif estacion_nombre == "ROSARIO":
                        nombre_mostrar = "Rosario"
                    
                    # Agregar línea al mensaje
                    if altura != 'Sin datos':
                        mensaje += f"{nombre_mostrar}:   {altura} - {tendencia_emoji}\n"
                    else:
                        mensaje += f"{nombre_mostrar}:   Sin datos - {tendencia_emoji}\n"
                    break
        
        mensaje += "\nInformación brindada por la pagina web de Prefectura Naval Argentina."
        
        return mensaje
    
    def obtener_credenciales_sua(self):
        """Obtener credenciales SUA de forma segura"""
        print(f"\n{Fore.CYAN}🔐 CREDENCIALES SISTEMA SUA ROSARIO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        # Si ya están configuradas, usarlas
        if config.SUA_USERNAME and config.SUA_PASSWORD:
            print(f"{Fore.GREEN}✓ Credenciales encontradas en configuración{Style.RESET_ALL}")
            return config.SUA_USERNAME, config.SUA_PASSWORD
        
        print(f"{Fore.YELLOW}Por favor, ingresa tus credenciales del Sistema SUA:{Style.RESET_ALL}")
        
        while True:
            try:
                usuario = input(f"{Fore.CYAN}Usuario SUA: {Style.RESET_ALL}").strip()
                if not usuario:
                    print(f"{Fore.RED}✗ El usuario no puede estar vacío{Style.RESET_ALL}")
                    continue
                
                contraseña = getpass.getpass(f"{Fore.CYAN}Contraseña SUA: {Style.RESET_ALL}")
                if not contraseña:
                    print(f"{Fore.RED}✗ La contraseña no puede estar vacía{Style.RESET_ALL}")
                    continue
                
                # Confirmar credenciales
                print(f"\n{Fore.YELLOW}Credenciales ingresadas:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Usuario: {usuario}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Contraseña: {'*' * len(contraseña)}{Style.RESET_ALL}")
                
                confirmar = input(f"{Fore.CYAN}¿Son correctas? (s/n): {Style.RESET_ALL}").strip().lower()
                if confirmar in ['s', 'si', 'yes', 'y']:
                    return usuario, contraseña
                else:
                    print(f"{Fore.YELLOW}Volviendo a solicitar credenciales...{Style.RESET_ALL}\n")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}✗ Operación cancelada por el usuario{Style.RESET_ALL}")
                return None, None
    
    def cargar_datos_sua(self):
        """Cargar datos automáticamente en el sistema SUA de Rosario"""
        if not config.SUA_ENABLED:
            print(f"{Fore.YELLOW}ℹ SUA activado: No habilitado en configuración{Style.RESET_ALL}")
            return True
            
        if not self.datos_extraidos:
            print(f"{Fore.RED}✗ No hay datos para cargar en SUA{Style.RESET_ALL}")
            return False
        
        # Obtener credenciales de forma segura
        usuario, contraseña = self.obtener_credenciales_sua()
        if not usuario or not contraseña:
            print(f"{Fore.RED}✗ No se pudieron obtener credenciales válidas{Style.RESET_ALL}")
            return False
        
        # Intentar hasta 3 veces en caso de error de autorización    
        max_intentos = 3
        for intento in range(1, max_intentos + 1):
            print(f"{Fore.CYAN}🌐 Intento {intento}/{max_intentos} - Iniciando carga automática en SUA Rosario...{Style.RESET_ALL}")
            
            resultado = self._cargar_datos_sua_intento(usuario, contraseña)
            
            if resultado == "reintentar":
                print(f"{Fore.YELLOW}⚠ Error de autorización detectado. Reintentando...{Style.RESET_ALL}")
                time.sleep(5)  # Esperar antes del siguiente intento
                continue
            elif resultado:
                return True
            else:
                if intento < max_intentos:
                    print(f"{Fore.YELLOW}⚠ Intento {intento} falló. Reintentando...{Style.RESET_ALL}")
                    time.sleep(5)
                    continue
                else:
                    print(f"{Fore.RED}✗ Todos los intentos fallaron{Style.RESET_ALL}")
                    return False
        
        return False
    
    def _cargar_datos_sua_intento(self, usuario, contraseña):
        """Intento individual de cargar datos en SUA"""
        driver = None
        try:
            # Configurar Chrome para que no se cierre automáticamente
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Inicializar driver con ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            wait = WebDriverWait(driver, config.SUA_TIMEOUT)
            
            # 1. Ir a la página de login
            print(f"{Fore.BLUE}[1/7] Accediendo al sistema SUA...{Style.RESET_ALL}")
            driver.get(config.SUA_URL_LOGIN)
            time.sleep(config.SUA_DELAY)
            
            # 2. Login
            print(f"{Fore.BLUE}[2/7] Realizando login...{Style.RESET_ALL}")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = driver.find_element(By.NAME, "password")
            
            # Hacer click para activar los campos (quitar readonly)
            username_field.click()
            time.sleep(1)
            username_field.clear()
            username_field.send_keys(usuario)
            
            password_field.click()
            time.sleep(1)
            password_field.clear()
            password_field.send_keys(contraseña)
            
            # Buscar y hacer click en botón de login
            login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")
            login_button.click()
            time.sleep(config.SUA_DELAY * 2)
            
            # Verificar si hay error de autorización después del login
            if self._verificar_error_autorizacion(driver):
                return "reintentar"
            
            # 3. Navegar a Solicitud
            print(f"{Fore.BLUE}[3/7] Navegando a sección Solicitud...{Style.RESET_ALL}")
            try:
                solicitud_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='nivel1' and contains(text(), 'Solicitud')]")))
                print(f"{Fore.GREEN}   ✓ Enlace 'Solicitud' encontrado{Style.RESET_ALL}")
                solicitud_link.click()
                time.sleep(config.SUA_DELAY * 2)  # Más tiempo para cargar
                print(f"{Fore.GREEN}   ✓ Click en 'Solicitud' realizado{Style.RESET_ALL}")
                
                # Verificar si hay error de autorización después de navegar
                if self._verificar_error_autorizacion(driver):
                    return "reintentar"
                    
            except Exception as e:
                print(f"{Fore.RED}   ✗ Error navegando a Solicitud: {e}{Style.RESET_ALL}")
                raise
            
            # 4. Hacer click en "Carga ágil"
            print(f"{Fore.BLUE}[4/7] Navegando a Carga ágil...{Style.RESET_ALL}")
            try:
                carga_agil_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='subnivel1' and contains(text(), 'Carga ágil')]")))
                print(f"{Fore.GREEN}   ✓ Enlace 'Carga ágil' encontrado{Style.RESET_ALL}")
                carga_agil_link.click()
                time.sleep(config.SUA_DELAY * 2)
                print(f"{Fore.GREEN}   ✓ Click en 'Carga ágil' realizado{Style.RESET_ALL}")
                
                # Verificar si hay error de autorización después de navegar a Carga ágil
                if self._verificar_error_autorizacion(driver):
                    return "reintentar"
                    
            except Exception as e:
                print(f"{Fore.RED}   ✗ Error navegando a Carga ágil: {e}{Style.RESET_ALL}")
                raise
            
            # 5. Buscar y seleccionar tipo de solicitud
            print(f"{Fore.BLUE}[5/7] Seleccionando tipo de solicitud...{Style.RESET_ALL}")
            
            try:
                # Encontrar el campo de autocompletar
                subtipos_field = wait.until(EC.element_to_be_clickable((By.ID, "subtipos")))
                print(f"{Fore.GREEN}   ✓ Campo 'subtipos' encontrado{Style.RESET_ALL}")
                
                # Limpiar y escribir "Altura de los ríos"
                subtipos_field.clear()
                subtipos_field.send_keys("Altura de los ríos")
                print(f"{Fore.GREEN}   ✓ Texto 'Altura de los ríos' ingresado{Style.RESET_ALL}")
                time.sleep(config.SUA_DELAY)
                
                # Buscar y hacer click en la opción específica "Suceso [Clima] - Altura de los ríos"
                print(f"{Fore.GREEN}   ✓ Buscando opción 'Suceso [Clima] - Altura de los ríos'...{Style.RESET_ALL}")
                
                # Selector específico para la opción
                option = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ui-corner-all' and contains(text(), 'Suceso [Clima] - Altura de los ríos')]")))
                print(f"{Fore.GREEN}   ✓ Opción 'Suceso [Clima] - Altura de los ríos' encontrada{Style.RESET_ALL}")
                
                option.click()
                print(f"{Fore.GREEN}   ✓ Opción seleccionada - formulario habilitado{Style.RESET_ALL}")
                time.sleep(config.SUA_DELAY * 2)
                
            except Exception as e:
                print(f"{Fore.RED}   ✗ Error seleccionando tipo de solicitud: {e}{Style.RESET_ALL}")
                
                # Debug: mostrar opciones disponibles
                try:
                    print(f"{Fore.YELLOW}   Debug - Opciones disponibles en el autocompletar:{Style.RESET_ALL}")
                    opciones = driver.find_elements(By.XPATH, "//a[contains(@class, 'ui-corner-all')]")
                    for i, opcion in enumerate(opciones[:10]):  # Mostrar las primeras 10
                        texto = opcion.text.strip()
                        if texto:
                            print(f"{Fore.YELLOW}     {i+1}. '{texto}'{Style.RESET_ALL}")
                except:
                    pass
                    
                raise
            
            # Verificar si hay error de autorización después de seleccionar tipo
            if self._verificar_error_autorizacion(driver):
                return "reintentar"
            
            # 6. Llenar los 36 campos de datos
            print(f"{Fore.BLUE}[6/7] Cargando datos de las 36 estaciones...{Style.RESET_ALL}")
            
            # Preparar datos en el orden correcto
            datos_ordenados = []
            for estacion_nombre in config.ESTACIONES_OBJETIVO:
                # Buscar la estación en los datos extraídos
                dato_encontrado = None
                for dato in self.datos_extraidos:
                    if dato['estacion'] == estacion_nombre:
                        dato_encontrado = dato
                        break
                
                if dato_encontrado:
                    altura = dato_encontrado['altura'] if dato_encontrado['altura'] != 'S/E' else 'Sin datos'
                    tendencia = dato_encontrado['tendencia']
                    
                    # Formatear tendencia
                    if tendencia == "ESTAC.":
                        tendencia = "ESTACIONADO"
                    
                    # Formato: solo datos (opción B)
                    texto_campo = f"{altura}m - {tendencia}"
                    datos_ordenados.append(texto_campo)
                else:
                    datos_ordenados.append("Sin datos - S/E")
            
            # Llenar cada campo
            campos_llenos = 0
            for i, texto in enumerate(datos_ordenados):
                try:
                    campo = driver.find_element(By.NAME, f"preguntas[{i}].texto")
                    campo.clear()
                    campo.send_keys(texto)
                    campos_llenos += 1
                    
                    if (i + 1) % 10 == 0:  # Mostrar progreso cada 10 campos
                        print(f"{Fore.GREEN}   ✓ Campos llenados: {i + 1}/36{Style.RESET_ALL}")
                        
                except NoSuchElementException:
                    print(f"{Fore.YELLOW}   ⚠ Campo preguntas[{i}].texto no encontrado{Style.RESET_ALL}")
                    continue
            
            print(f"{Fore.GREEN}✓ Campos llenados exitosamente: {campos_llenos}/36{Style.RESET_ALL}")
            
            # 7. Esperar confirmación del usuario
            print(f"{Fore.BLUE}[7/7] Formulario completado - Esperando confirmación del usuario{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Se han cargado {campos_llenos} campos con datos de las estaciones{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📋 INSTRUCCIONES FINALES:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   1. Revisa que todos los datos sean correctos{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   2. Verifica que las alturas y tendencias estén bien{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   3. Haz click en 'Enviar' o 'Guardar' cuando estés listo{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
            
            # Mantener el navegador abierto para que el usuario confirme
            input(f"{Fore.CYAN}Presiona Enter DESPUÉS de revisar y enviar el formulario manualmente...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Proceso de carga en SUA completado{Style.RESET_ALL}")
            
            driver.quit()
            
            print(f"{Fore.GREEN}✓ Carga en SUA completada exitosamente{Style.RESET_ALL}")
            self.logger.info(f"Datos cargados en SUA: {campos_llenos} campos")
            return True
            
        except TimeoutException as e:
            print(f"{Fore.RED}✗ Timeout en SUA: {e}{Style.RESET_ALL}")
            self.logger.error(f"Timeout SUA: {e}")
            try:
                if driver:
                    driver.quit()
            except:
                pass
            return False
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error en carga SUA: {e}{Style.RESET_ALL}")
            self.logger.error(f"Error SUA: {e}")
            try:
                if driver:
                    driver.quit()
            except:
                pass
            return False
    
    def _verificar_error_autorizacion(self, driver):
        """Verificar si hay un error de 'Acceso no autorizado a esta sección'"""
        try:
            # Buscar el mensaje de error específico
            page_source = driver.page_source
            
            if "Acceso no autorizado a esta sección" in page_source:
                print(f"{Fore.RED}   ✗ Error detectado: Acceso no autorizado a esta sección{Style.RESET_ALL}")
                return True
                
            # También verificar por el elemento HTML específico
            try:
                error_element = driver.find_element(By.XPATH, "//b[contains(text(), 'Acceso no autorizado a esta sección')]")
                if error_element:
                    print(f"{Fore.RED}   ✗ Error detectado: Acceso no autorizado a esta sección{Style.RESET_ALL}")
                    return True
            except NoSuchElementException:
                pass
                
            return False
            
        except Exception as e:
            print(f"{Fore.YELLOW}   ⚠ Error verificando autorización: {e}{Style.RESET_ALL}")
            return False
    
    def ejecutar_scraping(self):
        """Ejecutar el proceso completo de scraping"""
        try:
            print(f"{Fore.MAGENTA}🚀 Iniciando proceso de scraping...{Style.RESET_ALL}\n")
            
            # 1. Obtener datos web
            html_content = self.obtener_datos_web()
            if not html_content:
                return False
            
            # 2. Parsear HTML
            datos_brutos = self.parsear_html(html_content)
            if not datos_brutos:
                print(f"{Fore.RED}✗ No se encontraron datos en la página{Style.RESET_ALL}")
                return False
            
            # 3. Filtrar estaciones objetivo
            datos_filtrados = self.filtrar_estaciones_objetivo(datos_brutos)
            if not datos_filtrados:
                print(f"{Fore.RED}✗ No se encontraron estaciones objetivo{Style.RESET_ALL}")
                return False
            
            # 4. Guardar datos
            if not self.guardar_datos():
                return False
            
            # 5. Detectar alertas
            alertas = self.detectar_alertas()
            
            if alertas:
                print(f"\n{Fore.RED}🚨 ALERTAS DETECTADAS: {len(alertas)}{Style.RESET_ALL}")
                for alerta in alertas:
                    print(f"   {Fore.RED}{alerta['tipo']}: {alerta['estacion']} - {alerta['altura']}m{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}✓ No se detectaron alertas críticas{Style.RESET_ALL}")
            
            # 6. Generar y enviar mensaje de WhatsApp (siempre)
            mensaje_whatsapp = self.generar_mensaje_whatsapp()
            if mensaje_whatsapp:
                print(f"\n{Fore.BLUE}📱 Mensaje de WhatsApp generado:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'-'*40}")
                print(mensaje_whatsapp)
                print(f"{'-'*40}{Style.RESET_ALL}")
                self.enviar_whatsapp(mensaje_whatsapp)
            else:
                print(f"\n{Fore.YELLOW}⚠ No se pudieron obtener datos para WhatsApp{Style.RESET_ALL}")
            
            # 7. Cargar datos en SUA Rosario (si está habilitado)
            sua_success = self.cargar_datos_sua()
            
            # Resumen final
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}📊 RESUMEN FINAL:")
            print(f"{Fore.GREEN}   • Estaciones procesadas: {len(datos_filtrados)}")
            print(f"{Fore.GREEN}   • Alertas detectadas: {len(alertas)}")
            print(f"{Fore.GREEN}   • WhatsApp enviado: {'Sí' if mensaje_whatsapp else 'No'}")
            print(f"{Fore.GREEN}   • SUA cargado: {'Sí' if sua_success else 'No'}")
            print(f"{Fore.GREEN}   • Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            self.logger.info(f"Scraping completado exitosamente: {len(datos_filtrados)} estaciones, {len(alertas)} alertas")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error fatal en scraping: {e}{Style.RESET_ALL}")
            self.logger.error(f"Error fatal: {e}")
            return False

def main():
    """Función principal"""
    try:
        scraper = ScraperPNA()
        success = scraper.ejecutar_scraping()
        
        if success:
            print(f"\n{Fore.GREEN}🎉 Proceso completado exitosamente{Style.RESET_ALL}")
            return 0
        else:
            print(f"\n{Fore.RED}❌ Proceso terminado con errores{Style.RESET_ALL}")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠ Proceso interrumpido por el usuario{Style.RESET_ALL}")
        return 2
    except Exception as e:
        print(f"\n{Fore.RED}💥 Error fatal: {e}{Style.RESET_ALL}")
        return 3

if __name__ == "__main__":
    exit(main())
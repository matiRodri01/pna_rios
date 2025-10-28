# CONFIGURACIÓN DEL SCRAPER PNA RÍOS
# ====================================
#
# Este archivo contiene todas las configuraciones del sistema
# de monitoreo de alturas de ríos de la Prefectura Naval Argentina

# === CONFIGURACIÓN DE LA PÁGINA WEB ===
URL_PNA = "https://contenidosweb.prefecturanaval.gob.ar/alturas/index.php"
TIMEOUT_REQUEST = 30  # segundos

# === CONFIGURACIÓN DE WHATSAPP ===
NUMERO_WHATSAPP = "+5493415704962"  # Formato correcto con código de país
DELAY_WHATSAPP = 15  # segundos entre mensajes

# === ESTACIONES ESPECÍFICAS PARA WHATSAPP ===
ESTACIONES_WHATSAPP = ["ANDRESITO", "IGUAZU", "ROSARIO"]

# === ESTACIONES A MONITOREAR (36 estaciones específicas) ===
ESTACIONES_OBJETIVO = [
    "ANDRESITO",
    "IGUAZU", 
    "LIBERTAD",
    "ELDORADO",
    "LIBERTADOR",
    "POSADAS",
    "ITUZAINGO",
    "ITA IBATE",
    "ITATI",
    "PASO DE LA PATRIA",
    "PILCOMAYO",
    "BOUVIER",
    "FORMOSA",
    "BERMEJO",
    "ISLA DEL CERRITO",
    "CORRIENTES",
    "BARRANQUERAS",
    "EMPEDRADO",
    "BELLA VISTA",
    "GOYA",
    "RECONQUISTA",
    "ESQUINA",
    "LA PAZ",
    "SANTA ELENA",
    "HERNANDARIAS",
    "PARANA",
    "SANTA FE",
    "DIAMANTE",
    "VICTORIA",
    "SAN LORENZO",
    "ROSARIO",
    "VILLA CONSTITUCION",
    "SAN NICOLAS",
    "RAMALLO",
    "SAN PEDRO",
    "BARADERO"
]

# === CONFIGURACIÓN DE ARCHIVOS ===
ARCHIVO_DATOS_EXCEL = "datos/alturas_rios_{}.xlsx"  # {} se reemplaza por fecha
ARCHIVO_DATOS_CSV = "datos/alturas_rios_{}.csv"
ARCHIVO_LOG = "logs/scraper_{}.log"
CARPETA_DATOS = "datos"
CARPETA_LOGS = "logs"

# === CONFIGURACIÓN DE ALERTAS ===
# Niveles que requieren alerta (en metros)
NIVEL_ALERTA_DEFECTO = 5.0  # Si no se especifica otro
NIVEL_EVACUACION_DEFECTO = 7.0

# Estaciones con niveles específicos de alerta
NIVELES_CRITICOS = {
    "ROSARIO": {"alerta": 4.5, "evacuacion": 6.0},
    "SANTA FE": {"alerta": 4.0, "evacuacion": 5.5},
    "PARANA": {"alerta": 5.5, "evacuacion": 7.0},
    "CORRIENTES": {"alerta": 6.0, "evacuacion": 8.0},
    "POSADAS": {"alerta": 8.0, "evacuacion": 10.0},
    "IGUAZU": {"alerta": 12.0, "evacuacion": 15.0}
}

# === CONFIGURACIÓN DE HORARIOS ===
# Horarios para ejecutar scraping automático
HORARIOS_SCRAPING = ["06:00", "12:00", "18:00", "00:00"]

# === CONFIGURACIÓN DE MENSAJES ===
MENSAJE_TITULO = "🌊 ALERTA HIDROLÓGICA - PNA"
MENSAJE_PIE = "\n📍 Fuente: Prefectura Naval Argentina\n⏰ Actualizado: {timestamp}"

# === CONFIGURACIÓN TÉCNICA ===
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REINTENTOS_MAX = 3
DELAY_ENTRE_REINTENTOS = 5  # segundos

# === CONFIGURACIÓN DE DEBUG ===
DEBUG_MODE = True  # Cambiar a False en producción
MOSTRAR_TODOS_LOS_DATOS = False  # True para mostrar todas las estaciones encontradas

# === CONFIGURACIÓN SISTEMA SUA ROSARIO ===
SUA_ENABLED = True  # Activar/desactivar carga automática en SUA
SUA_URL_LOGIN = "https://sua.rosario.gob.ar/sua-webapp/index.jsp"
SUA_USERNAME = ""  # Se pedirá al usuario cuando sea necesario
SUA_PASSWORD = ""  # Se pedirá al usuario cuando sea necesario
SUA_TIPO_SOLICITUD = "Suceso [Clima] - Altura de los ríos"
SUA_TIMEOUT = 30  # segundos para cargar páginas
SUA_DELAY = 2  # segundos entre acciones
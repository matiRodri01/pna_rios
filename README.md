# 🌊 SCRAPER PNA RÍOS - Sistema de Monitoreo Hidrológico

Sistema automatizado para monitoreo de alturas de ríos de la Prefectura Naval Argentina con integración a WhatsApp y Sistema SUA de Rosario.

## 🚀 Características

- ✅ **Monitoreo de 36 estaciones** específicas de ríos
- ✅ **WhatsApp automático** con datos de 3 estaciones principales (ANDRESITO, IGUAZÚ, ROSARIO)
- ✅ **Emojis de tendencia** (CRECE ⬆️, BAJA ⬇️, ESTACIONADO ➡️)
- ✅ **Sistema de alertas** por niveles de evacuación
- ✅ **Carga automática en SUA** (Sistema Único de Atención de Rosario)
- ✅ **Exportación a Excel y CSV** con histórico
- ✅ **Sistema de reintentos** y manejo de errores robusto

## 📋 Requisitos

- Python 3.8+
- Google Chrome instalado
- Conexión a internet
- Credenciales del Sistema SUA

## 🛠️ Instalación

### 🚀 Instalación Automática (Recomendada)

**Para Windows:**
1. **Ejecutar instalador:** Doble click en `Instalar_PNA_Rios.bat`
2. **Seguir instrucciones** en pantalla
3. **¡Listo!** El sistema se instala automáticamente

### 🔧 Instalación Manual

1. **Clonar o descargar** este proyecto
2. **Crear entorno virtual:**
   ```bash
   python -m venv venv_pna_rios
   ```
3. **Activar entorno virtual:**
   ```bash
   # Windows
   venv_pna_rios\Scripts\activate
   
   # Linux/Mac  
   source venv_pna_rios/bin/activate
   ```
4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

### 🔐 Configuración Segura

**Credenciales SUA:** Se solicitan automáticamente cuando ejecutas el programa (no se guardan en archivos)

**Configuraciones opcionales** en `config.py`:
```python
# Configurar WhatsApp
NUMERO_WHATSAPP = "+5493415704962"  # Tu número de WhatsApp
ESTACIONES_WHATSAPP = ["ANDRESITO", "IGUAZU", "ROSARIO"]

# Configurar SUA
SUA_ENABLED = True  # True para habilitar carga automática
# Las credenciales se pedirán de forma segura al ejecutar
```

## 🚀 Uso

### 🎯 Ejecución Automática (Recomendada)
**Para Windows:**
```batch
# Doble click en:
Ejecutar_Scraper.bat
```

### 🔧 Ejecución Manual
```bash
python scraper.py
```

### Funcionalidades incluidas:
1. **Scraping automático** de datos PNA
2. **Filtrado** de 36 estaciones específicas  
3. **Envío de WhatsApp** con datos de 3 estaciones
4. **Carga automática en SUA** (si está habilitado)
5. **Generación de archivos** Excel/CSV con timestamp

## 📊 Estaciones Monitoreadas (36)

Las 36 estaciones están configuradas en `config.ESTACIONES_OBJETIVO`:

1. ANDRESITO → Campo SUA: preguntas[0].texto
2. IGUAZU → Campo SUA: preguntas[1].texto  
3. LIBERTAD → Campo SUA: preguntas[2].texto
4. ELDORADO → Campo SUA: preguntas[3].texto
5. LIBERTADOR → Campo SUA: preguntas[4].texto
6. POSADAS → Campo SUA: preguntas[5].texto
...
36. BARADERO → Campo SUA: preguntas[35].texto

## 📱 Mensaje WhatsApp

Formato automático:
```
Buenos días
Altura de los ríos
27/10/25

Andresito:   1.5 - CRECE ⬆️
Iguazú:   8.8 - BAJA ⬇️
Rosario:   2.32 - CRECE ⬆️

Información brindada por la pagina web de Prefectura Naval Argentina.
```

## 🚨 Sistema de Alertas

- **Alerta**: Nivel por encima del umbral configurado
- **Evacuación**: Nivel crítico que requiere acción inmediata

Niveles configurables en `config.NIVELES_CRITICOS` por estación.

## 🌐 Integración SUA

El sistema puede cargar automáticamente los 36 datos en el Sistema Único de Atención de Rosario:

1. **Login automático** con credenciales
2. **Navegación**: Solicitud → Carga ágil
3. **Selección**: "Suceso [Clima] - Altura de los ríos"
4. **Carga de datos** en 36 campos numerados
5. **Confirmación manual** antes del envío

## 📁 Estructura del Proyecto

```
📦 PNA Rios/
├── 📄 config.py          # Configuración principal
├── 📄 scraper.py         # Script principal
├── 📄 requirements.txt   # Dependencias Python
├── 📁 datos/            # Archivos Excel/CSV generados
├── 📁 logs/             # Archivos de log
└── 📁 venv_pna_rios/    # Entorno virtual Python
```

## 🔧 Mantenimiento

### Archivos generados automáticamente:
- `datos/alturas_rios_YYYYMMDD_HHMMSS.xlsx`
- `datos/alturas_rios_YYYYMMDD_HHMMSS.csv`
- `logs/scraper_YYYYMMDD_HHMMSS.log`

### Para automatizar ejecución diaria:
Usar Task Scheduler (Windows) o cron (Linux) para ejecutar el script automáticamente.

## 📞 Soporte

- **Fuente de datos**: https://contenidosweb.prefecturanaval.gob.ar/alturas/index.php
- **Sistema SUA**: https://sua.rosario.gob.ar/sua-webapp/index.jsp

## 📄 Licencia

Proyecto desarrollado para Protección Civil - Monitoreo de Ríos

---
**Desarrollado en 2025 - Sistema de Monitoreo Hidrológico Automatizado** 🌊
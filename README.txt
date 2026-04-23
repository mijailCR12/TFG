==================================================
      PROYECTO SQL-TALK - GUÍA DE EJECUCIÓN
==================================================

Este proyecto permite interactuar con una base de datos SQL Server 
mediante lenguaje natural a través de un bot de Telegram.

1. REQUISITOS PREVIOS:
   - Python 3.10 o superior instalado.
   - SQL Server con la base de datos 'neptuno' configurada.
   - Un archivo .env con las llaves de OpenAI y Telegram.

2. INSTALACIÓN DE DEPENDENCIAS:
   Ejecutar el siguiente comando en la terminal:
   pip install -r requirements.txt

3. CONFIGURACIÓN DEL ENTORNO:
   Asegúrese de que el archivo .env contenga:
   OPENAI_API_KEY=tu_llave_aqui
   TELEGRAM_TOKEN=tu_token_aqui

4. NOTA PARA EL EVALUADOR:
   El archivo 'conexion.py' contiene los detalles de la cadena de 
   conexión al servidor local de base de datos.

==================================================
      PASOS PARA EJECUTAR SQL-TALK (TFG)
==================================================

1. LEVANTAR LA IA LOCAL (Ollama):
   - Abrir una terminal y ejecutar: ollama run llama3.2
   - Mantener esta ventana abierta o minimizada.

2. ACTIVAR ENTORNO DE PYTHON:
   - En la carpeta del proyecto, ejecutar: .\venv\Scripts\activate

3. VERIFICAR VARIABLES DE ENTORNO:
   - Asegurarse de que el archivo .env tenga el TELEGRAM_TOKEN correcto.

4. INICIAR EL BOT:
   - Ejecutar: python bot_sql.py

5. PRUEBA DE CONEXIÓN:
   - Enviar un mensaje al bot en Telegram: "¿Cuáles son los productos más caros?"
==================================================
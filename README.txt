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

4. EJECUCIÓN DEL PROYECTO:
   Para iniciar el asistente, ejecute:
   python bot_sql.py

5. NOTA PARA EL EVALUADOR:
   El archivo 'conexion.py' contiene los detalles de la cadena de 
   conexión al servidor local de base de datos.
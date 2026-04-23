import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from conexion import obtener_conexion

# --- CONFIGURACIÓN ---


# Función auxiliar para ejecutar SQL y devolver texto
def ejecutar_consulta_sql(query):
    conn = obtener_conexion()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            conn.close()
            if df.empty:
                return "No encontré datos con esa descripción."
            
            # Formateamos la respuesta (puedes ajustar las columnas de Neptuno)
            respuesta = "📊 **Resultados de Neptuno:**\n\n"
            for _, fila in df.iterrows():
                respuesta += f"🔹 *{fila['nombreProducto']}* | Precio: ${fila['precioUnidad']} | Stock: {fila['unidadesEnExistencia']}\n"
            return respuesta
        except Exception as e:
            return f"❌ Error en el query: {e}"
    return "❌ Error de conexión al servidor TFG."

# --- MANEJADORES DEL BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"¡Hola {user}! Soy el asistente de la base de datos Neptuno.\n\n"
        "Puedes usar /productos o simplemente preguntarme: '¿Qué productos hay?'"
    )

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text.lower()
    
    # Lógica inicial de "Lenguaje Natural" (Traducción manual)
    if "productos" in texto_usuario or "inventario" in texto_usuario:
        await update.message.reply_text("🔎 Buscando en la base de datos...")
        sql = "SELECT TOP 10 nombreProducto, precioUnidad, unidadesEnExistencia FROM [neptuno].[dbo].[productos]"
        respuesta = ejecutar_consulta_sql(sql)
        await update.message.reply_text(respuesta, parse_mode='Markdown')
        
    elif "caro" in texto_usuario or "costoso" in texto_usuario:
        await update.message.reply_text("💰 Buscando los productos más caros...")
        sql = "SELECT TOP 5 nombreProducto, precioUnidad, unidadesEnExistencia FROM [neptuno].[dbo].[productos] ORDER BY precioUnidad DESC"
        respuesta = ejecutar_consulta_sql(sql)
        await update.message.reply_text(respuesta, parse_mode='Markdown')
        
    else:
        await update.message.reply_text(
            "Todavía estoy aprendiendo. Prueba con:\n"
            "- 'Ver productos'\n"
            "- '¿Qué es lo más caro?'"
        )

# --- INICIO DEL PROGRAMA ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("productos", manejar_mensajes)) # También acepta el comando
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensajes))
    
    print("🤖 SQL-Talk en línea y listo para recibir mensajes...")
    app.run_polling()
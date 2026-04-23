import os  # <--- Agregamos esto
import ollama
import pandas as pd
import re
from dotenv import load_dotenv  # <--- Agregamos esto
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from conexion import obtener_conexion
from esquemas import ESQUEMA_BD

# --- CONFIGURACIÓN ---
Tload_dotenv()  # Esto lee tu archivo .env automáticamente
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN") # <--- Jalamos el token desde el archivo oculto
MODELO_IA = "llama3.2"

def limpiar_sql(texto):
    """Limpia la respuesta de la IA para obtener solo el SELECT puro"""
    if not texto: return None
    texto = re.sub(r'```sql|```', '', texto, flags=re.IGNORECASE).strip()
    match = re.search(r'(SELECT.*)', texto, re.IGNORECASE | re.DOTALL)
    return match.group(1).split(';')[0] if match else texto

def consultar_ia(prompt_usuario, es_correccion=False):
    """Función central para hablar con Ollama"""
    if es_correccion:
        # Prompt específico para cuando hubo un error previo
        system_msg = "Eres un DBA experto. Corrige el error de sintaxis SQL Server y responde SOLO con el código SQL corregido."
    else:
        # Prompt normal de operación
        system_msg = f"Eres un experto DBA de SQL Server. Usa este esquema:\n{ESQUEMA_BD}"

    try:
        response = ollama.chat(model=MODELO_IA, messages=[
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': prompt_usuario}
        ], options={'temperature': 0})
        return response['message']['content'].strip()
    except Exception as e:
        print(f"❌ Error Ollama: {e}")
        return None

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    status = await update.message.reply_text("🧠 Analizando solicitud...")

    # 1. Intento inicial de traducción
    respuesta_ia = consultar_ia(user_text)
    
    # Si la respuesta parece SQL, intentamos ejecutarla
    if "SELECT" in respuesta_ia.upper():
        sql_actual = limpiar_sql(respuesta_ia)
        intentos = 0
        max_intentos = 2 

        while intentos < max_intentos:
            intentos += 1
            print(f"🚀 [Intento {intentos}] Ejecutando: {sql_actual}")
            
            conn = obtener_conexion()
            if conn:
                try:
                    # Ejecución en SQL Server
                    df = pd.read_sql(sql_actual, conn)
                    conn.close()
                    
                    # SI FUNCIONA: Enviamos resultados
                    if df.empty:
                        await status.edit_text("No se encontraron registros.")
                    else:
                        res_txt = "📊 **Resultado Exitoso:**\n\n"
                        for _, fila in df.head(5).iterrows():
                            datos = " | ".join([f"*{k}*: {v}" for k, v in fila.items()])
                            res_txt += f"• {datos}\n\n"
                        await status.edit_text(res_txt, parse_mode='Markdown')
                    break # Salimos del bucle porque funcionó

                except Exception as e:
                    error_tecnico = str(e)
                    print(f"⚠️ Error en ejecución: {error_tecnico}")
                    
                    if intentos < max_intentos:
                        await status.edit_text("🔧 Detecté un error, intentando corregirlo automáticamente...")
                        # 2. SEGUNDO INTENTO: Pedimos a la IA que corrija basado en el error
                        prompt_correccion = f"El query: {sql_actual}\nFalló con el error: {error_tecnico}\nGenera el SQL corregido para SQL Server."
                        nueva_respuesta = consultar_ia(prompt_correccion, es_correccion=True)
                        sql_actual = limpiar_sql(nueva_respuesta)
                    else:
                        # Si falló los 2 intentos, ocultamos el error técnico feo
                        await status.edit_text("No pude procesar la consulta correctamente. Por favor, intenta ser más específico con los nombres de productos o categorías.")
            else:
                await status.edit_text("❌ Error de conexión a la BD.")
                break
    else:
        # Si la IA respondió un saludo o charla normal
        await status.edit_text(respuesta_ia)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    print(f"✅ SQL-Talk con Autocorrección iniciado (Modelo: {MODELO_IA})")
    app.run_polling(drop_pending_updates=True)
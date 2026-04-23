import pyodbc

def obtener_conexion():
    try:
        # Configuración de tu SQL Server local
        # SERVER: '.' o 'localhost' o 'TU_PC\SQLEXPRESS'
        # DATABASE: Poné el nombre de la BD de la tienda que vas a crear
        server = r'localhost\TFG' 
        database = 'neptuno' 
        
        # El Driver 17 es el estándar, si tenés el 18 cambialo abajo
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;' # Usa tu usuario de Windows
        )
        
        conexion = pyodbc.connect(conn_str)
        print("✅ Conexión exitosa a SQL Server")
        return conexion

    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None

# Prueba rápida al ejecutar el archivo
if __name__ == "__main__":
    con = obtener_conexion()
    if con:
        con.close()
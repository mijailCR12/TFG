import pandas as pd
from conexion import obtener_conexion # Reutilizamos tu función exitosa

def mostrar_productos():
    conn = obtener_conexion()
    if conn:
        try:
            # Tu consulta SQL de Neptuno
            query = """
            SELECT TOP (10) 
                nombreProducto, 
                precioUnidad, 
                unidadesEnExistencia, 
                categoriaProducto
            FROM [neptuno].[dbo].[productos]
            """
            
            # Usamos Pandas para leer el SQL y formatearlo
            df = pd.read_sql(query, conn)
            
            print("\n--- INVENTARIO DE NEPTUNO (Top 10) ---")
            print(df.to_string(index=False)) # Imprime la tabla sin el índice de fila
            
            conn.close()
        except Exception as e:
            print(f"❌ Error al consultar: {e}")

if __name__ == "__main__":
    mostrar_productos()
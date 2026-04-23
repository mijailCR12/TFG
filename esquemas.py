# Archivo de Metadatos para SQL-Talk
ESQUEMA_BD = """
DICCIONARIO DE DATOS - BASE DE DATOS NEPTUNO (T-SQL)

TABLAS DISPONIBLES:
- [dbo].[productos]: idproducto, nombreProducto, precioUnidad, unidadesEnExistencia, categoriaProducto.
- [dbo].[clientes]: idCliente, NombreCompañia, Ciudad, Pais.
- [dbo].[Empleados]: IdEmpleado, Nombre, Apellidos, cargo, sueldoBasico.
- [dbo].[Pedidos]: IdPedido, IdCliente, IdEmpleado, FechaPedido, PaisDestinatario.
- [dbo].[detallesdepedidos]: idpedido, idproducto, preciounidad, cantidad, descuento.
- [dbo].[categorias]: idcategoria, nombrecategoria.
- [dbo].[proveedores]: idProveedor, nombreCompañia, Pais.
- [dbo].[compañiasdeenvios]: idCompañiaEnvios, nombreCompañia, telefono.

REGLAS CRÍTICAS:
1. Motor: Microsoft SQL Server.
2. NUNCA usar 'LIMIT'. Usar siempre 'SELECT TOP X'.
3. Para cálculos de ventas: (cantidad * preciounidad) * (1 - descuento).
"""
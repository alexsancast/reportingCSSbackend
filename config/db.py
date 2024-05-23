import pyodbc

# Establecer la conexión
conn = pyodbc.connect('DSN=PixelSqlbase;UID=reportuser;PWD=Pixel1047')

# Crear un cursor
cursor = conn.cursor()



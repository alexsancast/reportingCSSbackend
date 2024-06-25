import pyodbc

class Connection():
    def get_conection():
        try:
            conn = pyodbc.connect('DSN=PixelSqlbase;UID=reportuser;PWD=Pixel1047')   
            return conn.cursor()
        except pyodbc.Error as e:
            error_message = f" Database conn failed:{e}"
            return {"Detail":error_message}






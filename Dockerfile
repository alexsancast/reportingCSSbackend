# Usa una imagen base de Windows con Python
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Instala Python
RUN powershell -Command \
    curl -L -o python-installer.exe https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe; \
    Start-Process python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait; \
    Remove-Item -Force python-installer.exe

# Crea el directorio para los controladores ODBC
RUN mkdir C:\odbc

# Copia el controlador ODBC de SQLBase
COPY drivers/dbodbc10.dll C:\odbc\dbodbc10.dll

# Configura ODBC
COPY odbc.ini C:\Windows\System32\odbc.ini
COPY odbcinst.ini C:\Windows\System32\odbcinst.ini

# Instala las dependencias usando pip
RUN pip install fastapi uvicorn pyodbc fpdf

# Copia el código de la aplicación al contenedor
COPY . C:\app

# Establece el directorio de trabajo
WORKDIR C:\app

# Exponer el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

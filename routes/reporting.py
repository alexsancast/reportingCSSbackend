from fastapi import APIRouter , HTTPException
from datetime import datetime
from config.db import  Connection
from config.reportpdf import Reportx


report_detail= APIRouter()#Instanciamos el modulo de las rutas
cursor = Connection.get_conection() #Instanciamos el la conexion a la db
create_report=Reportx() #Instanciamos el modulo de reporteria para generar los reportes

 #Reporte General por compañia
@report_detail.get("/detail_company/{company_name}/{start_date}/{end_date}")
def report_general_company(company_name: str, start_date: datetime, end_date: datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    
    consulta = f"""
    SELECT  
        PRODUCT.DESCRIPT AS Tipo_Servicio, 
        SUM(POSDETAIL.QUAN) AS Cantidad_Servicio,
        SUM(POSHEADER.NETTOTAL) AS Total_Precio
    FROM  
        DBA."Member" 
    INNER JOIN 
        DBA."MemberGroups" ON MEMBER.GROUPNUM = MemberGroups.GROUPNUM  
    INNER JOIN 
        DBA."POSHEADER" ON MEMBER.MEMCODE = POSHEADER.MEMCODE 
    INNER JOIN 
        DBA."POSDETAIL" ON POSHEADER.TRANSACT = POSDETAIL.TRANSACT 
    INNER JOIN 
        DBA."PRODUCT" ON POSDETAIL.PRODNUM = PRODUCT.PRODNUM
    WHERE 
        MemberGroups.GROUPNAME = '{company_name}' 
        AND POSHEADER.OPENDATE BETWEEN datetime('{start_date_format}') AND datetime('{end_date_format}')
    GROUP BY 
        PRODUCT.DESCRIPT
        ORDER BY 
    CASE 
        WHEN PRODUCT.DESCRIPT = 'CRED Desayuno' THEN 1
        WHEN PRODUCT.DESCRIPT = 'CRED Almuerzo' THEN 2
        WHEN PRODUCT.DESCRIPT = 'CRED Cena' THEN 3
        ELSE 4
    END
    """
    
    cursor.execute(consulta)
    results = cursor.fetchall()

    # Formatear los resultados con comas
    formatted_results = []
    for row in results:
        row = list(row)  # Convertir el resultado a una lista mutable
        row[1] = "{:,.0f}".format(row[1])  # Formatear la cantidad con comas y sin decimales
        row[2] = "{:,.0f}".format(row[2])  # Formatear el total con comas y sin decimales
        formatted_results.append(row)

    # Aquí llamamos la función para generar los reportes
    return create_report.reportcompany(
        company_name, 
        start_date_format, 
        end_date_format, 
        formatted_results,  # Usar los resultados formateados
        ["Servicio", "Cantidad", "Total"], 
        [35, 25, 35], 
        "Reporte general por Compañia"
    )

#Reporte General
@report_detail.get("/general_company/{start_date}/{end_date}")
def report_general(start_date: datetime, end_date: datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    
    query = f"""
    SELECT  
        MemberGroups.GROUPNAME AS Nombre_Compania,
        PRODUCT.DESCRIPT AS Tipo_Servicio, 
        SUM(POSDETAIL.QUAN) AS Cantidad_Servicio,
        SUM(POSHEADER.NETTOTAL) AS Total_Precio
    FROM  
        DBA."Member" 
    INNER JOIN 
        DBA."MemberGroups" ON MEMBER.GROUPNUM = MemberGroups.GROUPNUM  
    INNER JOIN 
        DBA."POSHEADER" ON MEMBER.MEMCODE = POSHEADER.MEMCODE 
    INNER JOIN 
        DBA."POSDETAIL" ON POSHEADER.TRANSACT = POSDETAIL.TRANSACT 
    INNER JOIN 
        DBA."PRODUCT" ON POSDETAIL.PRODNUM = PRODUCT.PRODNUM
    WHERE 
        POSHEADER.OPENDATE BETWEEN datetime('{start_date_format}') AND datetime('{end_date_format}')
    GROUP BY 
        PRODUCT.DESCRIPT
   ORDER BY 
    CASE 
        WHEN PRODUCT.DESCRIPT = 'CRED Desayuno' THEN 1
        WHEN PRODUCT.DESCRIPT = 'CRED Almuerzo' THEN 2
        WHEN PRODUCT.DESCRIPT = 'CRED Cena' THEN 3
        ELSE 4
    END;
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()

        # Formatear los resultados con comas
        formatted_results = []
        for row in results:
            row = list(row)  # Convertir el resultado a una lista mutable
            row[2] = "{:,.0f}".format(row[2])  # Formatear la cantidad con comas y sin decimales
            row[3] = "{:,.0f}".format(row[3])  # Formatear el total con comas y sin decimales
            formatted_results.append(row)

        if not formatted_results:
            print("Test")
            raise HTTPException(status_code=404, detail="No se encontraron datos registrados para esta fecha")

        # Usar los resultados formateados para generar el reporte
        return create_report.reportcompany(
            "company_name", 
            start_date_format, 
            end_date_format, 
            formatted_results,  # Usar los resultados formateados
            ["Compañia", "Servicio", "Cantidad", "Total"], 
            [60, 55, 50, 30, 30], 
            "Reporte General"
        )
    except:
        return cursor


#Reporte detallaldo por compañia 
@report_detail.get("/individual_company/{company_name}/{start_date}/{end_date}")
def report_detail_company(company_name:str , start_date:datetime, end_date:datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    query = f"""SELECT 
    MEMBER.FIRSTNAME AS Nombre , 
    MEMBER.LASTNAME AS Apellido , 
    CONVERT(VARCHAR, POSDETAIL.TIMEORD, 20) AS FECHA_HORA,
    PRODUCT.DESCRIPT AS Producto , 
    POSDETAIL.QUAN AS Cantidad ,
    ROUND(POSDETAIL.COSTEACH, 0) AS Precio FROM DBA."Member"
    INNER JOIN DBA."MemberGroups" ON MEMBER.GROUPNUM = MemberGroups.GROUPNUM  INNER JOIN DBA."POSHEADER" ON MEMBER.MEMCODE = POSHEADER.MEMCODE INNER JOIN DBA."POSDETAIL" ON POSHEADER.TRANSACT = POSDETAIL.TRANSACT INNER JOIN DBA."PRODUCT" ON POSDETAIL.PRODNUM = PRODUCT.PRODNUM
    WHERE MemberGroups.GROUPNAME = '{company_name}' and POSHEADER.OPENDATE BETWEEN  datetime ('{start_date_format}') and datetime ('{end_date_format}') ORDER BY PRODUCT.DESCRIPT;"""
    cursor.execute(query)
    results = [list(row) for row in cursor.fetchall()]

    #Funcion para generar los reportes
    return create_report.reportcompany(company_name,start_date_format ,end_date_format,results,["Nombre","Apellido" ,"Fecha_Hora", "Producto", "Cantidad", "Precio"],[40,40,40,40,20,30],"Reporte detallado por compañia")

#Reporte de venta individual por persona
@report_detail.get("/person/{ced}/{start_date}/{end_date}")
def report_person(ced:str, start_date:datetime, end_date:datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    query = f"""SELECT MEMBER.FIRSTNAME AS Nombre , 
                MEMBER.LASTNAME AS Apellido , 
                CONVERT(VARCHAR, POSDETAIL.TIMEORD, 20) AS FECHA_HORA,
                PRODUCT.DESCRIPT AS Producto , 
                POSDETAIL.QUAN AS Cantidad,
                ROUND(POSDETAIL.COSTEACH, 0) AS Precio FROM DBA."Member"
                INNER JOIN DBA."MemberGroups" ON MEMBER.GROUPNUM = MemberGroups.GROUPNUM  INNER JOIN DBA."POSHEADER" ON MEMBER.MEMCODE = POSHEADER.MEMCODE INNER JOIN DBA."POSDETAIL" ON POSHEADER.TRANSACT = POSDETAIL.TRANSACT INNER JOIN DBA."PRODUCT" ON POSDETAIL.PRODNUM = PRODUCT.PRODNUM
                WHERE MEMBER.CARDNUM = '{ced}' and POSHEADER.OPENDATE BETWEEN  datetime ('{start_date}') and datetime ('{end_date_format}');"""
    cursor.execute(query)
    results = [list(row) for row in cursor.fetchall()]

    #FUncion para generar los reportes
    return create_report.reportcompany(ced,start_date_format ,end_date_format,results,["Nombre", "Apellido","Fecha y hora", "Producto", "Cantidad", "Precio"],[50,35,35, 30 , 20, 25],"Reporte detallado por persona")
#Companias
@report_detail.get("/companies/")
def companies():
    query = f"""select groupname from dba."MemberGroups" where isactive = '1';"""
    cursor.execute(query)
    results = [list(row) for row in cursor.fetchall()]
    return results
    
    


    
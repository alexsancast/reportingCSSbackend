from fastapi import APIRouter
from datetime import datetime
from config.db import  cursor
from config.reportpdf import Reportx


report_detail= APIRouter()

#Instanciamos el modulo de reporteria para generar los reportes
create_report=Reportx() 

 #Reporte General por compañia
@report_detail.get("/detail_company/{company_name}/{start_date}/{end_date}")
def report_general_company(company_name:str,start_date :datetime, end_date:datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    consulta = f"""SELECT  PRODUCT.DESCRIPT AS Tipo_Servicio, 
                    SUM(POSDETAIL.QUAN) AS Cantidad_Servicio,
                    SUM(POSHEADER.NETTOTAL) AS Total_Precio
                    FROM  DBA."Member" INNER JOIN 
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
                    PRODUCT.DESCRIPT;"""
    cursor.execute(consulta)
    results = [list(row) for row in cursor.fetchall()]

    #Aqui llamamos la funcion para generar los reportes
    return create_report.reportcompany(company_name,start_date_format ,end_date_format,results,["Servicio", "Cantidad", "Total"],[35, 25, 35],"Reporte general por Compañia")
#Reporte General
@report_detail.get("/general_company/{start_date}/{end_date}")
def report_general(start_date:datetime,end_date:datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    query = f""" SELECT  
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
    MemberGroups.GROUPNAME, PRODUCT.DESCRIPT
ORDER BY 
    MemberGroups.GROUPNAME;"""
    cursor.execute(query)
    results = [list(row) for row in cursor.fetchall()]

    #Funcion para generar los reportes
    return create_report.reportcompany("company_name",start_date_format ,end_date_format,results,["Compañia", "Servicio","Cantidad", "Total"],[60, 55, 50, 30, 30],"Reporte General")

#Reporte detallaldo por compañia 
@report_detail.get("/individual_company/{company_name}/{start_date}/{end_date}")
def report_detail_company(company_name:str , start_date:datetime, end_date:datetime):
    start_date_format = start_date.strftime('%b-%d-%Y')
    end_date_format = end_date.strftime('%b-%d-%Y')
    query = f"""SELECT 
    POSHEADER.TRANSACT AS Transact , 
    CONVERT(VARCHAR, POSDETAIL.TIMEORD, 20) AS FECHA_HORA,
    PRODUCT.DESCRIPT AS Producto , 
    POSDETAIL.QUAN AS Cantidad ,
    ROUND(POSDETAIL.COSTEACH, 0) AS Precio FROM DBA."Member"
    INNER JOIN DBA."MemberGroups" ON MEMBER.GROUPNUM = MemberGroups.GROUPNUM  INNER JOIN DBA."POSHEADER" ON MEMBER.MEMCODE = POSHEADER.MEMCODE INNER JOIN DBA."POSDETAIL" ON POSHEADER.TRANSACT = POSDETAIL.TRANSACT INNER JOIN DBA."PRODUCT" ON POSDETAIL.PRODNUM = PRODUCT.PRODNUM
    WHERE MemberGroups.GROUPNAME = '{company_name}' and POSHEADER.OPENDATE BETWEEN  datetime ('{start_date_format}') and datetime ('{end_date_format}') ORDER BY PRODUCT.DESCRIPT;"""
    cursor.execute(query)
    results = [list(row) for row in cursor.fetchall()]

    #Funcion para generar los reportes
    return create_report.reportcompany(company_name,start_date_format ,end_date_format,results,["Transact", "Fecha y Hora", "Producto", "Cantidad", "Precio"],[30, 50, 50, 30, 30],"Reporte detallado por compañia")

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

    


    
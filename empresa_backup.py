import pandas as pd
import mysql.connector

# Especificar el nombre del archivo Excel
archivo_excel = 'empresa_backup.xlsx'  # Asegúrate de que este sea el nombre correcto del archivo Excel

# Leer el archivo Excel e importar los datos a MySQL
def importar_datos_desde_excel(archivo_excel):
    df = pd.read_excel(archivo_excel)

    # Convertir la columna de fechas al formato adecuado
    if 'fecha_contratacion' in df.columns:
        df['fecha_contratacion'] = pd.to_datetime(df['fecha_contratacion']).dt.strftime('%Y-%m-%d')

    # Configurar la conexión a MySQL
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost', 
        database='empresa'
    )
    cursor = cnx.cursor()

    # Truncar la tabla para eliminar los datos anteriores
    cursor.execute("TRUNCATE TABLE empleados")

    # Inserción dinámica de los datos en una tabla
    for index, row in df.iterrows():
        sql = """
        INSERT INTO empleados (nombre, apellido, email, telefono, fecha_contratacion, salario, departamento_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, tuple(row))

    # Confirmar los cambios en la base de datos
    cnx.commit()

    # Cerrar la conexión
    cursor.close()
    cnx.close()

    print("Datos importados desde Excel.")

# Exportar datos desde MySQL al mismo archivo Excel
def exportar_datos_a_excel(archivo_excel):
    # Configurar la conexión a MySQL
    cnx = mysql.connector.connect(
        user='root', 
        password='root', 
        host='localhost', 
        database='empresa'
    )

    # Consulta SQL para extraer los datos, excluyendo la columna id
    query = "SELECT nombre, apellido, email, telefono, fecha_contratacion, salario, departamento_id FROM empleados"

    # Leer los datos desde MySQL a un DataFrame de pandas
    df = pd.read_sql(query, cnx)

    # Exportar los datos al archivo Excel (sobrescribiendo el existente)
    df.to_excel(archivo_excel, index=False)

    # Cerrar la conexión a la base de datos
    cnx.close()

    print(f"Datos exportados a {archivo_excel}")

# Ejecutar las funciones en secuencia
importar_datos_desde_excel(archivo_excel)
exportar_datos_a_excel(archivo_excel)



import sqlite3 as sql
import os

def createDB(): # Se crea la base de datos si es que no existe
    conn = sql.connect('Gastos.db') 
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Gastos (
            Id INTEGER PRIMARY KEY NOT NULL,
            Tipo TEXT NOT NULL CHECK (Tipo IN('comida','transporte','salida','otros','income')),
            Descripcion TEXT NOT NULL,
            Monto REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def ingresar_gasto():
    limpiar_consola()
    tipo = input('Ingrese el tipo de gasto Comida, Transporte, Salida, Otros: ')
    tipo.lower()
    descripcion = input("Ingrese una descripción del gasto: ")
    monto = float(input("Ingrese el monto del gasto: "))
    monto *= -1
    
    conn = sql.connect('Gastos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Gastos (Tipo, Descripcion, Monto) VALUES (?, ?, ?)", (tipo, descripcion, monto))
    
    conn.commit()
    conn.close()
    
    print("Gasto cargado exitosamente.")


def cargar_plata():
    limpiar_consola()
    monto = float(input("Ingrese el monto a cargar: "))
    tipo = 'income'
    descripcion = input("Ingrese una descripción del Ingreso: ")
    
    conn = sql.connect('Gastos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Gastos (Tipo, Descripcion, Monto) VALUES (?, ?, ?)", (tipo, descripcion, monto))
    
    conn.commit()
    conn.close()
    
    print("Carga de plata realizada exitosamente.")


def ver_plata():
    conn = sql.connect('Gastos.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(Monto) FROM Gastos")
    result = cursor.fetchone()[0]
    result = result if result is not None else 0.0
    limpiar_consola()
    print("Plata disponible:", result)
    
    conn.close()

def ver_gastos():
    conn = sql.connect('Gastos.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id, Tipo, Descripcion, Monto FROM Gastos")
    gastos = cursor.fetchall()
    limpiar_consola()
    
    if not gastos:
        print("No se encontraron gastos registrados.")
    else:
        print("Gastos registrados:")
        for gasto in gastos:
            print("---------------------------------------------")
            print("ID: ", gasto[0])
            print("Tipo: ", gasto[1])
            print("Descripción: ", gasto[2])
            print("Monto: ", gasto[3])
            print("---------------------------------------------")
    
    conn.close()

    consulta = input('Quieres generar un archivo txt en el escritorio con la informacion (Si,No): ')
    consulta.lower()
    carpetaDesktop = r'C:\Users\Mateo\Desktop'
    
    
    if consulta == 'si':
        
        archivo = os.path.join(carpetaDesktop, "gastos.txt")

        with open(archivo, "w") as file:
            file.write("Gastos registrados:\n")
            for gasto in gastos:
                file.write("---------------------------------------------\n")
                file.write("ID: " + str(gasto[0]) + "\n")
                file.write("Tipo: " + gasto[1] + "\n")
                file.write("Descripción: " + gasto[2] + "\n")
                file.write("Monto: " + str(gasto[3]) + "\n")
                file.write("---------------------------------------------\n")
        print("Se ha generado el archivo 'gastos.txt' en el escritorio con la información de los gastos.")
    else:
        pass
def mostrar_menu(): # Menu para saber como manejarme en el programa
    print("1. Cargar gasto")
    print("2. Cargar plata")
    print("3. Ver plata disponible")
    print("4. Ver gastos")
    print("5. Salir")

def ejecutar_opcion(opcion):
    if opcion == "1":
        ingresar_gasto()
    elif opcion == "2":
        cargar_plata()
    elif opcion == "3":
        ver_plata()
    elif opcion == "4":
        ver_gastos()
    elif opcion == "5":
        return False
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
    
    return True


def limpiar_consola(): #limpiar consola asi puedo tener algo mas comodo de leer (preparado para todos los sitemas operativos)
    if os.name == 'posix':  # Sistema UNIX/Linux/Mac
        _ = os.system('clear')
    else:  # Windows
        _ = os.system('cls')


if __name__ == '__main__':
    createDB()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if not ejecutar_opcion(opcion):
            break



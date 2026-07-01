import sqlite3

def inicializar_base_datos():
    conexion = sqlite3.connect("inventario_maderas.db") #Conexión base de datos
    cursor = conexion.cursor()
    
    # Tabla de productos (inventario)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_madera TEXT NOT NULL,
            metros_cubicos REAL NOT NULL,
            precio_por_m3 REAL NOT NULL
        )
    """)

    # Tabla de mermas (pérdidas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mermas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad_perdida REAL NOT NULL,
            motivo TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES inventario(id)
        )
    """)
    
    conexion.commit()
    conexion.close()

    ######################################################
    ### FUNCIÓN registrar_ingreso(tipo, metros, precio)###
    ######################################################

def registrar_ingreso(tipo, metros, precio):
    conexion = sqlite3.connect("inventario_maderas.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
        INSERT INTO inventario (tipo_madera, metros_cubicos, precio_por_m3)
        VALUES (?, ?, ?)
    """, (tipo, metros, precio))
    
    conexion.commit()
    conexion.close()
    print(f"Se han registrado {metros} m³ de madera de {tipo}.")

    ##############################################################
    ### FUNCIÓN registrar_merma(id_producto), cantidad, motivo)###
    ##############################################################

def registrar_merma(id_producto, cantidad, motivo):
    conexion = sqlite3.connect("inventario_maderas.db")
    cursor = conexion.cursor()
    
    # Se verifica si hay suficiente madera de ese ID
    cursor.execute("SELECT tipo_madera, metros_cubicos FROM inventario WHERE id = ?", (id_producto,))
    producto = cursor.fetchone() 
    
    if not producto:
        print(f"Error: No existe ningún producto con el ID {id_producto}")
        conexion.close()
        return

    stock_actual = producto[1]
    nombre_madera = producto[0]
    
    if cantidad > stock_actual:
        print(f"Error: No puedes perder {cantidad} m³ de {nombre_madera}. ¡Solo quedan {stock_actual} m³!")
        conexion.close()
        return
        
    # 2. Si hay, se inserta la pérdida
    cursor.execute("""
        INSERT INTO mermas (producto_id, cantidad_perdida, motivo)
        VALUES (?, ?, ?)
    """, (id_producto, cantidad, motivo))
    
    # 3. Restamos esa cantidad de la tabla 'inventario'
    nuevo_stock = stock_actual - cantidad
    cursor.execute("""
        UPDATE inventario 
        SET metros_cubicos = ? 
        WHERE id = ?
    """, (nuevo_stock, id_producto))
    
    conexion.commit()
    conexion.close()
    print(f"Se han perdido {cantidad} m³ de {nombre_madera} debido a: '{motivo}'.")

    ###################################
    ### FUNCIÓN mostrar_inventario()###
    ###################################

def mostrar_inventario():
    conexion = sqlite3.connect("inventario_maderas.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM inventory" if False else "SELECT * FROM inventario")
    lineas = cursor.fetchall()  
    conexion.close()
    
    print("\n=== INVENTARIO DE MADERAS ===")
    if not lineas:
        print("El almacén está vacío.")
    else:
        for fila in lineas:
            print(f"ID: {fila[0]} | Madera: {fila[1]} | Stock: {fila[2]} m³ | Precio: {fila[3]}€/m³")
    print("=============================\n")

    #############################################
    ### FUNCIÓN eliminar_producto(id_producto)###
    #############################################

def eliminar_producto(id_producto):
    conexion = sqlite3.connect("inventario_maderas.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT tipo_madera FROM inventario WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        print(f"Error: No se puede eliminar. No existe ningún producto con el ID {id_producto}")
        conexion.close()
        return

    nombre_madera = producto[0]
    
    cursor.execute("DELETE FROM inventario WHERE id = ?", (id_producto,))
    cursor.execute("DELETE FROM mermas WHERE id_producto = ?" if False else "DELETE FROM mermas WHERE producto_id = ?", (id_producto,))
    
    conexion.commit()
    conexion.close()
    print(f"El producto '{nombre_madera}' (ID: {id_producto}) ha sido borrado del sistema.")

###############################
# --- PRUEBAS DEL SIMULACRO ---
###############################

def menu_principal():
    inicializar_base_datos()
    
    while True:
        print("\n=========================================")
        print("    SISTEMA DE GESTIÓN: MADERAS DEL NORTE")
        print("=========================================")
        print("1. Ver Inventario Actual")
        print("2. Registrar Ingreso / Importación")
        print("3. Registrar Pérdida / Merma")
        print("4. Eliminar un Producto")
        print("5. Salir de la Aplicación")
        print("=========================================")
        
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == "1":
            mostrar_inventario()
            
        elif opcion == "2":
            print("\n--- NUEVO INGRESO ---")
            tipo = input("Tipo de madera (ej. Pino, Cedro): ")
            metros = float(input("Cantidad en metros cúbicos (m³): "))
            precio = float(input("Precio por metro cúbico (€/m³): "))
            registrar_ingreso(tipo, metros, precio)
            
        elif opcion == "3":
            print("\n--- REGISTRAR PÉRDIDA ---")
            mostrar_inventario()
            id_prod = int(input("Introduce el ID del producto afectado: "))
            cantidad = float(input("Cantidad perdida en m³: "))
            motivo = input("Motivo de la pérdida: ")
            registrar_merma(id_prod, cantidad, motivo)
            
        elif opcion == "4":
            print("\n--- ELIMINAR PRODUCTO ---")
            mostrar_inventario()
            id_prod = int(input("Introduce el ID del producto que deseas BORRAR por completo: "))
            confirmar = input(f"¿Estás seguro de que deseas eliminar el ID {id_prod}? (s/n): ")
            if confirmar.lower() == 's':
                eliminar_producto(id_prod)
            else:
                print("Operación cancelada.")
                
        elif opcion == "5":
            print("\n¡Gracias por usar el sistema! Saliendo...")
            break
            
        else:
            print("\n Opción no válida. Por favor, introduce un número del 1 al 5.")

if __name__ == '__main__':
    menu_principal()
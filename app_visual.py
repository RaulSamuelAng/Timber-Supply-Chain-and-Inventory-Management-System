import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import sqlite3 
import maderera  # Importamos tu lógica del primer archivo

# =========================================================================
# FUNCIÓN: VISTA DE TABLA + GESTIÓN DE PÉRDIDAS (MERMAS)
# =========================================================================
def abrir_inventario():
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Inventario de Maderas - Vista de Tabla")
    ventana_tabla.geometry("600x420")
    ventana_tabla.configure(bg="#f5f5f5")
    
    columnas = ("id", "tipo", "metros", "precio")
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")
    
    tabla.heading("id", text="ID")
    tabla.heading("tipo", text="Tipo de Madera")
    tabla.heading("metros", text="Stock Disponible (m³)")
    tabla.heading("precio", text="Precio (€/m³)")
    
    tabla.column("id", width=50, anchor="center")
    tabla.column("tipo", width=200, anchor="w")
    tabla.column("metros", width=150, anchor="center")
    tabla.column("precio", width=120, anchor="center")
    
    def cargar_datos():
        for item in tabla.get_children():
            tabla.delete(item)
        try:
            conexion = sqlite3.connect("inventario_maderas.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM inventario")
            filas = cursor.fetchall()
            conexion.close()
            for fila in filas:
                tabla.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la base de datos: {e}")

    cargar_datos()
    tabla.pack(expand=True, fill="both", padx=15, pady=15)

    def procesar_merma_seleccionada():
        item_seleccionado = tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, selecciona un producto de la tabla con el ratón.")
            return
        
        valores = tabla.item(item_seleccionado, "values")
        id_producto = int(valores[0])
        nombre_producto = valores[1]

        ventana_merma = tk.Toplevel(ventana_tabla)
        ventana_merma.title(f"Registrar Merma: {nombre_producto}")
        ventana_merma.geometry("320x260")
        ventana_merma.configure(bg="#f0f0f0")

        tk.Label(ventana_merma, text=f"Pérdida para: {nombre_producto} (ID: {id_producto})", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(ventana_merma, text="Cantidad perdida (m³):", bg="#f0f0f0").pack(pady=3)
        txt_cant = tk.Entry(ventana_merma, font=("Arial", 10), width=20)
        txt_cant.pack(pady=5)

        tk.Label(ventana_merma, text="Motivo de la pérdida:", bg="#f0f0f0").pack(pady=3)
        txt_motivo = tk.Entry(ventana_merma, font=("Arial", 10), width=20)
        txt_motivo.pack(pady=5)

        def ejecutar_guardado_merma():
            try:
                cant = float(txt_cant.get().strip())
                motivo = txt_motivo.get().strip()

                if not motivo:
                    messagebox.showwarning("Faltan datos", "Por favor, introduce el motivo.")
                    return

                maderera.registrar_merma(id_producto, cant, motivo)
                messagebox.showinfo("Éxito", "Pérdida registrada correctamente. Stock actualizado.")
                ventana_merma.destroy()
                cargar_datos()

            except ValueError:
                messagebox.showerror("Error de formato", "La cantidad debe ser un número válido.")

        tk.Button(ventana_merma, text="⚠️ Confirmar Pérdida", font=("Arial", 10, "bold"), bg="#f44336", fg="white", command=ejecutar_guardado_merma).pack(pady=15)

    btn_accion_merma = tk.Button(ventana_tabla, text="⚠️ Registrar Pérdida del Producto Seleccionado", font=("Arial", 10, "bold"), bg="#ff9800", fg="white", command=procesar_merma_seleccionada)
    btn_accion_merma.pack(pady=10)

# =========================================================================
# FUNCIÓN: VISTA DEL HISTORIAL DE PÉRDIDAS (MERMAS)
# =========================================================================
def abrir_historial_mermas():
    ventana_mermas = tk.Toplevel()
    ventana_mermas.title("Historial de Pérdidas / Mermas")
    ventana_mermas.geometry("650x350")
    ventana_mermas.configure(bg="#f5f5f5")
    
    columnas = ("id", "producto", "cantidad", "motivo", "fecha")
    tabla_mermas = ttk.Treeview(ventana_mermas, columns=columnas, show="headings")
    
    tabla_mermas.heading("id", text="ID Merma")
    tabla_mermas.heading("producto", text="Madera")
    tabla_mermas.heading("cantidad", text="Cantidad Perdida")
    tabla_mermas.heading("motivo", text="Motivo")
    tabla_mermas.heading("fecha", text="Fecha / Hora")
    
    tabla_mermas.column("id", width=70, anchor="center")
    tabla_mermas.column("producto", width=120, anchor="w")
    tabla_mermas.column("cantidad", width=110, anchor="center")
    tabla_mermas.column("motivo", width=180, anchor="w")
    tabla_mermas.column("fecha", width=150, anchor="center")
    
    try:
        conexion = sqlite3.connect("inventario_maderas.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT mermas.id, inventario.tipo_madera, mermas.cantidad_perdida, mermas.motivo, mermas.fecha 
            FROM mermas
            INNER JOIN inventario ON mermas.producto_id = inventario.id
        """)
        filas = cursor.fetchall()
        conexion.close()
        
        for fila in filas:
            tabla_mermas.insert("", tk.END, values=fila)
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar el historial: {e}")

    tabla_mermas.pack(expand=True, fill="both", padx=15, pady=15)

# =========================================================================
# FUNCIÓN: FORMULARIO PARA REGISTRAR NUEVO INGRESO
# =========================================================================
def abrir_formulario_ingreso():
    ventana_form = tk.Toplevel()
    ventana_form.title("Registrar Ingreso de Madera")
    ventana_form.geometry("350x300")
    ventana_form.configure(bg="#f0f0f0")

    tk.Label(ventana_form, text="Tipo de Madera (Ej: Pino, Cedro):", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    txt_tipo = tk.Entry(ventana_form, font=("Arial", 10), width=25)
    txt_tipo.pack(pady=5)

    tk.Label(ventana_form, text="Metros Cúbicos (m³):", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    txt_metros = tk.Entry(ventana_form, font=("Arial", 10), width=25)
    txt_metros.pack(pady=5)

    tk.Label(ventana_form, text="Precio por m³ (€):", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    txt_precio = tk.Entry(ventana_form, font=("Arial", 10), width=25)
    txt_precio.pack(pady=5)

    def guardar_datos():
        tipo = txt_tipo.get().strip()
        metros_str = txt_metros.get().strip()
        precio_str = txt_precio.get().strip()

        if not tipo or not metros_str or not precio_str:
            messagebox.showwarning("Campos vacíos", "Por favor, rellena todos los campos.")
            return

        try:
            metros = float(metros_str)
            precio = float(precio_str)
            maderera.registrar_ingreso(tipo, metros, precio)
            messagebox.showinfo("Éxito", f"¡Se han registrado {metros} m³ de {tipo} correctamente!")
            ventana_form.destroy()
        except ValueError:
            messagebox.showerror("Error de formato", "Los metros y el precio deben ser números válidos.")

    btn_guardar = tk.Button(ventana_form, text="💾 Guardar en Almacén", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=guardar_datos)
    btn_guardar.pack(pady=20)

# =========================================================================
# VENTANA PRINCIPAL DE LA APLICACIÓN
# =========================================================================
def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Maderas del Norte - Control de Inventario")
    ventana.geometry("500x460") # Ajustamos la altura para el nuevo botón
    ventana.configure(bg="#e0e0e0")

    titulo = tk.Label(ventana, text="Panel de Control del Almacén", font=("Arial", 16, "bold"), bg="#e0e0e0", fg="#333333")
    titulo.pack(pady=20)

    btn_ver = tk.Button(ventana, text="📊 Ver Inventario Actual", font=("Arial", 11), width=28, command=abrir_inventario)
    btn_ver.pack(pady=8)

    btn_ingreso = tk.Button(ventana, text="📥 Registrar Nuevo Ingreso", font=("Arial", 11), width=28, command=abrir_formulario_ingreso)
    btn_ingreso.pack(pady=8)

    btn_merma = tk.Button(ventana, text="⚠️ Registrar Pérdida / Merma", font=("Arial", 11), width=28, command=abrir_inventario)
    btn_merma.pack(pady=8)

    # NUEVO BOTÓN: Ver Historial de Pérdidas
    btn_historial = tk.Button(ventana, text="📋 Ver Historial de Pérdidas", font=("Arial", 11), width=28, bg="#2196F3", fg="white", command=abrir_historial_mermas)
    btn_historial.pack(pady=8)

    btn_salir = tk.Button(ventana, text="❌ Salir de la Aplicación", font=("Arial", 11), width=28, command=ventana.quit)
    btn_salir.pack(pady=20)

    ventana.mainloop()

if __name__ == '__main__':
    crear_ventana_principal()
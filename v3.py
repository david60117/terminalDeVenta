import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

COLOR_FONDO = "#ecf0f1"
COLOR_TITULO = "#2c3e50"
COLOR_GRIS = "#555555"
FUENTE = ("Arial", 11)
FUENTE_CHICA = ("Arial", 9)
FUENTE_LISTA = ("Courier New", 11)
FUENTE_LISTA_NEGRITA = ("Courier New", 11, "bold")
IVA = 0.16
NOMBRE_TIENDA = "MUEBLERÍA EL ROBLE"

usuarios = {
    "admin": {"contrasena": "admin123", "nombre": "David Jonathan Hernández Mejía", "rol": "Administrador"},
    "vendedor": {"contrasena": "vendedor123", "nombre": "Jonathan Flores Cordero", "rol": "Vendedor"},
}

productos = [
    {"codigo": 1, "nombre": "Sofá de 3 plazas", "tipo": "Sala", "precio": 8999.00, "existencia": 5},
    {"codigo": 2, "nombre": "Sillón reclinable", "tipo": "Sala", "precio": 6499.00, "existencia": 6},
    {"codigo": 3, "nombre": "Mesa de centro", "tipo": "Sala", "precio": 1899.00, "existencia": 10},
    {"codigo": 4, "nombre": "Comedor 6 sillas", "tipo": "Comedor", "precio": 12999.00, "existencia": 3},
    {"codigo": 5, "nombre": "Silla de comedor", "tipo": "Comedor", "precio": 899.00, "existencia": 24},
    {"codigo": 6, "nombre": "Cama matrimonial", "tipo": "Recámara", "precio": 7499.00, "existencia": 4},
    {"codigo": 7, "nombre": "Colchón individual", "tipo": "Recámara", "precio": 3299.00, "existencia": 8},
    {"codigo": 8, "nombre": "Buró 2 cajones", "tipo": "Recámara", "precio": 1299.00, "existencia": 12},
    {"codigo": 9, "nombre": "Ropero 3 puertas", "tipo": "Recámara", "precio": 5799.00, "existencia": 4},
    {"codigo": 10, "nombre": "Escritorio juvenil", "tipo": "Oficina", "precio": 2799.00, "existencia": 7},
]


clientes = [
    {"id": 1, "nombre": "Público en general", "telefono": "", "correo": ""},
]

ventas = []
carrito = []
sesion = {"nombre": "", "rol": ""}



def iniciar_sesion():
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get()

    if usuario not in usuarios or usuarios[usuario]["contrasena"] != contrasena:
        messagebox.showerror("Iniciar sesión", "Usuario o contraseña incorrectos.")
        return

    sesion["nombre"] = usuarios[usuario]["nombre"]
    sesion["rol"] = usuarios[usuario]["rol"]
    etiqueta_sesion.config(text=f"Sesión: {sesion['nombre']}  ({sesion['rol']})")


    if sesion["rol"] == "Administrador":
        estado_pestana = "normal"
        estado_boton = "normal"
    else:
        estado_pestana = "hidden"
        estado_boton = "disabled"
    pestanas.tab(tab_inventario, state=estado_pestana)
    pestanas.tab(tab_historial, state=estado_pestana)
    boton_eliminar_cliente.config(state=estado_boton)
    pestanas.select(tab_venta)

    entrada_usuario.delete(0, tk.END)
    entrada_contrasena.delete(0, tk.END)
    marco_login.pack_forget()
    marco_principal.pack(padx=15, pady=10)
    entrada_codigo.focus()


def cerrar_sesion():
    if not messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar la sesión?"):
        return
    limpiar_venta()
    marco_principal.pack_forget()
    marco_login.pack(padx=40, pady=30)
    entrada_usuario.focus()



def buscar_producto(codigo):
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    return None


def calcular_totales():
    total = 0
    for linea in carrito:
        total = total + linea["importe"]
    total = round(total, 2)
    subtotal = round(total / (1 + IVA), 2)
    iva = round(total - subtotal, 2)
    return subtotal, iva, total


def mostrar_catalogo():
    lista_catalogo.delete(0, tk.END)
    for producto in productos:
        lista_catalogo.insert(tk.END, f"{producto['codigo']:>4}  {producto['nombre'][:24]:<24}"
                                      f"{producto['precio']:>12,.2f}{producto['existencia']:>10}")


def mostrar_carrito():
    lista_carrito.delete(0, tk.END)
    for linea in carrito:
        lista_carrito.insert(tk.END, f"{linea['cantidad']:>4}  {linea['nombre'][:24]:<24}"
                                     f"{linea['precio']:>11,.2f}{linea['importe']:>12,.2f}")

    subtotal, iva, total = calcular_totales()
    etiqueta_subtotal.config(text=f"${subtotal:,.2f}")
    etiqueta_iva.config(text=f"${iva:,.2f}")
    etiqueta_total.config(text=f"${total:,.2f}")


def seleccionar_del_catalogo(evento):
    seleccion = lista_catalogo.curselection()
    if not seleccion:
        return
    producto = productos[seleccion[0]]
    entrada_codigo.delete(0, tk.END)
    entrada_codigo.insert(0, str(producto["codigo"]))
    entrada_cantidad.focus()
    entrada_cantidad.select_range(0, tk.END)


def agregar_a_venta():
    try:
        codigo = int(entrada_codigo.get())
        cantidad = int(entrada_cantidad.get())
    except ValueError:
        messagebox.showerror("Dato inválido", "El código y la cantidad deben ser números enteros.")
        return

    producto = buscar_producto(codigo)
    if producto is None:
        messagebox.showerror("Producto", f"No existe un producto con el código {codigo}.")
        return
    if cantidad <= 0:
        messagebox.showerror("Cantidad", "La cantidad debe ser mayor a 0.")
        return


    linea_existente = None
    for linea in carrito:
        if linea["codigo"] == codigo:
            linea_existente = linea

    ya_en_venta = 0
    if linea_existente is not None:
        ya_en_venta = linea_existente["cantidad"]

    if ya_en_venta + cantidad > producto["existencia"]:
        messagebox.showwarning("Existencia insuficiente",
                               f"Solo hay {producto['existencia']} de \"{producto['nombre']}\".")
        return

    if linea_existente is None:
        carrito.append({"codigo": codigo, "nombre": producto["nombre"], "precio": producto["precio"],
                        "cantidad": cantidad, "importe": producto["precio"] * cantidad})
    else:
        linea_existente["cantidad"] = linea_existente["cantidad"] + cantidad
        linea_existente["importe"] = linea_existente["precio"] * linea_existente["cantidad"]

    mostrar_carrito()
    entrada_codigo.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_cantidad.insert(0, "1")
    entrada_codigo.focus()


def quitar_de_venta():
    seleccion = lista_carrito.curselection()
    if not seleccion:
        messagebox.showinfo("Quitar producto", "Selecciona un producto de la venta.")
        return
    carrito.pop(seleccion[0])
    mostrar_carrito()


def limpiar_venta():
    carrito.clear()
    mostrar_carrito()
    entrada_codigo.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_cantidad.insert(0, "1")
    entrada_pago.delete(0, tk.END)
    combo_cliente.current(0)
    lista_catalogo.selection_clear(0, tk.END)


def cancelar_venta():
    if carrito and messagebox.askyesno("Cancelar venta", "¿Quitar todos los productos de la venta?"):
        limpiar_venta()


def cobrar():
    if not carrito:
        messagebox.showwarning("Cobrar", "No hay productos en la venta.")
        return

    subtotal, iva, total = calcular_totales()
    try:
        pago = float(entrada_pago.get())
    except ValueError:
        messagebox.showerror("Pago", "Escribe con cuánto paga el cliente.")
        return
    if pago < total:
        messagebox.showerror("Pago", f"Pago insuficiente. Faltan ${total - pago:,.2f}")
        return


    for linea in carrito:
        producto = buscar_producto(linea["codigo"])
        if producto is not None:
            producto["existencia"] = producto["existencia"] - linea["cantidad"]

    cliente = clientes[combo_cliente.current()]
    venta = {
        "folio": len(ventas) + 1,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "cliente": cliente["nombre"],
        "vendedor": sesion["nombre"],
        "productos": carrito.copy(),
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "pago": pago,
        "cambio": pago - total,
    }
    ventas.append(venta)

    mostrar_ticket(venta)
    limpiar_venta()
    mostrar_catalogo()
    mostrar_inventario()
    mostrar_historial()



def generar_ticket(venta):
    separador = "-" * 46 + "\n"
    texto = NOMBRE_TIENDA.center(46) + "\n"
    texto += "Ticket de venta".center(46) + "\n"
    texto += separador
    texto += f"Folio:   {venta['folio']:04d}\n"
    texto += f"Fecha:   {venta['fecha']}\n"
    texto += f"Cliente: {venta['cliente']}\n"
    texto += f"Atendió: {venta['vendedor']}\n"
    texto += separador
    texto += f"{'Cant':>4}  {'Producto':<19}{'P. Unit.':>10}{'Importe':>11}\n"
    for linea in venta["productos"]:
        texto += (f"{linea['cantidad']:>4}  {linea['nombre'][:18]:<19}"
                  f"{linea['precio']:>10,.2f}{linea['importe']:>11,.2f}\n")
    texto += separador
    texto += f"{'Subtotal:':>31}  ${venta['subtotal']:>12,.2f}\n"
    texto += f"{'IVA (16%):':>31}  ${venta['iva']:>12,.2f}\n"
    texto += f"{'TOTAL:':>31}  ${venta['total']:>12,.2f}\n"
    texto += f"{'Pago:':>31}  ${venta['pago']:>12,.2f}\n"
    texto += f"{'Cambio:':>31}  ${venta['cambio']:>12,.2f}\n"
    texto += separador
    texto += "¡Gracias por su compra!".center(46) + "\n"
    return texto


def mostrar_ticket(venta):
    ventana_ticket = tk.Toplevel(ventana)
    ventana_ticket.title(f"Ticket - Folio {venta['folio']:04d}")
    ventana_ticket.config(bg=COLOR_FONDO)
    ventana_ticket.resizable(False, False)

    texto = generar_ticket(venta)
    caja_ticket = tk.Text(ventana_ticket, font=FUENTE_LISTA, width=46, height=texto.count("\n"),
                          bg="white", padx=10, pady=10)
    caja_ticket.insert("1.0", texto)
    caja_ticket.config(state="disabled")
    caja_ticket.pack(padx=15, pady=15)

    tk.Button(ventana_ticket, text="Cerrar", font=FUENTE, width=12,
              command=ventana_ticket.destroy).pack(pady=(0, 15))



def mostrar_inventario():
    lista_inventario.delete(0, tk.END)
    for producto in productos:
        lista_inventario.insert(tk.END, f"{producto['codigo']:>4}  {producto['nombre'][:19]:<20}"
                                        f"{producto['tipo'][:11]:<12}{producto['precio']:>9,.2f}"
                                        f"{producto['existencia']:>7}")


def limpiar_campos_producto():
    etiqueta_codigo_producto.config(text="(nuevo)")
    entrada_nombre_producto.delete(0, tk.END)
    entrada_tipo_producto.delete(0, tk.END)
    entrada_precio_producto.delete(0, tk.END)
    entrada_existencia_producto.delete(0, tk.END)
    lista_inventario.selection_clear(0, tk.END)


def seleccionar_producto(evento):
    seleccion = lista_inventario.curselection()
    if not seleccion:
        return
    producto = productos[seleccion[0]]
    etiqueta_codigo_producto.config(text=str(producto["codigo"]))
    entrada_nombre_producto.delete(0, tk.END)
    entrada_nombre_producto.insert(0, producto["nombre"])
    entrada_tipo_producto.delete(0, tk.END)
    entrada_tipo_producto.insert(0, producto["tipo"])
    entrada_precio_producto.delete(0, tk.END)
    entrada_precio_producto.insert(0, f"{producto['precio']:.2f}")
    entrada_existencia_producto.delete(0, tk.END)
    entrada_existencia_producto.insert(0, str(producto["existencia"]))


def leer_campos_producto():

    nombre = entrada_nombre_producto.get().strip()
    tipo = entrada_tipo_producto.get().strip()
    if nombre == "" or tipo == "":
        messagebox.showwarning("Campos vacíos", "Escribe el nombre y el tipo del producto.")
        return None
    try:
        precio = float(entrada_precio_producto.get())
        existencia = int(entrada_existencia_producto.get())
    except ValueError:
        messagebox.showerror("Dato inválido", "El precio debe ser un número y la existencia un número entero.")
        return None
    if precio <= 0 or existencia < 0:
        messagebox.showerror("Dato inválido", "El precio debe ser mayor a 0 y la existencia no puede ser negativa.")
        return None
    return {"nombre": nombre, "tipo": tipo, "precio": precio, "existencia": existencia}


def agregar_producto():
    datos = leer_campos_producto()
    if datos is None:
        return

    if productos:
        datos["codigo"] = productos[-1]["codigo"] + 1
    else:
        datos["codigo"] = 1
    productos.append(datos)

    mostrar_inventario()
    mostrar_catalogo()
    limpiar_campos_producto()
    messagebox.showinfo("Inventario", f"Producto agregado con el código {datos['codigo']}.")


def guardar_producto():
    seleccion = lista_inventario.curselection()
    if not seleccion:
        messagebox.showinfo("Guardar cambios", "Selecciona un producto de la lista.")
        return
    datos = leer_campos_producto()
    if datos is None:
        return

    productos[seleccion[0]].update(datos)

    mostrar_inventario()
    mostrar_catalogo()
    limpiar_campos_producto()
    messagebox.showinfo("Inventario", "Cambios guardados.")


def eliminar_producto():
    seleccion = lista_inventario.curselection()
    if not seleccion:
        messagebox.showinfo("Eliminar", "Selecciona un producto de la lista.")
        return
    producto = productos[seleccion[0]]
    if not messagebox.askyesno("Eliminar", f"¿Eliminar \"{producto['nombre']}\" del inventario?"):
        return

    productos.pop(seleccion[0])
    mostrar_inventario()
    mostrar_catalogo()
    limpiar_campos_producto()



def mostrar_clientes():
    lista_clientes.delete(0, tk.END)
    nombres = []
    for cliente in clientes:
        lista_clientes.insert(tk.END, f"{cliente['id']:>4}  {cliente['nombre'][:18]:<19}"
                                      f"{cliente['telefono'][:10]:<11}{cliente['correo'][:18]}")
        nombres.append(cliente["nombre"])

    combo_cliente.config(values=nombres)
    combo_cliente.current(0)


def limpiar_campos_cliente():
    etiqueta_id_cliente.config(text="(nuevo)")
    entrada_nombre_cliente.delete(0, tk.END)
    entrada_telefono_cliente.delete(0, tk.END)
    entrada_correo_cliente.delete(0, tk.END)
    lista_clientes.selection_clear(0, tk.END)


def seleccionar_cliente(evento):
    seleccion = lista_clientes.curselection()
    if not seleccion:
        return
    cliente = clientes[seleccion[0]]
    etiqueta_id_cliente.config(text=str(cliente["id"]))
    entrada_nombre_cliente.delete(0, tk.END)
    entrada_nombre_cliente.insert(0, cliente["nombre"])
    entrada_telefono_cliente.delete(0, tk.END)
    entrada_telefono_cliente.insert(0, cliente["telefono"])
    entrada_correo_cliente.delete(0, tk.END)
    entrada_correo_cliente.insert(0, cliente["correo"])


def leer_campos_cliente():
    nombre = entrada_nombre_cliente.get().strip()
    if nombre == "":
        messagebox.showwarning("Campos vacíos", "Escribe el nombre del cliente.")
        return None
    return {"nombre": nombre,
            "telefono": entrada_telefono_cliente.get().strip(),
            "correo": entrada_correo_cliente.get().strip()}


def agregar_cliente():
    datos = leer_campos_cliente()
    if datos is None:
        return
    datos["id"] = clientes[-1]["id"] + 1
    clientes.append(datos)

    mostrar_clientes()
    combo_cliente.current(len(clientes) - 1)
    limpiar_campos_cliente()
    messagebox.showinfo("Clientes", f"Cliente registrado con el ID {datos['id']}.\n"
                                    "Ya quedó seleccionado en la pestaña Venta.")


def ir_a_clientes():
    pestanas.select(tab_clientes)
    limpiar_campos_cliente()
    entrada_nombre_cliente.focus()


def guardar_cliente():
    seleccion = lista_clientes.curselection()
    if not seleccion:
        messagebox.showinfo("Guardar cambios", "Selecciona un cliente de la lista.")
        return
    datos = leer_campos_cliente()
    if datos is None:
        return

    clientes[seleccion[0]].update(datos)

    mostrar_clientes()
    limpiar_campos_cliente()
    messagebox.showinfo("Clientes", "Cambios guardados.")


def eliminar_cliente():
    seleccion = lista_clientes.curselection()
    if not seleccion:
        messagebox.showinfo("Eliminar", "Selecciona un cliente de la lista.")
        return
    cliente = clientes[seleccion[0]]
    if cliente["id"] == 1:
        messagebox.showwarning("Eliminar", "\"Público en general\" no se puede eliminar.")
        return
    if not messagebox.askyesno("Eliminar", f"¿Eliminar al cliente \"{cliente['nombre']}\"?"):
        return

    clientes.pop(seleccion[0])
    mostrar_clientes()
    limpiar_campos_cliente()



def mostrar_historial():
    lista_historial.delete(0, tk.END)
    total_vendido = 0
    for venta in ventas:
        lista_historial.insert(tk.END, f"{venta['folio']:>5}  {venta['fecha']:<18}"
                                       f"{venta['cliente'][:17]:<17}{venta['total']:>12,.2f}")
        total_vendido = total_vendido + venta["total"]

    etiqueta_num_ventas.config(text=str(len(ventas)))
    etiqueta_total_vendido.config(text=f"${total_vendido:,.2f}")


def ver_ticket():
    seleccion = lista_historial.curselection()
    if not seleccion:
        messagebox.showinfo("Ver ticket", "Selecciona una venta de la lista.")
        return
    mostrar_ticket(ventas[seleccion[0]])





ventana = tk.Tk()
ventana.title(f"{NOMBRE_TIENDA} - Punto de venta")
ventana.config(bg=COLOR_FONDO)
ventana.resizable(False, False)


ventana.option_add("*foreground", "black")
ventana.option_add("*Entry.background", "white")
ventana.option_add("*Listbox.background", "white")
ventana.option_add("*insertBackground", "black")
ventana.option_add("*highlightBackground", COLOR_FONDO)

titulo = tk.Label(ventana, text=NOMBRE_TIENDA, font=("Arial", 18, "bold"),
                  bg=COLOR_TITULO, fg="white", pady=10)
titulo.pack(fill="x")


marco_login = tk.Frame(ventana, bg=COLOR_FONDO)
marco_login.pack(padx=40, pady=30)

caja_login = tk.LabelFrame(marco_login, text=" Iniciar sesión ", font=FUENTE,
                           bg=COLOR_FONDO, padx=20, pady=15)
caja_login.pack()

tk.Label(caja_login, text="Usuario:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
entrada_usuario = tk.Entry(caja_login, font=FUENTE, width=20)
entrada_usuario.grid(row=0, column=1, padx=5, pady=5)

tk.Label(caja_login, text="Contraseña:", font=FUENTE, bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
entrada_contrasena = tk.Entry(caja_login, font=FUENTE, width=20, show="*")
entrada_contrasena.grid(row=1, column=1, padx=5, pady=5)

tk.Button(caja_login, text="Iniciar sesión", font=FUENTE, bg="#f1948a",
          command=iniciar_sesion).grid(row=2, column=0, columnspan=2, sticky="we", pady=(10, 0))



marco_principal = tk.Frame(ventana, bg=COLOR_FONDO)

barra_sesion = tk.Frame(marco_principal, bg=COLOR_FONDO)
barra_sesion.pack(fill="x", pady=(0, 10))
etiqueta_sesion = tk.Label(barra_sesion, text="", font=FUENTE, bg=COLOR_FONDO)
etiqueta_sesion.pack(side="left")
tk.Button(barra_sesion, text="Cerrar sesión", font=FUENTE, bg="#f1948a",
          command=cerrar_sesion).pack(side="right")

pestanas = ttk.Notebook(marco_principal)
pestanas.pack()

tab_venta = tk.Frame(pestanas, bg=COLOR_FONDO, padx=10, pady=10)
tab_inventario = tk.Frame(pestanas, bg=COLOR_FONDO, padx=10, pady=10)
tab_clientes = tk.Frame(pestanas, bg=COLOR_FONDO, padx=10, pady=10)
tab_historial = tk.Frame(pestanas, bg=COLOR_FONDO, padx=10, pady=10)

pestanas.add(tab_venta, text="  Venta  ")
pestanas.add(tab_inventario, text="  Inventario  ")
pestanas.add(tab_clientes, text="  Clientes  ")
pestanas.add(tab_historial, text="  Historial de ventas  ")



marco_catalogo = tk.LabelFrame(tab_venta, text=" Catálogo de productos ", font=FUENTE,
                               bg=COLOR_FONDO, padx=10, pady=10)
marco_catalogo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

tk.Label(marco_catalogo, text=f"{'Cód':>4}  {'Producto':<24}{'Precio':>12}{'Exist.':>10}",
         font=FUENTE_LISTA_NEGRITA, bg=COLOR_FONDO, padx=3).grid(row=0, column=0, sticky="w")
lista_catalogo = tk.Listbox(marco_catalogo, font=FUENTE_LISTA, width=54, height=8, exportselection=False)
lista_catalogo.grid(row=1, column=0)
barra_catalogo = tk.Scrollbar(marco_catalogo, command=lista_catalogo.yview)
barra_catalogo.grid(row=1, column=1, sticky="ns")
lista_catalogo.config(yscrollcommand=barra_catalogo.set)
lista_catalogo.bind("<<ListboxSelect>>", seleccionar_del_catalogo)
tk.Label(marco_catalogo, text="Haz clic en un producto para usar su código.", font=FUENTE_CHICA,
         fg=COLOR_GRIS, bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=(5, 0))


marco_datos_venta = tk.LabelFrame(tab_venta, text=" Datos de la venta ", font=FUENTE,
                                  bg=COLOR_FONDO, padx=10, pady=10)
marco_datos_venta.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(marco_datos_venta, text="Cliente:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
combo_cliente = ttk.Combobox(marco_datos_venta, font=FUENTE, width=22, state="readonly")
combo_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=5)
tk.Button(marco_datos_venta, text="+ Registrar cliente nuevo", font=FUENTE_CHICA,
          command=ir_a_clientes).grid(row=1, column=1, sticky="w", padx=5)

tk.Label(marco_datos_venta, text="Código:", font=FUENTE, bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=5)
entrada_codigo = tk.Entry(marco_datos_venta, font=FUENTE, width=8)
entrada_codigo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(marco_datos_venta, text="Cantidad:", font=FUENTE, bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=5)
entrada_cantidad = tk.Entry(marco_datos_venta, font=FUENTE, width=8)
entrada_cantidad.grid(row=3, column=1, sticky="w", padx=5, pady=5)
entrada_cantidad.insert(0, "1")

tk.Button(marco_datos_venta, text="Agregar a la venta", font=FUENTE, bg="#82e0aa",
          command=agregar_a_venta).grid(row=4, column=0, columnspan=2, sticky="we", pady=(15, 0))


marco_carrito = tk.LabelFrame(tab_venta, text=" Productos en la venta ", font=FUENTE,
                              bg=COLOR_FONDO, padx=10, pady=10)
marco_carrito.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

tk.Label(marco_carrito, text=f"{'Cant':>4}  {'Producto':<24}{'P. Unit.':>11}{'Importe':>12}",
         font=FUENTE_LISTA_NEGRITA, bg=COLOR_FONDO, padx=3).grid(row=0, column=0, sticky="w")
lista_carrito = tk.Listbox(marco_carrito, font=FUENTE_LISTA, width=54, height=7, exportselection=False)
lista_carrito.grid(row=1, column=0)
barra_carrito = tk.Scrollbar(marco_carrito, command=lista_carrito.yview)
barra_carrito.grid(row=1, column=1, sticky="ns")
lista_carrito.config(yscrollcommand=barra_carrito.set)

marco_botones_carrito = tk.Frame(marco_carrito, bg=COLOR_FONDO)
marco_botones_carrito.grid(row=2, column=0, columnspan=2, pady=(10, 0))
tk.Button(marco_botones_carrito, text="Quitar producto", font=FUENTE, bg="#f1948a", width=18,
          command=quitar_de_venta).pack(side="left", padx=5)
tk.Button(marco_botones_carrito, text="Cancelar venta", font=FUENTE, bg="#85c1e9", width=18,
          command=cancelar_venta).pack(side="left", padx=5)


marco_cobro = tk.LabelFrame(tab_venta, text=" Cobro ", font=FUENTE,
                            bg=COLOR_FONDO, padx=10, pady=10)
marco_cobro.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(marco_cobro, text="Subtotal:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=3)
etiqueta_subtotal = tk.Label(marco_cobro, text="$0.00", font=FUENTE, bg=COLOR_FONDO)
etiqueta_subtotal.grid(row=0, column=1, sticky="e", pady=3)

tk.Label(marco_cobro, text="IVA (16%):", font=FUENTE, bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=3)
etiqueta_iva = tk.Label(marco_cobro, text="$0.00", font=FUENTE, bg=COLOR_FONDO)
etiqueta_iva.grid(row=1, column=1, sticky="e", pady=3)

tk.Label(marco_cobro, text="TOTAL:", font=("Arial", 16, "bold"), fg=COLOR_TITULO,
         bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=(5, 10))
etiqueta_total = tk.Label(marco_cobro, text="$0.00", font=("Arial", 16, "bold"), fg=COLOR_TITULO, bg=COLOR_FONDO)
etiqueta_total.grid(row=2, column=1, sticky="e", pady=(5, 10))

tk.Label(marco_cobro, text="Paga con: $", font=FUENTE, bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=5)
entrada_pago = tk.Entry(marco_cobro, font=FUENTE, width=10)
entrada_pago.grid(row=3, column=1, sticky="e", pady=5)

tk.Button(marco_cobro, text="Cobrar y generar ticket", font=("Arial", 11, "bold"), bg="#f8c471",
          command=cobrar).grid(row=4, column=0, columnspan=2, sticky="we", pady=(15, 0))


marco_inventario = tk.LabelFrame(tab_inventario, text=" Productos en inventario ", font=FUENTE,
                                 bg=COLOR_FONDO, padx=10, pady=10)
marco_inventario.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

tk.Label(marco_inventario, text=f"{'Cód':>4}  {'Nombre':<20}{'Tipo':<12}{'Precio':>9}{'Exist.':>7}",
         font=FUENTE_LISTA_NEGRITA, bg=COLOR_FONDO, padx=3).grid(row=0, column=0, sticky="w")
lista_inventario = tk.Listbox(marco_inventario, font=FUENTE_LISTA, width=54, height=22, exportselection=False)
lista_inventario.grid(row=1, column=0)
barra_inventario = tk.Scrollbar(marco_inventario, command=lista_inventario.yview)
barra_inventario.grid(row=1, column=1, sticky="ns")
lista_inventario.config(yscrollcommand=barra_inventario.set)
lista_inventario.bind("<<ListboxSelect>>", seleccionar_producto)

marco_opciones_producto = tk.LabelFrame(tab_inventario, text=" Opciones ", font=FUENTE,
                                        bg=COLOR_FONDO, padx=10, pady=10)
marco_opciones_producto.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(marco_opciones_producto, text="Código:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
etiqueta_codigo_producto = tk.Label(marco_opciones_producto, text="(nuevo)", font=FUENTE, bg=COLOR_FONDO)
etiqueta_codigo_producto.grid(row=0, column=1, sticky="w", padx=5, pady=5)

tk.Label(marco_opciones_producto, text="Nombre:", font=FUENTE, bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
entrada_nombre_producto = tk.Entry(marco_opciones_producto, font=FUENTE, width=20)
entrada_nombre_producto.grid(row=1, column=1, padx=5, pady=5)

tk.Label(marco_opciones_producto, text="Tipo:", font=FUENTE, bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=5)
entrada_tipo_producto = tk.Entry(marco_opciones_producto, font=FUENTE, width=20)
entrada_tipo_producto.grid(row=2, column=1, padx=5, pady=5)

tk.Label(marco_opciones_producto, text="Precio: $", font=FUENTE, bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=5)
entrada_precio_producto = tk.Entry(marco_opciones_producto, font=FUENTE, width=20)
entrada_precio_producto.grid(row=3, column=1, padx=5, pady=5)

tk.Label(marco_opciones_producto, text="Existencia:", font=FUENTE, bg=COLOR_FONDO).grid(row=4, column=0, sticky="w", pady=5)
entrada_existencia_producto = tk.Entry(marco_opciones_producto, font=FUENTE, width=20)
entrada_existencia_producto.grid(row=4, column=1, padx=5, pady=5)

tk.Button(marco_opciones_producto, text="Agregar nuevo", font=FUENTE, bg="#82e0aa",
          command=agregar_producto).grid(row=5, column=0, columnspan=2, sticky="we", pady=(15, 3))
tk.Button(marco_opciones_producto, text="Guardar cambios", font=FUENTE, bg="#85c1e9",
          command=guardar_producto).grid(row=6, column=0, columnspan=2, sticky="we", pady=3)
tk.Button(marco_opciones_producto, text="Eliminar", font=FUENTE, bg="#f1948a",
          command=eliminar_producto).grid(row=7, column=0, columnspan=2, sticky="we", pady=3)
tk.Button(marco_opciones_producto, text="Limpiar campos", font=FUENTE,
          command=limpiar_campos_producto).grid(row=8, column=0, columnspan=2, sticky="we", pady=3)
tk.Label(marco_opciones_producto, text="Selecciona un producto de la lista\npara editarlo o eliminarlo.",
         font=FUENTE_CHICA, fg=COLOR_GRIS, bg=COLOR_FONDO).grid(row=9, column=0, columnspan=2, pady=(10, 0))


marco_clientes = tk.LabelFrame(tab_clientes, text=" Clientes registrados ", font=FUENTE,
                               bg=COLOR_FONDO, padx=10, pady=10)
marco_clientes.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

tk.Label(marco_clientes, text=f"{'ID':>4}  {'Nombre':<19}{'Teléfono':<11}{'Correo'}",
         font=FUENTE_LISTA_NEGRITA, bg=COLOR_FONDO, padx=3).grid(row=0, column=0, sticky="w")
lista_clientes = tk.Listbox(marco_clientes, font=FUENTE_LISTA, width=54, height=22, exportselection=False)
lista_clientes.grid(row=1, column=0)
barra_clientes = tk.Scrollbar(marco_clientes, command=lista_clientes.yview)
barra_clientes.grid(row=1, column=1, sticky="ns")
lista_clientes.config(yscrollcommand=barra_clientes.set)
lista_clientes.bind("<<ListboxSelect>>", seleccionar_cliente)

marco_opciones_cliente = tk.LabelFrame(tab_clientes, text=" Opciones ", font=FUENTE,
                                       bg=COLOR_FONDO, padx=10, pady=10)
marco_opciones_cliente.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(marco_opciones_cliente, text="ID:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
etiqueta_id_cliente = tk.Label(marco_opciones_cliente, text="(nuevo)", font=FUENTE, bg=COLOR_FONDO)
etiqueta_id_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=5)

tk.Label(marco_opciones_cliente, text="Nombre:", font=FUENTE, bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
entrada_nombre_cliente = tk.Entry(marco_opciones_cliente, font=FUENTE, width=20)
entrada_nombre_cliente.grid(row=1, column=1, padx=5, pady=5)

tk.Label(marco_opciones_cliente, text="Teléfono:", font=FUENTE, bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=5)
entrada_telefono_cliente = tk.Entry(marco_opciones_cliente, font=FUENTE, width=20)
entrada_telefono_cliente.grid(row=2, column=1, padx=5, pady=5)

tk.Label(marco_opciones_cliente, text="Correo:", font=FUENTE, bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=5)
entrada_correo_cliente = tk.Entry(marco_opciones_cliente, font=FUENTE, width=20)
entrada_correo_cliente.grid(row=3, column=1, padx=5, pady=5)

tk.Button(marco_opciones_cliente, text="Agregar nuevo", font=FUENTE, bg="#82e0aa",
          command=agregar_cliente).grid(row=4, column=0, columnspan=2, sticky="we", pady=(15, 3))
tk.Button(marco_opciones_cliente, text="Guardar cambios", font=FUENTE, bg="#85c1e9",
          command=guardar_cliente).grid(row=5, column=0, columnspan=2, sticky="we", pady=3)
boton_eliminar_cliente = tk.Button(marco_opciones_cliente, text="Eliminar", font=FUENTE, bg="#f1948a",
                                   command=eliminar_cliente)
boton_eliminar_cliente.grid(row=6, column=0, columnspan=2, sticky="we", pady=3)
tk.Button(marco_opciones_cliente, text="Limpiar campos", font=FUENTE,
          command=limpiar_campos_cliente).grid(row=7, column=0, columnspan=2, sticky="we", pady=3)
tk.Label(marco_opciones_cliente, text="Selecciona un cliente de la lista\npara editarlo o eliminarlo.",
         font=FUENTE_CHICA, fg=COLOR_GRIS, bg=COLOR_FONDO).grid(row=8, column=0, columnspan=2, pady=(10, 0))


marco_historial = tk.LabelFrame(tab_historial, text=" Ventas realizadas ", font=FUENTE,
                                bg=COLOR_FONDO, padx=10, pady=10)
marco_historial.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

tk.Label(marco_historial, text=f"{'Folio':>5}  {'Fecha':<18}{'Cliente':<17}{'Total':>12}",
         font=FUENTE_LISTA_NEGRITA, bg=COLOR_FONDO, padx=3).grid(row=0, column=0, sticky="w")
lista_historial = tk.Listbox(marco_historial, font=FUENTE_LISTA, width=54, height=22, exportselection=False)
lista_historial.grid(row=1, column=0)
barra_historial = tk.Scrollbar(marco_historial, command=lista_historial.yview)
barra_historial.grid(row=1, column=1, sticky="ns")
lista_historial.config(yscrollcommand=barra_historial.set)

marco_resumen = tk.LabelFrame(tab_historial, text=" Resumen ", font=FUENTE,
                              bg=COLOR_FONDO, padx=10, pady=10)
marco_resumen.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(marco_resumen, text="Ventas realizadas:", font=FUENTE, bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
etiqueta_num_ventas = tk.Label(marco_resumen, text="0", font=FUENTE, bg=COLOR_FONDO)
etiqueta_num_ventas.grid(row=0, column=1, sticky="e", padx=5, pady=5)

tk.Label(marco_resumen, text="Total vendido:", font=FUENTE, bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
etiqueta_total_vendido = tk.Label(marco_resumen, text="$0.00", font=("Arial", 11, "bold"), bg=COLOR_FONDO)
etiqueta_total_vendido.grid(row=1, column=1, sticky="e", padx=5, pady=5)

tk.Button(marco_resumen, text="Ver ticket", font=FUENTE, bg="#85c1e9",
          command=ver_ticket).grid(row=2, column=0, columnspan=2, sticky="we", pady=(15, 0))
tk.Label(marco_resumen, text="Selecciona una venta para\nver su ticket.",
         font=FUENTE_CHICA, fg=COLOR_GRIS, bg=COLOR_FONDO).grid(row=3, column=0, columnspan=2, pady=(10, 0))

mostrar_catalogo()
mostrar_inventario()
mostrar_clientes()
mostrar_historial()
mostrar_carrito()

entrada_usuario.focus()
ventana.mainloop()
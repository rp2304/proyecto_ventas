#conectar a la base de datos
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistema_ventas"
)


# Clase Producto para representar los productos en el inventario
class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = 0

# Clase Venta para representar una venta
class Venta:
    def __init__(self, id_venta, vendedor):
        self.id_venta = id_venta
        self.vendedor = vendedor
        self.productos = []
        self.fecha_venta = None
        self.run = None
        self.tipo_documento = None


    def agregar_producto(self, producto, cantidad):
        self.productos.append((producto, cantidad))

    def calcular_total(self):
        total = 0
        for producto, cantidad in self.productos:
            total += producto.precio * cantidad
        return total

# Clase Cliente para representar la información del cliente en la factura
class Cliente:
    def __init__(self, razon_social, rut, giro, direccion, nombres, apellidos, telefono):
        self.razon_social = razon_social
        self.rut = rut
        self.giro = giro
        self.direccion = direccion
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono

# Clase empleado para representar la información del empleado
class Empleado:
    def __init__(self, nombres, apellidos, cargo, contrasena):
        self.nombres = nombres
        self.apellidos = apellidos
        self.cargo = cargo
        self.contrasena = contrasena

# Clase detalle_venta para representar el detalle de la venta
class DetalleVenta:
    def __init__(self,id_detalle_venta, id_venta, id_producto, cantidad, precio_total):
        self.id_detalle_venta = id_detalle_venta
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_total = precio_total

# Función para generar una factura
def generar_factura(venta, cliente):
    total_neto = venta.calcular_total()
    iva = total_neto * 0.19
    total_final = total_neto + iva
    print("Factura:")
    print("Razón social:", cliente.razon_social)
    print("RUT:", cliente.rut)
    print("Giro:", cliente.giro)
    print("Dirección:", cliente.direccion)
    print("Detalle de productos:")
    for producto, cantidad in venta.productos:
        print(f"- {producto.nombre}: {cantidad} x ${producto.precio}")
    print(f"Total neto: ${total_neto}")
    print(f"IVA (19%): ${iva}")
    print(f"Total final: ${total_final}")

# Función para generar boleta
def generar_boleta(venta):
    total_neto = venta.calcular_total()
    iva = total_neto * 0.19
    total_final = total_neto + iva
    print("Boleta:")
    print("Detalle de productos:")
    for producto, cantidad in venta.productos:
        print(f"- {cantidad} x {producto.nombre}: ${producto.precio * cantidad}")
    print(f"Total a pagar: ${total_final}")

# Función para ingresar datos de empleado
def ingresar_empleado():
    try:
        nombres = input("Ingrese los nombres del empleado: ")
        apellidos = input("Ingrese los apellidos del empleado: ")
        cargo = input("Ingrese el cargo del empleado: ")
        contrasena = input("Ingrese la contraseña del empleado: ")
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos: {}".format(error))
    return Empleado(nombres, apellidos, cargo, contrasena)

# Función para ingresar datos de producto
def ingresar_producto():
    try:
        codigo = input("Ingrese el código del producto: ")
        nombre = input("Ingrese el nombre del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        stock = input("Ingrese el stock del producto: ")

        mycursor = mydb.cursor()

        mycursor = mydb.cursor()
        consulta="insert into producto  values ({},'{}',{},'{}')".format(codigo,nombre,precio,stock) 
        mycursor.execute(consulta)
        mydb.commit() 
        print("Producto insertado correctamente")
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos: {}".format(error))
    return Producto(codigo, nombre, precio)

# Función para ingresar datos de detalle de venta
def ingresar_detalle_venta():
    try:
        id_detalle_venta = input("Ingrese el id del detalle de venta: ")
        id_venta = input("Ingrese el id de la venta: ")
        id_producto = input("Ingrese el id del producto: ")
        cantidad = float(input("Ingrese la cantidad: "))  # Convertir a float
        precio_total = float(input("Ingrese el precio total: "))  # Convertir a float
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos: {}".format(error))
    return DetalleVenta(id_detalle_venta, id_venta, id_producto, cantidad, precio_total)

# Función para ingresar datos de cliente
def ingresar_cliente():
    try:
        razon_social = input("Ingrese la razón social del cliente: ")
        rut = input("Ingrese el RUT del cliente: ")
        giro = input("Ingrese el giro del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")
        nombres = input("Ingrese los nombres del cliente: ")
        apellidos = input("Ingrese los apellidos del cliente: ")
        telefono = input("Ingrese el teléfono del cliente: ")
    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos: {}".format(error))
    return Cliente(razon_social, rut, giro, direccion, nombres, apellidos, telefono)

# Función principal
def main():
    productos = []
    ventas = []
    opcion = ""
    while opcion != "5":
        print("\nBienvenido al sistema de ventas")
        print("1. Agregar producto")
        print("2. Realizar venta")
        print("3. Generar factura")
        print("4. Generar boleta")
        print("5. Salir")
        opcion = input("Ingrese la opción deseada: ")
        if opcion == "1":
            producto = ingresar_producto()
            productos.append(producto)
            print("Producto agregado correctamente.")
        elif opcion == "2":
            if not productos:
                print("No hay productos disponibles. Agregue productos primero.")
                continue
            print("Productos disponibles:")
            for i, producto in enumerate(productos, 1):
                print(f"{i}. {producto.nombre} - ${producto.precio}")
            seleccion = int(input("Seleccione el número del producto a vender: "))
            cantidad = int(input("Ingrese la cantidad a vender: "))
            venta = Venta(len(ventas) + 1, "Vendedor1")  # Considera implementar un sistema para asignar el vendedor automáticamente
            venta.agregar_producto(productos[seleccion - 1], cantidad)
            ventas.append(venta)
            print("Venta realizada correctamente.")
        elif opcion == "3":
            if not ventas:
                print("No hay ventas registradas.")
                continue
            cliente = ingresar_cliente()
            venta = ventas[-1]  # Suponemos que se genera factura para la última venta registrada
            generar_factura(venta, cliente)
        elif opcion == "4":
            if not ventas:
                print("No hay ventas registradas.")
                continue
            venta = ventas[-1]  # Suponemos que se genera boleta para la última venta registrada
            generar_boleta(venta)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción")
main()

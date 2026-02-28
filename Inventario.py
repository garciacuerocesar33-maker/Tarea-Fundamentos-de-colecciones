"""
Sistema de Gestión de Inventario
Curso: Programación Orientada a Objetos - Segundo Semestre
"""

import json
import os


# ==================== CLASE PRODUCTO ====================

class Producto:
    """Clase que representa un producto del inventario."""

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.cantidad = cantidad
        else:
            print("Error: La cantidad no puede ser negativa")

    def set_precio(self, precio):
        if precio >= 0:
            self.precio = precio
        else:
            print("Error: El precio no puede ser negativo")

    def __str__(self):
        return f"ID: {self.id} | {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# ==================== CLASE INVENTARIO ====================

class Inventario:
    """
    Clase que gestiona el inventario de la tienda.

    Uso de colecciones:
    - Diccionario (dict): Almacena productos con ID como clave
      - Búsqueda por ID: O(1) - muy rápido
    """

    def __init__(self):
        # Diccionario público: {id_producto: objeto_producto}
        self.productos = {}

    # ==================== OPERACIONES BÁSICAS ====================

    def agregar_producto(self, producto):
        """Añade un producto al inventario."""
        id_producto = producto.get_id()

        if id_producto in self.productos:
            print(f"Error: Ya existe un producto con ID {id_producto}")
            return False

        self.productos[id_producto] = producto
        print(f"Producto '{producto.get_nombre()}' añadido correctamente")
        return True

    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID."""
        if id_producto in self.productos:
            nombre = self.productos[id_producto].get_nombre()
            del self.productos[id_producto]
            print(f"Producto '{nombre}' eliminado")
            return True
        else:
            print(f"Error: No existe producto con ID {id_producto}")
            return False

    def actualizar_cantidad(self, id_producto, cantidad):
        """Actualiza la cantidad de un producto."""
        if id_producto in self.productos:
            self.productos[id_producto].set_cantidad(cantidad)
            print("Cantidad actualizada")
            return True
        print("Error: Producto no encontrado")
        return False

    def actualizar_precio(self, id_producto, precio):
        """Actualiza el precio de un producto."""
        if id_producto in self.productos:
            self.productos[id_producto].set_precio(precio)
            print("Precio actualizado")
            return True
        print("Error: Producto no encontrado")
        return False

    # ==================== BÚSQUEDAS ====================

    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (búsqueda parcial)."""
        resultados = []
        nombre = nombre.lower()

        for producto in self.productos.values():
            if nombre in producto.get_nombre().lower():
                resultados.append(producto)

        return resultados

    def buscar_por_id(self, id_producto):
        """Busca un producto por su ID."""
        return self.productos.get(id_producto)

    def mostrar_todos(self):
        """Muestra todos los productos."""
        if not self.productos:
            print("\nEl inventario está vacío")
            return

        print("\n" + "=" * 60)
        print("             INVENTARIO COMPLETO")
        print("=" * 60)

        for producto in self.productos.values():
            print(producto)

        print("=" * 60)
        print(f"Total de productos: {len(self.productos)}")
        print("=" * 60)

    # ==================== ARCHIVOS ====================

    def to_dict(self):
        """Convierte el inventario a diccionario para guardar en archivo."""
        productos_lista = []

        for producto in self.productos.values():
            productos_lista.append({
                "id_producto": producto.get_id(),
                "nombre": producto.get_nombre(),
                "cantidad": producto.get_cantidad(),
                "precio": producto.get_precio()
            })

        return {"productos": productos_lista}

    def cargar_desde_dict(self, datos):
        """Carga el inventario desde un diccionario."""
        self.productos.clear()

        if "productos" not in datos:
            return

        for prod_dict in datos["productos"]:
            producto = Producto(
                prod_dict["id_producto"],
                prod_dict["nombre"],
                prod_dict["cantidad"],
                prod_dict["precio"]
            )
            self.productos[producto.get_id()] = producto


# ==================== FUNCIONES DE ARCHIVOS ====================

def guardar_inventario(inventario, nombre_archivo="inventario.json"):
    """Guarda el inventario en un archivo JSON."""
    try:
        datos = inventario.to_dict()

        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        print(f"Inventario guardado en '{nombre_archivo}'")
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False


def cargar_inventario(nombre_archivo="inventario.json"):
    """Carga el inventario desde un archivo JSON."""
    inventario = Inventario()

    if not os.path.exists(nombre_archivo):
        print(f"No existe '{nombre_archivo}'. Se creará uno nuevo.")
        return inventario

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        inventario.cargar_desde_dict(datos)
        print(f"Inventario cargado. {len(inventario.productos)} productos.")
    except Exception as e:
        print(f"Error al cargar: {e}")

    return inventario


# ==================== MENÚ PRINCIPAL ====================

def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 50)
    print("     GESTIÓN DE INVENTARIO - TIENDA")
    print("=" * 50)
    print("1. Agregar producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar cantidad")
    print("4. Actualizar precio")
    print("5. Buscar por nombre")
    print("6. Buscar por ID")
    print("7. Mostrar todos los productos")
    print("8. Guardar en archivo")
    print("9. Cargar desde archivo")
    print("0. Salir")
    print("=" * 50)


def obtener_siguiente_id(inventario):
    """Calcula el siguiente ID disponible."""
    if not inventario.productos:
        return 1
    return max(inventario.productos.keys()) + 1


def main():
    """Función principal del programa."""
    inventario = cargar_inventario()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- AGREGAR PRODUCTO ---")
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))

            nuevo_id = obtener_siguiente_id(inventario)
            producto = Producto(nuevo_id, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == "2":
            id_producto = int(input("\nID del producto a eliminar: "))
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = int(input("\nID del producto: "))
            cantidad = int(input("Nueva cantidad: "))
            inventario.actualizar_cantidad(id_producto, cantidad)

        elif opcion == "4":
            id_producto = int(input("\nID del producto: "))
            precio = float(input("Nuevo precio: "))
            inventario.actualizar_precio(id_producto, precio)

        elif opcion == "5":
            nombre = input("\nNombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)

            if resultados:
                print(f"\nSe encontraron {len(resultados)} productos:")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos")

        elif opcion == "6":
            id_producto = int(input("\nID a buscar: "))
            producto = inventario.buscar_por_id(id_producto)

            if producto:
                print(f"\nProducto encontrado:\n{producto}")
            else:
                print("Producto no encontrado")

        elif opcion == "7":
            inventario.mostrar_todos()

        elif opcion == "8":
            guardar_inventario(inventario)

        elif opcion == "9":
            inventario = cargar_inventario()

        elif opcion == "0":
            print("\n¡Gracias por usar el sistema!")
            guardar_inventario(inventario)
            break

        else:
            print("Opción inválida")


# Ejecutar el programa
if __name__ == "__main__":
    main()
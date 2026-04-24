from sqlalchemy.orm import Session
from models import engine, Producto, Productor, Repartidor, Comprador
from datetime import date
from models import *
import os

def reset_db():
    os.system("alembic upgrade head")
    seed_data()

def seed_data():
    with Session(engine) as session:
        if session.query(Producto).first():
            print("La BD ya tiene datos")
            return

        print("Poblando base de datos...")

        # -------------------------
        # PRODUCTORES
        # -------------------------
        productores_nombres = [
            "AgroMex", "Campo Verde", "Distribuidora León",
            "Frutas del Bajío", "Granja San Miguel"
        ]

        productores = []
        for nombre in productores_nombres:
            p = crear_productor(nombre)
            productores.append(p)

        # -------------------------
        # PRODUCTOS
        # -------------------------
        productos_data = [
            ("Manzana", "Fruta", "Manzana roja fresca"),
            ("Plátano", "Fruta", "Plátano orgánico"),
            ("Zanahoria", "Verdura", "Zanahoria grande"),
            ("Lechuga", "Verdura", "Lechuga romana"),
            ("Tomate", "Verdura", "Tomate saladet"),
            ("Naranja", "Fruta", "Naranja dulce"),
        ]

        productos = []
        for nombre, categoria, descripcion in productos_data:
            prod = crear_producto(
                nombre=nombre,
                categoria=categoria,
                descripcion=descripcion,
                cantidad=0  # inicia en 0, se llena con entradas
            )
            productos.append(prod)

        # -------------------------
        # REPARTIDORES
        # -------------------------
        repartidores_nombres = [
            "Pedro", "Luis", "Andrea", "Sofía", "Miguel"
        ]

        repartidores = []
        for nombre in repartidores_nombres:
            r = crear_repartidor(nombre, disponible=True)
            repartidores.append(r)

        # -------------------------
        # COMPRADORES
        # -------------------------
        compradores_nombres = [
            "Juan Pérez", "María López", "Carlos Ramírez",
            "Ana Torres", "Luis Fernández"
        ]

        compradores = []
        for nombre in compradores_nombres:
            c = crear_comprador(nombre)
            compradores.append(c)

        # -------------------------
        # GENERAR ENTRADAS (stock inicial)
        # -------------------------
        for _ in range(15):
            producto = random.choice(productos)
            productor = random.choice(productores)

            cantidad = random.randint(5, 25)
            precio_compra = round(random.uniform(10, 50), 2)
            precio_venta = round(precio_compra * random.uniform(1.2, 1.6), 2)

            crear_entrada(
                id_producto=producto.id_producto,
                id_productor=productor.id_productor,
                cantidad=cantidad,
                fecha=date.today(),
                precio_compra=precio_compra,
                precio_venta=precio_venta
            )

        print("Base de datos poblada correctamente")

if __name__ == "__main__":
    reset_db()
    #seed_data()
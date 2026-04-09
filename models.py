from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import create_engine,String, Integer, Boolean, ForeignKey, Date, Float, event
import random
from datetime import date

import os

#Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Build the absolute path to your database
db_path = os.path.join(BASE_DIR, "requests.db")

#The connection string format is 'dialect+driver://user:password@host/database'
engine = create_engine(f"sqlite:///{db_path}")


# activate foreign keys to validate fields
@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor=dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Base(DeclarativeBase):
    @classmethod
    def attributes(self): #method defined to show attributes
        return [c.key for c in self.__table__.columns]

Base.metadata.create_all(engine)

class Producto(Base):
    __tablename__ ="productos"
    
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    categoria: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[str] = mapped_column(String(150))
    cantidad: Mapped[int] = mapped_column(Integer)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __str__(self):
        return f"Producto(id_producto={self.id_producto}, \
        nombre='{self.nombre}',categoria='{self.categoria}',\
        descripcion='{self.descripcion}',cantidad={self.cantidad}')"

    #used to recreate the object and for debugging purposes
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Producto):
            return False
        return self.id_producto == other.id_producto
    
class Productor(Base):
    __tablename__ = "productores"
    
    id_productor: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __str__(self):
        return f"Productor(id_productor={self.id_productor}, nombre='{self.nombre}')"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class Entrada(Base):
    __tablename__ = "entradas"
    
    id_entrada: Mapped[int] = mapped_column(primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto",ondelete="CASCADE"))
    id_productor: Mapped[int] = mapped_column(ForeignKey("productores.id_productor",ondelete="CASCADE"))  
    cantidad: Mapped[int] = mapped_column(Integer)
    fecha: Mapped[date] = mapped_column(Date)
    precio_compra: Mapped[float] = mapped_column(Float)
    precio_venta: Mapped[float] = mapped_column(Float)

    producto = relationship("Producto")
    productor = relationship("Productor")

    def __str__(self):
        return f"Entrada(id_entrada={self.id_entrada},id_producto='{self.id_producto}',\
        id_productor={self.id_productor},cantidad={self.cantidad},fecha={self.fecha},\
        precio_compra={self.precio_compra},precio_venta={self.precio_venta})"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class Comprador(Base):
    __tablename__ = "compradores"
    
    id_comprador: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))

    def __str__(self):
        return f"Comprador(id_comprador={self.id_comprador}, nombre='{self.nombre}')"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class Repartidor(Base):
    __tablename__ = "repartidores"
    
    id_repartidor: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    disponible: Mapped[bool] = mapped_column(Boolean)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __str__(self):
        return f"Repartidor(id_repartidor={self.id_repartidor}, nombre='{self.nombre}',disponible={self.disponible})"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class Entrega(Base):
    __tablename__ = "entregas"
    
    id_entrega: Mapped[int] = mapped_column(primary_key=True)
    
    id_comprador: Mapped[int] = mapped_column(ForeignKey("compradores.id_comprador",ondelete="CASCADE"))
    id_repartidor: Mapped[int | None] = mapped_column(ForeignKey("repartidores.id_repartidor",ondelete="SET NULL"),nullable=True)
    
    fecha: Mapped[date] = mapped_column(Date)
    entregado: Mapped[bool] = mapped_column(Boolean)

    comprador = relationship("Comprador")
    repartidor = relationship("Repartidor")
    detalles = relationship("DetalleEntrega", back_populates="entrega") 
    #arguemnt back_populates points at the attribute from the related class

    def __str__(self):
        return f"Entrega(id_entrega={self.id_entrega},id_comprador={self.id_comprador},\
        id_repartidor={self.id_repartidor},fecha={self.fecha},entregado?{self.entregado})"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class DetalleEntrega(Base):
    __tablename__ = "detalle_entrega"
    
    id_detalle_entrega: Mapped[int] = mapped_column(primary_key=True)
    
    id_entrega: Mapped[int] = mapped_column(ForeignKey("entregas.id_entrega", ondelete="CASCADE"))
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"))
    cantidad: Mapped[int] = mapped_column(Integer)

    producto = relationship("Producto")  
    entrega = relationship("Entrega", back_populates="detalles")
 
    def __str__(self):
        return f"DetalleEntrega(id={self.id_detalle_entrega}, id_entrega='{self.id_entrega}',\
        id_producto={self.id_producto},cantidad={self.cantidad})"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()


#Functions

def crear_comprador(nombre: str):
    #use ,expire_on_commit=False to keep the attibutes after the session closes
    with Session(engine,expire_on_commit=False) as session:
        nuevo = Comprador(nombre=nombre)
        session.add(nuevo)
        session.commit()
        return nuevo
    
def crear_productor(nombre:str):
    with Session(engine,expire_on_commit=False) as session:
        nuevo=Productor(nombre=nombre)
        session.add(nuevo)
        session.commit()
        return nuevo
    
def crear_repartidor(nombre:str,disponible:bool=True):
    with Session(engine,expire_on_commit=False) as session:
        nuevo=Repartidor(nombre=nombre,disponible=disponible)
        session.add(nuevo)
        session.commit()
        return nuevo

def crear_producto(nombre:str,categoria:str,descripcion:str,cantidad:int=0):
    with Session(engine,expire_on_commit=False) as session:
        nuevo=Producto(nombre=nombre,categoria=categoria,descripcion=descripcion,cantidad= cantidad)
        session.add(nuevo)
        session.commit()
        return nuevo

def crear_entrada(id_producto,id_productor,cantidad,fecha, precio_compra,precio_venta):
    with Session(engine,expire_on_commit=False) as session:
        producto=session.get(Producto,id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")
        nuevo=Entrada(id_producto=id_producto,id_productor=id_productor,cantidad=cantidad,fecha=fecha,precio_compra=precio_compra,precio_venta=precio_venta)
        session.add(nuevo)

        producto.cantidad += cantidad 

        session.commit()
        return nuevo  

def crear_entrega(id_comprador:int,fecha,detalle:dict[int:int],entregado:bool=False):
    with Session(engine,expire_on_commit=False) as session:
        nuevo=Entrega(id_comprador=id_comprador,fecha=fecha,entregado=entregado)
        session.add(nuevo)
        session.flush() #send data to the db to execute queries before commiting it
        id_entrega=nuevo.id_entrega
        try:
            for id_producto,cantidad in detalle.items():
                prod=session.get(Producto, id_producto)

                if not prod:
                    raise ValueError("Producto no encontrado")
                
                if prod.cantidad<cantidad:
                    raise ValueError("Stock insuficiente")
                
                detalle_entrada=DetalleEntrega(id_entrega=id_entrega,id_producto=id_producto,cantidad=cantidad)
                session.add(detalle_entrada)
                #actualizar_producto(nuevo.id_entrada,k,v) 
        
                prod.cantidad-=cantidad

        except Exception as e:
            session.rollback() #to revvert changes 
            print(f"Error: {e}")
            return False
        session.commit()
        return nuevo

def asignar_repartidor(id_entrega:int,id_repartidor:int):
    with Session(engine,expire_on_commit=False) as session:
        entrega=session.get(Entrega,id_entrega)
        if not entrega:
            raise ValueError("Entrega no encontrada")
        repartidor=session.get(Repartidor,id_repartidor)
        if not repartidor.disponible:
            raise Exception("Repartidor no disponible")
        repartidor.disponible=False
        
        entrega.id_repartidor=id_repartidor
        session.commit()

def actualizar_entrega(id_entrega:int):
    with Session(engine,expire_on_commit=False) as session:
        entrega:Entrega=session.get(Entrega,id_entrega)
        if not entrega:
            return

        if entrega.id_repartidor and not entrega.entregado:
            repartidor:Repartidor=session.get(Repartidor, entrega.id_repartidor)
            if repartidor:
                repartidor.disponible=True
                entrega.entregado=True
                session.commit()

def buscar(model:type[Base],id:int):
    with Session(engine,expire_on_commit=False) as session:
        return session.get(model,id)
    
# use type[Base] to specify you want the Class, not an instance of the class
def listar(model:type[Base],filter=None,value=None):
    with Session(engine,expire_on_commit=False) as session:
        query=session.query(model)
        if filter:
            if not hasattr(model, filter):
                raise ValueError(f"{filter} no es un atributo válido de {model}")
            attribute=getattr(model, filter) #get attribute from class
            query=query.filter(attribute==value)
        return query.all()

def get_page(elements,page:int=1,per_page:int=10):
    total=len(elements)
    total_pages=(total+per_page-1)//per_page
    if 1>page>total_pages:
        print("pagina no valida")
        page=1
    if per_page<1:
        print("no de elementos por pagina no validos")
        page=20
    start=(page-1)*per_page
    end=start+per_page
    return {"data":elements[start:end],"page":page,"per_page":per_page,"total":total,"total_pages":total_pages}

def modify(model:type[Base],id:int,attr:str,value:any):
    with Session(engine,expire_on_commit=False) as session:
        obj=session.get(model, id)
        if not obj:
            raise ValueError(f"{model.__name__} con id {id} no existe")
        if not hasattr(obj, attr):
            raise ValueError(f"{model.__name__} no tiene el atributo {attr}")
        column_type = type(getattr(obj, attr))
        if not isinstance(value, column_type) and value is not None:
            raise TypeError(f"Tipo inválido para {attr}")
        try:
            setattr(obj, attr, value)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

def soft_delete(model:type[Base],id:int):#Compradores,REpartidores, Productores
    with Session(engine, expire_on_commit=False) as session:
        obj=session.get(model, id)
        if not obj:
            raise ValueError(f"{model.__name__} con id {id} no existe")
        if not hasattr(obj, "activo"):
            raise ValueError(f"{model.__name__} no soporta soft delete")
        obj.activo=False
        session.commit()
        return obj
    
def delete(model: type[Base],id:int):
    with Session(engine, expire_on_commit=False) as session:
        obj=session.get(model, id)
        if not obj:
            raise ValueError(f"{model.__name__} con id {id} no existe")
        session.delete(obj)
        session.commit()
        return obj

"""
def actualizar_producto(id_producto: int, cantidad: int, movimiento: str):
    with Session(engine) as session:
        try:
            prod = session.get(Producto, id_producto)
            if not prod:
                raise ValueError("Producto no encontrado")
            if movimiento == "entrada":
                prod.cantidad += cantidad
            elif movimiento == "salida":
                if prod.cantidad < cantidad:
                    raise ValueError("Stock insuficiente")
                prod.cantidad -= cantidad
            else:
                raise ValueError("Movimiento inválido")
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False
"""

if __name__=="__main__":
    #use alembic for migrations 
    
    #initialize migrations
    #alembic init alembic
    
    #save current state of db   
    #alembic stamp head

    #create a migration
    #alembic revision --autogenerate -m "nombre_de_la_migracion"

    #update database
    #alembic upgrade head


    Base.metadata.drop_all(engine)  # drop existing tables to recreate with correct schema
    Base.metadata.create_all(engine) #create tables

    def poblar_bd():

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

        print("Base de datos poblada correctamente ✅")

    poblar_bd()
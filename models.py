from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import create_engine,String, Integer, Boolean, ForeignKey, Date, Float, event
import random
from datetime import date

# The connection string format is 'dialect+driver://user:password@host/database'
engine=create_engine("sqlite:///requests.db")

# activate foreign keys to validate fields
@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor=dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Base(DeclarativeBase):
    pass
class Producto(Base):
    __tablename__ ="productos"
    
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    categoria: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[str] = mapped_column(String(150))
    cantidad: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return f"Producto(id_producto={self.id_producto}, \
        nombre='{self.nombre},categoria='{self.categoria}',\
        descripcion='{self.descripcion}',cantidad={self.cantidad}')"

    #used to recreate the object and for debugging purposes
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, value):
        return self.id_producto==value.id_producto

class Productor(Base):
    __tablename__ = "productores"
    
    id_productor: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))

    def __str__(self):
        return f"Productor(id_productor={self.id_productor}, nombre='{self.nombre}')"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()


class Entrada(Base):
    __tablename__ = "entradas"
    
    id_entrada: Mapped[int] = mapped_column(primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto"))
    id_productor: Mapped[int] = mapped_column(ForeignKey("productores.id_productor"))  
    cantidad: Mapped[int] = mapped_column(Integer)
    fecha: Mapped[str] = mapped_column(Date)
    precio_compra: Mapped[float] = mapped_column(Float)
    precio_venta: Mapped[float] = mapped_column(Float)

    producto = relationship("Producto")
    productor = relationship("Productor")

    def __str__(self):
        return f"Entrada(id_entrada={self.id_entrada},id_producto='{self.id_producto}',\
        id_productor={self.id_productor},cantidad={self.cantidad},fecha={self.fecha},\
        precio_compra={self.precio_compra},precio_venta={self.precio_compra})"

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

    def __str__(self):
        return f"Repartidor(id_repartidor={self.id_repartidor}, nombre='{self.nombre}',disponible={self.disponible})"

    #used to recreate the object 
    def __repr__(self):
        return self.__str__()

class Entrega(Base):
    __tablename__ = "entregas"
    
    id_entrega: Mapped[int] = mapped_column(primary_key=True)
    
    id_comprador: Mapped[int] = mapped_column(ForeignKey("compradores.id_comprador"))
    id_repartidor: Mapped[int] = mapped_column(ForeignKey("repartidores.id_repartidor"))
    
    fecha: Mapped[str] = mapped_column(String(20))
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
    
    id_entrega: Mapped[int] = mapped_column(ForeignKey("entregas.id_entrega"))
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto"))
    cantidad: Mapped[int] = mapped_column(Integer)

    producto = relationship("Producto")  
    entrega = relationship("Entrega", back_populates="detalles")
 
    def __str__(self):
        return f"Productor(id={self.id_detalle_entrega}, id_entrega='{self.id_entrega}',\
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
        nuevo=Entrada(id_producto=id_producto,id_productor=id_productor,cantidad=cantidad,fecha=fecha,precio_compra=precio_compra,precio_venta=precio_venta)
        session.add(nuevo)

        producto.cantidad += cantidad 

        session.commit()
        return nuevo  

def crear_entrega(id_comprador:int,id_repartidor:int,fecha,detalle:dict[int:int],entregado:bool=False):
    with Session(engine,expire_on_commit=False) as session:
        repartidor=session.get(Repartidor,id_repartidor)
        if not repartidor.disponible:
            raise Exception("Repartidor no disponible")
        nuevo=Entrega(id_comprador=id_comprador,id_repartidor=id_repartidor,fecha=fecha,entregado=entregado)
        session.add(nuevo)
        session.flush() #send data to the db to execute queries before commiting it
        id_entrega=nuevo.id_entrega
        try:
            for id_producto,cantidad in detalle.items():
                detalle_entrada=DetalleEntrega(id_entrega=id_entrega,id_producto=id_producto,cantidad=cantidad)
                session.add(detalle_entrada)
                #actualizar_producto(nuevo.id_entrada,k,v) 
                
                prod=session.get(Producto, id_producto)
                if not prod:
                    raise ValueError("Producto no encontrado")
                
                if prod.cantidad<cantidad:
                    raise ValueError("Stock insuficiente")
                prod.cantidad-=cantidad

        except Exception as e:
            session.rollback() #to revvert changes 
            print(f"Error: {e}")
            return False
        repartidor.disponible=False
        session.commit()
        return nuevo
    
def actualizar_entrega(id_entrega:int):
    with Session(engine,expire_on_commit=False) as session:
        entrega:Entrega=session.get(Entrega,id_entrega)
        repartidor:Repartidor=session.get(Repartidor,entrega.id_repartidor)
        if entrega:
            entrega.entregado=True
            repartidor.disponible=True
            session.commit()

def buscar(model:type[Base],id:int):
    with Session(engine,expire_on_commit=False) as session:
        return session.get(model,id)
    
# use type[Base] to specify you want the Class, not an instance of the class
def listar(model:type[Base],filter=None,value=None):
    with Session(engine,expire_on_commit=False) as session:
        query=session.query(model)
        if filter:
            attribute=getattr(model, filter) #get attribute from class
            query=query.filter(attribute==value)
        return query.all()


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
    Base.metadata.create_all(engine) #create tables

    def poblar_bd():
        try:
            productores = [crear_productor(f"Productor {i+1}") for i in range(10)]
            productos = [
                crear_producto(
                    nombre=f"Producto {i+1}",
                    categoria=random.choice(["Electrónica", "Ropa", "Alimentos"]),
                    descripcion=f"Descripción del producto {i+1}",
                    cantidad=0
                )
                for i in range(20)
            ]
            compradores = [crear_comprador(f"Comprador {i+1}") for i in range(10)]
            repartidores = [crear_repartidor(f"Repartidor {i+1}", True) for i in range(5)]
            for _ in range(30):
                producto = random.choice(productos)
                productor = random.choice(productores)

                cantidad = random.randint(10, 50)

                crear_entrada(
                    id_producto=producto.id_producto,
                    id_productor=productor.id_productor,
                    cantidad=cantidad,
                    fecha=date.today(),
                    precio_compra=random.uniform(10, 50),
                    precio_venta=random.uniform(60, 100)
                )

            for _ in range(20):
                comprador = random.choice(compradores)
                repartidor = random.choice(repartidores)
                detalle = {}
                for _ in range(random.randint(1, 3)):
                    producto = random.choice(productos)
                    cantidad = random.randint(1, 5)
                    detalle[producto.id_producto] = cantidad
                try:
                    crear_entrega(
                        id_comprador=comprador.id_comprador,
                        id_repartidor=repartidor.id_repartidor,
                        fecha=str(date.today()),
                        detalle=detalle
                    )
                except Exception as ex:
                    print(ex)

            print("Base de datos poblada")

        except Exception as e:
            print(f"Error: {e}")
    
    poblar_bd()
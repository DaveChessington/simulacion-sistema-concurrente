import models as m
import random
import threading 
import time
import datetime
import queue
from views.log_view import global_logger

lock=threading.Lock()
pending_deliveries=queue.Queue()

def comprar(id=None):
    comprador=random.choice(m.listar(m.Comprador))
    
    while True:
        productos=random.choices(m.listar(m.Producto),k=random.randint(1,5))
        aprobado=True
        detalle={}
        for producto in productos:
            cantidad=random.randint(1,10)

            if producto.cantidad<cantidad:
                global_logger.create_message("warning", 
                    f"Stock insuficiente para compra {id}: {cantidad} {producto.nombre} por {comprador.nombre}")
                aprobado = False
                break 
            detalle[producto.id_producto]=cantidad  

        if aprobado and detalle:
            break   

    with lock:
        try:
            entrega=m.crear_entrega(comprador.id_comprador,datetime.date.today(),detalle=detalle)
            global_logger.create_message("success", 
                f"Compra {id} procesada - Entrega #{entrega.id_entrega} para {comprador.nombre}")
        except Exception as e:
            global_logger.create_message("error", f"Error en compra {id}: {str(e)}")
            return
    
    pending_deliveries.put(entrega)
    time.sleep(random.randint(1,5))
    global_logger.create_message("info", f"Compra {id} completada y en cola de entregas")

def entregar(id=None):
    try:
        pedido = pending_deliveries.get(timeout=5)
    except queue.Empty:
        global_logger.create_message("info", f"Entrega {id}: No hay pedidos pendientes")
        return
    
    global_logger.create_message("info", f"Entrega {id}: Procesando pedido #{pedido.id_entrega}")
    repartidor=None
    intentos = 5
    while intentos > 0 and not repartidor:
        global_logger.create_message("info", f"Entrega {id}: Buscando repartidor disponible...")
        try:
            repartidor=random.choice(m.listar(m.Repartidor,"disponible",True))
        except IndexError:
            for i in range(5,0,-1):
                global_logger.create_message("warning", f"Entrega {id}: Repartidores ocupados, esperando {i}s...")
                time.sleep(1)
            intentos -= 1
    if not repartidor:
        global_logger.create_message("error", f"Entrega {id}: No se encontró repartidor disponible, reencolando pedido")
        pending_deliveries.put(pedido)
        return
    with lock:
        m.asignar_repartidor(pedido.id_entrega,repartidor.id_repartidor)
        m.actualizar_entrega(pedido.id_entrega)
    global_logger.create_message("success", 
        f"Entrega {id}: Repartidor {repartidor.nombre} asignado a pedido #{pedido.id_entrega}")
    time.sleep(random.randint(5,10))
    global_logger.create_message("success", f"Entrega {id}: Pedido #{pedido.id_entrega} completado por {repartidor.nombre}")
        

#simulate restocking of a product by choosing random producer and random amount of prod
def restock(id=None):
    productor=random.choice(m.listar(m.Productor))
    producto=random.choice(m.listar(m.Producto))
    precio_compra=round(random.uniform(10.0,50.0),2)
    precio_venta=precio_compra*1.16
    cantidad = random.randint(10,20)
    
    global_logger.create_message("info", f"Restock {id}: Procesando entrada de {cantidad} {producto.nombre}")
    with lock:
        try:
            entrada = m.crear_entrada(producto.id_producto,productor.id_productor,cantidad,datetime.datetime.now(),precio_compra,precio_venta)
            global_logger.create_message("success", 
                f"Restock {id}: Entrada #{entrada.id_entrada} creada - {cantidad} {producto.nombre} de {productor.nombre}")
        except Exception as e:
            global_logger.create_message("error", f"Restock {id}: Error al crear entrada: {str(e)}")
            return
    
    time.sleep(random.randint(1,5))
    global_logger.create_message("info", f"Restock {id}: Proceso completado")


class Simulation:
    def __init__(self, limit=20,daemon=False):
        self.limit=limit
        self.daemon=daemon

    def start(self):
        global_logger.create_message("info", f"Iniciando simulación del sistema (límite: {self.limit})")
        i=1
        if type(self.limit)==int:
            condition=lambda: i<=self.limit
        else:
            condition=lambda: True
        while condition():
            time.sleep(random.randint(1,3))
            restocking=threading.Thread(target=restock,args=(i,),daemon=self.daemon,name=f"entrada {i}")
            purchase=threading.Thread(target=comprar,args=(i,),daemon=self.daemon,name=f"compra {i}")
            delivery=threading.Thread(target=entregar,args=(i,),daemon=self.daemon,name=f"entrega {i}")
            restocking.start()
            purchase.start()
            delivery.start()
            i+=1
        global_logger.create_message("success", f"Simulación completada - {i-1} operaciones procesadas")
        print(f"procesos pendientes: {threading.enumerate()}")

if __name__=="__main__":
    Simulation().start()
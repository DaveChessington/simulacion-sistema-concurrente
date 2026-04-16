import models as m
import random
import threading 
import time
import datetime
import queue

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
                print(f"stock insuficiente para compra {id} de {cantidad} {producto.nombre} por comprador {comprador.id_comprador}, buscando otro producto...")
                #productos.pop(producto)
                aprobado = False
                break 
            detalle[producto.id_producto]=cantidad  

        if aprobado and detalle:
            break   

    with lock:
        try:
            entrega=m.crear_entrega(comprador.id_comprador,datetime.date.today(),detalle=detalle)
            print(f"procesando compra {id} con id de entrega {entrega.id_entrega} por comprador {comprador.id_comprador}...")
        except Exception as e:
            print(f"Error al crear entrega para compra {id}: {e}")
    pending_deliveries.put(entrega)
    time.sleep(random.randint(1,5))
    print(f"compra {id} terminada")

def entregar(id=None):
    try:
        pedido = pending_deliveries.get(timeout=5)
    except queue.Empty:
        print("No hay pedidos pendientes")
        return
    #pedido=random.choice(m.listar(m.Entrega,"entregado",False))  
    print(f"[Entrega {id}] Pedido recibido: {pedido.id_entrega}")
    repartidor=None
    intentos = 5
    while intentos > 0 and not repartidor:
        print(f"Buscando Repartidor disponible para entrega {id} de pedido {pedido.id_entrega}...")
        try:
            repartidor=random.choice(m.listar(m.Repartidor,"disponible",True))
        except IndexError:
            for i in range(5,0,-1):
                print(f"[Entrega {id}] Repartidores ocupados espere {i}...")
                time.sleep(1)
            intentos -= 1
    if not repartidor:
        print(f"[Entrega {id}] No se encontró repartidor, reencolando pedido")
        pending_deliveries.put(pedido)
        return
    with lock:
        m.asignar_repartidor(pedido.id_entrega,repartidor.id_repartidor)
        m.actualizar_entrega(pedido.id_entrega)
    print(f"repartidor {repartidor.id_repartidor} asginado para pedido {pedido.id_entrega}")
    time.sleep(random.randint(5,10))
    print(f"repartidor {repartidor.id_repartidor}")
        

#simulate restocking of a product by choosing random producer and random amount of prod
def restock(id=None):
    productor=random.choice(m.listar(m.Productor))
    producto=random.choice(m.listar(m.Producto))
    precio_compra=round(random.uniform(10.0,50.0),2)
    precio_venta=precio_compra*1.16
    print(f"procesando entrega {id}...")
    with lock:
        m.crear_entrada(producto.id_producto,productor.id_productor,random.randint(10,20),datetime.datetime.now(),precio_compra,precio_venta)
    time.sleep(random.randint(1,5))
    print(f"entrega {id} terminada")


class Simulation:
    def __init__(self, limit=20,daemon=False):
        self.limit=limit
        self.daemon=daemon

    def start(self):
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
        print(f"procesos pendientes: {threading.enumerate()}")

if __name__=="__main__":
    Simulation().start()
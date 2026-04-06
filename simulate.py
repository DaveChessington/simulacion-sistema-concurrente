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
    aprobado=False
    detalle={}
    while not aprobado:
        productos=random.choices(m.listar(m.Producto),k=random.randint(1,5))
        for producto in productos:
            cantidad=random.randint(1,10)

            if producto.cantidad<cantidad:
                print(f"stock insuficiente para compra {id} de {cantidad} {producto.nombre} por comprador {comprador.id_comprador}, buscando otro producto...")
                #productos.pop(producto)
            else:
                aprobado=True
                detalle[producto.id_producto]=cantidad  

        if not detalle:
            aprobado=False   

    with lock:
        entrega=m.crear_entrega(comprador.id_comprador,datetime.date.today(),detalle=detalle)
        print(f"procesando compra {id} con id de entrega {entrega.id_entrega} por comprador {comprador.id_comprador}...")
        pending_deliveries.put(entrega)
    time.sleep(random.randint(1,5))
    print(f"compra {id} terminada")

def entregar(id=None):
    with lock:
        pedido=pending_deliveries.get()
    #pedido=random.choice(m.listar(m.Entrega,"entregado",False))
    repartidor=None
    while not repartidor:
        print(f"Buscando Repartidor disponible para entrega {id} de pedido {pedido.id_entrega}...")
        try:
            repartidor=random.choice(m.listar(m.Repartidor,"disponible",True))
        except IndexError:
            for i in range(5,0,-1):
                print(f"Repartidores ocupados espere {i}...")
                time.sleep(1)
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
    precio_venta=precio_compra*0.16
    print(f"procesando entrega {id}...")
    with lock:
        m.crear_entrada(producto.id_producto,productor.id_productor,random.randint(10,200),datetime.datetime.now(),precio_compra,precio_venta)
    time.sleep(random.randint(1,5))
    print(f"entrega {id} terminada")

def simulation(limit=20):
    i=1
    while i <= limit:
        restocking=threading.Thread(target=restock,args=(i,),daemon=True,name=f"entrada {i}")
        purchase=threading.Thread(target=comprar,args=(i,),daemon=True,name=f"compra {i}")
        delivery=threading.Thread(target=entregar,args=(i,),daemon=True,name=f"entrega {i}")
        restocking.start()
        purchase.start()
        delivery.start()
        i+=1
    print(f"procesos pendientes: {threading.enumerate()}")

if __name__=="__main__":
    simulation()
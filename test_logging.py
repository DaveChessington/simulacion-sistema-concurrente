import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.log_view import Logs
import time
import flet as ft

def log_simulation(logging:Logs):
    print("Probando sistema de logging...")

    logging.create_message("info", "Prueba de mensaje informativo")
    time.sleep(0.5)

    logging.create_message("success", "Operación completada exitosamente")
    time.sleep(0.5)

    logging.create_message("warning", "Advertencia: stock bajo detectado")
    time.sleep(0.5)

    logging.create_message("error", "Error: conexión fallida al servidor")
    time.sleep(0.5)

    logging.create_message("info", "Procesando compra #123")
    time.sleep(0.5)

    logging.create_message("success", "Compra #123 procesada - Entrega #456 creada")
    time.sleep(0.5)

    logging.create_message("info", "Asignando repartidor a entrega #456")
    time.sleep(0.5)

    logging.create_message("success", "Repartidor Juan asignado a entrega #456")
    time.sleep(0.5)

    logging.create_message("warning", "Repartidor María no disponible")
    time.sleep(0.5)

    logging.create_message("error", "Error al procesar restock: producto no encontrado")
    time.sleep(0.5)

    print("finish")

def test_logging(page:ft.Page):
    """Prueba el sistema de logging con diferentes tipos de mensajes"""
    logging=Logs()  

    page.add(
        ft.Container(
            content=ft.Column([
                ft.ElevatedButton(
                    "Log simulation",
                    on_click=lambda e: log_simulation(logging),
                ),
                ft.ElevatedButton(
                    "Clear logs",
                    on_click=lambda e: (logging.clear_logs(), page.update()),
                ),
                logging.get_components()
            ])
        )
    )

if __name__ == "__main__":
    ft.run(test_logging)
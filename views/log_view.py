import flet as ft
from datetime import datetime
import threading

class Logs:
    def __init__(self, initial_controls=None):
        self.log_screen = ft.ListView(
            controls=initial_controls or [],
            auto_scroll=True,
            height=400,
            spacing=5
        )
        self._lock = threading.Lock()
        self._update_callback = None

    def set_update_callback(self, callback):
        self._update_callback = callback

    def create_message(self, message_type: str, content: str, icon=None):
        type_config = {
            'success': {'color': ft.Colors.GREEN, 'icon': ft.Icons.CHECK_CIRCLE},
            'error': {'color': ft.Colors.RED, 'icon': ft.Icons.ERROR},
            'warning': {'color': ft.Colors.ORANGE, 'icon': ft.Icons.WARNING},
            'info': {'color': ft.Colors.BLUE, 'icon': ft.Icons.INFO}
        }

        config = type_config.get(message_type.lower(), {'color': ft.Colors.GREY, 'icon': ft.Icons.HELP})
        icon_to_use = icon or config['icon']

        timestamp = datetime.now().strftime("%H:%M:%S")

        message = ft.Card(
            shadow_color=config['color'],
            content=ft.Container(
                padding=10,
                content=ft.Row([
                    ft.Icon(icon_to_use, color=config['color'], size=20),
                    ft.VerticalDivider(width=10),
                    ft.Column([
                        ft.Text(f"[{timestamp}] {message_type.upper()}", size=12, color=ft.Colors.GREY_700),
                        ft.Text(content, size=14)
                    ], tight=True, spacing=2)
                ], tight=True)
            )
        )

        with self._lock:
            self.log_screen.controls.append(message)
            if self._update_callback:
                self._update_callback()

    def clear_logs(self):
        with self._lock:
            self.log_screen.controls.clear()

    def get_components(self):
        return self.log_screen

global_logger = Logs()

#ejemplo
"""
global_logger.create_message("info", "Sistema de logs inicializado")
global_logger.create_message("success", "Conexión a base de datos establecida")
global_logger.create_message("warning", "Algunos repartidores no disponibles")
"""

def log_view(page: ft.Page):
    global_logger.set_update_callback(page.update)
    content = ft.Column([
        ft.Text("Logs", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([
            ft.ElevatedButton(
                "Limpiar Logs",
                icon=ft.Icons.CLEAR,
                on_click=lambda e: (global_logger.clear_logs(), page.update())
            )
        ]),
        ft.Container(height=10),
        global_logger.get_components()
    ], expand=True)

    if __name__ == "__main__":
        page.add(content)
    else:
        return content


if __name__ == "__main__":
    ft.run(log_view)
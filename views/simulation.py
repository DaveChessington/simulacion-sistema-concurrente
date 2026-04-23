import flet as ft
import pagination as p
import cardview as c
import simulate as sm
import threading
from views.log_view import global_logger

_LEVEL_CONFIG = {
    "success": {"color": ft.Colors.GREEN_700,  "icon": ft.Icons.CHECK_CIRCLE, "label": "OK  "},
    "error":   {"color": ft.Colors.RED_700,    "icon": ft.Icons.ERROR,        "label": "ERR "},
    "warning": {"color": ft.Colors.ORANGE_700, "icon": ft.Icons.WARNING,      "label": "WARN"},
    "info":    {"color": ft.Colors.BLUE_600,   "icon": ft.Icons.INFO,         "label": "INFO"},
}

def simulation_view(page:ft.Page):
    _is_running=False
    sim=sm.Simulation()

    global_logger.set_update_callback(page.update)

    def start_sim(e):
        nonlocal sim, _is_running

        if not limit.value:
            sim.limit=None
        else:
            sim.limit=int(limit.value)
        
        _is_running=True
        print("started")
        start_button.disabled = True
        stop_button.disabled = False
        status_text.value = "Estado: Ejecutando…"
        status_text.color = ft.Colors.GREEN_700
        page.update()

        def run_sim():
            sim.start()
            start_button.disabled = False
            stop_button.disabled = True
            status_text.value = "Estado: Detenida"
            status_text.color = ft.Colors.GREY_600
            page.update()
            
        
        threading.Thread(target=run_sim, daemon=True).start()

    def stop_sim(e):
        nonlocal sim,_is_running
        sim.stop()
        _is_running=False
        print("stopped")
        start_button.disabled = False
        stop_button.disabled = True
        status_text.value = "Estado: Deteniendo..."
        status_text.color = ft.Colors.GREY_600
        page.update()


    start_button = ft.Button(
        "Iniciar",
        icon=ft.Icons.PLAY_ARROW,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700,
        on_click=lambda e: start_sim(e),
    )
    stop_button = ft.Button(
        "Detener",
        icon=ft.Icons.STOP,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        disabled=True,
        on_click=lambda e: stop_sim(e),
    )
    limit=ft.TextField(label="Limite de operaciones", hint_text="Deje en blanco para ilimitado")
    status_text = ft.Text("Estado: Detenida", size=13, color=ft.Colors.GREY_600)
    
    main_content = ft.AlertDialog(
        title= ft.Text("Control de Simulación", size=24, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            status_text, 
            limit,
        ], alignment=ft.MainAxisAlignment.START, expand=False, tight=True),
        actions=[
            start_button,
            stop_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    if __name__=="__main__":
        page.show_dialog(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(simulation_view)

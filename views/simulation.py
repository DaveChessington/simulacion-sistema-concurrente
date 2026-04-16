import flet as ft
import pagination as p
import cardview as c
import simulate as sm

def simulation_view(page:ft.Page):
    def cerrar_y_simular(e):
        sm.simulation(True, True)
        main_content.open = False
        page.snack_bar = aviso
        aviso.open = True
        page.update()
        
    aviso=ft.SnackBar(
        ft.Text("Simulación en progreso..."),
        open=True,
        bgcolor=ft.Colors.BLUE_GREY_700,
    )
    main_content=ft.AlertDialog(
        title="Simulation settings",
        content=ft.Text("settings"),
        open=True,
        actions=[
    ft.TextButton("Simulate", on_click=cerrar_y_simular),
    ft.TextButton("Close", on_click=lambda e: (setattr(main_content, "open", False), page.update()))
]
    )
    


    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(simulation_view)
import flet as ft
import pagination as p
import cardview as c

def simulation_view(page:ft.Page):
    main_content=ft.AlertDialog(
        title="Simulation settings",
        content=ft.Text("settings"),
        open=True
    )

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(simulation_view)
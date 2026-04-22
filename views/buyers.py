import flet as ft
import pagination as p
import cardview as c
import models as m
import crud_dialogs as cd

def buyers_view(page: ft.Page):
    content_container = ft.Container(expand=True)
    
    def refresh_list():
        compradores = m.listar(m.Comprador)
        content_container.content = c.card_view(page, compradores, structure=create_content)
        page.update()
    
    def create_content(element: m.Comprador):
        def on_edit(e):
            nombre_input = ft.TextField(label="Nombre", value=element.nombre, width=300)
            
            def save_changes(e):
                try:
                    if not nombre_input.value:
                        page.show_dialog(ft.SnackBar(ft.Text("El nombre es requerido")))
                        page.update()
                        return
                    m.modify(m.Comprador, element.id_comprador, "nombre", nombre_input.value)
                    dialog.open = False
                    page.show_dialog(ft.SnackBar(ft.Text("Comprador actualizado"), bgcolor=ft.Colors.GREEN))
                    refresh_list()
                except Exception as ex:
                    page.show_dialog(ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED))
                    page.update()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Editar Comprador"),
                content=ft.Column([nombre_input], spacing=10, tight=True),
                actions=[
                    ft.TextButton("Guardar", on_click=save_changes),
                    ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
                ],
            )
            page.show_dialog(dialog)
            page.update()
        
        def on_delete(e):
            dialog = cd.create_delete_dialog(page, "Comprador", element.id_comprador, refresh_list)
            page.show_dialog(dialog)
            page.update()
        
        return ft.Column(
            controls=[
                ft.Text("Comprador", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f"{element.nombre}"),
                    subtitle=ft.Text(f"ID: {element.id_comprador}"),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.TextButton("Modificar", on_click=on_edit),
                        ft.TextButton("Eliminar", on_click=on_delete),
                    ],
                ),
            ]
        )
    
    def on_add_new(e):
        dialog = cd.create_comprador_dialog(page, refresh_list)
        page.show_dialog(dialog)
        page.update()
    
    refresh_list()
    
    main_content = p.pagination_view(page,
        lambda page, elements: c.card_view(page, elements, structure=create_content),
        elements=m.listar(m.Comprador),
        page_title="Compradores Registrados",
        add_button_callback=on_add_new
    )

    if __name__ == "__main__":
        page.add(main_content)
    else:
        return main_content

if __name__ == "__main__":
    ft.run(buyers_view)
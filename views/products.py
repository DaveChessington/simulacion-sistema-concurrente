import flet as ft
import pagination as p
import cardview as c
import models as m
import crud_dialogs as cd

def products_view(page: ft.Page):
    # Contenedor para refrescar la lista
    content_container = ft.Container(expand=True)
    
    def refresh_list():
        """Refresca la lista de productos"""
        productos = m.listar(m.Producto)
        content_container.content = c.card_view(page, productos, structure=create_content)
        page.update()
    
    def create_content(element: m.Producto):
        """Crea el contenido de la tarjeta de producto"""
        def on_edit(e):
            dialog = cd.create_edit_producto_dialog(page, element, refresh_list)
            page.show_dialog(dialog)
            page.update()
        
        def on_delete(e):
            dialog = cd.create_delete_dialog(page, "Producto", element.id_producto, refresh_list)
            page.show_dialog(dialog)
            page.update()
        
        return ft.Column(
            controls=[
                ft.Text("Producto", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCAL_GROCERY_STORE),
                    title=ft.Text(f"{element.nombre}"),
                    subtitle=ft.Text(
                        "Descripcion: {}\nCategoría:{}\nStock: {}".format(
                            element.descripcion, element.categoria, element.cantidad
                        )
                    ),
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
        dialog = cd.create_producto_dialog(page, refresh_list)
        page.show_dialog(dialog)
        page.update()
    
    # Cargar productos inicialmente
    refresh_list()
    
    main_content = p.pagination_view(
        page,
        lambda page, elements: c.card_view(page, elements, structure=create_content),
        elements=m.listar(m.Producto),
        page_title="Productos Registrados",
        add_button_callback=on_add_new
    )

    if __name__ == "__main__":
        page.add(main_content)
    else:
        return main_content

if __name__ == "__main__":
    ft.run(products_view)
import flet as ft
import pagination as p
import cardview as c
import models as m

def products_view(page:ft.Page):
    def content(element:m.Producto):
        return ft.Column(
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCAL_GROCERY_STORE),
                title=ft.Text(f"{element.nombre}"),
                subtitle=ft.Text(
                    "Descripcion: {}\nCategoría:{}\nStock: {}".format(
                        element.descripcion,element.categoria,element.cantidad
                    )
                ),
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.TextButton("Modificar"),
                    ft.TextButton("Eliminar"),
                ],
            ),
        ]
    ) 
    main_content=p.pagination_view(page,lambda page,elements:c.card_view(page,elements,structure=content),elements=m.listar(m.Producto))

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(products_view)
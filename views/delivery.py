import flet as ft
import pagination as p
import cardview as c
import models as m

def delivery_view(page:ft.Page):
    def content(element:m.Repartidor):
        return ft.Column(
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.MARKUNREAD_MAILBOX),
                title=ft.Text(f"{element.nombre}"),
                subtitle=ft.Text(
                    f"Estatus: {'Disponible' if element.disponible else 'Ocupado'}",color=ft.Colors.GREEN if element.disponible else ft.Colors.RED
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

    main_content=p.pagination_view(page,lambda page,elements:c.card_view(page,elements,structure=content),elements=m.listar(m.Repartidor))


    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(delivery_view)
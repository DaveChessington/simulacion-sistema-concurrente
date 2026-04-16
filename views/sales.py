import flet as ft
import pagination as p
import chartview as c
import models as m

def details(id):
    detail=ft.IconButton(ft.Icons.INFO,tooltip="Detalles",on_click=lambda e:print(m.buscar(m.Entrega,id).to_dict()))
    return [detail]

def sales_view(page:ft.Page):
    main_content=p.pagination_view(page,
        lambda page,elements: c.chart_view(page,m.Entrega.attributes(),elements,identifier_attr="id_entrega",actions=details),m.listar(m.Entrega))

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(sales_view)
import flet as ft
import pagination as p
import chartview as c
import models as m

def restock_view(page:ft.Page):
    main_content=p.pagination_view(page,
        lambda page,elements: c.chart_view(page,m.Entrada.attributes(),elements),m.listar(m.Entrada))

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(restock_view)
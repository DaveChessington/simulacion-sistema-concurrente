import flet as ft
import pagination as p
import chartview as c
import models as m

def restock_view(page:ft.Page):
    # Transformar elementos para mostrar nombres en lugar de IDs
    elementos_originales = m.listar(m.Entrada)
    elementos_display = [elem.get_display_data() for elem in elementos_originales]
    
    main_content = p.pagination_view(page,
        lambda page, elements: c.chart_view(page, m.Entrada.display_attributes(), elements), 
        elementos_display)

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(restock_view)
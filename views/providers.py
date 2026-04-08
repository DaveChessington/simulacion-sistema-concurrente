import flet as ft
import pagination as p
import chartview as c

def providers_view(page:ft.Page):
    main_content=p.pagination_view(page,lambda page,elements:ft.Column(controls=[c.chart_view(page,columns=c.columns,elements=elements)]),elements=c.elements)

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(providers_view)
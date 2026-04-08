import flet as ft
import pagination as p
import cardview as c

def sales_view(page:ft.Page):
    main_content=p.pagination_view(page,c.card_view,)

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(sales_view)
import flet as ft
import dashboard as d
import products as p
import providers as pr
import buyers as b
import delivery as dy
import restock as r
import sales as s
import simulation as sm
import log_view as lv

def home(page:ft.Page):  
    
    def sidebar_controller(e):
        print("selected index:",e.control.selected_index)
        match e.control.selected_index:
            case 0:
                content.content=d.dashboard_view(page, )          
                topbar.title="Dashboard"
            case 1:
                content.content=p.products_view(page)
                topbar.title="Products"
            case 2:
                content.content=pr.providers_view(page)
                topbar.title="Providers"
            case 3:
                content.content=b.buyers_view(page)
                topbar.title="Buyers"
            case 4:
                content.content=dy.delivery_view(page)
                topbar.title="Delivery Staff"
            case 5:
                content.content=r.restock_view(page)
                topbar.title="Restock"
            case 6:
                content.content=s.sales_view(page)
                topbar.title="Sales"
            case 7:
                content.content=lv.log_view(page)
                topbar.title="System Logs"
        page.update()

    topbar=ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU,on_click=lambda e:(setattr(sidebar_container,"visible",not sidebar_container.visible),print(f"sidebar visibility is now: {sidebar_container.visible}"),page.update())),
        title="Dashboard",
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        actions=[
            ft.IconButton(ft.Icons.MORE_VERT),
        ],
    )

    sidebar=ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        leading=ft.FloatingActionButton(
            icon=ft.Icons.SETTINGS,
            content="Simulación",
            on_click=lambda e:page.add(sm.simulation_view(page)) ,
        ), 
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.BAR_CHART),label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.INVENTORY),label="Productos"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.PEOPLE_ALT),label="Productores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.SHOPPING_BAG_ROUNDED),label="Compradores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.DELIVERY_DINING),label="Repartidores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.LOGIN),label="Entradas"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.LOGOUT),label="Pedidos"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.LIST_ALT),label="Logs"),
        ],
        on_change=sidebar_controller
    )

    sidebar_container = ft.Container(
        content=ft.Row(controls=[ft.SelectionArea(content=sidebar),ft.VerticalDivider(width=1)]),
    )
    content=ft.Container(expand=True,content=d.dashboard_view(page))

    page.appbar=topbar
    page.add(ft.SafeArea(
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    #ft.SelectionArea(content=sidebar),
                    sidebar_container,
                    #ft.VerticalDivider(width=1),
                    content
                ],
            ),
        ))

if __name__=="__main__":
    ft.run(home)
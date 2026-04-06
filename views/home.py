import flet as ft
location="Dashboard"

def home(page:ft.Page):  
    topbar=ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU,on_click=lambda e:(setattr(sidebar_container,"visible",not sidebar_container.visible),print(f"sidebar visibility is now: {sidebar_container.visible}"),page.update())),
        title=ft.Text(location),
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
            on_click=lambda e: print("FAB clicked!"),
        ), 
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.BAR_CHART),label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.INVENTORY),label="Productos"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.PEOPLE_ALT),label="Productores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.SHOPPING_BAG_ROUNDED),label="Compradores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.DELIVERY_DINING),label="Repartidores"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.LOGIN),label="Entradas"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.LOGOUT),label="Pedidos"),
        ]
    )

    sidebar_container = ft.Container(
        content=ft.Row(controls=[ft.SelectionArea(content=sidebar),ft.VerticalDivider(width=1)]),
    )
    content=ft.Container()

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
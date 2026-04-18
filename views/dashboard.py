import flet as ft
import flet_charts as fch
import sys
import os

try:
    import models as m
except ModuleNotFoundError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import models as m

def dashboard_view(page: ft.Page, elements=None, columns=None):
    # Si no se proporcionan elementos, obtener stock de productos
    if elements is None:
        try:
            productos_stock = m.get_stock_por_producto()
            elements = [
                {"label": p["nombre"][:10], "value": p["cantidad"]}
                for p in productos_stock
            ]
        except Exception as e:
            print(f"Error al obtener stock: {e}")
            elements = []
    
    # Obtener información adicional de stock
    try:
        stock_total = m.get_stock_total()
        productos_bajo_stock = m.get_productos_bajo_stock(5)
        productos_sin_stock = m.get_productos_sin_stock()
        movimientos = m.get_movimientos_stock_resumen()
    except Exception as e:
        print(f"Error al obtener información de stock: {e}")
        stock_total = 0
        productos_bajo_stock = []
        productos_sin_stock = []
        movimientos = {"entradas": 0, "salidas": 0, "balance": 0}
    
    # Crear información de estado
    estado_info = ft.Column([
        ft.Row([
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text("Stock Total", size=12, color=ft.Colors.GREY),
                        ft.Text(str(stock_total), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
                    ], tight=True, spacing=5)
                )
            ),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text("Entradas", size=12, color=ft.Colors.GREY),
                        ft.Text(str(movimientos["entradas"]), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
                    ], tight=True, spacing=5)
                )
            ),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text("Salidas", size=12, color=ft.Colors.GREY),
                        ft.Text(str(movimientos["salidas"]), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE)
                    ], tight=True, spacing=5)
                )
            ),
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text("Balance", size=12, color=ft.Colors.GREY),
                        ft.Text(str(movimientos["balance"]), size=24, weight=ft.FontWeight.BOLD, 
                               color=ft.Colors.GREEN if movimientos["balance"] >= 0 else ft.Colors.RED)
                    ], tight=True, spacing=5)
                )
            ),
        ], spacing=10),
        
        # Advertencias
        ft.Column([
            *([ft.Banner(
                content=ft.Row([
                    ft.Icon(ft.Icons.WARNING, color=ft.Colors.ORANGE),
                    ft.Text(f"⚠ {len(productos_bajo_stock)} productos con stock bajo")
                ], spacing=10),
                leading=None,
            )] if productos_bajo_stock else []),
            *([ft.Banner(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                    ft.Text(f"❌ {len(productos_sin_stock)} productos sin stock")
                ], spacing=10),
                leading=None,
            )] if productos_sin_stock else []),
        ], spacing=5)
    ], spacing=15)
    
    if elements:
        chart_content = fch.BarChart(
            expand=True,
            interactive=True,
            max_y=max([e["value"] for e in elements] or [1]) * 1.10,
            border=ft.Border.all(1, ft.Colors.GREY_400),
            horizontal_grid_lines=fch.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip=fch.BarChartTooltip(
                bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
                border_radius=ft.BorderRadius.all(20),
            ),
            left_axis=fch.ChartAxis(
                label_size=40, title=ft.Text("Stocks de productos"), title_size=40
            ),
            right_axis=fch.ChartAxis(show_labels=False),
            bottom_axis=fch.ChartAxis(
                label_size=40,
                labels=[
                    fch.ChartAxisLabel(
                        value=i, label=ft.Container(ft.Text(element["label"], size=10), padding=10)
                    )
                    for i, element in enumerate(elements)
                ],
            ),
            groups=[
                fch.BarChartGroup(
                    x=i,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=element["value"],
                            width=40,
                            color=ft.Colors.GREEN if element["value"] > 5 else ft.Colors.ORANGE if element["value"] > 0 else ft.Colors.RED,
                            border_radius=0,
                        ),
                    ],
                ) for i, element in enumerate(elements)
            ],
        )
        content = ft.Column([
            ft.SafeArea(content=estado_info),
            ft.SafeArea(content=chart_content, expand=True)
        ], expand=True, spacing=10)
    else:
        content = ft.Column([
            ft.SafeArea(content=estado_info),
            ft.Container(
                content=ft.Text("No hay datos de productos para mostrar"),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        ], expand=True, spacing=10)
    
    if __name__ == "__main__":
        page.add(content)
    else:
        return content
    

if __name__ == "__main__":
    ft.run(dashboard_view)


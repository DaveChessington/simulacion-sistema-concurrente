import flet as ft
import pagination as p
import chartview as c
import models as m


def sales_view(page: ft.Page):

    def details(entrega_id: int):
        def on_click(e: ft.ControlEvent):
            with m.Session(m.engine, expire_on_commit=False) as session:
                stmt = m.select(m.Entrega).options(
                    m.selectinload(m.Entrega.detalles).selectinload(m.DetalleEntrega.producto),
                    m.selectinload(m.Entrega.comprador),
                    m.selectinload(m.Entrega.repartidor)
                ).where(m.Entrega.id_entrega == entrega_id)
                entrega = session.execute(stmt).scalar_one_or_none()

                if not entrega:
                    return

                product_rows = []
                for detalle in entrega.detalles:
                    nombre_producto = detalle.producto.nombre if detalle.producto else f"ID {detalle.id_producto}"
                    producto_text = ft.Text(f"{nombre_producto}", expand=True)
                    cantidad_text = ft.Text(str(detalle.cantidad), size=14)
                    product_rows.append(
                        ft.Row(
                            [producto_text, cantidad_text],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            width=400
                        )
                    )

                if not product_rows:
                    product_rows.append(ft.Text("No hay productos registrados en esta entrega."))

                dialog = ft.AlertDialog(
                    title=ft.Text(f"Productos en entrega #{entrega_id}"),
                    content=ft.Column([
                        ft.Text(f"Comprador: {entrega.comprador.nombre if entrega.comprador else 'Desconocido'}"),
                        ft.Text(f"Repartidor: {entrega.repartidor.nombre if entrega.repartidor else 'No asignado'}"),
                        ft.Divider(),
                        ft.Text("Productos:"),
                        ft.Column(product_rows, spacing=5)
                    ], tight=True),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ],
                    open=True
                )
                page.show_dialog(dialog)

        return [ft.IconButton(ft.Icons.INFO, tooltip="Detalles", on_click=on_click)]

    # Transformar elementos para mostrar nombres en lugar de IDs
    elementos_originales = m.listar(m.Entrega)
    elementos_display = [elem.get_display_data() for elem in elementos_originales]

    main_content = p.pagination_view(page,
        lambda page, elements: c.chart_view(page, m.Entrega.display_attributes(), elements,
                                           identifier_attr="id_entrega", actions=details),
        elementos_display, page_title="Entregas Registradas")

    if __name__=="__main__":
        page.add(main_content)
    else:
        return main_content

if __name__=="__main__":
    ft.run(sales_view)
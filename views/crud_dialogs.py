import flet as ft
import sys
import os

try:
    import models as m
except ModuleNotFoundError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import models as m


def create_producto_dialog(page: ft.Page, on_save_callback=None):
    """Diálogo para crear/editar un Producto"""
    nombre_input = ft.TextField(label="Nombre", width=300)
    categoria_input = ft.TextField(label="Categoría", width=300)
    descripcion_input = ft.TextField(label="Descripción", width=300, multiline=True)
    cantidad_input = ft.TextField(label="Cantidad", width=300, input_filter="digits")

    def save_producto(e):
        try:
            if not nombre_input.value or not categoria_input.value:
                page.snack_bar = ft.SnackBar(ft.Text("Nombre y categoría son requeridos"))
                page.snack_bar.open = True
                page.update()
                return
            
            nuevo = m.crear_producto(
                nombre=nombre_input.value,
                categoria=categoria_input.value,
                descripcion=descripcion_input.value,
                cantidad=int(cantidad_input.value or 0)
            )
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ Producto '{nombre_input.value}' creado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_save_callback:
                on_save_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Nuevo Producto"),
        content=ft.Column([
            nombre_input,
            categoria_input,
            descripcion_input,
            cantidad_input,
        ], spacing=10, tight=True),
        actions=[
            ft.TextButton("Guardar", on_click=save_producto),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog


def create_productor_dialog(page: ft.Page, on_save_callback=None):
    """Diálogo para crear/editar un Productor"""
    nombre_input = ft.TextField(label="Nombre", width=300)

    def save_productor(e):
        try:
            if not nombre_input.value:
                page.snack_bar = ft.SnackBar(ft.Text("El nombre es requerido"))
                page.snack_bar.open = True
                page.update()
                return
            
            nuevo = m.crear_productor(nombre=nombre_input.value)
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ Productor '{nombre_input.value}' creado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_save_callback:
                on_save_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Nuevo Productor"),
        content=ft.Column([nombre_input], spacing=10, tight=True),
        actions=[
            ft.TextButton("Guardar", on_click=save_productor),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog


def create_comprador_dialog(page: ft.Page, on_save_callback=None):
    """Diálogo para crear/editar un Comprador"""
    nombre_input = ft.TextField(label="Nombre", width=300)

    def save_comprador(e):
        try:
            if not nombre_input.value:
                page.snack_bar = ft.SnackBar(ft.Text("El nombre es requerido"))
                page.snack_bar.open = True
                page.update()
                return
            
            nuevo = m.crear_comprador(nombre=nombre_input.value)
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ Comprador '{nombre_input.value}' creado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_save_callback:
                on_save_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Nuevo Comprador"),
        content=ft.Column([nombre_input], spacing=10, tight=True),
        actions=[
            ft.TextButton("Guardar", on_click=save_comprador),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog


def create_repartidor_dialog(page: ft.Page, on_save_callback=None):
    """Diálogo para crear/editar un Repartidor"""
    nombre_input = ft.TextField(label="Nombre", width=300)
    disponible_checkbox = ft.Checkbox(label="Disponible", value=True)

    def save_repartidor(e):
        try:
            if not nombre_input.value:
                page.snack_bar = ft.SnackBar(ft.Text("El nombre es requerido"))
                page.snack_bar.open = True
                page.update()
                return
            
            nuevo = m.crear_repartidor(nombre=nombre_input.value, disponible=disponible_checkbox.value)
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ Repartidor '{nombre_input.value}' creado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_save_callback:
                on_save_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Nuevo Repartidor"),
        content=ft.Column([nombre_input, disponible_checkbox], spacing=10, tight=True),
        actions=[
            ft.TextButton("Guardar", on_click=save_repartidor),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog


def create_edit_producto_dialog(page: ft.Page, producto: m.Producto, on_save_callback=None):
    """Diálogo para editar un Producto"""
    nombre_input = ft.TextField(label="Nombre", value=producto.nombre, width=300)
    categoria_input = ft.TextField(label="Categoría", value=producto.categoria, width=300)
    descripcion_input = ft.TextField(label="Descripción", value=producto.descripcion, width=300, multiline=True)
    cantidad_input = ft.TextField(label="Cantidad", value=str(producto.cantidad), width=300, input_filter="digits")

    def save_changes(e):
        try:
            if not nombre_input.value or not categoria_input.value:
                page.snack_bar = ft.SnackBar(ft.Text("Nombre y categoría son requeridos"))
                page.snack_bar.open = True
                page.update()
                return
            
            m.modify(m.Producto, producto.id_producto, "nombre", nombre_input.value)
            m.modify(m.Producto, producto.id_producto, "categoria", categoria_input.value)
            m.modify(m.Producto, producto.id_producto, "descripcion", descripcion_input.value)
            m.modify(m.Producto, producto.id_producto, "cantidad", int(cantidad_input.value or 0))
            
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ Producto actualizado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_save_callback:
                on_save_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Editar Producto"),
        content=ft.Column([nombre_input, categoria_input, descripcion_input, cantidad_input], spacing=10, tight=True),
        actions=[
            ft.TextButton("Guardar", on_click=save_changes),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog


def create_delete_dialog(page: ft.Page, model_name: str, item_id: int, on_delete_callback=None):
    """Diálogo de confirmación para eliminar"""
    def confirm_delete(e):
        try:
            if model_name == "Producto":
                m.delete(m.Producto, item_id)
            elif model_name == "Productor":
                m.soft_delete(m.Productor, item_id)
            elif model_name == "Comprador":
                m.soft_delete(m.Comprador, item_id)
            elif model_name == "Repartidor":
                m.soft_delete(m.Repartidor, item_id)
            
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"✓ {model_name} eliminado"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            page.update()
            if on_delete_callback:
                on_delete_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text(f"Eliminar {model_name}"),
        content=ft.Text(f"¿Estás seguro de que deseas eliminar este {model_name}?"),
        actions=[
            ft.TextButton("Eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
        ],
    )
    return dialog

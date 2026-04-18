import flet as ft
import flet_datatable2 as fdt
from typing import List, Dict, Callable, Optional, Any

class Person:
    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age

columns = {"First name": "name", "Last name": "last_name", "Age": "age"}
elements = [Person("Alice", "Smith", 30), Person("Bob", "Johnson", 25), Person("Charlie", "Williams", 35),
    Person("Diana", "Brown", 28), Person("Edward", "Jones", 42), Person("Fiona", "Garcia", 31),
    Person("George", "Miller", 19), Person("Hannah", "Davis", 24), Person("Ian", "Rodriguez", 37),
    Person("Julia", "Martinez", 22), Person("David", "Adame", 20)] * 11

class TableSortManager:
    """Gestor de ordenamiento para tablas con soporte para múltiples columnas"""
    
    def __init__(self, elements: List[Any], columns: Dict[str, str]):
        self.elements = elements
        self.columns = columns
        self.sorted_elements = elements.copy()
        self.sort_column = None
        self.sort_ascending = True
    
    def sort_by_column(self, column_attr: str, is_numeric: bool = False) -> List[Any]:
        """
        Ordena los elementos por una columna específica.
        
        Args:
            column_attr: Atributo del objeto a ordenar
            is_numeric: Si es True, ordena numéricamente; si no, alfabéticamente
        
        Returns:
            Lista ordenada de elementos
        """
        # Si es la misma columna, invertir el orden; si no, ordenar ascendente
        if self.sort_column == column_attr:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column_attr
            self.sort_ascending = True
        
        try:
            self.sorted_elements = sorted(
                self.elements,
                key=lambda x: getattr(x, column_attr, ""),
                reverse=not self.sort_ascending
            )
        except (AttributeError, TypeError):
            self.sorted_elements = self.elements.copy()
        
        return self.sorted_elements
    
    def get_sorted_elements(self) -> List[Any]:
        """Retorna los elementos actualmente ordenados"""
        return self.sorted_elements

def create_sort_handler(table: fdt.DataTable2, sort_manager: TableSortManager, 
                       column_mapping: Dict[str, str], page: ft.Page, actions: Optional[Callable] = None, 
                       identifier_attr: Optional[str] = None):
    """
    Crea un manejador de eventos para el ordenamiento de columnas.
    
    Args:
        table: Tabla DataTable2 a actualizar
        sort_manager: Gestor de ordenamiento
        column_mapping: Mapeo de nombres de columna a atributos
        page: Página de Flet para actualizar
        actions: Función que genera acciones para cada fila
        identifier_attr: Atributo usado como identificador único
    """
    def on_sort(e: ft.ControlEvent):
        if not hasattr(e, 'data'):
            return
        
        column_name = e.data
        column_attr = column_mapping.get(column_name)
        
        if not column_attr:
            return
        
        # Determinar si es numérico basado en el atributo
        is_numeric = column_attr.lower() in ['age', 'id', 'cantidad']
        
        # Ordenar elementos
        sorted_elements = sort_manager.sort_by_column(column_attr, is_numeric)
        
        # Actualizar tabla con acciones regeneradas
        update_table_rows(table, sorted_elements, column_mapping, actions, identifier_attr)
        
        # Actualizar página
        page.update()
    
    return on_sort

def update_table_rows(table: fdt.DataTable2, elements: List[Any], 
                     column_mapping: Dict[str, str], actions: Optional[Callable] = None, 
                     identifier_attr: Optional[str] = None):
    """
    Actualiza las filas de la tabla con los elementos ordenados y regenera acciones.
    
    Args:
        table: Tabla a actualizar
        elements: Elementos ordenados
        column_mapping: Mapeo de nombres de columna a atributos
        actions: Función que genera acciones para cada fila
        identifier_attr: Atributo usado como identificador único
    """
    # Crear nuevas filas con los elementos ordenados
    table.rows.clear()
    for element in elements:
        cells = [
            ft.DataCell(ft.Text(str(getattr(element, attr, "")))) 
            for attr in column_mapping.values()
        ]
        
        # Regenerar celda de acciones si se proporcionan
        if actions and identifier_attr:
            identifier = getattr(element, identifier_attr, None)
            cells.append(
                ft.DataCell(
                    ft.Row(
                        controls=actions(identifier),
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            )
        
        table.rows.append(fdt.DataRow2(cells=cells))

def chart_view(page: ft.Page, columns: Dict[str, str] = None, 
               elements: List[Any] = None, identifier_attr: Optional[str] = None, 
               actions: Optional[Callable] = None) -> ft.Column:
    
    if columns is None:
        columns = globals()["columns"]
    if elements is None:
        elements = globals()["elements"]
    
    if isinstance(columns, (list, tuple)):
        columns = {attr: attr for attr in columns}
    elif not isinstance(columns, dict):
        raise TypeError(f"columns debe ser un diccionario o lista, pero se recibió {type(columns)}")
    
    sort_manager = TableSortManager(elements, columns)
    
    table = fdt.DataTable2(
        expand=True,
        empty=ft.Text("This table is empty."),
        column_spacing=12,
        columns=[
            fdt.DataColumn2(
                label=ft.Text(column),
                tooltip=f"Click to sort by {column}",
            )
            for column in columns.keys()
        ],
        rows=[
            fdt.DataRow2(cells=[
                ft.DataCell(ft.Text(str(getattr(element, attr, ""))))
                for attr in columns.values()
            ])
            for element in sort_manager.get_sorted_elements()
        ]
    )
    
    # Configurar manejadores de ordenamiento
    sort_handler = create_sort_handler(table, sort_manager, columns, page, actions, identifier_attr)
    column_keys = list(columns.keys())
    for i, col in enumerate(table.columns):
        col.on_sort = lambda e, col_name=column_keys[i]: (
            setattr(e, 'data', col_name),
            sort_handler(e)
        )[1]
    
    if actions and identifier_attr:
        table.columns.append(fdt.DataColumn2(label=ft.Text("Actions")))
        for i, row in enumerate(table.rows):
            element = sort_manager.get_sorted_elements()[i]
            identifier = getattr(element, identifier_attr, None)
            
            row.cells.append(
                ft.DataCell(
                    ft.Row(
                        controls=actions(identifier),
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            )
    
    content = ft.Column(
        ft.SafeArea(content=table, expand=True),
        expand=True
    )
    
    if __name__ == "__main__":
        page.add(content)
    else:
        return content

if __name__ == "__main__":
    ft.run(chart_view)

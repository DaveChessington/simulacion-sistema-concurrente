import flet as ft
import flet_datatable2 as fdt

class Person:
    def __init__(self,name,last_name,age):
        self.name=name
        self.last_name=last_name
        self.age=age

columns={"First name":"name","Last name":"last_name","Age":"age"}#mapping table column name with class attribute
elements=[Person("Alice", "Smith", 30), Person("Bob", "Johnson", 25), Person("Charlie", "Williams", 35),
    Person("Diana", "Brown", 28), Person("Edward", "Jones", 42), Person("Fiona", "Garcia", 31),
    Person("George", "Miller", 19), Person("Hannah", "Davis", 24), Person("Ian", "Rodriguez", 37),
    Person("Julia", "Martinez", 22),Person("David","Adame",20)]*11

def chart_view(page: ft.Page,columns=columns,elements=elements,identifier_attr=None,actions=None):
    table = fdt.DataTable2(
        expand=True,
        empty=ft.Text("This table is empty."),
        column_spacing=12,
        columns=[
            fdt.DataColumn2(label=ft.Text(column),tooltip=column,
                            on_sort=lambda e:()) for column in columns
        ],
        rows=[
            fdt.DataRow2(cells=[
                ft.DataCell(ft.Text(getattr(element,attr))) for attr in columns
            ])
            for element in elements
        ]
    )

    if actions:
        table.columns.append(fdt.DataColumn2(label=ft.Text("Actions")))
        for i, row in enumerate(table.rows):
            identifier=getattr(elements[i], identifier_attr)

            row.cells.append(
                ft.DataCell(
                    ft.Row(
                        controls=actions(identifier), 
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            )    
            
    content=ft.Column(ft.SafeArea(content=table,expand=True),expand=True)

    
    if __name__ == "__main__":
        page.add(
            content
        )
    else:
        return content

if __name__ == "__main__":
    ft.run(chart_view)

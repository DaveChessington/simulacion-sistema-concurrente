import flet as ft

def content(element):
    return ft.Column(
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ALBUM),
                title=ft.Text(f"The Enchanted Nightingale {element}"),
                subtitle=ft.Text(
                    "Music by Julie Gable. Lyrics by Sidney Stein."
                ),
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.TextButton("Buy tickets"),
                    ft.TextButton("Listen"),
                ],
            ),
        ]
    )

def card_view(page:ft.Page,elements=[i for i in range(120)],structure=content):
    #structure is meant to the body of the card, you  should be able to pass a custom elemnt to display its values
    #elements is supposed to be 
    view= ft.GridView(
                    expand=True,
                    runs_count=2,
                    spacing=8,
                    child_aspect_ratio=3.5, 
                    controls=[ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=structure(element)
                            ),
                        ) for element in elements
                    ]   
                )
    
    if __name__=="__main__":
        page.add(view)
    else:
        return view
    
if __name__=="__main__":
    ft.run(card_view)
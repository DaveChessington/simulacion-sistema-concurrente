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

def card_view(page:ft.Page, elements=[i for i in range(120)], structure=content,
              runs_count: int = 2, spacing: int = 8,
              child_aspect_ratio: float = 2.4,
              card_width: int = 360, card_height: int = 180):
    # structure is meant to be the body of the card; you should be able to pass a custom element to display its values
    view = ft.GridView(
        expand=True,
        runs_count=runs_count,
        spacing=spacing,
        child_aspect_ratio=child_aspect_ratio,
        controls=[
            ft.Card(
                content=ft.Container(
                    padding=12,
                    width=card_width,
                    height=card_height,
                    content=structure(element)
                ),
                margin=ft.margin.only(bottom=8)
            )
            for element in elements
        ]
    )
    
    if __name__=="__main__":
        page.add(view)
    else:
        return view
    
if __name__=="__main__":
    ft.run(card_view)
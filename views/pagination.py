import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
import models as m
import cardview

def pagination_view(page:ft.Page,generate=cardview.card_view,elements=[i for i in range(120)]):
    #elements must be a model from models.py
    #generate parameter must be a function to generate the content for pagination
    
    def next_pressed(e):
        if int(current_page.value)+1>pagination["total_pages"]:
            next_button.disabled=True
        else:
            current_page.value=int(current_page.value)+1
            prev_button.disabled=False
        update_pagination()

    def prev_pressed(e):
        if int(current_page.value)-1<1:
            prev_button.disabled=True
        else:
            current_page.value=int(current_page.value)-1
            next_button.disabled=False
        update_pagination()

    def current_changed(e):
        try:
            if not 0<int(current_page.value)<=pagination["total_pages"]:
                current_page.value=1     
        except:
            return 
        update_pagination() 
        
    def update_pagination():
        try:
            if current_page.value=="":
                current_page.value=1
            pagination=m.get_page(elements,int(current_page.value))
        except Exception as ex:
            print(ex)
            pagination=m.get_page(elements)
        content.content=generate(page,pagination["data"])
       
        page.update()

    pagination=m.get_page(elements)
    content=ft.Container()
    
    
    current_page=ft.TextField(value=1,keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$"),#on_change=current_changed,
                              on_blur=current_changed,width=50)
                              
    next_button=ft.IconButton(icon=ft.Icons.NAVIGATE_NEXT,on_click=next_pressed)
    prev_button=ft.IconButton(icon=ft.Icons.NAVIGATE_BEFORE,on_click=prev_pressed)
    navigation=ft.Row([prev_button,current_page,next_button],alignment=ft.MainAxisAlignment.CENTER)
    
    component=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[content,navigation],expand=True,scroll=ft.ScrollMode.AUTO,)

    update_pagination()
    
    if __name__=="__main__":
        page.add(component)
    else:
        return component

if __name__=="__main__":
    ft.run(pagination_view)
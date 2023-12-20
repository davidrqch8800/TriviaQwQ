import time
import flet as ft

import pandas as pd
import csv
import numpy as np
import pickle
import random

def main(page: ft.Page):
    
    word_embeddings = pickle.load( open( "word_embeddings_subset.p", "rb" ) )
    len(word_embeddings)

    data = pd.read_csv('capitals.txt', delimiter=' ')
    data.columns = ['city1', 'country1', 'city2', 'country2']

    page.title = "Trivia"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def cosine_similarity(A, B):
        dot = np.dot(A,B)
        norma = np.sqrt(np.dot(A,A))
        normb = np.sqrt(np.dot(B,B))
        cos = dot/(norma*normb)
        return cos

    def get_top_cities(city1, country1, city2, embeddings, cosine_similarity=cosine_similarity, num_cities=3):
        group = set((city1, country1, city2))
        city1_emb = embeddings[city1]
        country1_emb = embeddings[country1]
        city2_emb = embeddings[city2]
        vec = country1_emb - city1_emb + city2_emb
        top_cities = []

        for word in embeddings.keys():
            if word not in group:
                word_emb = embeddings[word]
                cur_similarity = cosine_similarity(vec, word_emb)
                top_cities.append([word, cur_similarity])

        top_cities.sort(key=lambda x: x[1], reverse=True)

        return top_cities[:num_cities]

    
    def iniciar_juego():
        global cg
        global txt2
        random_index = np.random.randint(0, len(data))
        random_city1 = data.loc[random_index, 'city1']
        random_country1 = data.loc[random_index, 'country1']
        random_city2 = data['city2'].sample().values[0]
        paises = get_top_cities(random_city1, random_country1, random_city2, word_embeddings, num_cities=3)
        txt2 =paises[0][0]
        opciones = [
            ft.Radio(value=paises[0][0], label=paises[0][0]),
            ft.Radio(value=paises[1][0], label=paises[1][0]),
            ft.Radio(value=paises[2][0], label=paises[2][0])
        ]
        random.shuffle(opciones)
        cg = ft.RadioGroup(content=ft.Column(opciones), on_change=capitalEs)
        bienvenido: ft.Text = ft.Text(value="Trivia de Paises del Mundo", text_align = ft.TextAlign.CENTER, size = 40)
        capital: ft.Text = ft.Text(value=f"¿Cual es el pais que tiene como capital a {random_city2}?", text_align= ft.TextAlign.CENTER, size = 25)
        page.add(
            ft.ResponsiveRow(
                controls = [
                    ft.Column([bienvenido,
                               capital,
                               cg,
                               t,
                               boton_comprobar,
                    ])
                ], 
                alignment = ft.MainAxisAlignment.CENTER
            )
        )

    def capitalEs(e):
        page.update()

    def comprobar(e):
        global cg
        global txt2
        opcion_seleccionada = cg.value
        if opcion_seleccionada == txt2:
            resultado = "¡Correcto!"
        else:
            resultado = "Incorrecto. La respuesta correcta es: \n" + txt2
        page.clean()
        page.add(ft.Text(value=resultado, text_align=ft.TextAlign.CENTER, size = 30))
        page.update()
        time.sleep(2)
        page.clean()
        iniciar_juego()

    t = ft.Text()
    boton_comprobar = ft.ElevatedButton(text="Comprobar", on_click=comprobar)

    iniciar_juego()

ft.app(main)

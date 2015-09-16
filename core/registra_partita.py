#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from core.models import Squadra, Giocatore, Partita, Evento, DettaglioPartita
from Tkinter import *
import ttk

TEMPI = ('primo', 'secondo')
MINUS = 'minus.gif'
__author__ = 'roberto'


def popola_giocatori(conndb, finestra, partita, combo_partita):
    eventi = Evento(conndb).collection(orderby='position ASC')
    minus = PhotoImage(file=MINUS)

    def fx(tk_event):
        model_partita = Partita(conndb).load(combo_partita[partita.get()])
        print combo_partita[partita.get()], model_partita.get_data()
        # squadra = Squadra(conndb).load(model_partita.get('squadra'))
        giocatori = Giocatore(conndb).collection(where_sql="squadra = ?", vals=(model_partita.get('squadra'), ))
        Label(finestra, text='Nome').grid(row=1, column=0)
        Label(finestra, text='Ruolo', background='white').grid(row=1, column=1, sticky=W + E + N + S)
        first = True
        moltiplicatore = 3
        ox, oy = 2, 2
        for y, giocatore in enumerate(giocatori):
            Label(finestra, text=giocatore['nome']).grid(row=y + oy, column=0)
            Label(finestra, text=giocatore['ruolo'], background='white').grid(row=y + oy, column=1,
                                                                              sticky=W + E + N + S)
            for x, evento in enumerate(eventi):
                print evento
                if first:
                    # label degli eventi
                    Label(finestra,
                          text=evento['nome'],
                          background=evento.get('colore_fondo', '')
                    ).grid(row=1, column=ox + (x * moltiplicatore), sticky=W + E + N + S, columnspan=2)
                    Label(finestra, text=" ", background='black').grid(row=1, column=ox + (x * moltiplicatore) + 2,
                                                                       sticky=W + E + N + S)
                # bottoni degli eventi
                gif = PhotoImage(file=evento.get('icona', 'ball.gif'))
                Button(finestra,
                       image=minus,
                       background=evento.get('colore_fondo', '')
                ).grid(row=y + oy, column=x * moltiplicatore + ox)
                b = Button(finestra,
                           image=gif,
                           background=evento.get('colore_fondo', '')
                )
                b.grid(row=y + oy, column=x * moltiplicatore + ox + 1)
                b.image = gif
                b.minus = minus
                Label(finestra, text=" ", background='black').grid(row=y + oy, column=x * moltiplicatore + ox + 2,
                                                                   sticky=W + E + N + S)
            first = False

    return fx


def crea_finestra(conndb, root, finestre, destroy):
    nome_finestra = 'Registra Partita'

    def gui_factory(e, finestra):
        if e == 'squadra':
            entry = ttk.Combobox(finestra)
            entry['values'] = Squadra(conndb).collection_keys()
        elif e == 'ruolo':
            entry = ttk.Combobox(finestra)
            entry['values'] = ['-', 'portiere']
        else:
            entry = Entry(finestra)
        return entry


    def fx():
        if nome_finestra not in finestre:
            finestra = Toplevel(root)
            finestre[nome_finestra] = finestra
            finestra.grab_set()
            finestra.protocol("WM_DELETE_WINDOW", destroy(finestra))
            finestra.geometry('+250+100')
            finestra.wm_iconbitmap(bitmap='ball.ico')
            finestra.title(nome_finestra)

            Label(finestra, text="Scegli una partita:").grid(row=0, column=0)

            combo_partita = {}
            partita = ttk.Combobox(finestra)
            values = []
            for part in Partita(conndb).collection():
                print part
                label = "{squadra} - {altra_squadra} ({data})".format(**part)
                values.append(label)
                combo_partita[label] = part['id']
            partita['values'] = values
            partita.config(width=max([len(x) for x in values]))
            # if values:
            # partita.insert(0, values[-1])
            # partita.current(0)
            partita.grid(row=0, column=1, columnspan=6)
            partita.bind("<<ComboboxSelected>>", popola_giocatori(conndb, finestra, partita, combo_partita))


    return fx

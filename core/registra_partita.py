#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from core.models import Squadra, Giocatore, Partita, Evento, DettaglioPartita
from Tkinter import *
import ttk

TEMPI = ('primo', 'secondo')
MINUS = 'minus.gif'
__author__ = 'roberto'


def segnapunto(punteggi_giocatori, nome_giocatore, codice_evento, delta=1):

    def fx():
        obj_gui = punteggi_giocatori[(nome_giocatore, codice_evento)]
        punti = int(obj_gui.cget('text'))
        punti += delta
        if punti < 0:
            punti = 0
        obj_gui.config(text=punti)

    return fx


def popola_giocatori(conndb, finestra, partita, combo_partita):
    eventi = Evento(conndb).collection(orderby='position ASC')
    minus = PhotoImage(file=MINUS)
    pixel = PhotoImage(file='pixel.gif')

    oggetti_gui = list()
    punteggi_giocatori = dict()

    def fx(tk_event):
        print len(oggetti_gui)
        while oggetti_gui:  # vuota la finestra dei cotnrolli qui creati
            oggetti_gui.pop().destroy()
        while punteggi_giocatori:  # vuota i punteggi giocatori
            fk = punteggi_giocatori.keys()[0]
            punteggi_giocatori.pop(fk)
        model_partita = Partita(conndb).load(combo_partita[partita.get()])
        # print combo_partita[partita.get()], model_partita.get_data()
        # squadra = Squadra(conndb).load(model_partita.get('squadra'))
        giocatori = Giocatore(conndb).collection(where_sql="squadra = ?", vals=(model_partita.get('squadra'), ))
        l = Label(finestra, text='Nome')
        l.grid(row=1, column=0)
        oggetti_gui.append(l)
        l = Label(finestra, text='Ruolo', background='white')
        l.grid(row=1, column=1, sticky=W + E + N + S)
        oggetti_gui.append(l)
        first = True
        moltiplicatore = 3
        ox, oy = 2, 2
        for y, giocatore in enumerate(giocatori):
            l = Label(finestra, text=giocatore['nome'])
            l.grid(row=y * 2 + oy, column=0, rowspan=2)
            oggetti_gui.append(l)
            l = Label(finestra, text=giocatore['ruolo'], background='white')
            l.grid(row=y * 2 + oy, column=1, rowspan=2, sticky=W + E + N + S)
            oggetti_gui.append(l)
            for x, evento in enumerate(eventi):
                # print evento
                if first:
                    # label degli eventi
                    l = Label(finestra,
                              text=evento['nome'],
                              background=evento.get('colore_fondo', '')
                    )
                    l.grid(row=1, column=ox + (x * moltiplicatore), sticky=W + E + N + S, columnspan=moltiplicatore - 1)
                    oggetti_gui.append(l)
                    l = Label(finestra,
                              image=pixel,
                              background='black',
                              width=1)
                    l.image = pixel
                    l.grid(row=1, column=ox + (x * moltiplicatore) + 2, sticky=W + E + N + S, rowspan=2)
                    oggetti_gui.append(l)
                # bottoni degli eventi
                gif = PhotoImage(file=evento.get('icona', 'ball.gif'))
                b = Button(finestra,
                           image=minus,
                           background=evento.get('colore_fondo', ''),
                           command=segnapunto(punteggi_giocatori, giocatore['nome'], evento['codice'], -1)
                )
                b.grid(row=y * 2 + oy, column=x * moltiplicatore + ox, sticky=E + W)
                b.minus = minus
                oggetti_gui.append(b)
                b = Button(finestra,
                           image=gif,
                           background=evento.get('colore_fondo', ''),
                           command=segnapunto(punteggi_giocatori, giocatore['nome'], evento['codice'])
                )
                b.grid(row=y * 2 + oy, column=x * moltiplicatore + ox + 1, sticky=E + W)
                b.image = gif
                oggetti_gui.append(b)
                punti = get_punti(partita,giocatore,evento)
                l = Label(finestra,
                          text = punti,
                          background=evento.get('colore_fondo', '')
                )
                l.grid(row=y * 2 + oy + 1, column=x * moltiplicatore + ox, sticky=W + E + N + S, columnspan=2)
                oggetti_gui.append(l)
                punteggi_giocatori[(giocatore['nome'], evento['codice'])] = l
                l = Label(finestra, image=pixel, width=1, background='black')
                l.grid(row=y * 2 + oy, column=x * moltiplicatore + ox + 2, sticky=W + E + N + S, rowspan=2)
                oggetti_gui.append(l)
            first = False

    return fx


def crea_finestra(conndb, root, finestre, destroy):
    nome_finestra = 'Registra Partita'

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
            partita.grid(row=0, column=1, columnspan=12)
            partita.bind("<<ComboboxSelected>>", popola_giocatori(conndb, finestra, partita, combo_partita))


    return fx

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from core.models import Squadra, Giocatore, Partita, Evento, DettaglioPartita
from Tkinter import *
import tkMessageBox
import ttk
import time
import threading

TEMPI = ('primo', 'secondo')
MINUS = 'minus.gif'
__author__ = 'roberto'


def segnapunto(conndb, punteggi_giocatori, id_partita, nome_giocatore, codice_evento, timer, delta=1):
    def fx():
        obj_gui = punteggi_giocatori[(nome_giocatore, codice_evento)]
        punti = int(obj_gui.cget('text'))
        punti += delta
        if punti < 0:
            punti = 0
        obj_gui.config(text=punti)
        if delta == 1:
            DettaglioPartita(conndb).set_data(id_partita=id_partita,
                                              giocatore=nome_giocatore,
                                              evento=codice_evento,
                                              time=timer.cget('text')
            ).save()
            Partita(conndb).load(id_partita).set('timer', timer.cget('text')).save()
        elif delta == -1:
            c = DettaglioPartita(conndb).collection(where_sql='id_partita = ? AND giocatore = ? AND evento = ?',
                                                    vals=(
                                                        id_partita,
                                                        nome_giocatore,
                                                        codice_evento
                                                    ),
                                                    orderby="time DESC"
            )
            if c:
                print c[0]
                DettaglioPartita(conndb).set_key(c[0]['id']).delete()

    return fx


def get_punti(conndb, partita, giocatore, evento):
    c = DettaglioPartita(conndb).collection(where_sql='id_partita = ? AND giocatore = ? AND evento = ?',
                                            vals=(
                                                partita.get(Partita.get_key()),
                                                giocatore.get('nome'),
                                                evento.get('codice')
                                            )
    )
    return len(c)


starttime = {'start': False}


def start_timer(timer):
    def worker():
        while timer.running:
            dt = int(time.time() - starttime['start'])
            try:
                timer.config(text="%02i:%02i" % (dt / 60, dt % 60))
            except TclError:
                break
            time.sleep(0.25)

    def fx():
        if not timer.running:
            timer_value = timer.cget('text')
            dt = int(timer_value[:2]) * 60 + int(timer_value[-2:])
            starttime['start'] = time.time() - dt
            starttime['thread'] = threading.Thread(target=worker)
            timer.running = True
            starttime['thread'].start()


    return fx


def pause_timer(timer):
    def fx():
        if timer.running != False:
            timer.running = False

    return fx


def reset_timer(timer):
    def fx():
        result = tkMessageBox.askquestion("Reset Timer", "Sei Sicuro?", icon='warning')
        if result:
            starttime['start'] = time.time()
            timer.running = False
            timer.config(text="00:00")
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

        # TIMER
        timer_value = model_partita.get('timer')
        if not timer_value:
            timer_value = "00:00"
        timer = Label(finestra, text=timer_value, bg='black', fg='red', font=("Helvetica", 16))
        timer.grid(row=0, column=15, columnspan=3)
        timer.running = False
        oggetti_gui.append(timer)

        play_gif = PhotoImage(file='play.gif')
        pause_gif = PhotoImage(file='pause.gif')
        reset_gif = PhotoImage(file='reset.gif')

        play_button = Button(finestra, image=play_gif, command=start_timer(timer))
        play_button.grid(row=0, column=18)
        play_button.image = play_gif
        oggetti_gui.append(play_button)

        button = Button(finestra, image=pause_gif, command=pause_timer(timer))
        button.grid(row=0, column=20)
        button.image = pause_gif
        oggetti_gui.append(button)

        button = Button(finestra, image=reset_gif, command=reset_timer(timer))
        button.grid(row=0, column=21)
        button.image = reset_gif
        oggetti_gui.append(button)

        # FINE TIMER

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
                           command=segnapunto(conndb,
                                              punteggi_giocatori,
                                              model_partita.get(Partita.get_key()),
                                              giocatore['nome'],
                                              evento['codice'],
                                              timer,
                                              -1)
                )
                b.grid(row=y * 2 + oy, column=x * moltiplicatore + ox, sticky=E + W)
                b.minus = minus
                oggetti_gui.append(b)
                b = Button(finestra,
                           image=gif,
                           background=evento.get('colore_fondo', ''),
                           command=segnapunto(conndb,
                                              punteggi_giocatori,
                                              model_partita.get(Partita.get_key()),
                                              giocatore['nome'],
                                              evento['codice'],
                                              timer)
                )
                b.grid(row=y * 2 + oy, column=x * moltiplicatore + ox + 1, sticky=E + W)
                b.image = gif
                oggetti_gui.append(b)
                punti = get_punti(conndb, model_partita, giocatore, evento)
                l = Label(finestra,
                          text=punti,
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

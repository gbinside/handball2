#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from core.models import Squadra, Giocatore, Partita, Evento, DettaglioPartita
import core.registra_partita
import pymodel.abstract

import tkMessageBox
from Tkinter import *
import ttk
import sys
import os

finestre = {}
conndb = None


def todo():
    pass


def destroy(o):
    def fx():
        for k, v in finestre.items():
            if v == o:
                del finestre[k]
        o.grab_release()
        o.destroy()

    return fx


def cancella_riga(finestra, classe, valore_chiave, switch):
    def fx():
        if tkMessageBox.askyesno('Sei Sicuro ?', 'Sei Sicuro ?'):
            classe(conndb).set_key(valore_chiave).delete()
            destroy(finestra)()
            switch()

    return fx


def salva_riga(finestra, classe, entries, switch):
    def fx():
        if entries[0].get() == '' and entries[0].myfieldname != 'id':
            return
        finestra.withdraw()
        model = classe(conndb)
        model.new()
        try:
            model.load(entries[0].get())
        except pymodel.abstract.RecordNotFoundException:
            pass
        for e in entries:
            if e.myfieldname != 'id':
                model.set(e.myfieldname, e.get())
        model.save()
        destroy(finestra)()
        switch()

    return fx


def salva(finestra, classe, entries, switch):
    def fx():
        finestra.withdraw()
        model = classe(conndb)
        for row in entries:
            model.new()
            try:
                model.load(row[0].get())
            except pymodel.abstract.RecordNotFoundException:
                pass
            for e in row:
                model.set(e.myfieldname, e.get())
            model.save()
        destroy(finestra)()
        switch()

    return fx


def crea_finestra_tabelle(nome_finestra, classe_db):
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
            s = classe_db(conndb)
            try:
                c = s.collection(orderby='CAST(position AS decimal) ASC')
            except pymodel.abstract.OperationalError:
                c = s.collection()
            i = 0
            for i, e in enumerate(c[0]):
                Label(finestra, text=e).grid(row=1, column=i, sticky=W)
            row = -1
            entries = list()
            for row, riga in enumerate(c):
                row_entries = list()
                for i, e in enumerate(riga):
                    # print e, riga
                    entry = gui_factory(e, finestra)
                    entry.myfieldname = e
                    entry.insert(0, riga[e])
                    if e == 'id':
                        entry.config(state='readonly')
                    entry.grid(row=2 + row, column=i, sticky=W)
                    row_entries.append(entry)
                entries.append(row_entries)
                Button(finestra,
                       text='Cancella',
                       command=cancella_riga(finestra, classe_db, riga[classe_db.get_key()],
                                             crea_finestra_tabelle(nome_finestra, classe_db))
                ).grid(row=2 + row, column=i + 1)
            Button(finestra,
                   text='Salva',
                   command=salva(finestra, classe_db, entries, crea_finestra_tabelle(nome_finestra, classe_db))) \
                .grid(row=1, column=i + 1, sticky=N)
            # nuova riga
            new_entries = list()
            for i, e in enumerate(c[0]):
                entry = gui_factory(e, finestra)
                entry.grid(row=row + 3, column=i, sticky=W)
                entry.myfieldname = e
                if e == 'id':
                    entry.config(state='readonly')
                new_entries.append(entry)
            Button(finestra,
                   text='Aggiungi',
                   command=salva_riga(finestra, classe_db, new_entries,
                                      crea_finestra_tabelle(nome_finestra, classe_db))) \
                .grid(row=3 + row, column=i + 1)

    return fx


def schema(conndb):
    if len(Evento(conndb).collection_keys()) == 0:
        Evento(conndb).set('codice', 'ed') \
            .set('nome', 'errore difesa') \
            .set('punti', 0) \
            .set('icona', 'cancel.gif') \
            .set('colore_fondo', 'red') \
            .set('position', 10) \
            .save()
        Evento(conndb).set_data(codice='goal9',
                                nome='GOAL9',
                                icona='ball.gif',
                                punti=1,
                                colore_fondo='green',
                                position=20
        ).save()
        Evento(conndb).set_data(codice='goal6',
                                nome='GOAL6',
                                icona='ball.gif',
                                punti=1,
                                colore_fondo='green',
                                position=30
        ).save()
        Evento(conndb).set_data(codice='goalcontro',
                                nome='GOAL C',
                                icona='ball.gif',
                                punti=1,
                                colore_fondo='green',
                                position=40
        ).save()
        Evento(conndb).set_data(codice='goalrigore',
                                nome='GOAL R',
                                icona='ball.gif',
                                punti=1,
                                colore_fondo='green',
                                position=50
        ).save()
        Evento(conndb).set_data(codice='errore9',
                                nome='ERRORE GOAL9',
                                icona='cancel.gif',
                                punti=0,
                                colore_fondo='red',
                                position=60
        ).save()
        Evento(conndb).set_data(codice='errore6',
                                nome='ERRORE GOAL6',
                                icona='cancel.gif',
                                punti=0,
                                colore_fondo='red',
                                position=70
        ).save()
        Evento(conndb).set_data(codice='errorecontro',
                                nome='ERRORE GOAL C',
                                icona='cancel.gif',
                                punti=0,
                                colore_fondo='red',
                                position=80
        ).save()
        Evento(conndb).set_data(codice='errorerigorre',
                                nome='ERRORE GOAL R',
                                icona='cancel.gif',
                                punti=0,
                                colore_fondo='red',
                                position=90
        ).save()
        Evento(conndb).set_data(codice='pallarec',
                                nome='PR',
                                icona='angularbracket.gif',
                                punti=0,
                                colore_fondo='white',
                                position=100
        ).save()
        Evento(conndb).set_data(codice='erroretec',
                                nome='ET',
                                icona='cancel.gif',
                                punti=0,
                                colore_fondo='red',
                                position=110
        ).save()
        Evento(conndb).set_data(codice='ammonizione',
                                nome='AM',
                                icona='angularbracket.gif',
                                punti=0,
                                colore_fondo='yellow',
                                position=120
        ).save()
        Evento(conndb).set_data(codice='2min',
                                nome='2M',
                                icona='angularbracket.gif',
                                punti=0,
                                colore_fondo='red',
                                position=130
        ).save()
        Evento(conndb).set_data(codice='assist',
                                nome='AS',
                                icona='angularbracket.gif',
                                punti=0,
                                colore_fondo='white',
                                position=140
        ).save()
    if len(Squadra(conndb).collection_keys()) == 0:
        Squadra(conndb).set_data(nome='casalgrande', genere='maschile').save()
        Squadra(conndb).set_data(nome='pratisollo', genere='maschile').save()
    if len(Giocatore(conndb).collection_keys()) == 0:
        Giocatore(conndb).set_data(nome='prova 1',
                                   squadra='casalgrande',
                                   numero='00',
                                   ruolo='-'
        ).save()
        Giocatore(conndb).set_data(nome='prova 2',
                                   squadra='casalgrande',
                                   numero='01',
                                   ruolo='-'
        ).save()
        Giocatore(conndb).set_data(nome='prova 3',
                                   squadra='casalgrande',
                                   numero='02',
                                   ruolo='-'
        ).save()
        Giocatore(conndb).set_data(nome='prova 4',
                                   squadra='casalgrande',
                                   numero='03',
                                   ruolo='portiere'
        ).save()
        Giocatore(conndb).set_data(nome='prova 5',
                                   squadra='pratissolo',
                                   numero='00',
                                   ruolo='-'
        ).save()
    if len(Partita(conndb).collection_keys()) == 0:
        # .set('risultato_primo_tempo', '0-0') \
        # .set('risultato_secondo_tempo', '0-0') \
        Partita(conndb).set('squadra', 'casalgrande') \
            .set('altra_squadra', 'montegrotto') \
            .set('data', '01-01-2015') \
            .set('risultato_finale', '0-0') \
            .set('timer', '00:00') \
            .save()
        Partita(conndb).set('squadra', 'pratissolo') \
            .set('altra_squadra', 'montegrotto') \
            .set('data', '01-02-2015') \
            .set('risultato_finale', '0-0') \
            .set('timer', '00:00') \
            .save()
    if len(DettaglioPartita(conndb).collection_keys()) == 0:
        DettaglioPartita(conndb).set_data(id_partita=1,
                                          giocatore='prova 1',
                                          evento='goal6',
                                          time='00:00'
                                          # tempo="primo"
        ).save()


def main(argv):
    global conndb
    global root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    conndb = pymodel.abstract.create_sqlite_connection('handball.sqlite')

    schema(conndb)

    root = Tk()  # main window
    root.geometry('+100+100')
    root.wm_iconbitmap(bitmap='ball.ico')
    Label(root, text="Handball").pack(fill=X)
    Button(root, text="Squadre", command=crea_finestra_tabelle('Squadre', Squadra)).pack(fill=X)
    Button(root, text="Partite", command=crea_finestra_tabelle('Partite', Partita)).pack(fill=X)
    Button(root, text="Giocatori", command=crea_finestra_tabelle('Giocatori', Giocatore)).pack(fill=X)
    Button(root, text="Eventi", command=crea_finestra_tabelle('Eventi', Evento)).pack(fill=X)
    Button(root, text="Registra Partita",
           command=core.registra_partita.crea_finestra(conndb, root, finestre, destroy)
    ).pack(fill=X)
    Button(root, text="Statistiche", command=todo).pack(fill=X)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

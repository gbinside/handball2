#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymodel.abstract
import tkMessageBox
from Tkinter import *
import sys
import os

TEMPI = ('primo', 'secondo')
conndb = None
finestra_squadre = None


class Squadra(pymodel.abstract.Abstract):
    _tablename = 'squadre'
    _chiave = 'nome'
    _tipo_chiave = 'VARCHAR(255)'


class Giocatore(pymodel.abstract.Abstract):
    _tablename = 'giocatori'
    _chiave = 'nome'
    _tipo_chiave = 'VARCHAR(255)'


class Partita(pymodel.abstract.Abstract):
    _tablename = 'partite'
    _chiave = 'id'
    _tipo_chiave = 'INTEGER'
    _autoincrement = 'AUTOINCREMENT'


class Evento(pymodel.abstract.Abstract):
    _tablename = 'eventi'
    _chiave = 'codice'
    _tipo_chiave = 'VARCHAR(255)'


# _field_managers = {'info': json}
class DettaglioPartita(pymodel.abstract.Abstract):
    _tablename = 'dettalio_partite'
    _chiave = 'id'
    _tipo_chiave = 'INTEGER'
    _autoincrement = 'AUTOINCREMENT'


def todo():
    pass


def destroy(o):
    def fx():
        for k, v in globals().items():
            if v == o:
                del globals()[k]
                # globals()[k] == None
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
        finestra.withdraw()
        model = classe(conndb)
        model.new()
        try:
            model.load(entries[0].get())
        except pymodel.abstract.RecordNotFoundException:
            pass
        for e in entries:
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


def switch_to_eventi():
    global finestra_eventi
    if 'finestra_eventi' not in globals():
        finestra_eventi = Toplevel(root)
        finestra_eventi.grab_set()
        finestra_eventi.protocol("WM_DELETE_WINDOW", destroy(finestra_eventi))
        finestra_eventi.geometry('+250+100')
        finestra_eventi.wm_iconbitmap(bitmap='ball.ico')
        finestra_eventi.title('Eventi')
        s = Evento(conndb)
        c = s.collection()
        i = 0
        for i, e in enumerate(c[0]):
            Label(finestra_eventi, text=e).grid(row=1, column=i, sticky=W)
        row = -1
        entries = list()
        for row, riga in enumerate(c):
            row_entries = list()
            for i, e in enumerate(riga):
                # print e, riga
                entry = Entry(finestra_eventi)
                entry.myfieldname = e
                entry.insert(0, riga[e])
                entry.grid(row=2 + row, column=i, sticky=W)
                row_entries.append(entry)
            entries.append(row_entries)
            Button(finestra_eventi,
                   text='Cancella',
                   command=cancella_riga(finestra_eventi, Evento, riga[Evento.get_key()], switch_to_eventi)
                   ).grid(row=2 + row, column=i + 1)
        Button(finestra_eventi,
               text='Salva',
               command=salva(finestra_eventi, Evento, entries, switch_to_eventi)) \
            .grid(row=1, column=i + 1, sticky=N)

        new_entries = list()
        for i, e in enumerate(c[0]):
            entry = Entry(finestra_eventi)
            entry.grid(row=row + 3, column=i, sticky=W)
            entry.myfieldname = e
            new_entries.append(entry)
        Button(finestra_eventi,
               text='Aggiungi',
               command=salva_riga(finestra_eventi, Evento, new_entries, switch_to_eventi))\
            .grid(row=3 + row, column=i + 1)


def switch_to_squadre():
    global finestra_squadre
    if 'finestra_squadre' not in globals() or finestra_squadre is None:
        finestra_squadre = Toplevel(root)
        finestra_squadre.grab_set()
        finestra_squadre.protocol("WM_DELETE_WINDOW", destroy(finestra_squadre))
        finestra_squadre.geometry('+250+100')
        finestra_squadre.wm_iconbitmap(bitmap='ball.ico')
        finestra_squadre.title('Squadre')
        s = Squadra(conndb)
        c = s.collection()
        for i, e in enumerate(c[0]):
            Label(finestra_squadre, text=e).grid(row=1, column=i, sticky=W)
        row = -1
        i = 0
        for row, riga in enumerate(c):
            for i, e in enumerate(riga):
                # print e, riga
                entry = Entry(finestra_squadre)
                entry.insert(0, riga[e])
                entry.grid(row=2 + row, column=i, sticky=W)
            Button(finestra_squadre, text='Cancella',
                   command=cancella_riga(finestra_squadre, Squadra, riga[Squadra.get_key()], switch_to_squadre)).grid(
                row=2 + row,
                column=i + 1)
        for i, e in enumerate(c[0]):
            e = Entry(finestra_squadre)
            e.grid(row=row + 3, column=i, sticky=W)
        Button(finestra_squadre, text='Aggiungi', command=todo).grid(row=3 + row, column=i + 1)


def main(argv):
    global conndb
    global root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    conndb = pymodel.abstract.create_sqlite_connection('handball.sqlite')

    if len(Evento(conndb).collection_keys()) == 0:
        Evento(conndb).set('codice', 'ed') \
            .set('nome', 'errore difesa') \
            .set('icona', 'cancel.ico') \
            .set('colore_fondo', 'red') \
            .set('position', 10) \
            .save()
        Evento(conndb).set_data(codice='goal9',
                                nome='GOAL9',
                                icona='ball.ico',
                                colore_fondo='green',
                                position=20
                                ).save()
        Evento(conndb).set_data(codice='goal6',
                                nome='GOAL6',
                                icona='ball.ico',
                                colore_fondo='green',
                                position=30
                                ).save()
        Evento(conndb).set_data(codice='goalcontro',
                                nome='GOAL C',
                                icona='ball.ico',
                                colore_fondo='green',
                                position=40
                                ).save()
        Evento(conndb).set_data(codice='goalrigore',
                                nome='GOAL R',
                                icona='ball.ico',
                                colore_fondo='green',
                                position=50
                                ).save()
        Evento(conndb).set_data(codice='errore9',
                                nome='ERRORE GOAL9',
                                icona='cancel.ico',
                                colore_fondo='red',
                                position=60
                                ).save()
        Evento(conndb).set_data(codice='errore6',
                                nome='ERRORE GOAL6',
                                icona='cancel.ico',
                                colore_fondo='red',
                                position=70
                                ).save()
        Evento(conndb).set_data(codice='errorecontro',
                                nome='ERRORE GOAL C',
                                icona='cancel.ico',
                                colore_fondo='red',
                                position=80
                                ).save()
        Evento(conndb).set_data(codice='errorerigorre',
                                nome='ERRORE GOAL R',
                                icona='cancel.ico',
                                colore_fondo='red',
                                position=90
                                ).save()
        Evento(conndb).set_data(codice='pallarec',
                                nome='PR',
                                icona='angularbracket.ico',
                                colore_fondo='white',
                                position=100
                                ).save()
        Evento(conndb).set_data(codice='erroretec',
                                nome='ET',
                                icona='cancel.ico',
                                colore_fondo='red',
                                position=110
                                ).save()
        Evento(conndb).set_data(codice='ammonizione',
                                nome='AM',
                                icona='angularbrachet.ico',
                                colore_fondo='yellow',
                                position=120
                                ).save()
        Evento(conndb).set_data(codice='2min',
                                nome='2M',
                                icona='angularbrachet.ico',
                                colore_fondo='red',
                                position=130
                                ).save()
        Evento(conndb).set_data(codice='assist',
                                nome='AS',
                                icona='angularbrachet.ico',
                                colore_fondo='white',
                                position=140
                                ).save()
    if len(Squadra(conndb).collection_keys()) == 0:
        Squadra(conndb).set_data(nome='casalgrande', genere='maschile').save()
    if len(Giocatore(conndb).collection_keys()) == 0:
        Giocatore(conndb).set_data(nome='prova giocatore',
                                   squadra='casalgrande',
                                   numero='00',
                                   ruolo=''
                                   ).save()
    if len(Partita(conndb).collection_keys()) == 0:
        Partita(conndb).set_data(squadra='casalgrande',
                                 altra_squadra='montegrotto',
                                 data='01-01-2015',
                                 risultato_primo_tempo='0-0',
                                 risultato_secondo_tempo='0-0',
                                 risultato_finale='0-0'
                                 ).save()
    if len(DettaglioPartita(conndb).collection_keys()) == 0:
        DettaglioPartita(conndb).set_data(id_partita=1,
                                          giocatore='prova giocatore',
                                          evento='goal6',
                                          time='00:00',
                                          tempo="primo"
                                          ).save()

    root = Tk()  # main window
    root.geometry('+100+100')
    root.wm_iconbitmap(bitmap='ball.ico')
    Label(root, text="Handball").pack(fill=X)
    Button(root, text="Squadre", command=switch_to_squadre).pack(fill=X)
    Button(root, text="Partite", command=switch_to_squadre).pack(fill=X)
    Button(root, text="Giocatori", command=switch_to_squadre).pack(fill=X)
    Button(root, text="Eventi", command=switch_to_eventi).pack(fill=X)
    Button(root, text="Registra Partita", command=switch_to_squadre).pack(fill=X)
    Button(root, text="Statistiche", command=switch_to_squadre).pack(fill=X)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

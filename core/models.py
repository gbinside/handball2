#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymodel.abstract

__author__ = 'roberto'


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

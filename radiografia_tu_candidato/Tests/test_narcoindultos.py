# coding: utf8

import os
import unittest
import sys
sys.path.append("../..")

from radiografia_tu_candidato.narcoindultos import extract_conmutados
from radiografia_tu_candidato.narcoindultos import convert_to_minjus_url
from radiografia_tu_candidato.narcoindultos import has_alias
from radiografia_tu_candidato.narcoindultos import extract_alias


class NarcoindultosTest(unittest.TestCase):

    # extraer nombres de indultados de normas jurídicas
    def setUp(self):
        self.filename = os.path.join("Narcoindultos", "01-05-09.txt")

    def test_extraer_conmutados(self):
        expected_names = [
            u'ALZAMORA CARDOZO, VICTOR MARTIN',
            u'NUÑEZ VILCHEZ, JOSE SAMUEL',
            u'DEL PUERTO TARAZONA, FRANCISCO',
            u'DE LA PUERTA TARAZONA, FRANCISCO',
            u'DE LA PUERTA TARAZONA, FRANCISCO MIGUEL',
            u'DE LA PUERTA TARAZONA, FRANCISCO MIGUEL ALONSO',
            u'DE LA PUERTA TARAZONA,FRANCISCO MIGUEL ALONSO',
        ]
        i = 0
        for name in expected_names:
            result = extract_conmutados(self.filename)[i]
            obj = dict()
            obj['categoria'] = 'conmutado'
            obj['url'] = 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf'
            obj['nombres'] = [name]
            i += 1
            self.assertEqual(result, obj)

    def test_convert_to_minjus_url(self):
        result = convert_to_minjus_url(self.filename)
        result_goal = 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf'
        self.assertEqual(result, result_goal)

    def test_has_alias(self):
        line = "PARCO ZARATE, FOSTER ALFREDO o PARCO ZARATE, FOSTER RAFAEL,"
        result = has_alias(line)
        self.assertTrue(result)

        line = "PARCO ZARATE, FOSTER ALFREDO, conmutarle,"
        result = has_alias(line)
        self.assertFalse(result)

    def test_extract_alias(self):
        line = "7. CANALES PASTOR, MAICOL o PEREZ SALAS, RICARDO, conmutarle d"
        next_line = "04 años de pena privativa de libertad; la que vencerá el"
        expected_result = ["CANALES PASTOR, MAICOL", "PEREZ SALAS, RICARDO"]
        result = extract_alias(line, next_line)
        self.assertEqual(result, expected_result)

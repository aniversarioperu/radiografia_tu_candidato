#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import sys
sys.path.append("../..")

from radiografia_tu_candidato.narcoindultos import extract_conmutados
from radiografia_tu_candidato.narcoindultos import extract_indultados
from radiografia_tu_candidato.narcoindultos import convert_to_minjus_url
from radiografia_tu_candidato.narcoindultos import has_alias
from radiografia_tu_candidato.narcoindultos import extract_alias
from radiografia_tu_candidato.narcoindultos import parse_names


class NarcoindultosTest(unittest.TestCase):

    # extraer nombres de indultados de normas jurídicas
    def setUp(self):
        self.filename = os.path.join("Narcoindultos", "01-05-09.txt")

    def test_extract_conmutados(self):
        expected_names = [
            [u'ALZAMORA CARDOZO, VICTOR MARTIN'],
            [u'NUÑEZ VILCHEZ, JOSE SAMUEL'],
            [u'DEL PUERTO TARAZONA, FRANCISCO'],
            [u'DE LA PUERTA TARAZONA, FRANCISCO'],
            [u'DE LA PUERTA TARAZONA, FRANCISCO MIGUEL'],
            [u'DE LA PUERTA TARAZONA, FRANCISCO MIGUEL ALONSO'],
            [u'DE LA PUERTA TARAZONA,FRANCISCO MIGUEL ALONSO'],
            [u'CANALES PASTOR, MAICOL', u'PEREZ SALAS, RICARDO'],
            [
                u'CANALES PASTOR, MAICOL RICARDO1A',
                u'CANALES PASTOR, MAICOL RICARDO2A',
                u'CANALES PASTOR, MAICOL RICARDO3A',
            ],
            [
                u'CANALES PASTOR, MAICOL RICARDO1B',
                u'CANALES PASTOR, MAICOL RICARDO2B',
                u'CANALES PASTOR, MAICOL RICARDO3B',
            ],
        ]
        i = 0
        for name in expected_names:
            result = extract_conmutados(self.filename)[i]
            obj = dict()
            obj['categoria'] = 'conmutado'
            obj['url'] = 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf'
            obj['nombres'] = name
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

    def test_extract_alias1(self):
        line = "7. CANALES PASTOR, MAICOL o PEREZ SALAS, RICARDO, conmutarle d"
        next_line = "04 años de pena privativa de libertad; la que vencerá el"

        line = line.decode("utf-8")
        next_line = next_line.decode("utf-8")
        expected_result = ["CANALES PASTOR, MAICOL", "PEREZ SALAS, RICARDO"]
        result = extract_alias(line, next_line)
        self.assertEqual(result, expected_result)

    def test_extract_alias2(self):
        line = "8. CANA PAST, MAI RICARDO1 o CANA PAST, MAI RICARDO2 o CANA"
        next_line = "PAST, MAI RICARDO3, conmutarle de 06 años a 04 años de"

        line = line.decode("utf-8")
        next_line = next_line.decode("utf-8")
        expected_result = [
            "CANA PAST, MAI RICARDO1",
            "CANA PAST, MAI RICARDO2",
            "CANA PAST, MAI RICARDO3",
        ]
        result = extract_alias(line, next_line)
        self.assertEqual(result, expected_result)

    def test_extract_indultados(self):
        expected_names = [
            [u'BARRIOS, LUCIA MARTINEZ'],
            [
                u'PINTO LLANOS, MARIELLA SOFIA',
                u'PINTO LLANOS, MARIELA SOFIA',
            ],
            [u'CHAPARRO JURADO, CARLOS'],
        ]
        i = 0
        for name in expected_names:
            result = extract_indultados(self.filename)[i]
            obj = dict()
            obj['categoria'] = 'indultado'
            obj['url'] = 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf'
            obj['nombres'] = name
            i += 1
            self.assertEqual(result, obj)

    def test_parse_names(self):
        names = ["LUCIA MARTINEZ BARRIOS", ]
        result = parse_names(names)
        self.assertEqual(result, ["BARRIOS, LUCIA MARTINEZ"])


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)

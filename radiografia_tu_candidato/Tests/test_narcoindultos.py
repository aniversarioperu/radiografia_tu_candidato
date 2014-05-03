# coding: utf8

import os
import unittest
import sys
sys.path.append("../..")

from radiografia_tu_candidato.narcoindultos import extraer_conmutados
from radiografia_tu_candidato.narcoindultos import convert_to_minjus_url


class NarcoindultosTest(unittest.TestCase):
    # extraer nombres de indultados de normas jurídicas
    def setUp(self):
        self.filename = os.path.join("Narcoindultos", "01-05-09.txt")

    def test_extraer_conmutados(self):
        result = extraer_conmutados(self.filename)[0]
        obj = {
                'nombre': 'ALZAMORA CARDOZO, VICTOR MARTIN',
                'categoria': 'conmutado',
                'url': 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf',
                }
        self.assertEqual(result, obj)

    def test_convert_to_minjus_url(self):
        result = convert_to_minjus_url(self.filename)
        self.assertEqual(result, 'http://spij.minjus.gob.pe/Normas/textos/010509T.pdf')


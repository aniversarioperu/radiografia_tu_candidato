# coding: utf8

import os
import unittest
import sys
sys.path.append("../..")

from radiografia_tu_candidato.narcoindultos import extraer_conmutados


class NarcoindultosTest(unittest.TestCase):
    # extraer nombres de indultados de normas jurídicas
    def setUp(self):
        self.filename = os.path.join("Narcoindultos", "01-05-09.txt")

    def test_extraer_conmutados(self):
        result = extraer_conmutados(self.filename)[0]

        self.assertEqual(result, "ALZAMORA CARDOZO, VICTOR MARTIN")


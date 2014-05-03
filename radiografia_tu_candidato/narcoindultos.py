# coding=utf8
import codecs
import os.path
import re

import argparse
from argparse import RawTextHelpFormatter


def convert_to_minjus_url(filename):
    filename = os.path.basename(filename)
    filename = filename.replace("-", "")
    filename = filename.replace(".txt", "T.pdf")
    url = "http://spij.minjus.gob.pe/Normas/textos/" + filename
    return url

def extraer_conmutados(filename):
    individuos = []
    pattern = "([A-Z]+\s+[A-Z]+,\s[A-Z]+\s*[A-Z]*\s*[A-Z]*)"
    if os.path.isfile(filename):
        with codecs.open(filename, "r", "utf8") as f:
            for line in f:
                if 'conmutarle' in line.lower():
                    res = re.search(pattern, line.strip())
                    if res:
                        nombre = res.groups()[0]

                        # crear nuestro individuo
                        obj = {'nombre': nombre}
                        obj['categoria'] = "conmutado"
                        obj['url'] = convert_to_minjus_url(filename)
                        individuos.append(obj)
        return individuos


def main():
    description = """Extaer lista de conmutados e indultados de las normas
    jurídicas emitidas durante el 2do gobierno aprista."""

    parser = argparse.ArgumentParser(
            description=description,
            formatter_class=RawTextHelpFormatter,
            )
    parser.add_argument('-f', '--filename', action='store',
            metavar='01-01-08.txt',
            help='Norma Jurídica en formato TXT',
            required=True, dest='filename')

    args = parser.parse_args()
    if args.filename:
        print extraer_conmutados(args.filename.strip())


if __name__ == "__main__":
    main()

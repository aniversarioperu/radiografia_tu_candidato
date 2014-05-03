#!/usr/bin/env python
# coding=utf8
import codecs
import json
import os.path
import re

import argparse
from argparse import RawTextHelpFormatter


def extract_alias(line, next_line):
    line = line.strip() + " " + next_line.strip()
    print line
    line = re.sub("\s+", " ", line)
    line = line.split(" o ")
    names = []
    for i in line:
        # pattern for a person's name
        pattern = "((\w{2,}\s*)+,(\s*\w{2,})+)"
        res = re.search(pattern, i.strip(), re.UNICODE)
        if res:
            name = res.groups()[0].strip()
            names.append(name)
    return names


def has_alias(line):
    if ' o ' in line:
        return True
    else:
        return False


def convert_to_minjus_url(filename):
    filename = os.path.basename(filename)
    filename = filename.replace("-", "")
    filename = filename.replace(".txt", "T.pdf")
    url = "http://spij.minjus.gob.pe/Normas/textos/" + filename
    return url


def extract_conmutados(filename):
    individuals = []
    # pattern for a person's name
    pattern = "((\w{2,}\s*)+,(\s*\w{2,})+)"
    if os.path.isfile(filename):
        with codecs.open(filename, "r", "utf8") as f:
            for line in f:
                names = False
                if has_alias(line) is True:
                    next_line = f.next()
                    if 'conmutarle' in line.lower() or \
                            'conmutarle' in next_line.lower():
                        try:
                            names = extract_alias(line, next_line)
                        except StopIteration:
                            pass
                else:
                    if 'conmutarle' in line.lower():
                        res = re.search(pattern, line.strip(), re.UNICODE)
                        if res:
                            names = [res.groups()[0].strip()]

                if names:
                    # crear nuestro individuo
                    obj = {'nombres': names}
                    obj['categoria'] = "conmutado"
                    obj['url'] = convert_to_minjus_url(filename)
                    individuals.append(obj)

        return individuals


def main():
    description = """Extaer lista de conmutados e indultados de las normas
    jurídicas emitidas durante el 2do gobierno aprista."""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        '-f', '--filename', action='store',
        metavar='01-01-08.txt',
        help='Norma Jurídica en formato TXT',
        required=True, dest='filename',
    )

    args = parser.parse_args()
    if args.filename:
        print json.dumps(extract_conmutados(args.filename.strip()), indent=4)


if __name__ == "__main__":
    main()

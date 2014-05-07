#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import glob
import json
import os.path
import re
import sys
import unicodedata

import argparse
from argparse import RawTextHelpFormatter
from nameparser import HumanName


def parse_names(names):
    i = 0
    for item in names:
        out = ""
        for x in item.split():
            if x[0].isupper() and not x[1].islower():
                out += x + " "
        item = re.sub(",\s*$", "", out)
        item = re.sub("INDULTO POR RAZONES HUMANITARIAS\s*", "", item)

        name = HumanName(item)
        out = name.last + ", "
        out += name.first + " "
        out += name.middle
        names[i] = out.strip()
        i += 1
    return names


def extract_alias(line, next_line):
    line = line.strip() + " " + next_line.strip()
    line = re.sub("\s+", " ", line)
    if u' ó ' in line:
        line = line.split(u' ó ')
    elif ' o ' in line:
        line = line.split(" o ")
    else:
        line = [line]
    names = []
    for i in line:
        # pattern for a person's name
        pattern = "((\w{2,}\s*){2,},(\s*\w{2,})+)"
        res = re.search(pattern, i.strip(), re.UNICODE)
        if res:
            name = res.groups()[0].strip()
            names.append(name)
    return names


def has_alias(line):
    if ' o ' in line:
        return True
    elif u' ó ' in line:
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
    pattern = "((\w{2,}\s*){2,},(\s*\w{2,})+)"
    if os.path.isfile(filename):
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                names = False
                if has_alias(line) is True:
                    next_line = f.readline()
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


def extract_indultados(filename):
    individuals = []
    if os.path.isfile(filename):
        with codecs.open(filename, "r", encoding="utf-8") as f:
            for line in f:
                names = False
                if 'conceder indult' in line.lower():
                    try:
                        next_line = f.readline()
                        names = extract_alias(line, next_line)
                        names = parse_names(names)
                        if names is False:
                            # pattern for a person's name
                            pattern = "((\w{2,}\s*){2,},(\s*\w{2,})+)"
                            res = re.search(pattern, line.strip(), re.UNICODE)
                            if res:
                                names = [res.groups()[0].strip()]
                                names = parse_names(names)

                    except StopIteration:
                        pass

                if names:
                    # crear nuestro individuo
                    obj = {'nombres': names}
                    obj['categoria'] = "indultado"
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
        required=False, dest='filename',
    )
    parser.add_argument(
        '-d', '--directory', action='store',
        metavar='myfolder/',
        help='Folder contenindo Normas Jurídicas en formato TXT',
        required=False, dest='directory',
    )

    objects = []

    args = parser.parse_args()
    if args.filename:
        # print json.dumps(extract_conmutados(args.filename.strip()), indent=4)
        print(json.dumps(extract_indultados(args.filename.strip()), indent=4))
    elif args.directory:
        for filename in glob.glob(os.path.join(args.directory, "*txt")):
            objects += extract_indultados(filename)
            objects += extract_conmutados(filename)
    else:
        parser.print_help()
        sys.exit()

    with codecs.open("narcoindultados.json", "w", "utf-8") as handle:
        handle.write(json.dumps(objects, indent=4))

if __name__ == "__main__":
    main()

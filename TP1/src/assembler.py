#!/usr/bin/python3
# MIT License
# Copyright (c) 2023 David Alejandro Gonzalez Marquez
# ----------------------------------------------------------------------------
# Trabajo Practico - Dise~o de procesadores
# Materia: Programacion de softcores en FPGAs
# Programa de Profesoras/es Visitantes
# ----------------------------------------------------------------------------
# Este codigo esta pensado para que lo utilicen como ejemplo para armar
# el ensamblador de su propia arquitectura.
# No es obligatorio utilizar este codigo como base.

from __future__ import print_function

import sys
from common import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: assembler.py file.asm")
        exit(1)

    filename = sys.argv[1]
    if filename[-4:] == ".asm":
        outputH=filename[:-4] + ".txt"
        outputCV=filename[:-4] + "CodeVerilog.mem"
        outputDV=filename[:-4] + "DataVerilog.mem"
    else:
        outputH=filename + ".txt"
        outputCV=filename + "CodeVerilog.mem"
        outputDV=filename + "DataVerilog.mem"

    try:
        tokens = tokenizator(filename)
        instructions,labels = removeLabels(tokens,16)
        parseBytes, parseHuman = parseInstructions(instructions,labels)
        if parseBytes != None:
            printCodeVerilog(outputDV,parseBytes,1)
            printCodeVerilog(outputCV,parseBytes,2)
        if parseHuman != None:
            printHuman(outputH,parseHuman,labels,filename)

    except ValueError as e:
        print(e)
        

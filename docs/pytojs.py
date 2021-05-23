"""
Take files from /src and put then into /docs/python_modules

Allows running Python in the browser using WebAssembly
"""

import os
from pathlib import Path
src_file_list = os.listdir(Path('src'))   # list all source files of the main program
src_file_list = [f for f in src_file_list if f.endswith(".py")]     # remove __pycache__ etc.

p = Path('docs') / 'python_modules' / 'py_import.js'
with open (p, 'w') as f_w:          # write all external imports
            f_w.write(
"""
async function py_import () {
return (`
import sys
import io
import base64
import random
from collections import deque
import argparse
import datetime
from pathlib import Path
import numpy
import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt
`)
}
"""
            )

for src_f in src_file_list:
    p = Path('src') / src_f
    print(p)
    with open (p, 'r') as f_r:          # file read
        code = f_r.readlines()
        for i in range(len(code)):
            # remove all imports
            code[i] = "\n" if "import" in code[i] else code[i]

            # replace prints with writing to a HTML text area
            code[i] = str.replace(code[i], r"print(", "js.document.getElementById('text_output').value += '\\n' + str(")

            # \n has to be \\n to be escaped by JavaScript
            # line[:-1] to ignore end of line (EOL) new lines (\n)
            code[i] = str.replace(code[i][:-1], r'\n', r'\\n') + '\n'

            # turn of saving pdfs
            # TODO replace with better solution later
            code[i] = str.replace(code[i], "'save_pdf': True,", "'save_pdf': False,")

        p = Path('docs') / 'python_modules' / (src_f + '.js')
        with open (p, 'w') as f_w:      # file write
            js_func_name = src_f[:-3]   # remove ".py" from filename
            start_string = "async function " + js_func_name + "() {\n"
            start_string += "return (\n`\n"
            f_w.write(start_string)
            f_w.writelines(code)
            f_w.write("\n`)\n}\n")



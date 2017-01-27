#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import os
import subprocess
import shlex
import core.core as core
from flask import Flask, render_template, request


# ==========================
# Core START
# ==========================
config = core.config()
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
# ==========================
# Core END
# ==========================


# START Log files, global variables, etc.
global modules
global fwVersion
# END Log files, global variables, etc.


app = Flask(__name__)


# =======================================
# START - Routing
# =======================================
@app.before_first_request
def _run_on_start():
    pass


@app.route('/')
def index():
    return render_template('index.html', version=fwVersion)


@app.route('/start')
def start():
    module = request.args.get('module')
    if os.path.isfile('www/templates/modules/' + str(module) + '.html') and module:
        return render_template('modules/' + module + '.html', interface=INTERFACE_NET)
    else:
        if module:
            runmodule(module)
        return render_template('start.html', modules=modules, version=fwVersion)


def runmodule(module):
    try:
        call = ('xterm -hold -T ' + module + ' -bg black -fg white -geometry 200x50+1280+0 -e python ./wmd.py -m ' + module + ' -q')
        args = shlex.split(call)
        subprocess.Popen(args)
    except:
        print('Module does not exists')


# =====================================
# INTERACTIVE MODULES
# =====================================
@app.route('/sniffhttp_execute', methods=['POST'])
def execute():
    interface = request.form['interface']
    filter = request.form['filter']
    creds = request.form['creds']
    empty = request.form['empty']
    ignore = request.form['ignore']
    modulename = 'Sniff_HTTP'
    module = 'modules/sniff/sniff_http.py -r' + ' -int ' + interface + ' -f ' + filter + ' -c ' + creds + ' -e ' + empty + ' -i ' + ignore
    try:
        call = ('xterm -hold -T ' + modulename + ' -bg black -fg white -geometry 200x50+1280+0 -e python ./' + module)
        args = shlex.split(call)
        subprocess.Popen(args)
    except:
        print('Module does not exists')

    return render_template('start.html', modules=modules, version=fwVersion)
# =====================================
# INTERACTIVE MODULES
# =====================================


def main(modulesData, versionData):
    global modules
    global fwVersion
    modules = modulesData
    fwVersion = versionData
    app.run(host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0', extra_files=['./data/refresh'])

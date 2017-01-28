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
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])
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
    if not os.path.isfile('www/templates/modules/' + str(module) + '.html') and not module:
        return render_template('start.html', modules=modules, version=fwVersion)
    elif os.path.isfile('www/templates/modules/' + str(module) + '.html') and module:
        return render_template('modules/' + module + '.html', interfacen=INTERFACE_NET, interfacem=INTERFACE_MON)
    else:
        if module:
            runmodule(module)
        return render_template('start.html', modules=modules, version=fwVersion)


def runmodule(module):
    """Open and run module."""
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
def sniffhttp_execute():
    interface = request.form['interface']
    filter = request.form['filter']
    creds = request.form['creds']
    empty = request.form['empty']
    ignore = request.form['ignore']

    modulename = 'Sniff_HTTP'
    command = 'modules/sniff/sniff_http.py -r' + ' -int ' + interface + ' -f ' + filter + ' -c ' + creds + ' -e ' + empty + ' -i ' + ignore

    runmodule_args(modulename, command)

    return render_template('start.html', modules=modules, version=fwVersion)


@app.route('/apsniff_execute', methods=['POST'])
def apsniff_execute():
    interface_net = request.form['interface_net']
    interface_mon = request.form['interface_mon']
    gateway = request.form['gateway']
    sniffer = request.form['sniffer']
    proxy = request.form['proxy']
    target = request.form['target']
    sniff_log = request.form['sniff_log']
    ap_name = request.form['ap_name']
    ap_log = request.form['ap_log']
    beef = request.form['beef']
    # args_ap = request.form['args_ap']
    # args_sniff = request.form['args_sniff']

    modulename = 'AP_sniff'
    command = 'modules/sniff/apsniff.py -r' + ' -in ' + interface_net + ' -im ' + interface_mon + ' -g ' + gateway + ' -s ' + sniffer + ' -p ' + proxy + ' -t ' + target + ' -sl ' + sniff_log + ' -an ' + ap_name + ' -al ' + ap_log + ' -b ' + beef

    runmodule_args(modulename, command)

    return render_template('start.html', modules=modules, version=fwVersion)
# =====================================
# INTERACTIVE MODULES
# =====================================


def runmodule_args(modulename, command):
    """Run command with settings specified in browser."""
    try:
        call = ('xterm -hold -T ' + modulename + ' -bg black -fg white -geometry 200x50+1280+0 -e python ./' + command)
        args = shlex.split(call)
        subprocess.Popen(args)
    except:
        print('Module does not exists')
    return None


def main(modules_data, version_data):
    """Main function for starting."""
    global modules
    global fwVersion
    modules = modules_data
    fwVersion = version_data
    app.run(host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0', extra_files=['./data/refresh'])

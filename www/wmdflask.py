#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


from flask import Flask, render_template, request
import subprocess
import shlex


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


# @app.route('/alarm/deactivate', methods=['POST'])
# def alarm_deactivate():
#    pwd = request.form['submitPWD']
#
#    if pwd == "123":
#        return render_template('alarm.html')
#
#    elif fileStatus == 'ringing':
#        return render_template('alarmCode.html', tries=triesNr)
# =======================================
# END - Routing
# =======================================


def main(modulesData, versionData):
    global modules
    global fwVersion
    modules = modulesData
    fwVersion = versionData
    app.run(host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0', extra_files=['./data/refresh'])

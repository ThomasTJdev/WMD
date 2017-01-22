#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import configparser
from www import wmdflask
from core.modules import loadXML as cmodulesXML


config = configparser.ConfigParser()
config.read('core/config.ini')
fwVERSION = (config['FRAMEWORK']['VERSION'])
fwDATE = (config['FRAMEWORK']['DATE'])


def startWWW():
    """Start the webserver."""
    modulesXML = cmodulesXML()
    modules = showModules(modulesXML)
    wmdflask.main(modules, fwVERSION)


def showModules(root):
    """Get the modules and make them HTML ready."""
    html = ''

    # Get data from modules.xml
    default_data = {}
    for child in root.findall('module'):
        name = child.get('name')
        category = child.find('category').text
        type = child.find('type').text
        call = child.find('call').text
        description = child.find('description').text
        default_data[name + '\\' + category + '\\' + type + '\\' + call + '\\' + description] = (category + type + name + str('1'))

    # Start the looping through the data
    cat = 'start'
    counter = 0
    for k, v in sorted(default_data.items(), key=lambda x: x[1]):
        a, b, c, d, e = k.split('\\')
        if b != cat:
            # Finish current toolbox for ensuring it fill all columns
            if counter < 3 and cat != 'start':
                for i in range(counter, 3, 1):
                    html += '\n\t<div class=".col-md-4" style="display: inline-block; width: 29%; vertical-align: top; margin-left: 2%; margin-right: 2%;"></div>'
            counter = 0
            # Start new toolbox
            html += '\n</div>\n</div>\n\n<div class="toolbox blockbox">'
            html += '<a name="' + b.capitalize() + '" id="' + b.capitalize() + '"></a>'
            html += '\n<h1 class="editContent">' + b.capitalize() + '</h1>'
            html += '\n<p class="editContent"></p>'
            html += '\n<div class="toolboxholder">'
            cat = b

        # Insert module
        html += '\n\t<div class=".col-md-4" style="display: inline-block; width: 29%; vertical-align: top; margin-left: 2%; margin-right: 2%;" id="' + d + '">'
        html += '\n\t\t<div class="gobtn"><a href="/start?module=' + d + '#' + b.capitalize() + '" class="btn btn-primary btn-lg btn-wide toolboxbtn">' + d + '</a></div>'
        html += '\n\t\t<p><b>' + a + '</b></p>'
        html += '\n\t\t<p>' + e + '</p>'
        html += '\n\t</div>'
        if counter == 3:
            counter = 0
        counter += 1

    # Check the final module and ensure to fill out the columns
    if (counter - 1) < 3:
        for i in range(counter, 3, 1):
            html += '\n\t<div class=".col-md-4" style="display: inline-block; width: 29%; vertical-align: top; margin-left: 2%; margin-right: 2%;"></div>'

    # Closing tags
    html += '\n</div>'
    html += '\n</div>'

    # Removing closing tags in front
    return html[14:]

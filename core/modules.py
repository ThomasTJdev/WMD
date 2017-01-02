#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import xml.etree.ElementTree as ET
import importlib
import os
from core.colors import bc as bc


modulesXML = 'core/modules.xml'


def loadXML():
    tree = ET.parse(modulesXML)
    return tree.getroot()


def addModule(modulePath):
    print('\n')
    # Copy to tmp folder first
    os.system('cp ' + modulePath + ' ' + 'tmp/tmpImportModule.py')
    root = loadXML()
    importModule = importlib.import_module('tmp.tmpImportModule')
    print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module copied to tmp folder')
    print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module imported into memory')
    try:
        pass
    except:
        print(bc.FAIL + '  -> Error, can\'t find module: ' + modulePath + bc.ENDC)
        return None

    # Check if module name already exists
    try:
        for child in root.findall('module'):
            if importModule.options.Name == (child.get('name')):
                print(bc.FAIL + '  -> Error, module already exist with name: ' + importModule.options.Name + bc.ENDC)
                return None
    except:
        print(bc.FAIL + '  -> Error, something is wrong when checking the name against module.xml. Is the name defined in the module?' + bc.ENDC)

    # New category - then create it
    try:
        if os.path.isdir("modules/" + importModule.options.Category + "/") is False:
            print(bc.OKGREEN + '  -> Creating new category: ' + importModule.options.Category + bc.ENDC)
            os.system("mkdir modules/" + importModule.options.Category)
            os.system("touch modules/" + importModule.options.Category + "/__init__.py")
    except:
        print(bc.FAIL + '  -> Error, couldn\'t create new folder. Got enough user privileges?' + bc.ENDC)
        return None

    # Copying to tmp folder
    try:
        os.system('cp tmp/tmpImportModule.py' + ' ' + 'modules/' + importModule.options.Category + '/' + importModule.options.Modulename + '.py')
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Copying module to folder')
    except:
        print(bc.FAIL + '  -> Error, couldn\'t copy to folder. Got enough user privileges?' + bc.ENDC)
        return None

    # Add data to modules.xml
    print(bc.OKGREEN + '  ->' + bc.ENDC + ' Adding module to core.')
    try:
        if os.path.isfile('tmp/modules.xml.tmp'):
            os.system('rm tmp/modules.xml.tmp')
        os.system('cp ' + modulesXML + ' tmp/modules.xml.tmp')
        with open(modulesXML, 'r') as rawXML:
            data = rawXML.readlines()
            data = data[:-1]
        with open(modulesXML, 'w') as rawXML:
            rawXML.writelines(data)
        module = (
            '\t<module name="' + importModule.options.Name + '">' + '\n' +
            '\t\t<call>' + importModule.options.Call + '</call>' + '\n' +
            '\t\t<modulename>' + importModule.options.Modulename + '</modulename>' + '\n' +
            '\t\t<version>' + importModule.options.Version + '</version>' + '\n' +
            '\t\t<type>' + importModule.options.Type + '</type>' + '\n' +
            '\t\t<category>' + importModule.options.Category + '</category>' + '\n' +
            '\t\t<description>' + importModule.options.Description + '</description>' + '\n' +
            '\t</module>' + '\n' +
            '</data>'
        )
        with open(modulesXML, 'a') as rawXML:
            rawXML.writelines(module)
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module data: \n\n' + module[:-7])
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module succesfully added: ' + importModule.options.Name)
    except:
        print(bc.FAIL + '  -> Error, something went wrong while adding moduledata to modules.xml' + bc.ENDC)
        if os.path.isfile('tmp/modules.xml.tmp'):
            os.system('mv tmp/modules.xml.tmp ' + modulesXML)
            print(bc.FAIL + '  -> Backup of module.xml restored' + bc.ENDC)
        return None

    # Deleting module in tmp folder
    os.system('rm tmp/tmpImportModule.py')
    print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module in tmp folder deleted')
    print(bc.OKGREEN + '  !! ' + bc.ENDC + 'Thank you for adding a new module')


def removeModule(modulePath):
    print('')
    os.system('cp ' + modulePath + ' ' + 'tmp/tmpRemoveModule.py')
    print(bc.ENDC + '  -> ' + bc.ENDC + 'Module copied to tmp folder for backup.')
    removeModule = importlib.import_module('tmp.tmpRemoveModule')

    name = removeModule.options.Name
    mName = removeModule.options.Modulename
    category = removeModule.options.Category
    exists = 0
    print('  -> ' + 'Checking if module exists in XML file.' + bc.ENDC)
    try:
        with open(modulesXML) as infile, open(modulesXML + 'tmp', 'w') as outfile:
            for line in infile:
                if line.strip() == '<module name="' + name + '">':
                    exists = 1
                    break
                outfile.write(line)
            for line in infile:
                if line.strip() == '</module>':
                    break
            for line in infile:
                outfile.write(line)
        if exists == 1:
            os.system('mv core/modules.xmltmp core/modules.xml')
            print(bc.OKGREEN + '  -> ' + 'Module deleted in XML file. Name: ' + name + bc.ENDC)
        else:
            print(bc.WARN + '  -> ' + 'Module does not exists XML file. Name: ' + name + bc.ENDC)
            os.system('rm core/modules.xmltmp')
    except:
        print(bc.FAIL + '  -> ' + 'ERROR encountered while checking XML file.' + bc.ENDC)
        os.system('rm core/modules.xmltmp')

    print('  -> ' + 'Going for deletion of module in modulefolder.' + bc.ENDC)
    if os.path.isfile('modules/' + category + '/' + mName + '.py'):
        os.system('rm modules/' + category + '/' + mName + '.py')
        print(bc.OKGREEN + '  -> ' + 'Module deleted in folder. Category: ' + category + ' Modulename: ' + mName + bc.ENDC)
    else:
        print(bc.WARN + '  -> ' + 'Module does not exists in modulefolder. Path: ' + 'modules/' + category + '/' + mName + '.py' + bc.ENDC)


def showModules():
    root = loadXML()

    print('\n')
    print('%-*s %s%s' % (5, '', bc.FAIL, '## MODULES ##'))
    print('')
    print('%-*s%s %-*s %-*s %-*s %-*s %s %s' % (5, '', bc.FAIL, 15, 'CAT:', 30, 'NAME:', 12, 'TYPE:', 15, 'CALL:', 'DESCRIPTION:', bc.ENDC))
    default_data = {}
    for child in root.findall('module'):
        name = child.get('name')
        category = child.find('category').text
        type = child.find('type').text
        call = child.find('call').text
        description = child.find('description').text
        default_data[name + '\\' + category + '\\' + type + '\\' + call + '\\' + description] = (category + type + name + str('1'))

    type = ''
    for k, v in sorted(default_data.items(), key=lambda x: x[1]):
        a, b, c, d, e = k.split('\\')
        if b != type:
            print('%-*s %-*s' % (5, '', 40, '---------------------------------------------------------------------------------------------------------------------------------'))
            type = b
        print('%-*s %-*s %-*s %-*s %s%-*s %s%s %s' % (5, '', 15, b, 30, a, 12, c, bc.BOLD, 15, d, bc.ENDC, e, bc.ENDC))
    print('\n')


def showModuleData(Author, Name, Call, Category, Type, Version, Description, License, Datecreation, Lastmodified):
    print(
        ""
        + "\n\t" + bc.OKBLUE + "METADATA:" + bc.ENDC
        + "\n\t" + "---------"
        + "\n" + "\tArthur:\t\t" + Author
        + '\n' + '\tName:\t\t' + Name
        + '\n' + '\tCall:\t\t' + Call
        + '\n' + '\tCat:\t\t' + Category
        + '\n' + '\tType:\t\t' + Type
        + "\n" + "\tVersion:\t" + Version
        + "\n" + "\tDescription:\t" + Description
        + "\n" + "\tLicense:\t" + License
        + "\n" + "\tDatecreation:\t" + Datecreation
        + "\n" + "\tLastmodified:\t" + Lastmodified
        + "\n"
        )


def existModule(call):
    root = loadXML()
    check = 'false'
    for child in root.findall('module'):
        if call == (child.find('call').text):
            check = 'true'
    if check == 'false':
        return 'false'
    else:
        return 'true'


def loadModuleCategory(call):
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.find('category').text


def loadModuleMName(call):
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.find('modulename').text


def loadModuleName(call):
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.get('name')


def loadModulePath(call):
    call = cleanModuleCall(call)
    category = loadModuleCategory(call)
    modulename = loadModuleMName(call)
    return category + '.' + modulename


def loadModule(call):
    call = cleanModuleCall(call)
    if existModule(call) == 'true':
        modulepath = loadModulePath(call)
        # Check if file exists first
        return importlib.import_module('modules.' + modulepath)
    else:
        return (bc.WARN + '  ERROR, no module call found with: ' + call + bc.ENDC)


def cleanModuleCall(call):
    call = call.strip('[]\'')
    return call

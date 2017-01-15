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
    """Load the XML tree."""
    tree = ET.parse(modulesXML)
    return tree.getroot()


def addModule(module_path):
    """Add a module to the WMDframe."""
    print('\n')
    # Copy to tmp folder first
    os.system('cp ' + module_path + ' ' + 'tmp/tmpImportModule.py')
    print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module copied to tmp folder')
    root = loadXML()
    try:
        importModule = importlib.import_module('tmp.tmpImportModule')
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module imported into memory')
    except:
        print(bc.FAIL + '  -> Error, can\'t find module: ' + module_path + bc.ENDC)
        return None

    # Check if module name already exists
    try:
        for child in root.findall('module'):
            if importModule.Options.Name == (child.get('name')):
                print(bc.FAIL + '  -> Error, module already exist with name: ' + importModule.Options.Name + bc.ENDC)
                return None
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Modulename does not exist already')
    except:
        print(bc.FAIL + '  -> Error, something is wrong when checking the name against module.xml. Is the name defined in the module?' + bc.ENDC)
        return None

    # New category - then create it
    try:
        if os.path.isdir("modules/" + importModule.Options.Category + "/") is False:
            print(bc.OKGREEN + '  -> Creating new category: ' + importModule.Options.Category + bc.ENDC)
            os.system("mkdir modules/" + importModule.Options.Category)
            os.system("touch modules/" + importModule.Options.Category + "/__init__.py")
    except:
        print(bc.FAIL + '  -> Error, couldn\'t create new folder. Got enough user privileges?' + bc.ENDC)
        return None

    # Copying to tmp folder
    try:
        os.system('cp tmp/tmpImportModule.py' + ' ' + 'modules/' + importModule.Options.Category + '/' + importModule.Options.Modulename + '.py')
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
            '\t<module name="' + importModule.Options.Name + '">' + '\n' +
            '\t\t<call>' + importModule.Options.Call + '</call>' + '\n' +
            '\t\t<modulename>' + importModule.Options.Modulename + '</modulename>' + '\n' +
            '\t\t<version>' + importModule.Options.Version + '</version>' + '\n' +
            '\t\t<type>' + importModule.Options.Type + '</type>' + '\n' +
            '\t\t<category>' + importModule.Options.Category + '</category>' + '\n' +
            '\t\t<description>' + importModule.Options.Description + '</description>' + '\n' +
            '\t</module>' + '\n' +
            '</data>'
        )
        with open(modulesXML, 'a') as rawXML:
            rawXML.writelines(module)
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module data: \n\n' + module[:-7])
        print(bc.OKGREEN + '  -> ' + bc.ENDC + 'Module succesfully added: ' + importModule.Options.Name)
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


def removeModule(module_path):
    """Remove a module from the WMDframe - ALPHA."""
    print('')
    os.system('cp ' + module_path + ' ' + 'tmp/tmpRemoveModule.py')
    print(bc.ENDC + '  -> ' + bc.ENDC + 'Module copied to tmp folder for backup.')
    removeModule = importlib.import_module('tmp.tmpRemoveModule')

    name = removeModule.Options.Name
    mName = removeModule.Options.Modulename
    category = removeModule.Options.Category
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
    """Show all modules."""
    root = loadXML()

    print('\n')
    print('%-*s %s%s' % (5, '', bc.FAIL, '## MODULES ##'))
    print('')
    # print('%-*s%s %-*s | %-*s | %-*s | %-*s | %s %s' % (5, '', bc.FAIL, 15, 'CAT:', 12, 'TYPE:', 15, 'CALL:', 30, 'NAME:', 'DESCRIPTION:', bc.ENDC))
    print('%-*s%s %-*s %-*s %-*s %-*s %s %s' % (5, '', bc.FAIL, 15, 'CAT:', 12, 'TYPE:', 15, 'CALL:', 30, 'NAME:', 'DESCRIPTION:', bc.ENDC))
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
        # print('%-*s %-*s | %-*s | %s%-*s | %s%-*s | %s %s' % (5, '', 15, b, 12, c, bc.BOLD, 15, d, bc.ENDC, 30, a, e, bc.ENDC))
        print('%-*s %-*s %-*s %s%-*s %s%-*s %s %s' % (5, '', 15, b, 12, c, bc.BOLD, 15, d, bc.ENDC, 30, a, e, bc.ENDC))
    print('\n')


def showModuleData(author, name, call, category, type, version, description, license, datecreation, lastmodified):
    """Show a specific modules information."""
    print(
        '' +
        '\n\t' + bc.OKBLUE + 'METADATA:' + bc.ENDC +
        '\n\t' + '---------' +
        '\n' + '\tArthur:\t\t' + author +
        '\n' + '\tName:\t\t' + name +
        '\n' + '\tCall:\t\t' + call +
        '\n' + '\tCat:\t\t' + category +
        '\n' + '\tType:\t\t' + type +
        '\n' + '\tVersion:\t' + version +
        '\n' + '\tDescription:\t' + description +
        '\n' + '\tLicense:\t' + license +
        '\n' + '\tDatecreation:\t' + datecreation +
        '\n' + '\tLastmodified:\t' + lastmodified +
        '\n'
    )


def existModule(call):
    """Check if the modules exists in the modules.xml."""
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
    """Get module category."""
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.find('category').text


def loadModuleMName(call):
    """Get module filename."""
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.find('modulename').text


def loadModuleName(call):
    """Get module name."""
    root = loadXML()
    for child in root.findall('module'):
        if call == (child.find('call').text):
            return child.get('name')


def loadModulePath(call):
    """Get module path."""
    call = cleanModuleCall(call)
    category = loadModuleCategory(call)
    modulename = loadModuleMName(call)
    return category + '.' + modulename


def loadModule(call):
    """Load module for running."""
    call = cleanModuleCall(call)
    if existModule(call) == 'true':
        modulepath = loadModulePath(call)
        # Check if file exists first
        return importlib.import_module('modules.' + modulepath)
    else:
        return (bc.WARN + '  ERROR, no module call found with: ' + call + bc.ENDC)


def cleanModuleCall(call):
    """Simple cleaner to strip unwanted chars."""
    call = call.strip('[]\'')
    return call

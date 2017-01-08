#!/usr/bin/python python3

import os
import requests
from bs4 import BeautifulSoup
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


# START Log files, global variables, etc.
filename = 'files/blackarchtools.txt'
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Search hacktools'
    Call = 'searchht'
    Modulename = 'searchhacktools'
    Category = 'tools'
    Type = 'search'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Searchengine for hackingtools'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, searchName, searchCategory, searchDescription, searchFull):
        self.name = searchName
        self.category = searchCategory
        self.description = searchDescription
        self.full = searchFull
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('name', 'category', 'description', 'full')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'name:', 8, 'n', 18, self.name, 'Search in tool name'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'category:', 8, 'n', 18, self.category, 'Search in tool category'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'description:', 8, 'n', 18, self.description, 'Search in tool description'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'full:', 8, 'n', 18, self.full, 'Search across all (overrides parameter search)'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (16, 'run', 'Search for hacktools'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'data [toolname]', 'Specific data for the tool'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'update', 'Updates toolslist'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'cat', 'Show categories'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'invoke', 'Invoke module'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'exit', 'Exit'))
            + '\n'
            )

    # Show all info
    def show_all(self):
        cmodules.showModuleData(
            options.Author,
            options.Name,
            options.Call,
            options.Category,
            options.Type,
            options.Version,
            options.Description,
            options.License,
            options.Datecreation,
            options.Lastmodified
            )
        self.show_commands()
        self.show_opt()
# END OPTIONS


def onstart():
    if not os.path.isfile(filename):
        os.mknod(filename)
        print(bc.WARN + '\t[!]  Database is empty. Run the command "update" to gather data about the tools.' + bc. ENDC)


# Internal usage
def searchdata():
    with open(filename, 'r') as f:
        return f.readlines()


def getcategories():
    searchlines = searchdata()
    categories = ''
    for i, line in enumerate(searchlines):
        try:
            try:
                blackName, blackVersion, blackDescription, blackCategory, blackLink = line.split('\\\\')
            except:
                blackName, blackVersion, blackDescription, blackCategory = line.split('\\\\')
            blackCategory = blackCategory.replace(' blackarch-', '')
            blackCategory = blackCategory.replace('-', '')
            categories += blackCategory
        except:
            pass

    lst = (set(categories.split()))
    lst = (sorted(lst))
    print('')
    print(bc.OKBLUE + '\t' + 'CATEGORY' + bc.ENDC)
    for item in lst:
        print('\t-> ' + item)
    print('')


# Fullsearch search
def fullSearch(searchString):
    searchlines = searchdata()
    counter = 0
    print('')
    print(bc.OKBLUE + '\t' + ('%-*s %-*s %-*s %s' % (5, '[X]', 22, 'NAME', 14, 'CATEGORY', 'DESCRIPTION')) + bc.ENDC)
    print(bc.OKBLUE + '\t' + ('%-*s %-*s %-*s %s' % (5, '---', 22, '----', 14, '--------', '-----------')) + bc.ENDC)
    for i, line in enumerate(searchlines):
        if searchString in line:
            try:
                try:
                    blackName, blackVersion, blackDescription, blackCategory, blackLink = line.split('\\\\')
                except:
                    blackName, blackVersion, blackDescription, blackCategory = line.split('\\\\')
                blackCategory = blackCategory.replace(' blackarch-', '')
                counter += 1
                print('\t' + ('%-*s %-*s %-*s %s' % (5, '[' + str(counter) + ']', 22, blackName, 14, blackCategory, blackDescription)))
            except:
                print('\tEncountered an error with: ' + str(line))
    print('')


def multiSearch(searchString1, searchString2, searchString3):
    searchlines = searchdata()
    counter = 0
    print('')
    print(bc.OKBLUE + '\t' + ('%-*s %-*s %-*s %s' % (5, '[X]', 22, 'NAME', 14, 'CATEGORY', 'DESCRIPTION')) + bc.ENDC)
    print(bc.OKBLUE + '\t' + ('%-*s %-*s %-*s %s' % (5, '---', 22, '----', 14, '--------', '-----------')) + bc.ENDC)
    for i, line in enumerate(searchlines):
        try:
            try:
                blackName, blackVersion, blackDescription, blackCategory, blackLink = line.split('\\\\')
            except:
                blackName, blackVersion, blackDescription, blackCategory = line.split('\\\\')
            blackCategory = blackCategory.strip('\n').replace(' blackarch-', '')
            if searchString1 in blackName and searchString2 in blackCategory and searchString3 in blackDescription:
                counter += 1
                print('\t' + ('%-*s %-*s %-*s %s' % (5, '[' + str(counter) + ']', 22, blackName, 14, blackCategory, blackDescription)))
        except:
            # Skipped malformed or blank lines
            pass
    print('')


def run(searchString1, searchString2, searchString3, searchString4):
    if searchString4:
        fullSearch(searchString4)
    else:
        multiSearch(searchString1, searchString2, searchString3)


# Get info on single tool
def infoSearch(searchString1):
    searchlines = searchdata()
    counter = 0
    for i, line in enumerate(searchlines):
        try:
            try:
                blackName, blackVersion, blackDescription, blackCategory, blackLink = line.split('\\\\')
            except:
                blackName, blackVersion, blackDescription, blackCategory = line.split('\\\\')
            blackCategory = blackCategory.strip('\n').replace(' blackarch-', '')
            if searchString1 in blackName:
                counter += 1
                print(bc.OKBLUE + '\n\tINFO' + bc.ENDC)
                print(bc.OKBLUE + '\tNAME       : ' + bc.ENDC + blackName)
                print(bc.OKBLUE + '\tCATEGORY   : ' + bc.ENDC + blackCategory)
                if blackLink:
                    print(bc.OKBLUE + '\tLINK       : ' + bc.ENDC + blackLink.strip('\n'))
                else:
                    print(bc.OKBLUE + '\tLINK       : ' + bc.ENDC + 'None available')
                print(bc.OKBLUE + '\tDESCRIPTION: ' + bc.ENDC + blackDescription + '\n')
        except:
            pass


def update():
    print('\n\t[*]  Started gathering data from blackarch.')
    address = "https://blackarch.org/tools.html"
    r = requests.get(address)
    soup = BeautifulSoup(r.text, 'lxml')
    data = ''

    for d in soup.find_all('tr'):
        datatmp = ''
        for a in d.find_all('td'):
            datatmp += ('\\\\' + a.text)
        for a in d.find_all('a', target='_blank', href=True):
            datatmp += (a['href'])
        data += datatmp[2:-2]
        data += '\n'

    if not data.isspace():
        with open(filename, 'w') as file:
            file.write(data)

    print(bc.OKGREEN + '\t[+]' + bc.ENDC + '  Database created. You can now start searching.\n')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'hacktools:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'run' in userinput[:1]:
        run(sop.name, sop.category, sop.description, sop.full)
    elif 'data' in userinput[:1]:
        s1 = str(userinput[1:2]).strip('[]\'')
        infoSearch(s1)
    elif 'cat' in userinput[:1]:
        getcategories()
    elif 'update' in userinput[:1]:
        update()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + '\n    Error, no options for: ' + useroption + '\n' + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + '\n')
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('     _____                      __       __  __           __  ______            __      ')
    print('    / ___/___  ____ ___________/ /_     / / / /___ ______/ /_/_  __/___  ____  / /____  ')
    print('    \__ \/ _ \/ __ `/ ___/ ___/ __ \   / /_/ / __ `/ ___/ //_// / / __ \/ __ \/ / ___/  ')
    print('   ___/ /  __/ /_/ / /  / /__/ / / /  / __  / /_/ / /__/ ,<  / / / /_/ / /_/ / (__  )   ')
    print('  /____/\___/\__,_/_/   \___/_/ /_/  /_/ /_/\__,_/\___/_/|_|/_/  \____/\____/_/____/    ')
    print('                                                                                        ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkNetConnectionV()
    onstart()
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options('', '', '', '')
    console()

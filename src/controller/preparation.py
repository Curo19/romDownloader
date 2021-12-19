import os.path
import csv
import requests
import pandas

from bs4 import BeautifulSoup
from .romDataEntry import romDataEntry

class preparation(object):
    def __init__(self):
        print("------------------------")
        print("Calling preparation class")
        print("------------------------")

    def writeDataEntryToFile(self, path, entry):
        print("Starting writing entry to file")
        print("----------------")

        print("Path: ",path)
        print("RomName: ", entry.get_romName())

        # append to the end of file the data entry.
        with open(path, 'a', newline='') as csvfile:

            romCsvWriter = csv.writer(csvfile, delimiter=',',
                                      quotechar=',', quoting=csv.QUOTE_MINIMAL)
            romCsvWriter.writerow([entry.get_romName(), entry.get_console(), entry.get_fileSize(), entry.get_fileType(),
                                   entry.get_locationUrl(), entry.get_downloadUrl(), entry.get_dateFirstAdded(),
                                   entry.get_dateLastUpDated(), entry.get_flagDownload(),
                                   entry.get_previouslyDownloaded(),entry.get_rating(), entry.get_localPath(),
                                   entry.get_notes()])

        print("----------------")
        print("Ending write entry to file")

    def reportReader(self, path):
        with open(path, newline='') as csvfile:
            romCsvReport = csv.reader(csvfile, delimiter=' ', quotechar=',')
        for row in romCsvReport:
            print(', '.join(row))

    def vimmsLairSiteScan(self, path):
        # start scanning vimms lair. for rom information.
        print("Starting vimm lair scan")
        print("----------------")
        # start with consoles read them in and start creating a list.

        # access vimms lair
        vimmsConsoleListRequest = requests.get('https://vimm.net/?p=vault')

        parsedConsoleListHtml = BeautifulSoup(vimmsConsoleListRequest.text, 'html.parser')

        consoleTableHtml = parsedConsoleListHtml.table.findAll("a")

        # find console list and parse it out.
        consolelist = []
        for consoleTag in consoleTableHtml:
            consolelist.append([consoleTag.contents[0],consoleTag['href']])
        print("----------------")
        for consoles in consolelist:
            print("Name:", consoles[0])
            print("Url:", consoles[1])

            # list out all alphanumeric links.
            consoleVault = "https://vimm.net" + consoles[1]
            print("Console Vault is: ", consoleVault)
            consoleRequest = requests.get(consoleVault)
            parsedconsoleRequestHtml = BeautifulSoup(consoleRequest.text, 'html.parser')

            #print(parsedconsoleRequestHtml.prettify())

            consoleVaultMenu = parsedconsoleRequestHtml.find_all("td", class_="menu")[0].find_all("a")

            print("-------ConsoleVaultMenu--------")
            print(consoleVaultMenu)
            print("----------------")

            # find console list and parse it out.
            consoleVaultMenulist = []
            for consoleMenuTag in consoleVaultMenu:
                consoleVaultMenulist.append([consoleMenuTag.contents[0], consoleMenuTag['href']])
            print("----------------")
            for consoleMenuEntry in consoleVaultMenulist:
                print("Name:", consoleMenuEntry[0])
                print("Url:", consoleMenuEntry[1])

                # navigate into first link
                romsInCategorylistUrl = "https://vimm.net" + consoleMenuEntry[1]

                romsInCategorylist = requests.get(romsInCategorylistUrl)
                romsInCategory = BeautifulSoup(romsInCategorylist.text, 'html.parser')

                print("--------tbody--------")
                try:
                    romsListCat = romsInCategory.find_all("table", class_="rounded centered cellpadding1 hovertable")[
                    0].find_all("a")
                    print("----------------")

                    # list out all games in list and if there is a other page list them aswell.

                    # find console list and parse it out.
                    romList = []
                    for rom in romsListCat:
                        if "/vault" in rom['href'] and "rating" not in rom['href']:
                            romList.append([rom.contents[0], rom['href']])
                    print("--------Romlist--------")
                    for test in romList:
                        print("Name:", test[0])
                        print("Url:", test[1])

                        # insert data into csv report.
                        romEntry = romDataEntry()
                        print("--------Rom Data Extracted from Vimms lair--------")
                        print("Rom Name: ",test[0].replace(",", "").replace("\"",""))
                        romEntry.set_romName(test[0].replace(",", "").replace("\"",""))
                        print("Console Name: ",consoles[0])
                        romEntry.set_console(consoles[0])
                        print("Rom Page Url: https://vimm.net", test[1].replace(" ",""))
                        romEntry.set_locationUrl("https://vimm.net" + test[1])
                        romId = test[1].replace("/vault/","")

                        print("----------------")
                        romPageFileSizeResponse = requests.get("https://vimm.net" + test[1])
                        romPageFileSizeParsed = BeautifulSoup(romPageFileSizeResponse.text, 'html.parser')
                        romSize = romPageFileSizeParsed.find("td", id="download_size").contents[0]
                        print("Rom file Size:", romSize)

                        romEntry.set_fileSize(romSize)

                        romDownloadtag = romPageFileSizeParsed.find("form", id="download_form")
                        print("Rom download tag:", romDownloadtag)

                        romDownloadServer = romPageFileSizeParsed.find("form", id="download_form")["action"]
                        print("Rom download server action:", romDownloadServer)

                        romMediaId = romPageFileSizeParsed.find("form", id="download_form").contents[0]["value"]
                        print("Rom media id:", romMediaId)

                        romDownloadUrl = "https:"+romDownloadServer+"?mediaId=" +romMediaId+ "&download=Download"

                        print("Rom Download Url: ", romDownloadUrl)
                        romEntry.set_downloadUrl(romDownloadUrl)

                        self.writeDataEntryToFile(path, romEntry)
                except:
                    print("No roms detected in category")

                print("----------------")

            print("----------------")

        print("----------------")


        # note it looks like download request is https://download2.vimm.net/download/?mediaId=3 with 3 being the vault id captured in the previous url..
        # that Is what i will set for the moment until I start writing the download rom fucntion and being more specific.

        # add all information to romEntry and write it to file. Then cleanup and move onto next in list.

        print("----------------")
        print("Ending vimmLairScan")

    def geneateNewConfig(self, path):
        print("Starting config generation process")
        print("----------------")
        print(path)
        print("Searching for config...")
        if os.path.isfile(path):
            print("Config file detected")
        else:
            print("No config file detected")
            f = open(path, "a")
            f.write(
                "RomName,Console,FileSize,FileType,LocationUrl,DownloadUrl,DateFirstAdded, DateLastUpdated,FlagDownload,PreviouslyDownloaded,Rating,LocalPath,Notes\n")
            f.close()

        self.vimmsLairSiteScan(path)

        print("----------------")
        print("Ending config generation process")

    def updateExistingConfig(self, path, console, value):
        print("Starting update process")
        print("----------------")

        print("Searching for config...")
        if os.path.isfile(path) and console != False:
            print("Config file detected")
            configRomsData = pandas.read_csv(path, index_col=0)

            consoleFilter = (configRomsData["Console"] == console)

            if value == "True":
                configRomsData.loc[consoleFilter, "FlagDownload"] = "True"
            else:
                configRomsData.loc[consoleFilter, "FlagDownload"] = "False"

            configRomsData.to_csv(path)
        else:
            print("FAIL -- Unable to detect config file")

        print("----------------")
        print("Ending update")

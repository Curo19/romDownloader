import argh
import os.path
import configparser
import requests
import httplib2
import string
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

CONFIGFILE="./resources/config.ini"
HOSTURL=""
ROMDOWNLOADPATH=""
REPORTSPATH=""
ROMDOWNLOADLAYOUT=""
ROMREPORT="romReport.csv"
consolesList = []

# @argh.arg('--output', '-o', help="Set the output report name")
# @argh.arg('updateConfig', help="Update existing config")
# @argh.arg('enableDownload', help="Enable all Downloads within a console type.")

def startup():
    print("----------------")
    print("Checking if config file and required folders are present.")
    print("----------------")
    # check if config is present. 
    if (os.path.isfile(CONFIGFILE)):
        print("The config file is present.")
        
    else:
        print("The config file is not detected.... creating config file with defaults.")
        configSetup()

    # Print config file varaibles and values for testing.
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIGFILE)
    
    global HOSTURL
    global ROMDOWNLOADPATH
    global REPORTSPATH
    global ROMDOWNLOADLAYOUT

    HOSTURL = config_obj["BasicConfig"]["hosturl"]
    ROMDOWNLOADPATH = config_obj["BasicConfig"]["romdownloadpath"]
    REPORTSPATH = config_obj["BasicConfig"]["reportspath"]
    ROMDOWNLOADLAYOUT = config_obj["BasicConfig"]["romdownloadlayout"]

    print("----------------")
    print("Config Values")
    print("HOSTURL: "+HOSTURL)
    print("ROMDOWNLOADPATH: "+ROMDOWNLOADPATH)
    print("REPORTSPATH: "+REPORTSPATH)
    print("ROMDOWNLOADLAYOUT: "+ROMDOWNLOADLAYOUT)
    print("----------------")


    # check if rom download folders is present.
    if (os.path.isdir(ROMDOWNLOADPATH)):
        print("The rom download folder is present.")
        
    else:
        print("The rom download folder is not detected.... creating rom download folder.")
        os.mkdir(ROMDOWNLOADPATH)

    # check if report folder is present.
    if (os.path.isdir(REPORTSPATH)):
        print("The reports folder is present.")
        
    else:
        print("The reports folder is not detected.... creating reports folder.")
        os.mkdir(REPORTSPATH)

    print("----------------")
    print("Checks complete")
    print("----------------")

    return HOSTURL,ROMDOWNLOADPATH,REPORTSPATH,ROMDOWNLOADLAYOUT

def configSetup():
    print("----------------")
    print("Creating Default config file")
    print("----------------")

    config = configparser.ConfigParser()

    # Add the structure to the file we will create
    config.add_section('BasicConfig')
    config.set('BasicConfig', 'HOSTURL', 'https://vimm.net')
    config.set('BasicConfig', 'ROMDOWNLOADPATH', './roms')
    config.set('BasicConfig', 'REPORTSPATH', './report')
    config.set('BasicConfig', 'ROMDOWNLOADLAYOUT', 'alphabetical')

    # Write the new structure to the new file
    with open(CONFIGFILE, 'w') as configfile:
        config.write(configfile)


def getMemorySize(romPageUrl):

    http = httplib2.Http()
    status, response = http.request(romPageUrl)

    soup = BeautifulSoup(response,features="html.parser")

    
    try:
        memorySize = soup.find(id="download_size")
        memSizeString = memorySize.get_text()
        print("The memory size is : "+memSizeString)
    except Exception as e:
        print('No file present: '+ str(e))
        memSizeString = "NA"

    return memSizeString

def romDownload(consoleFolder, downloadUrl):
    print("----------------")
    print("Begining to download rom...")
    print("----------------")

    # Setup file download path

    print("Download folder is set to: -"+ ROMDOWNLOADPATH+"\\"+consoleFolder)
    fullpath = os.path.abspath(ROMDOWNLOADPATH)
    print("The fullpath is :"+fullpath)

    # check if rom download folders is present.
    if (os.path.isdir(fullpath+"/"+consoleFolder)):
        print("The download folder is present.")
        
    else:
        print("The download folder is not detected.... creating rom download folder.")
        os.mkdir(fullpath+"/"+consoleFolder)

    # Start rom download action note download progress bar if possible 

    options = Options()
    options.headless = True

    prefs = {"download.default_directory" : fullpath+"\\"+consoleFolder}
    options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=options)
    driver.get(downloadUrl)
    
    print(driver.title)
    downloadButton = driver.find_element(By.CSS_SELECTOR, "form#download_form > button")
    driver.execute_script("arguments[0].click();", downloadButton)

    while True:
        time.sleep(5)
        if not any(fname.endswith('.crdownload') for fname in os.listdir(fullpath+"\\"+consoleFolder)):
            # break out if file .crdownload doesn't exist. Download complete
            print("Rom download complete.")
            break
        print("Temp file .crdownload detected.... still downloadinng rom")
    
    print(driver.title)
    driver.close()
    

    # post download actions and cleanup note: delete vimmsLair if present.

    print("----------------")
    print("Ending Download rom process.")
    print("----------------")

def updateReportEntryStatus(entryloc, statusUpdate):
    print("Attepting to update entry : "+entryloc)
    data = pd.read_csv(REPORTSPATH+"/"+ROMREPORT, header=0)
    data.loc[int(entryloc), 'Status'] = statusUpdate
    data.to_csv(REPORTSPATH+"/"+ROMREPORT, index=False)

    updatedList = data.loc[data['Status'] == statusUpdate]

    print("Printing Output of updatedList:")
    print(updatedList)

def downloadRoms():
    print("----------------")
    print("Starting Download rom process.")
    print("----------------")

    # checking if reporting csv file is present.

    reportPathFull = REPORTSPATH+"/"+ROMREPORT
    print("Checking if report file is present within: ",reportPathFull)
 
    if (os.path.isfile(reportPathFull)):
        print("The report file is present.")

        data = pd.read_csv(reportPathFull, header=0)

        try:
            #clean up inprogress section
            romsListInProgress = data.loc[data['Status'] == 'InProgress']
            print("Printing Output of report:")
            print(romsListInProgress)
            
            for index, rINPROGRESS in romsListInProgress.iterrows():
                updateReportEntryStatus(str(index),"enable")
                print("rom which is in progress - "+rINPROGRESS["Console"]+" - "+rINPROGRESS["WebUrl"]+"")
                
        except Exception as e:
            print('No roms in progress detected note throws error for the moment: '+ str(e))

        

        

        romsListToDownload = data.loc[data['Status'] == 'enable']

        print("Printing Output of report:")
        print(romsListToDownload)

        for index, rDownload in romsListToDownload.iterrows():
            updateReportEntryStatus(str(index),"InProgress")
            print("rom to download - "+rDownload["Console"]+" - "+rDownload["WebUrl"]+"")
            try:
                romDownload(rDownload["Console"], rDownload["WebUrl"])
                updateReportEntryStatus(str(index),"done")
            except Exception as e:
                print('Error in rom download attempt download: '+ str(e))
                updateReportEntryStatus(str(index),"error")
            

    else:
        print("The report file is not detected.... suggest creating report with populateReport command")
        

    # request user if they what console they want to download all, or specific console. 

    # Checking if any roms are marked to be downloaded and or in progress

    # Check if roms download folder specifed in config file is present and create it if required. 

    # Start rom download.

    print("----------------")
    print("Ending Download rom process.")
    print("----------------")

def reportGeneration():
    print("----------------")
    print("Begining to generate csv report...")
    print("----------------")

    romReport = pd.DataFrame(columns=['Name', 'Console', 'WebUrl', 'memorySize', 'Status'])
    romReport.to_csv(REPORTSPATH+"/"+ROMREPORT, index=False)

    print("----------------")
    print("Ending report generation process.")
    print("----------------")

def consoleListRemove(consoleList):

    consoleListBlackList = ["NES", "Genesis", "SNES", "Saturn", "PS1", "N64", "Dreamcast"]
    
    # printing original list
    print ("The original list is : " + str(consoleList))
    
    # printing remove list
    print ("The removal list is : " + str(consoleListBlackList))
    
    # using list comprehension to perform task
    res = [i for i in consoleList if i not in consoleListBlackList]
    
    # printing result
    print ("The list after performing remove operation is : " + str(res))

    return res

def populateReport():
    print("----------------")
    print("Begining to retrieve data for csv report...")
    print("----------------")

    # check if report is present. 
    if (os.path.isfile(REPORTSPATH+"/"+ROMREPORT)):
        print("The Report is present.")
        
    else:
        print("The report file is not detected.... creating report file with defaults.")
        reportGeneration()

    #Starting data gathering. 

    # first access vimms lair. Identify all consols. and print to output.

    http = httplib2.Http()
    status, response = http.request('https://vimm.net/?p=vault')

    global consolesList

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href') and '/vault/' in link['href']:
            consoleString = link['href']
            consoleString = consoleString.replace("/vault/", "")

            exist_count = consolesList.count(consoleString)
 
            # checking if it is more then 0
            if not (exist_count > 0 or not consoleString.strip()):
                consolesList.append(consoleString)
                
    print("Output console list:")
    print(consolesList)

    consolesList = consoleListRemove(consolesList)

    # pick first in the list then go by alphabettical order and get all entries in all pages. 

    for consoleEntry in consolesList:
        
        alphabetString = string.ascii_uppercase
        alphabetList = list(alphabetString)
        
        for letter in alphabetList:

            url = 'https://vimm.net/vault/'+consoleEntry+'/'+letter
            print("Url request is now: "+url)

            http = httplib2.Http()
            status, response = http.request(url)

            for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
                if link.has_attr('href'):
                    romString = link['href']

                    if romString.replace("/vault/","").isnumeric():
                        print("Link matches the pattern of being a rom.Checking....")
                        # capture url and rom names with Replacements
                        print("Adding entry to report")
                        romName = link.contents[0]
                        romName = romName.replace("'","").replace(":","").replace(" ","-").replace("\"","").replace(",","").replace("(","-").replace(")","-").replace(";","-")
                        print("romName: "+romName)
                        
                        print(romName) # name
                        print(consoleEntry)
                        print(HOSTURL+romString)
                        memory = getMemorySize(HOSTURL+romString)
                        collectedRomData = [[romName, consoleEntry, HOSTURL+romString, memory, "check"]] #create entry

                        # add entry to csv file
                        df = pd.DataFrame(collectedRomData)
                        df.to_csv(REPORTSPATH+"/"+ROMREPORT, mode='a', index=False, header=False)

                        print("Console: "+consoleEntry+" rom: "+romString.replace("/vault/",""))
        
        # One additonal check to check roms which start with number values

        url = 'https://vimm.net/vault/?p=list&system='+consoleEntry+'&section=number'
        print("Url request is now: "+url)
        http = httplib2.Http()
        status, response = http.request(url)
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
            if link.has_attr('href'):
                romString = link['href']

                if romString.replace("/vault/","").isnumeric():
                    print("Link matches the pattern of being a rom.Checking....")
                    # capture url and rom names with Replacements
                    print("Adding entry to report")
                    romName = link.contents[0]
                    romName = romName.replace("'","").replace(":","").replace(" ","-").replace("\"","").replace(",","").replace("(","-").replace(")","-").replace(";","-")
                    print("romName: "+romName)
                    
                    print(romName) # name
                    print(consoleEntry)
                    print(HOSTURL+romString)
                    memory = getMemorySize(HOSTURL+romString)
                    collectedRomData = [[romName, consoleEntry, HOSTURL+romString, memory, "check"]] #create entry

                    # add entry to csv file
                    df = pd.DataFrame(collectedRomData)
                    df.to_csv(REPORTSPATH+"/"+ROMREPORT, mode='a', index=False, header=False)

                    print("Console: "+consoleEntry+" rom: "+romString.replace("/vault/",""))
    

    print("----------------")
    print("Ending report data gathering process.")
    print("----------------")

    return consolesList

parser = argh.ArghParser()
parser.add_commands([reportGeneration, populateReport, downloadRoms])

if __name__ == '__main__':
    print("Starting program")
    print("----------------")
    startup()
    print("REPORTSPATH: "+REPORTSPATH)
    parser.dispatch()
    print("----------------")
    print("Ending program")

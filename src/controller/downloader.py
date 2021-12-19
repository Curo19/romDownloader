import csv
import os.path
import asyncio
import pandas
from pyppeteer import launch

class downloader(object):
    def __init__(self):
        print("------------------------")
        print("Calling downloader class")
        print("------------------------")


    def updateDownloadRowCSV(self, path, row, fileLocationLocally):
        print("------------------------")
        print("Starting Update config row")
        print("------------------------")

        # reading the csv file
        print("Updating csv: ",path)
        print("Updating rom name: ",row['RomName'])
        print("Updating rom Console: ", row['Console'])
        configCSV = pandas.read_csv(path)

        rowId = (configCSV["Console"] == row['Console']) & (configCSV["LocationUrl"] == row['LocationUrl'])

        configCSV.loc[rowId, 'PreviouslyDownloaded'] = 'True'

        configCSV.loc[rowId, 'Notes'] = 'Updated Previously Downloaded'

        # writing into the file
        configCSV.to_csv(path, index=False)

        print("------------------------")
        print("Ending csv update: ")
        print("------------------------")

    async def downloadFile(self,url,storageLocation):
        print("------------------------")
        print("Starting download of: ",url)
        print("StorageLocation set: ", storageLocation)
        print("------------------------")
        browser = await launch({'headless': False})
        page = await browser.newPage()
        await page._client.send("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": r""+storageLocation
        })
        await page.goto(url)

        privacyAgreeElement = await page.querySelectorAll('div.qc-cmp2-summary-buttons > button')

        print("testing: ", len(privacyAgreeElement))

        if len(privacyAgreeElement):
            print("Download link not detected")
            await page.screenshot({'path': 'example.png'})
            await asyncio.sleep(3)
            await page.keyboard.press('Tab')
            await page.screenshot({'path': 'p1.png'})
            await asyncio.sleep(1)
            await page.keyboard.press('Tab')
            await page.screenshot({'path': 'p2.png'})
            await asyncio.sleep(3)
            await page.keyboard.press('Tab')
            await page.screenshot({'path': 'p3.png'})
            await asyncio.sleep(3)
            await page.keyboard.press('Enter')
            await page.screenshot({'path': 'p4.png'})
            await asyncio.sleep(3)
            await page.click('form#download_form > button')
            await page.screenshot({'path': 'p4.png'})
            await asyncio.sleep(1)

        else:
            print("Download link detected")
            await asyncio.sleep(3)
            await page.click('form#download_form > button')
            await page.screenshot({'path': 'p4.png'})
            await asyncio.sleep(1)

        print("Checking romfolder")
        print(os.listdir(storageLocation))

        downloadStatus = True

        while downloadStatus:
            print("Checking storage location: ",storageLocation)
            for fname in os.listdir(storageLocation):
                print("Checking filename: ",fname)
                if fname.endswith('.crdownload'):
                    print("File detected waiting 1 second")
                    await asyncio.sleep(1)
                else:
                    downloadStatus=False

        await browser.close()
        print("------------------------")
        print("Ending download of: ",url)
        print("------------------------")

    def downloadFromCsv(self,path,limit):

        #read in csv as dict

        with open(path, newline='') as csvfile:

            reader = csv.DictReader(csvfile)
            listToDownload = []

            for row in reader:
                #print(row['RomName'], row['Console'], row['FlagDownload'], row['PreviouslyDownloaded'])

                if limit != 0:
                    count = 0
                    while (count < limit):
                        if "False" not in row['FlagDownload'] and "True" not in row['PreviouslyDownloaded']:
                            listToDownload.append(row)
                            count = count + 1
                else:
                    if "False" not in row['FlagDownload'] and "True" not in row['PreviouslyDownloaded']:
                        print("Rom name adding to download list: ",row["RomName"])
                        listToDownload.append(row)


            for row in listToDownload:
                print(row['RomName'], row['Console'], row['FlagDownload'], row['PreviouslyDownloaded'])

            if not listToDownload:
                print("List of roms to download which have not already been downloaded is empty.")
            else:
                print("Starting download")
                if os.path.isdir("/romFolder"):
                    print("Rom folder detected")
                else:
                    os.mkdir("/romFolder")

                for downloadRomFile in listToDownload:
                    if os.path.isdir("/romFolder/"+downloadRomFile['Console']):
                        print("Console folder detected: ",downloadRomFile['Console'])
                    else:
                        os.mkdir("/romFolder/"+downloadRomFile['Console'])

                    romFolderName = downloadRomFile['RomName'].replace("/", "").replace("&", "And").replace(" ", "")\
                            .replace("-", "").replace("'", "").replace(":", "").replace("!", "").replace(".", "")

                    if os.path.isdir("/romFolder/"+downloadRomFile['Console']+"/"+romFolderName):
                        print("Console folder detected: ",romFolderName)
                    else:
                        os.mkdir("/romFolder/"+downloadRomFile['Console']+"/"+romFolderName)

                    asyncio.get_event_loop().run_until_complete(self.downloadFile(downloadRomFile["LocationUrl"], "/romFolder/"+downloadRomFile['Console']+"/"+romFolderName))

                    # update config file with previously downloaded set to true and adding in file location.
                    self.updateDownloadRowCSV(path, downloadRomFile, "/romFolder/"+romFolderName)



                #print completed message
                print("------------------------")
                print("Rom Download Process Complete.")
                print("------------------------")
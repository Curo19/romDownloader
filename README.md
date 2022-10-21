Vimm's lair Rom downloader version 2 
====================================
Note: in alpha state. It works with a bit of fiddling
With requirements.txt and chrome driver. But otherwise works 
Well


This project allows the user to do the following:

1) Webscrape all rom related information and data from vimm's lair website 
and send it to a report file in a csv format. Note: This report will be used to keep track 
of roms on the site, which roms to download and the current download state of all roms.

2) Download the roms by using the report csv file to both identify the rom download locations 
and to indicate which roms to download for the user and the current state the rom download process is
in.

=====================================

Setup
--------
pip3 install -r requirements.txt

Run
--------
python3 romDownloader.py 
 -- this displays the help screen and ensures that the configuration file is generated.

python3 romDownloader.py reportGeneration
 -- This generates a simple csv report template required for rom download and status management.

python3 romDownloader.py populateReport
 -- This connects to the vimm's lair website and web scrapes all the required links and data of all consoles and roms 
 that are present on the web site and export it to the romReport.csv file which was previously generated. 
 Note if report file has not already been generated it will attempt to create the template report file first. 

python3 romDownloader.py downloadRoms
 -- This function will download any roms which have the "Status" of "enable" within the romReport.csv file.
note the states are as follows:
    "check" -- this is just nural status after the roms data has been webscraped from vimm's lair
    "enable" -- this indicates which roms are to be downloaded.
    "InProgress" -- this indicates which roms are currently being downloaded from vimm's lair. In the event of network 
    connection issues such as network connection cut the "InProgress" allows the user to delete the rom from the downloads 
    folder and start again from that rom. 
    "done" -- this indicates that that a rom was successfully downloaded before. 
    "error" -- this indicates an unexplainable error occured during or before the download process. Recommendation to the user
    is to check the vimm's lair rom page to see if download is possible.

Note currnently this program uses a headless command line google chrome browser. The user may need to download the chrome selenium driver (https://chromedriver.chromium.org/downloads) and also download/ 
update the os chrome version. The chrome driver should be added to the romDownloader project folder. Additionally roms are downloaded one at a time and currently cannot be downloaded in parrallel. 

Finally this is a simple hobby project and I would like to add more features, such as progress download bars, memory size caulucaltion, mass
report enable or cleanup of reports as well as parallel download.

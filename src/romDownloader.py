import argh
from controller.preparation import preparation
from controller.downloader import downloader

@argh.arg('--output', '-o', help="Set the output report name")
@argh.arg('--updateConfig', help="Update existing config")
@argh.arg('--console', help="Console type")
@argh.arg('--enableDownload', help="Enable all Downloads within a console type.")

def prep(output="../config/romDownloader.csv", updateConfig=False, console="False", enableDownload="False"):
    print("Starting preperation")
    print("----------------")

    setup = preparation()
    
    if updateConfig:
        print("Updating Existing Config")
        setup.updateExistingConfig(output,console,enableDownload)
    else:
        setup.geneateNewConfig(output)

    print("----------------")
    print("Ending preperation")

@argh.arg('--csv', '-o', help="Location of the csv file to download all the roms.")
@argh.arg('--limit', '-n', help="limit the number of roms downloaded")
@argh.arg('--downloadLocation', '-dl', help="download location folder to download roms into")
def download(csv="../config/romDownloader.csv", limit=0, downloadLocation="../romFolder"):
    print("Starting download process")
    print("----------------")
    dl = downloader()
    dl.downloadFromCsv(csv, limit, downloadLocation+"/")
    print("----------------")
    print("Ending download process")

parser = argh.ArghParser()
parser.add_commands([prep, download])

if __name__ == '__main__':
    print("Starting program")
    print("----------------")
    parser.dispatch()
    print("----------------")
    print("Ending program")

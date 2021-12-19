class romDataEntry:
    def __init__(self):
        self._romName = "romname"
        self._console = "cname"
        self._fileSize = "fSize"
        self._fileType = "fType"
        self._locationUrl = "webUrl"
        self._downloadUrl = "dUrl"
        self._dateFirstAdded = "dateF"
        self._dateLastUpDated = "dateL"
        self._flagDownload = False
        self._previouslyDownloaded = False
        self._rating = "rate"
        self._localPath = "lPath"
        self._notes = "blah"

    def get_romName(self):
        return self._romName

    def set_romName(self, name):
        self._romName = name

    def del_romName(self):
        self._romName = ""

    romName = property(get_romName, set_romName, del_romName)

    def get_console(self):
        return self._console

    def set_console(self, console):
        self._console = console

    def del_console(self):
        self._console = ""

    console = property(get_console, set_console, del_console)

    def get_fileSize(self):
        return self._fileSize

    def set_fileSize(self, fs):
        self._fileSize = fs

    def del_fileSize(self):
        self._fileSize = ""

    fileSize = property(get_fileSize, set_fileSize, del_fileSize)

    def get_fileType(self):
        return self._fileType

    def set_fileType(self, ft):
        self._fileType = ft

    def del_fileType(self):
        self._fileType = ""

    fileType = property(get_fileType, set_fileType, del_fileType)

    def get_locationUrl(self):
        return self._locationUrl

    def set_locationUrl(self, lURL):
        self._locationUrl = lURL

    def del_locationUrl(self):
        self._locationUrl = ""

    locationUrl = property(get_locationUrl, set_locationUrl, del_locationUrl)

    def get_downloadUrl(self):
        return self._downloadUrl

    def set_downloadUrl(self, dURL):
        self._downloadUrl = dURL

    def del_downloadUrl(self):
        self._downloadUrl = ""

    downloadUrl = property(get_downloadUrl, set_downloadUrl, del_downloadUrl)

    def get_dateFirstAdded(self):
        return self._dateFirstAdded

    def set_dateFirstAdded(self, dfa):
        self._dateFirstAdded = dfa

    def del_dateFirstAdded(self):
        self._dateFirstAdded = ""

    dateFirstAdded = property(get_dateFirstAdded, set_dateFirstAdded, del_dateFirstAdded)

    def get_dateLastUpDated(self):
        return self._dateLastUpDated

    def set_dateLastUpDated(self, dlu):
        self._dateLastUpDated = dlu

    def del_dateLastUpDated(self):
        self._dateLastUpDated = ""

    dateLastUpDated = property(get_dateLastUpDated, set_dateLastUpDated, del_dateLastUpDated)

    def get_flagDownload(self):
        return self._flagDownload

    def set_flagDownload(self, fD):
        self._flagDownload = fD

    def del_flagDownload(self):
        self._flagDownload = False

    flagDownload = property(get_flagDownload, set_flagDownload, del_flagDownload)

    def get_previouslyDownloaded(self):
        return self._previouslyDownloaded

    def set_previouslyDownloaded(self, pD):
        self._previouslyDownloaded = pD

    def del_previouslyDownloaded(self):
        self._previouslyDownloaded = False

    previouslyDownloaded = property(get_previouslyDownloaded, set_previouslyDownloaded, del_previouslyDownloaded)

    def get_rating(self):
        return self._rating

    def set_rating(self, rate):
        self._rating = rate

    def del_rating(self):
        self._rating = ""

    rating = property(get_rating, set_rating, del_rating)

    def get_localPath(self):
        return self._localPath

    def set_localPath(self, lP):
        self._localPath = lP

    def del_localPath(self):
        self._localPath = ""

    localPath = property(get_localPath, set_localPath, del_localPath)

    def get_notes(self):
        return self._notes

    def set_notes(self, name):
        self._notes = name

    def del_notes(self):
        self._notes = ""

    notes = property(get_notes, set_notes, del_notes)



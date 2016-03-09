import sys, json
from PyQt4 import QtGui, QtCore
import unicodedata

class TextSearch:
    #Removes accents and lowers the cases.
    def normalizeText(self, text):
        return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')).lower()

    def normalStringSearch(self, searchString, text):
        return self.normalizeText(searchString) in self.normalizeText(text)

    def normalPartSearch(self, searchString, parts):
        for i in parts:
            if self.normalStringSearch(searchString, " ".join(i)):
                return True
        return False

    def normalSearch(self, searchString, song):
        return self.normalStringSearch(searchString, song["title"]) or self.normalPartSearch(searchString, song["parts"])

    def normalSearchAll(self, searchString, songList):
        resultList = []
        for i, s in enumerate(songList):
            if self.normalSearch(searchString, s):
                resultList.append(i)
        return resultList

class TextFitter:
    def __init__(self):
        pass

    def getWidth(self, text, size):
        font = QtGui.QFont('Source Code Pro Light', size)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(text)
        textHeight = fm.height()

        return textWidth, textHeight

    def marginWidth(self, widthMargin, width):
        return width - widthMargin * 2

    def marginHeight(self, heightMargin, height):
        return height - heightMargin * 2

    def getMaxTextSize(self, text, maxWidth, maxHeight, lineCount):
        size = 200
        width, height = self.getWidth(text, size)

        while (width > maxWidth or (height * lineCount) > maxHeight) and size > 1:
            size -= 1
            width, height = self.getWidth(text, size)
        return size

    #TODO: Split too long rows into columns.
    def fitText(self, qp, title, textLines, widthMargin, heightMargin, width, height, showTitle, splitColumns):
        centerX = widthMargin + self.marginWidth(widthMargin, width) / 2
        centerY = heightMargin + self.marginHeight(heightMargin, height) / 2

        lineCount = len(textLines)
        longestText = ""
        longestTextLen = 0

        if showTitle:
            lineCount += 2
            longestText = title
            longestTextLen = len(title)

        for i in textLines:
            if len(i) > longestTextLen:
                longestText = i
                longestTextLen = len(i)

        textSize = self.getMaxTextSize(longestText, self.marginWidth(widthMargin, width), self.marginHeight(heightMargin, height), lineCount)
        font = QtGui.QFont('Source Code Pro Light', textSize)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(longestText)
        textHeight = fm.height()

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtCore.Qt.gray)
        qp.setPen(pen)

        textX = centerX - (textWidth / 2)
        textY = centerY - (textHeight * len(textLines)) / 2

        if showTitle:
            path = QtGui.QPainterPath()
            path.addText(textX, textY, font, title)

            qp.drawPath(path)
            textY += textHeight * 2

        qp.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
        for i in textLines:
            path = QtGui.QPainterPath()
            path.addText(textX, textY, font, i)

            qp.drawPath(path)
            textY += textHeight

    def drawBackground(self, qp, width, height):
        qp.drawRect(0, 0, width, height)

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 25))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, width, height)

class ControlRoom(QtGui.QWidget):
    def __init__(self, parent, songList, textFitter):
        super(ControlRoom, self).__init__()
        self.parent = parent

        self.textFitter = textFitter
        self.setWindowTitle("ControlRoom")
        self.widthMargin = 50
        self.heightMargin = 50

        self.toggleFullscreen = False;
        self.songList = songList
        self.selectedSong = 0
        print (self.songList[0]["title"])

    def keyPressEvent(self, e):
        if not self.parent.searchMode and e.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen = not self.toggleFullscreen
            self.fullscreen(self.toggleFullscreen)
        else:
            self.parent.keyPressEvent(e)
    def setSelectedSong(self, number):
        self.selectedSong = number

    def fullscreen(self, state):
        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())

        self.textFitter.drawBackground(qp, self.width(), self.height())

        #Draw the red corners of the control room.
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 50), 10, QtCore.Qt.SolidLine))
        qp.drawLine(0, 100, 100, 0)
        qp.drawLine(self.width() - 100, 0, self.width(), 100)
        qp.drawLine(0, self.height() - 100, 100, self.height())
        qp.drawLine(self.width() - 100, self.height(), self.width(), self.height() - 100)

        titleList = []
        for i, s in enumerate(self.songList):
            if i == self.selectedSong:
                titleList.append("-" + s["title"])
            else:
                titleList.append(s["title"])

        self.textFitter.fitText(qp, self.songList[self.selectedSong]["title"], titleList, self.widthMargin, self.heightMargin, self.width(), self.height(), True, True)

        #Write search string:
        font = QtGui.QFont('Source Code Pro Light', 24)

        path = QtGui.QPainterPath()
        path.addText(50, 50, font, self.parent.searchString)
        qp.drawPath(path)

class AposSong(QtGui.QWidget):
    
    def __init__(self):
        super(AposSong, self).__init__()
        
        self.textFitter = TextFitter()
        self.textSearch = TextSearch()

        self.widthMargin = 50
        self.heightMargin = 50

        self.selectedSong = 0
        self.selectedPart = 0

        self.toggleFullscreen = False
        self.showTitle = False
        self.searchMode = False

        self.searchString = ""

        self.w = None

        #Dict that contains labels for song titles
        self.songList = []

        with open('chansons.json', 'r', encoding='utf8') as fp:
            self.songList = json.load(fp)

        #self.songList.append({"title": "Hello World!", "parts": [['Line1', 'Line2'], ['Second part line1', 'Second part line2.', 'YAY! Line3']]})
        #self.songList.append({"title": "Hello World!", "parts": [['Line1', 'Line2'], ['Second part line1', 'Second part line2.']]})
        #self.songList.append({"title": "Praise!", "parts": [['Line1', 'Line2'], ['Second part line1', 'Second part line2.']]})

        #with open('chansons.json', 'w', encoding='utf8') as fp:
        #    json.dump(self.songList, fp)

        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle("AposSong")
        self.show()


        #f_db = QtGui.QFontDatabase()
        #for family in f_db.families():
        #    print(family)

    def keyPressEvent(self, e):
        if self.searchMode:
            if e.key() == QtCore.Qt.Key_Escape:
                print ("Escaped to default mode.")
                self.searchMode = False
                self.searchString = ""
                if self.w is not None:
                    self.w.update()
            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print ("Searching now! {}".format(self.searchString))
                resultList = self.textSearch.normalSearchAll(self.searchString, self.songList)

                print (resultList)
                for i in resultList:
                    print (self.songList[i]["title"])

                self.searchMode = False
            elif e.key() == QtCore.Qt.Key_Backspace:
                self.searchString = self.searchString[:-1]
                print ("Remove last")
                if self.w is not None:
                    self.w.update()
            else:
                try:
                    char = "%c" % (e.key())
                    print ("Key pressed: {}, was: {}".format(char, e.key()))

                    self.searchString += char.lower()
                    if self.w is not None:
                        self.w.update()

                except OverflowError:
                    print ("Key pressed: error, was: {}".format(e.key()))
                    pass
        else:
            if e.key() == QtCore.Qt.Key_F:
                self.toggleFullscreen = not self.toggleFullscreen
                self.fullscreen(self.toggleFullscreen)
            elif e.key() == QtCore.Qt.Key_D:
                if self.w is None:
                    self.w = ControlRoom(self, self.songList, self.textFitter)
                    self.w.show()
                else:
                    self.w.show()
            elif e.key() == QtCore.Qt.Key_Right:
                print ("Next part")
                self.selectedPart = (self.selectedPart + 1) % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_Left:
                print ("Previous part")
                self.selectedPart = (self.selectedPart - 1) % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_Up:
                print ("Previous Song")
                self.selectedPart = 0
                self.selectedSong = (self.selectedSong - 1) % len(self.songList)
                self.update()
                if self.w is not None:
                    self.w.setSelectedSong(self.selectedSong)
                    self.w.update()
            elif e.key() == QtCore.Qt.Key_Down:
                print ("Next Song")
                self.selectedPart = 0
                self.selectedSong = (self.selectedSong + 1) % len(self.songList)
                self.update()
                if self.w is not None:
                    self.w.setSelectedSong(self.selectedSong)
                    self.w.update()
            elif e.key() == QtCore.Qt.Key_1:
                self.selectedPart = 1 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_2:
                self.selectedPart = 2 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_3:
                self.selectedPart = 3 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_4:
                self.selectedPart = 4 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_5:
                self.selectedPart = 5 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_6:
                self.selectedPart = 6 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_7:
                self.selectedPart = 7 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_8:
                self.selectedPart = 8 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_9:
                self.selectedPart = 9 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_0:
                self.selectedPart = 0 % len(self.songList[self.selectedSong]["parts"])
                self.update()
            elif e.key() == QtCore.Qt.Key_S:
                self.searchMode = True
                self.searchString = ""
                print ("SearchMode: {}".format(self.searchMode))
                if self.w is not None:
                    self.w.update()
            elif e.key() == QtCore.Qt.Key_T:
                self.showTitle = not self.showTitle
                self.update()
                print ("Toggle Title!")

    def fullscreen(self, state):

        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def paintEvent(self, e):
        #TODO: Center the text as a whole.
        #      Also, resize the text to fit the screen.

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        
        self.textFitter.drawBackground(qp, self.width(), self.height())

        self.textFitter.fitText(qp, self.songList[self.selectedSong]["title"], self.songList[self.selectedSong]["parts"][self.selectedPart], self.widthMargin, self.heightMargin, self.width(), self.height(), self.showTitle, False)


        qp.end()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = AposSong()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
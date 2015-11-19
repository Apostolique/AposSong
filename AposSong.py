import sys, json
from PyQt4 import QtGui, QtCore

class ControlRoom(QtGui.QWidget):
    def __init__(self, songList):
        super(ControlRoom, self).__init__()
        self.setWindowTitle("ControlRoom")
        self.text = "Cool Dialog"
        self.toggleFullscreen = False;
        self.songList = songList
        print (self.songList[0]["title"])

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen = not self.toggleFullscreen
            self.fullscreen(self.toggleFullscreen)

    def fullscreen(self, state):
        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        font = QtGui.QFont('Source Code Pro Light', 100)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(self.text)
        textHeight = fm.height()

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 25))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())

        qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 50), 10, QtCore.Qt.SolidLine))
        qp.drawLine(0, 100, 100, 0)
        qp.drawLine(self.width() - 100, 0, self.width(), 100)
        qp.drawLine(0, self.height() - 100, 100, self.height())
        qp.drawLine(self.width() - 100, self.height(), self.width(), self.height() - 100)

        centerX = self.width() / 2
        centerY = self.height() / 2

        qp.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtCore.Qt.gray)
        qp.setPen(pen)


        textX = centerX - (textWidth / 2)
        textY = centerY + textHeight - (textHeight * len(self.songList)) / 2

        for i in self.songList:

            path = QtGui.QPainterPath()
            path.addText(textX, textY, font, i["title"])

            qp.drawPath(path)

            textY += textHeight

class AposSong(QtGui.QWidget):
    
    def __init__(self):
        super(AposSong, self).__init__()
        
        self.widthMargin = 50
        self.heightMargin = 50

        self.selectedSong = 0
        self.selectedPart = 0

        self.toggleFullscreen = False
        self.showTitle = False

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
        if e.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen = not self.toggleFullscreen
            self.fullscreen(self.toggleFullscreen)
        if e.key() == QtCore.Qt.Key_D:
            if self.w is None:
                self.w = ControlRoom(self.songList)
                self.w.show()
            else:
                self.w.show()
        if e.key() == QtCore.Qt.Key_Right:
            print ("Next part")
            self.selectedPart = (self.selectedPart + 1) % len(self.songList[self.selectedSong]["parts"])
            self.update()
        if e.key() == QtCore.Qt.Key_Left:
            print ("Previous part")
            self.selectedPart = (self.selectedPart - 1) % len(self.songList[self.selectedSong]["parts"])
            self.update()


    def fullscreen(self, state):

        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def getWidth(self, text, size):
        font = QtGui.QFont('Source Code Pro Light', size)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(text)
        textHeight = fm.height()

        return textWidth, textHeight

    def getMaxTextSize(self, text, maxWidth, maxHeight, lineCount):
        size = 200
        width, height = self.getWidth(text, size)

        while (width > maxWidth or (height * lineCount) > maxHeight) and size > 1:
            size -= 1
            width, height = self.getWidth(text, size)
        return size

    def marginWidth(self):
        return self.width() - self.widthMargin * 2

    def marginHeight(self):
        return self.height() - self.heightMargin * 2

    def fitText(self, qp, title, textLines):
        centerX = self.widthMargin + self.marginWidth() / 2
        centerY = self.heightMargin + self.marginHeight() / 2

        lineCount = len(textLines)
        longestText = ""
        longestTextLen = 0

        if self.showTitle:
            lineCount += 2
            longestText = title
            longestTextLen = len(title)

        for i in textLines:
            if len(i) > longestTextLen:
                longestText = i
                longestTextLen = len(i)

        textSize = self.getMaxTextSize(longestText, self.marginWidth(), self.marginHeight(), lineCount)
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

        if self.showTitle:
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

    def drawBackground(self, qp):
        qp.drawRect(0, 0, self.width(), self.height())

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 25))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())

    def paintEvent(self, e):
        #TODO: Center the text as a whole.
        #      Also, resize the text to fit the screen.

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        
        self.drawBackground(qp)

        self.fitText(qp, self.songList[self.selectedSong]["title"], self.songList[self.selectedSong]["parts"][self.selectedPart])


        qp.end()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = AposSong()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
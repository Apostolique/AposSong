import sys
from PyQt4 import QtGui, QtCore

class ControlRoom(QtGui.QWidget):
    def __init__(self, songList):
        super(ControlRoom, self).__init__()
        self.setWindowTitle("ControlRoom")
        self.text = 'Cool Dialog'
        self.toggleFullscreen = False;
        self.songList = songList
        print (self.songList[0].title)

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
            path.addText(textX, textY, font, i.title)

            qp.drawPath(path)

            textY += textHeight

class SingleSong():
    def __init__(self, title, parts):
        self.title = title
        #Songs are broken into parts.
        ##Parts contains lists of lines.
        self.parts = parts

class AposSong(QtGui.QWidget):
    
    def __init__(self):
        super(AposSong, self).__init__()
        
        self.toggleFullscreen = False;
        self.text = "Hello World!"

        self.w = None

        #Dict that contains labels for song titles
        self.songList = []
        self.songList.append(SingleSong("Hello World!", [['Line1', 'Line2'], ['Second part line1', 'Second part line2.']]))
        self.songList.append(SingleSong("Hello World!", [['Line1', 'Line2'], ['Second part line1', 'Second part line2.']]))
        self.songList.append(SingleSong("Praise!", [['Line1', 'Line2'], ['Second part line1', 'Second part line2.']]))

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
        qp.drawRect(0, 0, self.width(), self.height())

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 25))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())

        centerX = self.width() / 2
        centerY = self.height() / 2

        font = QtGui.QFont('Source Code Pro Light', 100)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(self.text)
        textHeight = fm.height()

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtCore.Qt.gray)
        qp.setPen(pen)

        selected = 0

        textX = centerX - (textWidth / 2)
        textY = centerY - (textHeight * len(self.songList[selected].parts[1])) / 2

        path = QtGui.QPainterPath()
        path.addText(textX, textY, font, self.songList[selected].title)

        qp.drawPath(path)
        textY += textHeight

        qp.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
        for i in self.songList[0].parts[1]:
            path = QtGui.QPainterPath()
            path.addText(textX, textY, font, i)

            qp.drawPath(path)
            textY += textHeight


        qp.end()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = AposSong()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
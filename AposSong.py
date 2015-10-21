import sys
from PyQt4 import QtGui, QtCore

class AposSong(QtGui.QWidget):
    
    def __init__(self):
        super(AposSong, self).__init__()
        
        self.toggleFullscreen = False;
        self.text = "Hello World!"

        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('AposSong')
        self.show()


        f_db = QtGui.QFontDatabase()
        for family in f_db.families():
            print(family)

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
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.setBrush(QtGui.QColor(0, 0, 0, 255))
        qp.drawRect(0, 0, self.width(), self.height())

        centerX = self.width() / 2
        centerY = self.height() / 2

        font = QtGui.QFont('Source Code Pro Medium', 100)
        font2 = QtGui.QFont('Source Code Pro', 100)
        font3 = QtGui.QFont('Source Code Pro Light', 100)
        fm = QtGui.QFontMetrics(font)
        textWidth = fm.width(self.text)
        textHeight = fm.height()

        textX = centerX - textWidth / 2
        textY = centerY + textHeight / 2

        qp.setFont(font)
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 50), 3, QtCore.Qt.SolidLine))
        qp.drawText(QtCore.QPointF(textX, textY), self.text)

        qp.setFont(font2)
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 150), 3, QtCore.Qt.SolidLine))
        qp.drawText(QtCore.QPointF(textX, textY), self.text)

        qp.setFont(font3)
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3, QtCore.Qt.SolidLine))
        qp.drawText(QtCore.QPointF(textX, textY), self.text)

        qp.end()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = AposSong()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
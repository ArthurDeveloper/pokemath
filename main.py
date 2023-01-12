import sys
from PyQt5 import QtCore, QtWidgets
from splashscreen import Splashscreen

app = QtWidgets.QApplication(sys.argv)

def main():
    global app

    window = Splashscreen()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


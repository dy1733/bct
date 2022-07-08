import sys
import bct
import gui
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = gui.main_window()
    cg = bct.chatting_graph()
    app.exec_()
        
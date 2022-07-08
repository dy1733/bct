import bct
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QWidget

class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.cps = 10
        self.noi = 6
        self.sen = 6
        self.off = 3
        self.wid = 6
        self.hei = 3
        self.bctg = bct.chatting_graph()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Broadcasting Chatting Traffic")
        self.resize(600, 360)
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)

        self.line_cps = QLineEdit(self)
        label_cps = QLabel("chat per sec : default(10)", self)
        self.Lgrid.addWidget(label_cps, 1, 1)
        self.Lgrid.addWidget(self.line_cps, 1, 2)

        self.line_noi = QLineEdit(self)
        label_noi = QLabel("noise : default(6)", self)
        self.Lgrid.addWidget(label_noi, 1, 3)
        self.Lgrid.addWidget(self.line_noi, 1, 4)

        self.line_sen = QLineEdit(self)
        label_sen = QLabel("sensitive : default(6)", self)
        self.Lgrid.addWidget(label_sen, 2, 1)
        self.Lgrid.addWidget(self.line_sen, 2, 2)

        self.line_off = QLineEdit(self)
        label_off = QLabel("offset : default(3)", self)
        self.Lgrid.addWidget(label_off, 2, 3)
        self.Lgrid.addWidget(self.line_off, 2, 4)

        self.line_wid = QLineEdit(self)
        label_wid = QLabel("width : default(6)", self)
        self.Lgrid.addWidget(label_wid, 3, 1)
        self.Lgrid.addWidget(self.line_wid, 3, 2)
        
        self.line_hei = QLineEdit(self)
        label_hei = QLabel("height : default(3)", self)
        self.Lgrid.addWidget(label_hei, 3, 3)
        self.Lgrid.addWidget(self.line_hei, 3, 4)

        self.line_num = QLineEdit(self)
        label_num = QLabel("broadcast number :", self)
        self.Lgrid.addWidget(label_num, 4, 1)
        self.Lgrid.addWidget(self.line_num, 4, 2)

        btn_onebtn = QPushButton('원버튼', self)
        self.label_onebtn = QLabel('원 버튼',self)
        self.Lgrid.addWidget(btn_onebtn, 4, 3)
        self.Lgrid.addWidget(self.label_onebtn, 4, 4)
        btn_onebtn.clicked.connect(self.one_button)

        ######################################################

        btn_config = QPushButton('설정', self)
        self.label_config = QLabel('현재 기본 설정입니다',self)
        self.Lgrid.addWidget(btn_config, 6, 1)
        self.Lgrid.addWidget(self.label_config, 6, 2)
        btn_config.clicked.connect(self.config)

        btn_open = QPushButton('로그 파일 찾기',self)
        self.label_open = QLabel('로그 파일을 입력하세요',self)
        self.Lgrid.addWidget(btn_open, 6, 3)
        self.Lgrid.addWidget(self.label_open, 6, 4)
        btn_open.clicked.connect(self.add_open)

        btn_highlight = QPushButton('하이라이트 추출', self)
        self.label_highlight = QLabel('하이라이트를 추출합니다', self)
        self.Lgrid.addWidget(btn_highlight, 7, 1)
        self.Lgrid.addWidget(self.label_highlight, 7, 2)
        btn_highlight.clicked.connect(self.print_highlight)

        btn_print = QPushButton('그래프 출력', self)
        self.label_print = QLabel('채팅 트래픽 그래프를 출력합니다', self)
        self.Lgrid.addWidget(btn_print, 7, 3)
        self.Lgrid.addWidget(self.label_print, 7, 4)
        btn_print.clicked.connect(self.print_graph)
        self.show()
    
    def config(self):
        self.cps = (int)(self.line_cps.text())
        self.noi = (int)(self.line_noi.text())
        self.sen = (int)(self.line_sen.text())
        self.off = (int)(self.line_off.text())
        self.wid = (int)(self.line_wid.text())
        self.hei = (int)(self.line_hei.text())
        self.label_config.setText("설정 변경 완료")

    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
        file_name = FileOpen[0]
        self.bctg.initGraph(file_name, self.cps, self.noi)
        self.label_open.setText("로그 파일 입력 완료")

    def print_highlight(self):
        self.bctg.detectHighlight(self.sen, self.off)
        self.label_highlight.setText("하이라이트 추출 완료")
 
    def print_graph(self):
        self.bctg.printGraph(self.cps, self.wid, self.hei, self.sen)
        self.label_print.setText("그래프 출력 완료")

    def one_button(self):
        self.bctg.onebuttonrun()

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *

seasons_list = ["Winter", "Spring", "Summer", "Autumn"]
season_info = ["Cold, snowy season", "Nature's rise", "Equator's eternal season", "Season of Golden leaves"]


class Seasons(QWidget):
    cur_season = seasons_list[0]

    def _init_btn_group(self):
        btn_layout = QVBoxLayout()
        self.btns = QButtonGroup()
        for idx, s in enumerate(seasons_list):
            btn = QRadioButton(s)
            if idx == 0:
                btn.click()
            self.btns.addButton(btn, idx)
            btn_layout.addWidget(btn)
        self.btns.buttonClicked.connect(self.handle_season_change)
        return btn_layout

    def handle_season_change(self, button: QAbstractButton):
        print(self.btns.checkedId())
        self.info_label.setText(season_info[self.btns.checkedId()])
        

    def __init__(self):
        super().__init__()
        btns = self._init_btn_group()
        self.info_label = QLabel(season_info[0])
        self.info_label.setWordWrap(True)
        l = RowLayout(btns, self.info_label)
        self.setLayout(l)

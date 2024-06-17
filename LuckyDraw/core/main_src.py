# coding:utf-8
# @Author:AZ5394
# GitHub:github.com/AZ5394
import sys
from datetime import datetime
from random import sample
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.Qt import Qt, QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QTranslator

from db.db_src import Sqlite
from ui.main_window import Ui_Form as Main_ui
from .child_src import Child


class MainWindow(Main_ui, QWidget):  # 主窗口
    def __init__(self):
        super().__init__()
        self.oldPos = None
        self.show_anim = None
        self.close_anim = None
        self.setupUi(self)  # 加载图形界面
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setAttribute(Qt.WA_TranslucentBackground)

        # screen = QDesktopWidget().screenGeometry()  # 窗口居中屏幕显示
        # size = self.geometry()
        # self.move((screen.width() - size.width()) / 2,
        #           (screen.height() - size.height()) / 2)

        self.config = QSettings('wklQnlkm', 'LuckyDraw')
        # 从注册表里读取字体大小,没有就用默认大小
        self.font_size = self.config.value('font_size') if self.config.value('font_size') else 20
        # 从注册表里读取每行显示个数,没有就用默认个数
        self.current_quantity = self.config.value('quantity_per_row') if self.config.value('quantity_per_row') else 6
        # 从注册表里读取显示语言,没有就默认用英文
        self.language = self.config.value('language') if self.config.value('language') else 'English'
        # 从注册表里读取显示序号状态
        self.show_sequence_state = True if self.config.value('sequence_state') == 'true' else False
        # 从注册表里读取显示时间状态
        self.show_time_state = True if self.config.value('show_time_state') == 'true' else False
        # 实例化数据库
        self.sqlite = Sqlite()
        # 创建翻译家
        self.translator = QTranslator()
        # 实例化子窗口
        self.child = Child(self.font_size, self.current_quantity, self.language, self.show_sequence_state,
                           self.show_time_state,
                           self.maximize_btn2, self.page_label, self.set_spec_btn_style, self.clear_widget,
                           self.set_font_size, self.relayout, self.histo_record, self.show_time, self.change_font_size,
                           self.set_quantity, self.set_language, self.set_sequence_state, self.set_show_time_state,
                           self.sqlite, self.translator
                           )

    def showEvent(self, event):  # 显示动画
        if self.show_anim is None:
            self.show_anim = QPropertyAnimation(self, b'windowOpacity')
            self.show_anim.setStartValue(0)
            self.show_anim.setEndValue(1)
            self.show_anim.setDuration(500)
            self.show_anim.finished.connect(self.show)
            self.show_anim.start()
            event.ignore()

    def closeEvent(self, event):  # 关闭动画
        if self.close_anim is None:
            self.close_anim = QPropertyAnimation(self, b'windowOpacity')
            self.close_anim.setStartValue(1)
            self.close_anim.setEndValue(0)
            self.close_anim.setDuration(500)
            self.close_anim.finished.connect(self.close)
            self.close_anim.start()
            event.ignore()
            # 关闭窗口前保存数据到数据库
            self.config.setValue('show_time_state', self.show_time_state)
            self.config.setValue('font_size', self.font_size)
            self.config.setValue('language', self.language)
            self.config.setValue('quantity_per_row', self.current_quantity)
            self.config.setValue('sequence_state', self.show_sequence_state)
            # 每次关闭程序都清空数据库里保存的抽取记录,方便下次保存
            self.sqlite.clear_record_table()
            self.child.close()  # 主窗口关闭子窗口也随之关闭

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 当左键被点击
            self.oldPos = event.globalPos()  # 保存当前鼠标位置

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:  # 当左键被点击并且移动
            delta = event.globalPos() - self.oldPos  # 计算窗口移动距离
            self.move(self.x() + delta.x(), self.y() + delta.y())  # 移动到新的窗口位置
            self.oldPos = event.globalPos()

    def maximize(self):  # 最大化
        # 如果已经是最大化再次点击则显示正常窗口
        if self.isMaximized():
            self.set_spec_btn_style(self.maximize_btn, 'image/maximize.png')
            self.showNormal()
            return
        self.set_spec_btn_style(self.maximize_btn, 'image/minimize2.png')
        self.showMaximized()

    def minimize(self):  # 最小化
        self.showMinimized()

    def double_click(self):  # 双击最大化按钮事件
        self.maximize_btn2.mouseDoubleClickEvent = self.double_click_event

    def double_click_event(self, event):  # 双击最大化按钮处理
        if event.button() == Qt.LeftButton and self.isMaximized():
            self.set_spec_btn_style(self.maximize_btn, 'image/maximize.png')
            self.showNormal()
            return
        self.set_spec_btn_style(self.maximize_btn, 'image/minimize2.png')
        self.showMaximized()

    @staticmethod
    def set_spec_btn_style(btn, image):  # 设置特别按钮的样式
        btn.setStyleSheet("QPushButton{\n"
                          "  width:40px;\n"
                          "  height:30px;\n"
                          f"  image:url({image});\n"
                          "  border-radius:5px}\n"
                          "QPushButton:hover{\n"
                          "  background-color: rgb(222, 222, 222);}\n"
                          "width:15px;\n"
                          "height:15px;")

    @staticmethod
    def clear_widget(widgets):  # 清除控件
        for i in reversed(range(widgets.count())):  # 遍历父控件
            item = widgets.itemAt(i)
            if isinstance(item.widget(), QWidget):  # 如果是QWidget类型,调用deleteLater
                item.widget().deleteLater()
            else:
                widgets.remove(item)  # 否则调用remove

    def set_font_size(self, *widget, has_alignment=True):  # 设置字体样式,用*widget而不是widget是因为控件不可迭代,*会返回元组可以迭代
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(self.font_size)
        font.setBold(False)
        font.setWeight(50)
        for widget_font in widget:  # 迭代设置控件字体大小
            widget_font.setFont(font)
            if has_alignment:  # 控件有setAlignment方法的话设置居中显示
                widget_font.setAlignment(QtCore.Qt.AlignCenter)

    hint_dic = (('抽取个数不能为零,请重新输入', 'the number of extracts cannot be zero, please re-enter'),
                ('请输入数字', 'please enter the number'),
                ('抽取数量超出总数,请重新输入', 'the number of extracts exceeds the total, please re-enter'),
                ('往上没有更多记录了', 'there are no more records upwards'),
                ('往下没有更多记录了', 'there are no more records downwards'),
                ('现在还没有名字,请先添加名字叭', 'there have no names to extract,please add names to continue')
                )

    hint_index = 0

    hint_state = False

    def set_hint(self, hint):  # 设置提示标签
        self.clear_widget(self.gridLayout)
        self.hint_label = QtWidgets.QLabel(hint[0] if self.language == '简体中文' else hint[1])
        self.set_font_size(self.hint_label)
        self.gridLayout.addWidget(self.hint_label)
        self.hint_state = True

        # 每次设置hint都根据索引改变hint_index的值,方便改变语言后可以显示改变后的hint
        self.hint_index = self.hint_dic.index(hint)

    def relayout(self):  # 当改变每行显示个数时重新布局
        if self.gridLayout.count() == 1:  # 当页面上只有一个控件时不执行操作,避免不必要的资源使用
            return
        self.clear_widget(self.gridLayout)
        current_page = int(self.page_label.text())
        try:
            names = self.sqlite.query(current_page)[0][2].split()  # 当还没有抽取时界面依然有页数,但因为没有记录所以不能读取到名字
            self.layout_name_to_window(names)
        except IndexError:
            ...

    def layout_name_to_window(self, names):  # 将名字布局到页面
        # 初始化行为0，列为-1（因为每次点击都会先加1）
        self.clear_widget(self.gridLayout)
        self.row = 0
        self.col = -1
        counter = 0
        for name in names:
            counter += 1
            # 如果列达到指定个数，则换行，并将列重置为0，否则列加1
            if self.col == self.current_quantity - 1:
                self.row += 1
                self.col = 0
            else:
                self.col += 1
            # 创建新的名字标签,显示序号状态为真时在每个名字前添加序号
            self.name_label = QtWidgets.QLabel(str(counter) + name) if self.show_sequence_state else QtWidgets.QLabel(
                name)
            self.name_label.setMinimumSize(130, 40)  # 设置每个按钮的最小大小，以便看清楚文本
            # 将当前名字标签加入到gridlayout中的Layout中，指定位置为当前的行和列
            self.gridLayout.addWidget(self.name_label, self.row, self.col)
            # 设置每个名字标签字体大小
            self.set_font_size(self.name_label)

    current_page = 0

    def record(self, names):
        # 保存抽取记录
        self.current_page += 1
        record_time = str(datetime.now())
        self.sqlite.add_record(names, record_time)
        self.page_label.setText(str(self.current_page))  # 每次保存都更新页数
        self.page_comboBox.addItem(str(self.current_page))  # 每次保存记录都向查看记录下拉框添加新的页数

    def drawing_number(self):  # 抽号函数
        self.hint_state = False  # 当主窗口显示的内容不是提示信息时设置hint_state为False,避免每次改变语言主窗口都显示提示信息
        name_list = self.sqlite.name_data()  # 从数据库里读取要抽取名字
        num = self.lineEdit.text()  # 获取输入框内容
        if not name_list:  # 数据库里没有名字时停止函数
            self.set_hint(self.hint_dic[5])
            return
        if not num:  # 不输入数字默认抽一个
            self.clear_widget(self.gridLayout)
            name = sample(name_list, 1)[0]
            self.name_label = QtWidgets.QLabel('1' + name) if self.show_sequence_state else QtWidgets.QLabel(name)
            self.set_font_size(self.name_label)
            self.name_label.setMinimumSize(130, 40)  # 设置每个按钮的最小大小，以便看清楚文本
            self.gridLayout.addWidget(self.name_label)
            self.record(name)  # 每抽取一次就保存一次
            text = '当前页数:' if self.language == '简体中文' else 'current page:'
            self.page_comboBox.setItemText(0, f'{text}' + str(
                self.current_page))  # 实时显示当前页数
            return
        if num == '0':
            self.set_hint(self.hint_dic[0])
            return
        elif not num.isdigit():
            self.set_hint(self.hint_dic[1])
            return
        num = int(num)
        if num > len(name_list):
            self.set_hint(self.hint_dic[2])
            return

        names = sample(name_list, num)
        self.record(' '.join(names))  # 每抽取一次就保存一次
        self.page_comboBox.setItemText(0, '当前页数:' if self.language == '简体中文' else 'current page:' + str(
            self.current_page))  # 实时更新页数下拉框
        self.layout_name_to_window(names)  # 将名字显示到页面上

    def histo_record(self, page):  # 历史记录
        self.hint_state = False  # 当主窗口显示的内容不是提示信息时设置hint_state为False,避免每次改变语言主窗口都显示提示信息
        # 如果数据库没记录就终止函数
        extraction = self.sqlite.query(page)[0][2].split() if self.sqlite.query(page) else None
        if extraction is None:
            return
        self.layout_name_to_window(extraction)  # 将数据库里的记录显示到页面上
        self.page_label.setText(page)  # 每次查看记录都设置当前页数为选择的页数

    def last(self):  # 上一页
        self.hint_state = False  # 当主窗口显示的内容不是提示信息时设置hint_state为False,避免每次改变语言主窗口都显示提示信息
        current_page = int(self.page_label.text())  # 获取当前页数
        if current_page <= 1:  # 当下一页页数超出总数或数据库里没有记录时终止函数
            self.page_label.setText(str(0))
            self.set_hint(self.hint_dic[3])
            return
        pre_page = current_page - 1  # 上一页页数
        self.page_comboBox.blockSignals(True)  # 因为改变索引会执行combobox_histo(),与上翻功能重复,造成不必要的资源使用
        self.page_comboBox.setCurrentIndex(pre_page)
        self.page_comboBox.blockSignals(False)  # 解除禁用
        self.histo_record(str(pre_page))

    def next(self):  # 下一页
        self.hint_state = False  # 当主窗口显示的内容不是提示信息时设置hint_state为False,避免每次改变语言主窗口都显示提示信息
        next_page = int(self.page_label.text()) + 1  # 下一页页数
        last_page = self.sqlite.last_column()
        if next_page > last_page:  # 当没有记录或点击下一页超出总页数时结束函数并重置next_page
            self.page_label.setText(str(last_page + 1))
            self.set_hint(self.hint_dic[4])
            return
        self.page_comboBox.blockSignals(True)  # 因为改变索引会执行combobox_histo(),与下翻功能重复,造成不必要的资源使用
        self.page_comboBox.setCurrentIndex(next_page)
        self.page_comboBox.blockSignals(False)  # 解除禁用
        self.histo_record(str(next_page))

    def combobox_histo(self):  # 每次点击历史记录下拉框选择了非当前选择的页数就执行(历史记录下拉框索引改变)
        current_index = self.page_comboBox.currentIndex()  # 获取历史记录下拉框选择页数的索引
        self.histo_record(str(current_index))

    def show_time(self):  # 显示当前时间
        current_time = datetime.now().replace(microsecond=0)
        self.maximize_btn2.setText(str(current_time))

    def change_language(self, language):
        if language == 'English':  # 当选择的语言为英文时改变界面语言为英文
            self.translator.load('./languages/main_window_EN.qm')
            app = QApplication.instance()
            app.installTranslator(self.translator)
            self.retranslateUi(self)
        else:  # 当选择的语言为中文时改变界面语言为中文
            self.translator.load('./languages/main_window_CN.qm')
            app = QApplication.instance()
            app.installTranslator(self.translator)
            self.retranslateUi(self)

    def change_font_size(self, size):  # 设置控件显示字体大小
        self.font_size = size
        for widget_index in range(self.gridLayout.count()):  # 遍历显示当前名字的控件并设置字体大小,达到实时改变字体大小的效果
            widget = self.gridLayout.itemAt(widget_index).widget()
            self.set_font_size(widget)

    def set_quantity(self, quantity):  # 设置控件每行名字显示个数
        self.current_quantity = quantity

    def set_language(self, language):  # 设置当前语言
        self.language = language
        self.change_language(self.language)
        if self.hint_state is True:  # 当显示提示信息时hint_state为True
            self.set_hint(self.hint_dic[self.hint_index])

    def set_sequence_state(self, state):  # 设置序号显示状态
        self.show_sequence_state = state
        if self.show_sequence_state:  # 如果显示序号为真则遍历当前控件加上序号
            counter = 0
            for widget_index in range(self.gridLayout.count()):  # 获取gridLayout中的所有label控件
                counter += 1
                name_widget = self.gridLayout.itemAt(widget_index).widget()
                name = name_widget.text()
                name_widget.setText(str(counter) + name)

    def set_show_time_state(self, state):  # 设置时间显示状态
        self.show_time_state = state

    def settings(self):
        self.child.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

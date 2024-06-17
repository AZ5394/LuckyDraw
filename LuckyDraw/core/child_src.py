# coding:utf-8
# @Author:AZ5394
# GitHub:github.com/AZ5394
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt, QPropertyAnimation
from PyQt5 import QtWidgets
from ui.child_window import Ui_Form as Child_ui


class Child(Child_ui, QWidget):
    def __init__(self, font_size, current_quantity, language, show_sequence_state, show_time_state, time_button,
                 page_label, set_spec_btn_style, clear_widget, set_font_size, relayout, histo_record, show_time,
                 change_font_size, set_quantity, set_language, set_sequence_state, set_show_time_state, sqlite,
                 translator):
        super(Child, self).__init__()
        self.oldPos = None
        self.show_anim = None
        self.setupUi(self)  # 加载图形界面
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.font_size = font_size
        self.current_quantity = current_quantity
        self.language = language
        self.show_sequence_state = show_sequence_state
        self.show_time_state = show_time_state
        self.time_button = time_button
        self.page_label = page_label
        self.set_spec_btn_style = set_spec_btn_style
        self.clear_widget = clear_widget
        self.set_font_size = set_font_size
        self.relayout = relayout
        self.histo_record = histo_record
        self.show_time = show_time
        self.change_font_size = change_font_size
        self.set_quantity = set_quantity
        self.set_language = set_language
        self.set_sequence_state = set_sequence_state
        self.set_show_time_state = set_show_time_state
        self.sqlite = sqlite
        self.translator = translator

        if self.show_sequence_state:  # 如果序号显示状态为真则点击按钮
            self.show_sequence_btn.click()
        if self.show_time_state:  # 如果时间显示状态为真则点击按钮
            self.show_time_btn.click()

        # 实例化时根据注册表里的语言改变界面语言
        self.change_language(self.language)

        self.init_font_size_combobox()
        self.init_row_quantity_combobox()
        # 自动显示当前个数
        self.auto_show_current_number()
        # 自动显示当前名字
        self.auto_show_current_name(self.gridLayout_3, self.current_quantity)

    def showEvent(self, event):  # 显示动画
        self.show_anim = QPropertyAnimation(self, b'windowOpacity')
        self.show_anim.setStartValue(0)
        self.show_anim.setEndValue(1)
        self.show_anim.setDuration(500)
        self.show_anim.start()
        event.ignore()

    def hide_win(self):  # 隐藏动画
        self.hide_anim = QPropertyAnimation(self, b'windowOpacity')
        self.hide_anim.setStartValue(1)
        self.hide_anim.setEndValue(0)
        self.hide_anim.setDuration(500)
        self.hide_anim.finished.connect(self.hide)
        self.hide_anim.start()

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

    def auto_show_current_number(self):  # 自动显示当前名字和当前名字个数
        res = self.sqlite.name_data()  # 从数据库里读取要显示的名字
        self.label_1.setText(str(len(res)))

    def init_font_size_combobox(self):  # 自动添加字号大小选项到下拉框
        for num in range(1, 51):
            self.font_size_comboBox.addItem(str(num))

    def init_row_quantity_combobox(self):  # 自动添加每行显示个数到下拉框
        name_length = len(self.sqlite.name_data())
        if name_length == 0:  # 没有数据时结束函数
            return
        while self.row_quantity_comboBox.count() > 1:  # 当名字数据库里有数据时遍历删除每行显示个数下拉框选项
            self.row_quantity_comboBox.removeItem(1)  # 因为删除后索引会自动补齐,所以一直删除索引一
        for num in range(1, name_length + 1):
            self.row_quantity_comboBox.addItem(str(num))  # 添加个数选项到下拉框,最大值为名字个数

    # 设置普通按钮样式
    @staticmethod
    def set_general_btn_style(btn, width, height, image_path1, radius, image_path2):
        btn.setStyleSheet("QPushButton{"
                          f"width:{width}px;\n"
                          f"height:{height}px;\n"
                          f"image:url({image_path1});\n"
                          f"border-radius:{radius}px;\n"
                          "border:none}\n"
                          "QPushButton:hover{"
                          f"image:url({image_path2})"
                          "}")

    def add(self):  # 添加名字
        if self.add_btn.isChecked():  # 当点击添加按钮时开始添加名字功能
            if self.delete_btn.isChecked():  # 当删除按钮被点击一次时执行下一次点击,保证删除按钮功能完整运行
                self.delete_btn.click()
            self.set_general_btn_style(self.add_btn, 55, 55, 'image/complete1.png', 5, 'image/complete.png')
            self.add_btn.setToolTip('完成')
            self.plainTextEdit.clear()  # 清除上一次的输入结果
            self.stackedWidget.setCurrentIndex(1)  # 点击添加名字按钮时跳转到第2页
            self.plainTextEdit.setFocus()  # 光标自动移动到输入框
            hint = '名字之间请用空格分开' if self.language == '简体中文' else 'please separate the names with spaces'
            self.hint_label.setText(hint)
            self.hint_label.setStyleSheet("color: rgb(133, 133, 133)")
            return
        # 点击完成按钮时结束添加功能并保存名字到数据库
        self.set_general_btn_style(self.add_btn, 55, 55, 'image/add.png', 5, 'image/add1.png')
        self.add_btn.setToolTip('添加名字')
        self.hint_label.setText('')
        names = self.plainTextEdit.toPlainText().strip()  # 获取输入框的值并写入
        if names:  # 当输入框有名字时
            # 保存名字
            self.sqlite.add_name(names)
            # 重新加载下拉框选项
            self.init_row_quantity_combobox()
            # 重新显示当前个数,达到实时显示的效果
            self.auto_show_current_number()
            # 重新显示名字,达到实时更新名字的效果
            self.auto_show_current_name(self.gridLayout_3, self.current_quantity)
        # 再次点击按钮时返回主页面
        self.stackedWidget.setCurrentIndex(0)

    def delete(self):  # 删除名字
        if self.delete_btn.isChecked():  # 点击删除名字按钮时开始删除名字功能
            if self.add_btn.isChecked():  # 当添加按钮被点击一次时执行下一次点击,保证添加按钮功能完整运行
                self.add_btn.click()

            self.set_general_btn_style(self.delete_btn, 55, 55, 'image/complete1.png', 5, 'image/complete.png')
            self.delete_btn.setToolTip('完成')
            self.stackedWidget.setCurrentIndex(2)  # 点击删除名字按钮时跳转到第3页
            hint = '单击名字删除' if self.language == '简体中文' else 'click name to delete'
            self.hint_label.setText(hint)
            self.hint_label.setStyleSheet("color: rgb(133, 133, 133)")
            self.format_layout(self.gridLayout, self.current_quantity, set_stylesheet=True)  # 重新把名字添加到布局上
            return
        # 点击完成按钮时结束删除功能
        self.set_general_btn_style(self.delete_btn, 55, 55, 'image/delete.png', 5, 'image/delete1.png')
        self.delete_btn.setToolTip('删除名字')
        self.hint_label.setText('')
        self.stackedWidget.setCurrentIndex(0)  # 返回主页面
        self.auto_show_current_name(self.gridLayout_3, self.current_quantity)

    def new_btn_clicked(self):  # 点击删除的名字时
        # 获取点击的按钮对象和按钮显示的文本
        sender = self.sender()
        name = sender.text()
        self.sqlite.delete_name(name)  # 从数据库里删除点击的名字
        sender.deleteLater()  # 删除点击的按钮
        # 重新显示当前个数,达到实时显示的效果
        self.auto_show_current_number()
        # 重新初始化每行个数下拉框显示内容
        self.init_row_quantity_combobox()

    def change_current_font_size(self):  # 改变当前的字体大小
        self.font_size = self.font_size_comboBox.currentIndex()
        if self.font_size == 0:  # 当前索引为零时不执行操作
            return
        self.change_font_size(self.font_size)  # 改变整个程序字体大小
        show_res = '当前大小:' if self.language == '简体中文' else 'font size:'
        self.font_size_comboBox.setItemText(0, show_res + str(self.font_size))
        self.set_font_size(self.plainTextEdit, has_alignment=False)

        for widget_index in range(self.gridLayout_3.count()):  # 遍历显示当前名字的控件并设置字体大小,达到实时改变字体大小的效果
            widget = self.gridLayout_3.itemAt(widget_index).widget()
            self.set_font_size(widget)

        for i in range(self.gridLayout.count()):  # 遍历删除名字的控件并设置字体大小,达到实时改变字体大小的效果
            widget = self.gridLayout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QPushButton):
                self.set_font_size(widget, has_alignment=False)
                widget.setStyleSheet("QPushButton{\n"
                                     "border-radius:15px}\n"
                                     "QPushButton:hover{\n"
                                     "image:url(image/close4.png)\n"
                                     "}")

    # 每行按一定个数格式化显示名字
    def format_layout(self, layout, quantity_per_row, has_all_name=False, set_stylesheet=False):  # 格式化每行名字显示个数
        if quantity_per_row == 0:  # 当要布局的控件个数为零时结束函数
            return
        self.clear_widget(layout)
        all_name = has_all_name if has_all_name else self.sqlite.name_data()
        # 初始化行为0，列为-1（因为每次点击都会先加1）
        self.row = 0
        self.col = -1
        for name in all_name:
            # 如果列达到指定个数，则换行，并将列重置为0，否则列加1
            if self.col == quantity_per_row - 1:
                self.row += 1
                self.col = 0
            else:
                self.col += 1
            if set_stylesheet:  # 可以设置样式的是删除按钮页面,否则是显示名字的标签页面
                self.name_label = QtWidgets.QPushButton(name)
                self.set_font_size(self.name_label, has_alignment=False)  # 设置按钮文本大小
                self.name_label.clicked.connect(self.new_btn_clicked)  # 绑定点击事件
                self.name_label.setStyleSheet("QPushButton{\n"
                                              "width:45px;\n"
                                              "height:45px;\n"
                                              "border-radius:15px}\n"
                                              "QPushButton:hover{\n"
                                              "image:url(image/close4.png)\n"
                                              "}")
            else:
                self.name_label = QtWidgets.QLabel(name)
                self.set_font_size(self.name_label)
            self.name_label.setMinimumSize(130, 40)  # 设置每个按钮的最小大小，以便看清楚文本
            layout.addWidget(self.name_label, self.row, self.col)

    auto_show_current_name = format_layout

    def quantity_per_row(self):  # 改变每行显示的个数
        self.current_index = self.row_quantity_comboBox.currentIndex()
        self.current_quantity = self.current_index
        self.set_quantity(self.current_index)  # 更改主页面的quantity
        if self.current_index != 0:
            show_res = '当前个数:' if self.language == '简体中文' else 'number of displays per row:'
            self.row_quantity_comboBox.setItemText(0, show_res + str(self.current_index))  # 每次调用都显示调用时的个数
        self.format_layout(self.gridLayout_3, self.current_quantity)
        self.format_layout(self.gridLayout, self.current_quantity, set_stylesheet=True)
        self.relayout()

    def change_language(self, language=None):  # 改变语言
        lang = self.language_comboBox.currentIndex()
        if lang == 1 or language == 'English':  # 当选择的语言为英文时改变界面语言为英文
            self.language = language
            self.translator.load('./languages/child_window_EN.qm')
            app = QApplication.instance()
            app.installTranslator(self.translator)
            self.retranslateUi(self)
            self.set_language('English')
            # 字号下拉框索引为零项目的显示内容
            res1 = '当前大小:' if self.language == '简体中文' else 'font size:'
            self.font_size_comboBox.setItemText(0, res1 + str(self.font_size))
            # 每行个数下拉框索引为零项目的显示内容
            res2 = '当前个数:' if self.language == '简体中文' else 'number of displays per row:'
            self.row_quantity_comboBox.setItemText(0, res2 + str(self.current_quantity))
        elif lang == 0 or language == '简体中文':  # 当选择的语言为中文时改变界面语言为中文
            self.language = '简体中文'
            self.translator.load('./languages/child_window_CN.qm')
            app = QApplication.instance()
            app.installTranslator(self.translator)
            self.retranslateUi(self)
            self.set_language('简体中文')
            # 初始化字号下拉框显示内容
            res1 = '当前大小:' if self.language == '简体中文' else 'font size:'
            self.font_size_comboBox.setItemText(0, res1 + str(self.font_size))
            # 初始化每行个数下拉框显示内容
            res2 = '当前个数:' if self.language == '简体中文' else 'number of displays per row:'
            self.row_quantity_comboBox.setItemText(0, res2 + str(self.current_quantity))

    def display_sequence_number(self):  # 显示序号
        # 当显示序号按钮状态为开时
        if self.show_sequence_btn.isChecked():
            self.show_sequence_state = True  # 设置显示序号状态为开
            self.set_sequence_state(self.show_sequence_state)
            self.set_general_btn_style(self.show_sequence_btn, 45, 35, 'image/open.png', 5, 'image/open1.png')
            self.show_sequence_btn.setToolTip('关')

        # 当显示序号按钮状态为关时
        else:
            self.show_sequence_state = False  # 设置显示序号状态为关
            self.set_sequence_state(self.show_sequence_state)
            current_page = self.page_label.text()  # 获取当前页数
            self.histo_record(current_page)  # 重新显示原始记录
            self.set_general_btn_style(self.show_sequence_btn, 45, 35, 'image/close.png', 5, 'image/close1.png')
            self.show_sequence_btn.setToolTip('开')

    def show_current_time(self):  # 实时显示当前时间
        # 当显示时间按钮状态为关时
        if not self.show_time_btn.isChecked():
            self.set_general_btn_style(self.show_time_btn, 45, 35, 'image/close.png', 5, 'image/close1.png')
            self.show_time_btn.setToolTip('开')
            self.show_time_state = False  # 设置显示时间状态为关
            self.set_show_time_state(self.show_time_state)
            self.time_button.setText('')
            self.timer.stop()  # 停止显示时间
        # 当显示时间按钮状态为开时
        elif self.show_time_btn.isChecked() or self.show_time_state:
            self.set_general_btn_style(self.show_time_btn, 45, 35, 'image/open.png', 5, 'image/open1.png')
            self.show_time_btn.setToolTip('关')
            self.show_time_state = True  # 设置显示时间状态为开
            self.set_show_time_state(self.show_time_state)
            self.timer = QTimer(self)  # 开始显示时间
            self.timer.timeout.connect(self.show_time)
            self.timer.start(1000)

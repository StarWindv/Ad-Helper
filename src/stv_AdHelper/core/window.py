import time

import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QGroupBox, QCheckBox,
                             QSpinBox, QDoubleSpinBox, QTextEdit, QMessageBox, QTabWidget)
from stv_AdHelper.core.worker import AutomationWorker
from stv_AdHelper.utils.utils import load_config, play_sound, save_config


class AutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.config = {}
        self.init_ui()
        self.load_config()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("自动公屏广告助手  by 星灿长风v")
        self.setGeometry(300, 300, 800, 600)
        self.setWindowIcon(QIcon(self.create_icon()))

        # 设置深色主题
        self.set_dark_theme()

        # 创建主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # 配置标签页
        config_tab = QWidget()
        tab_widget.addTab(config_tab, "配置")
        self.setup_config_tab(config_tab)

        # 操作标签页
        action_tab = QWidget()
        tab_widget.addTab(action_tab, "操作")
        self.setup_action_tab(action_tab)

        # 日志标签页
        log_tab = QWidget()
        tab_widget.addTab(log_tab, "日志")
        self.setup_log_tab(log_tab)

        # 添加状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")

    def set_dark_theme(self):
        """设置深色主题"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        # 设置全局样式表
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #5c5c5c;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #6c6c6c;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #7c7c7c;
            }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 3px;
                color: white;
            }
            QLabel {
                color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background: #353535;
            }
            QTabBar::tab {
                background: #454545;
                color: white;
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #555555;
                border-bottom: 2px solid #8e2dc5;
            }
        """)

    def create_icon(self):
        """创建应用图标（程序内生成）"""
        from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush

        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        painter.setBrush(QBrush(QColor(142, 45, 197)))
        painter.drawEllipse(2, 2, 60, 60)

        # 绘制自动化图标（齿轮+鼠标）
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)

        # 绘制齿轮
        painter.drawEllipse(20, 20, 24, 24)
        for i in range(8):
            painter.save()
            painter.translate(32, 32)
            painter.rotate(i * 45)
            painter.drawLine(14, 0, 22, 0)
            painter.restore()

        # 绘制鼠标
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(40, 10, 12, 18)
        painter.drawLine(46, 28, 46, 40)

        painter.end()
        return pixmap

    def setup_config_tab(self, tab):
        """设置配置标签页"""
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # 坐标配置组
        coords_group = QGroupBox("坐标设置")
        coords_layout = QVBoxLayout(coords_group)

        # A点坐标
        a_layout = QHBoxLayout()
        a_layout.addWidget(QLabel("A点坐标 (文本框位置):"))
        self.a_x_input = QSpinBox()
        self.a_x_input.setRange(0, 9999)
        self.a_x_input.setFixedWidth(80)
        a_layout.addWidget(self.a_x_input)
        a_layout.addWidget(QLabel("X"))
        self.a_y_input = QSpinBox()
        self.a_y_input.setRange(0, 9999)
        self.a_y_input.setFixedWidth(80)
        a_layout.addWidget(self.a_y_input)
        a_layout.addWidget(QLabel("Y"))

        self.capture_a_btn = QPushButton("获取坐标")
        self.capture_a_btn.setFixedWidth(100)
        self.capture_a_btn.clicked.connect(lambda: self.capture_coordinates('a'))
        a_layout.addWidget(self.capture_a_btn)
        a_layout.addStretch()
        coords_layout.addLayout(a_layout)

        # B点坐标
        b_layout = QHBoxLayout()
        b_layout.addWidget(QLabel("B点坐标 (按钮位置):"))
        self.b_x_input = QSpinBox()
        self.b_x_input.setRange(0, 9999)
        self.b_x_input.setFixedWidth(80)
        b_layout.addWidget(self.b_x_input)
        b_layout.addWidget(QLabel("X"))
        self.b_y_input = QSpinBox()
        self.b_y_input.setRange(0, 9999)
        self.b_y_input.setFixedWidth(80)
        b_layout.addWidget(self.b_y_input)
        b_layout.addWidget(QLabel("Y"))

        self.capture_b_btn = QPushButton("获取坐标")
        self.capture_b_btn.setFixedWidth(100)
        self.capture_b_btn.clicked.connect(lambda: self.capture_coordinates('b'))
        b_layout.addWidget(self.capture_b_btn)
        b_layout.addStretch()
        coords_layout.addLayout(b_layout)

        layout.addWidget(coords_group)

        # 内容配置组
        content_group = QGroupBox("操作内容")
        content_layout = QVBoxLayout(content_group)

        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("请输入要粘贴的内容...")
        content_layout.addWidget(self.content_input)

        layout.addWidget(content_group)

        # 参数配置组
        params_group = QGroupBox("执行参数")
        params_layout = QVBoxLayout(params_group)

        # 间隔时间
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("操作间隔时间 (秒):"))
        self.interval_input = QDoubleSpinBox()
        self.interval_input.setRange(0.1, 3600)
        self.interval_input.setValue(10)
        self.interval_input.setSingleStep(1)
        interval_layout.addWidget(self.interval_input)
        interval_layout.addStretch()
        params_layout.addLayout(interval_layout)

        # 重复次数
        repeat_layout = QHBoxLayout()
        repeat_layout.addWidget(QLabel("重复次数 (0=无限):"))
        self.repeat_input = QSpinBox()
        self.repeat_input.setRange(0, 9999)
        self.repeat_input.setValue(0)
        repeat_layout.addWidget(self.repeat_input)
        repeat_layout.addStretch()
        params_layout.addLayout(repeat_layout)

        # 提示音
        self.sound_checkbox = QCheckBox("启用操作提示音")
        self.sound_checkbox.setChecked(True)
        params_layout.addWidget(self.sound_checkbox)

        layout.addWidget(params_group)

        # 保存按钮
        save_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存配置")
        self.save_btn.setFixedHeight(40)
        self.save_btn.clicked.connect(self.save_config)
        save_layout.addWidget(self.save_btn)

        layout.addLayout(save_layout)
        layout.addStretch()

    def setup_action_tab(self, tab):
        """设置操作标签页"""
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # 状态信息
        status_group = QGroupBox("当前状态")
        status_layout = QVBoxLayout(status_group)

        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.status_label)

        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.progress_label)

        self.next_time_label = QLabel("")
        self.next_time_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.next_time_label)

        layout.addWidget(status_group)

        # 操作按钮
        buttons_layout = QHBoxLayout()

        self.start_btn = QPushButton("开始执行")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setStyleSheet("background-color: #4CAF50; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_automation)
        buttons_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("停止执行")
        self.stop_btn.setFixedHeight(50)
        self.stop_btn.setStyleSheet("background-color: #F44336; font-weight: bold;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_automation)
        buttons_layout.addWidget(self.stop_btn)

        layout.addLayout(buttons_layout)

        # 测试按钮
        test_layout = QHBoxLayout()

        self.test_a_btn = QPushButton("测试A点")
        self.test_a_btn.setFixedHeight(40)
        self.test_a_btn.clicked.connect(self.test_point_a)
        test_layout.addWidget(self.test_a_btn)

        self.test_b_btn = QPushButton("测试B点")
        self.test_b_btn.setFixedHeight(40)
        self.test_b_btn.clicked.connect(self.test_point_b)
        test_layout.addWidget(self.test_b_btn)

        layout.addLayout(test_layout)

        layout.addStretch()

    def setup_log_tab(self, tab):
        """设置日志标签页"""
        layout = QVBoxLayout(tab)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_text)

        # 添加清除日志按钮
        clear_btn = QPushButton("清除日志")
        clear_btn.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(clear_btn)

    def load_config(self):
        """加载保存的配置"""
        self.config = load_config()

        # 更新UI元素
        if 'a_point' in self.config:
            x, y = self.config['a_point']
            self.a_x_input.setValue(x)
            self.a_y_input.setValue(y)

        if 'b_point' in self.config:
            x, y = self.config['b_point']
            self.b_x_input.setValue(x)
            self.b_y_input.setValue(y)

        if 'paste_content' in self.config:
            self.content_input.setText(self.config['paste_content'])

        if 'interval' in self.config:
            self.interval_input.setValue(self.config['interval'])

        if 'repeat_times' in self.config:
            self.repeat_input.setValue(self.config['repeat_times'])

        if 'sound_enabled' in self.config:
            self.sound_checkbox.setChecked(self.config['sound_enabled'])

    def save_config(self, info: bool = True):
        """保存配置到文件和内存"""
        self.config = {
            'a_point': (self.a_x_input.value(), self.a_y_input.value()),
            'b_point': (self.b_x_input.value(), self.b_y_input.value()),
            'paste_content': self.content_input.text(),
            'interval': self.interval_input.value(),
            'repeat_times': self.repeat_input.value(),
            'sound_enabled': self.sound_checkbox.isChecked()
        }

        if save_config(self.config):
            self.log("配置已保存")
            if info:
                QMessageBox.information(self, "保存成功", "配置已保存成功！")
        else:
            self.log("保存配置失败")
            if info:
                QMessageBox.warning(self, "保存失败", "保存配置时出错，请检查日志。")

    def capture_coordinates(self, point_type):
        """捕获鼠标坐标"""
        self.status_bar.showMessage(f"请将鼠标移动到{point_type.upper()}点位置...")
        self.log(f"准备捕获{point_type.upper()}点坐标")

        # 显示倒计时对话框
        from PyQt5.QtWidgets import QDialog, QProgressBar, QVBoxLayout
        dialog = QDialog(self)
        dialog.setWindowTitle(f"捕获{point_type.upper()}点")
        dialog.setModal(True)
        layout = QVBoxLayout(dialog)

        label = QLabel(f"请将鼠标移动到{point_type.upper()}点位置...\n\n程序将在5秒后捕获坐标")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        progress = QProgressBar()
        progress.setRange(0, 50)  # 50个0.1秒=5秒
        layout.addWidget(progress)

        dialog.show()

        # 开始倒计时
        for i in range(50):
            time.sleep(0.1)
            progress.setValue(i + 1)
            QApplication.processEvents()  # 处理UI事件

        # 获取坐标
        pos = pyautogui.position()
        self.log(f"捕获{point_type.upper()}点坐标: {pos}")

        # 更新UI
        if point_type == 'a':
            self.a_x_input.setValue(pos.x)
            self.a_y_input.setValue(pos.y)
        else:
            self.b_x_input.setValue(pos.x)
            self.b_y_input.setValue(pos.y)

        dialog.close()
        self.status_bar.showMessage(f"{point_type.upper()}点坐标已捕获: {pos}")
        play_sound(800, 200)  # 成功提示音

    def test_point_a(self):
        """测试A点位置"""
        try:
            x, y = self.a_x_input.value(), self.a_y_input.value()
            self.log(f"测试A点: ({x}, {y})")
            pyautogui.click(x, y)
            play_sound(1000, 200)
            self.status_bar.showMessage("A点测试成功")
        except Exception as e:
            self.log(f"测试A点失败: {str(e)}")
            self.status_bar.showMessage(f"测试A点失败: {str(e)}")

    def test_point_b(self):
        """测试B点位置"""
        try:
            x, y = self.b_x_input.value(), self.b_y_input.value()
            self.log(f"测试B点: ({x}, {y})")
            pyautogui.click(x, y)
            play_sound(1000, 200)
            self.status_bar.showMessage("B点测试成功")
        except Exception as e:
            self.log(f"测试B点失败: {str(e)}")
            self.status_bar.showMessage(f"测试B点失败: {str(e)}")

    def start_automation(self):
        """开始自动化任务"""
        # 确保配置已保存
        self.save_config(info = False)

        # 创建并启动工作线程
        self.worker = AutomationWorker(self.config)
        self.worker.operation_completed.connect(self.on_operation_completed)
        self.worker.finished.connect(self.on_automation_finished)
        self.worker.error_occurred.connect(self.on_automation_error)

        self.worker.start()

        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("运行中")
        self.status_label.setStyleSheet("color: #4CAF50;")

        total = self.config.get('repeat_times', 0)
        if total == 0:
            self.progress_label.setText("运行模式: 无限循环")
        else:
            self.progress_label.setText(f"进度: 0/{total}")

        self.log("自动化任务已启动")
        self.status_bar.showMessage("自动化任务已启动")

    def stop_automation(self):
        """停止自动化任务"""
        if self.worker:
            self.worker.stop()
            self.worker.wait(2000)  # 等待线程结束

            # 更新UI状态
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_label.setText("已停止")
            self.status_label.setStyleSheet("color: #F44336;")
            self.next_time_label.setText("")

            self.log("自动化任务已停止")
            self.status_bar.showMessage("自动化任务已停止")
            play_sound(400, 800)  # 终止提示音

    def on_operation_completed(self, count, success, message):
        """处理操作完成信号"""
        total = self.config.get('repeat_times', 0)

        # 更新进度
        if total > 0:
            self.progress_label.setText(f"进度: {count}/{total}")

        # 更新下次执行时间
        next_time = time.strftime("%H:%M:%S", time.localtime(time.time() + self.config.get('interval', 10)))
        self.next_time_label.setText(f"下次执行: {next_time}")

        # 记录日志
        status = "成功" if success else "失败"
        self.log(f"操作 #{count}: {status} - {message}")

    def on_automation_finished(self):
        """处理自动化完成信号"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("已完成")
        self.status_label.setStyleSheet("color: #4CAF50;")
        self.next_time_label.setText("")

        self.log("自动化任务已完成")
        self.status_bar.showMessage("自动化任务已完成")
        play_sound(1000, 500)  # 完成提示音

    def on_automation_error(self, message):
        """处理自动化错误"""
        self.log(f"错误: {message}")
        self.status_bar.showMessage(f"错误: {message}")

        # 自动停止任务
        self.stop_automation()

        # 显示错误对话框
        QMessageBox.critical(self, "操作错误", f"执行自动化操作时发生错误:\n\n{message}")

    def log(self, message):
        """记录日志"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

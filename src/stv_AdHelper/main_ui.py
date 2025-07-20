import sys

from PyQt5.QtWidgets import QApplication
from stv_AdHelper.core.window import AutomationApp


def main():
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle("Fusion")

    # 创建并显示主窗口
    window = AutomationApp()
    window.show()
    sys.exit(app.exec_())
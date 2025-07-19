import time

import pyautogui
import pyperclip
from PyQt5.QtCore import QThread, pyqtSignal
from stv_AdHelper.utils.utils import play_sound


class AutomationWorker(QThread):
    """执行自动化操作的线程"""
    operation_completed = pyqtSignal(int, bool, str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.running = True
        self.count = 0

    def run(self):
        """执行自动化任务"""
        try:
            total = self.config.get('repeat_times', 0)

            while self.running:
                self.count += 1
                success = self.perform_operation()
                status = "成功" if success else "失败"

                # 检查是否完成指定次数
                if total > 0 and self.count >= total:
                    self.operation_completed.emit(self.count, success, "已完成所有操作")
                    self.finished.emit()
                    return

                # 等待下次执行
                if self.running:
                    self.sleep(int(self.config.get('interval', 10)))

        except Exception as e:
            self.error_occurred.emit(str(e))

    def perform_operation(self):
        """执行单次操作"""
        try:
            if self.config.get('sound_enabled', True):
                play_sound(800, 100)  # 操作开始提示音

            # 点击A点（激活文本框）
            a_point = self.config.get('a_point', (0, 0))
            pyautogui.click(a_point)
            time.sleep(0.3)

            # 粘贴内容

            content = self.config.get('paste_content', '')
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)

            # 点击B点
            b_point = self.config.get('b_point', (0, 0))
            pyautogui.click(b_point)

            if self.config.get('sound_enabled', True):
                play_sound(1200, 100)  # 操作成功提示音

            return True
        except Exception as e:
            if self.config.get('sound_enabled', True):
                play_sound(300, 500)  # 错误提示音
            raise e

    def stop(self):
        """停止自动化任务"""
        self.running = False
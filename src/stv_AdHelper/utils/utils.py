import json
import os
import platform
from pathlib import Path


def get_config_path():
    """获取配置文件路径（用户主目录下的隐藏文件）"""
    home_dir = Path.home()
    config_path = home_dir / ".AutoAd_config.json"
    return config_path


def save_config(config, cli: bool = False):
    """保存配置到文件"""
    config_path = get_config_path()
    try:
        # 创建可序列化的配置副本
        saveable_config = config.copy()
        saveable_config['a_point'] = list(saveable_config['a_point'])
        saveable_config['b_point'] = list(saveable_config['b_point'])

        with open(config_path, 'w') as f:
            json.dump(saveable_config, f, indent=4)
        if cli:
            print(f"✓ 配置已保存至: {config_path}")
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def load_config():
    """从文件加载配置"""
    config_path = get_config_path()
    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # 转换坐标点为元组
        if 'a_point' in config:
            config['a_point'] = tuple(config['a_point'])
        if 'b_point' in config:
            config['b_point'] = tuple(config['b_point'])
        return config
    except Exception as e:
        print(f"加载配置失败: {e}")
        return {}


def play_sound(frequency=500, duration=300):
    """跨平台提示音"""
    try:
        if platform.system() == 'Windows':
            import winsound
            winsound.Beep(frequency, duration)
        elif platform.system() == 'Darwin':  # MacOS
            os.system(f'afplay /System/Library/Sounds/Ping.aiff')
        else:  # Linux
            os.system('echo -ne "\a"')
    except:
        print("\a", end='')  # 备选方案

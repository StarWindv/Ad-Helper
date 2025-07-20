import re
import time

import pyautogui
import pyperclip
from stv_AdHelper.utils.utils import play_sound, load_config, save_config
from stv_utils import system_clear


def get_point_with_prompt(point_name)->tuple:
    """交互式获取坐标点"""
    input(f"请将鼠标移到【{point_name}】(5秒内完成)，按回车键开始...")
    print(f"获取{point_name}位置中...")
    time.sleep(2)  # 给用户准备时间
    point = pyautogui.position()
    play_sound(800, 200)  # 成功提示音
    print(f"✓ {point_name}坐标已获取: {point}")
    return point


def get_user_config()->dict:
    """交互式获取用户配置"""
    # 尝试加载现有配置
    saved_config = load_config()

    if saved_config:
        system_clear()
        print("\n找到已保存的配置:")
        print(f"  目标窗口: A点{saved_config['a_point']} → 输入内容 → B点{saved_config['b_point']}")
        print(f"  操作内容: {re.sub("\n", "#n", saved_config['paste_content'])}")
        print(f"  执行频率: 每 {saved_config['interval']} 秒")
        print(f"  重复次数: {'无限' if saved_config['repeat_times'] == 0 else saved_config['repeat_times']}次")

        use_saved = input("\n是否使用已保存的配置? (y/n): ").lower() == 'y'
        if use_saved:
            # 询问是否启用提示音
            sound_enabled = input("启用操作提示音? (y/n): ").lower() == 'y'
            saved_config['sound_enabled'] = sound_enabled
            return saved_config

    system_clear()
    print("\n" + "="*50)
    print("自动化脚本配置向导".center(40))
    print("="*50)

    # 1. 坐标获取方式选择
    config_type = input("\n选择配置方式:\n1. 自动获取坐标\n2. 手动输入坐标\n请选择(1/2): ")

    if config_type == '1':
        print("\n【A点配置】文本框位置获取:")
        a_point = get_point_with_prompt("A点(文本框)")

        print("\n【B点配置】操作按钮位置获取:")
        b_point = get_point_with_prompt("B点(按钮)")
    else:
        print("\n【手动输入坐标】")
        try:
            a_x = int(input("请输入A点(X坐标): "))
            a_y = int(input("请输入A点(Y坐标): "))
            b_x = int(input("请输入B点(X坐标): "))
            b_y = int(input("请输入B点(Y坐标): "))
            a_point, b_point = (a_x, a_y), (b_x, b_y)
        except ValueError:
            print("错误: 请输入有效数字!")
            exit()

    # 2. 输入操作内容
    paste_content = input("\n请输入要粘贴的内容: ")

    # 3. 设置间隔时间
    while True:
        try:
            interval = float(input("\n设置操作间隔时间(秒): "))
            if interval <= 0:
                print("间隔时间需大于0!")
                continue
            break
        except ValueError:
            print("请输入有效数字!")

    # 4. 设置重复次数
    while True:
        try:
            repeat_times = int(input("\n设置重复次数(0=无限循环): "))
            if repeat_times < 0:
                print("重复次数不能为负数!")
                continue
            break
        except ValueError:
            print("请输入整数!")

    # 5. 配置提示音
    sound_enabled = input("\n启用操作提示音? (y/n): ").lower() == 'y'

    config = {
        'a_point': a_point,
        'b_point': b_point,
        'paste_content': paste_content,
        'interval': interval,
        'repeat_times': repeat_times,
        'sound_enabled': sound_enabled
    }

    config["paste_content"] = re.sub('#n', '\n', config["paste_content"])

    # 询问是否保存配置
    save_config_option = input("\n是否保存此配置以便下次使用? (y/n): ").lower() == 'y'
    if save_config_option:
        save_config(config, cli=True)

    return config


def auto_operate(config)->bool:
    """执行单次操作"""
    try:
        if config['sound_enabled']:
            play_sound(800, 100)  # 操作开始提示音

        # 点击A点（激活文本框）
        pyautogui.click(config['a_point'])
        time.sleep(0.3)

        # 粘贴内容
        pyperclip.copy(config['paste_content'])
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

        # 点击B点
        pyautogui.click(config['b_point'])

        if config['sound_enabled']:
            play_sound(1200, 100)  # 操作成功提示音

        return True
    except Exception as e:
        if config['sound_enabled']:
            play_sound(300, 500)  # 错误提示音
        print(f"⚠️ 操作出错: {e}")
        return False
import time

from stv_AdHelper.utils.cli_utils import get_user_config, auto_operate
from stv_AdHelper.utils.utils import play_sound
from stv_utils import system_clear


def main():    # 获取用户配置
    try:
        config = get_user_config()

        system_clear()
        print("\n" + "="*len("操作内容: {config['paste_content']}"))
        print("自动化脚本准备就绪".center(50))
        print("\n" + "="*len("操作内容: {config['paste_content']}"))
        print(f"目标窗口: A点{config['a_point']} → 输入内容 → B点{config['b_point']}")
        print(f"操作内容: {config['paste_content']}")
        print(f"执行频率: 每 {config['interval']} 秒")
        print(f"重复次数: {'无限' if config['repeat_times'] == 0 else config['repeat_times']}次")
        print(f"提示音: {'启用' if config['sound_enabled'] else '禁用'}")
        print("\n" + "="*len("操作内容: {config['paste_content']}"))

        input("\n按回车键开始执行，按Ctrl+C终止程序...")

        # 执行主循环
        count = 0
        total = config['repeat_times']
        start_time = time.time()
    except KeyboardInterrupt:
        print("\n\n⛔ 用户手动终止程序")
        play_sound(400, 800)  # 终止提示音
        return
    
    try:
        while True:
            count += 1
            print(f"\n▶ 开始第 {count}/{'∞' if total==0 else total} 次操作")
            
            success = auto_operate(config)
            status = "✓ 成功" if success else "✗ 失败"
            
            # 计算下次执行时间
            next_time = time.strftime("%H:%M:%S", 
                          time.localtime(start_time + count * config['interval']))
            
            print(f"{status} | 下次执行: {next_time}")
            
            # 检查是否完成指定次数
            if 0 < total <= count:
                print(f"\n✅ 已完成所有 {total} 次操作")
                play_sound(1000, 500)  # 完成提示音
                break
                
            # 等待下次执行
            time.sleep(config['interval'])
            
    except KeyboardInterrupt:
        print("\n\n⛔ 用户手动终止程序")
        play_sound(400, 800)  # 终止提示音

from nicegui import ui

import time

# 初始化 B 和 C 的值

burn_info = {'left': 100, 'total': 100}

TEXT_FONT='text-5xl '

# 创建按钮，点击按钮时修改 B 和 C 的值，并更新第一行的标签文本
def change_values(value):
    burn_info.update(left=50)


def create_ui(pre):

    # 创建主容器，用于包含行布局和按钮
    with ui.column().classes('w-full h-screen p-4').style('text-align: left; display: flex; flex-direction: column;'):

        # 创建第一行的标签，显示烧写信息和模式，并根据事件修改 B 和 C 的值
        with ui.row().classes('items-center relative w-full').style('flex-grow: 1; flex-shrink: 1; margin-bottom: 0;'):
            label_first_row_1 = ui.label('烧写信息: ').classes(TEXT_FONT)
            label_first_row_2 = ui.label().classes(TEXT_FONT).bind_text_from(pre.burn_info, 'left', backward= lambda t: f'{t}')
            label_first_row_3 = ui.label('/').classes(TEXT_FONT)
            label_first_row_4 = ui.label().classes(TEXT_FONT).bind_text_from(pre.burn_info, 'total', backward= lambda l: f'{l}')

            label_first_row_5 = ui.label(f' 模式:{pre.mode}').classes(TEXT_FONT)

        # 创建第二行到第四行的文本
        label_second_row = ui.label(f'当前芯片： {pre.chip}').classes(TEXT_FONT)
        label_third_row = ui.label(f'文件名字： {pre.fw} 已授权').classes(TEXT_FONT)
        label_fourth_row = ui.label(f'校验码： {pre.check}').classes(TEXT_FONT)

        # 创建八行布局，每行包含一个编号、一个居中显示的文本标签和一个长度较长的进度条
        for i in range(1, 9):
            with ui.row().classes('items-center relative w-full').style('flex-grow: 1; flex-shrink: 1; margin-bottom: 0;'):
                # 数字编号
                ui.label(f'{i}').classes(TEXT_FONT + 'mr-2')

                with ui.row().classes('relative flex-grow h-full items-center'):
                    # Ready文本
                    ui.label('Ready').classes(TEXT_FONT + 'w-full h-full bg-transparent text-left relative z-10 flex items-center')
                    
                    # 进度条
                    progress = ui.linear_progress(value=0, show_value=False).style('height: 100%; background-color: #f0f0f0;').classes('absolute top-0 left-0 w-full')


        # ui.button('Change Values').on('click', change_values)

    ui.run()
# 运行 NiceGUI 应用

CHANNELS = 8 # 通道数

class Ui_check:
    mode = None
    chip = None
    fw = None
    check = None
    burn_info = {'left': 100, 'total': 100}
    ui_labels = None
    ui_process = None


    def __init__(self, mode, chip, fw, check, total, left):
        Ui_check.mode = mode
        Ui_check.chip = chip
        Ui_check.fw = fw
        Ui_check.check = check
        Ui_check.burn_info.update(total=total)
        Ui_check.burn_info.update(left=left)

        create_ui(self)
    
    # def __del__(self):

    # def start(self, ch):


    # def set_process(self, ch, process):

    # def set_success(self, ch, text):

    # def set_failed(self, ch, text):


Ui_check('烧写', 'CSK5060', 'fw.bin', '4A33-76449996', 300, 300)
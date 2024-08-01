from nicegui import ui

CHANNELS = 8 # 通道数
TEXT_FONT='text-4xl ' # 文字字体大小

def create_ui(pre):

    progress_bars = []

    # 创建主容器，用于包含行布局和按钮
    with ui.column().classes('w-full h-screen p-8').style('text-align: left; display: flex; flex-direction: column;'):

        # 创建第一行的标签，显示烧写信息和模式，并根据事件修改 B 和 C 的值
        with ui.row().classes('items-center relative w-full'):
            label_first_row_1 = ui.label('烧写信息： ').classes(TEXT_FONT)
            label_first_row_2 = ui.label().classes(TEXT_FONT).bind_text_from(pre.burn_info, 'left', backward= lambda t: f'{t}')
            label_first_row_3 = ui.label('/').classes(TEXT_FONT)
            label_first_row_4 = ui.label().classes(TEXT_FONT).bind_text_from(pre.burn_info, 'total', backward= lambda l: f'{l}')

            label_first_row_5 = ui.label(f'模式：{pre.mode}').classes(TEXT_FONT)

        # 创建第二行到第四行的文本
        label_second_row = ui.label(f'当前芯片： {pre.chip}').classes(TEXT_FONT)
        label_third_row = ui.label(f'文件名字： {pre.fw} 已授权').classes(TEXT_FONT)
        label_fourth_row = ui.label(f'校验码： {pre.check}').classes(TEXT_FONT)

        # 创建八行布局，每行包含一个编号、一个居中显示的文本标签和一个长度较长的进度条
        for i in range(1, 1 + CHANNELS):
            with ui.row().classes('items-center relative w-full').style('flex-grow: 1; flex-shrink: 1; margin-bottom: 10;'):
                # 数字编号
                ui.label(f'{i}').classes(TEXT_FONT + 'mr-2')

                with ui.row().classes('relative flex-grow h-full items-center'):
                    # Ready文本
                    ui.label().classes(TEXT_FONT + 'w-full h-full bg-transparent text-left relative z-10 flex items-center').bind_text_from(pre.ui_labels, i -1, backward= lambda t: f'{t}') #.tailwind.background_color('orange-200')
                    
                    # 进度条
                    progress = ui.linear_progress(show_value=False).style('height: 100%; background-color: #f0f0f0;').classes('absolute top-0 left-0 w-full').bind_value_from(pre.ui_process, i -1)

                    progress_bars.append(progress)

    # 运行 NiceGUI 应用
    ui.run()

    return progress_bars

class Ui_check:
    mode = None
    chip = None
    fw = None
    check = None
    burn_info = {'left': 100, 'total': 100}
    ui_labels = {x:'Ready' for x in range(CHANNELS)}
    ui_process = {x:0 for x in range(CHANNELS)}
    ui_process_list = []

    def __init__(self, mode, chip, fw, check, total, left):
        Ui_check.mode = mode
        Ui_check.chip = chip
        Ui_check.fw = fw
        Ui_check.check = check
        Ui_check.burn_info['total']=total
        Ui_check.burn_info['left']=left

        print(Ui_check.ui_labels)
        print(Ui_check.ui_process)

        Ui_check.ui_process_list = create_ui(self)
    
    # def __del__(self):

    def start(self, ch):
        Ui_check.ui_labels[ch] = ''
        Ui_check.ui_process[ch] = 0
        Ui_check.ui_process_list[ch].style('background-color: #f0f0f0;')
        Ui_check.ui_process_list[ch].update()

    def set_process(self, ch, process):
        Ui_check.ui_process[ch]= process

    def set_success(self, ch, text):
        Ui_check.ui_labels[ch] = f'successful {text}'
        Ui_check.ui_process[ch] = 0
        Ui_check.ui_process_list[ch].style('background-color: green')
        Ui_check.ui_process_list[ch].update()

    def set_failed(self, ch, text):
        Ui_check.ui_labels[ch] = f'failed {text}'
        Ui_check.ui_process[ch]= 0
        Ui_check.ui_process_list[ch].style('background-color: red')
        Ui_check.ui_process_list[ch].update()


# Test
print('aaaa')
check = Ui_check('烧写', 'CSK5060', 'fw.bin', '4A33-76449996', 300, 300)
print('bbbb')

for i in range(8):
    check.start(i)
check.set_process(2, 0.2)
check.set_process(3, 0.8)
check.set_success(4,'yes i can')
check.set_failed(5, '08 mic check error')

from nicegui import ui

# 初始化 B 和 C 的值
value_b = 1
value_c = 100

TEXT_FONT='text-5xl '

# 创建按钮，点击按钮时修改 B 和 C 的值，并更新第一行的标签文本
def change_values(value):
    global value_b, value_c
    value_b = value
    value_c = 100
    label_first_row.text = f'烧写信息: {value_b}/{value_c} 模式：烧写'

# 创建主容器，用于包含行布局和按钮
with ui.column().classes('w-full h-screen p-4').style('text-align: left; display: flex; flex-direction: column;'):

    # 创建第一行的标签，显示烧写信息和模式，并根据事件修改 B 和 C 的值
    label_first_row = ui.label(f'烧写信息: {value_b}/{value_c} 模式：烧写').classes(TEXT_FONT)

    # 创建第二行到第四行的文本
    label_second_row = ui.label('当前芯片： CSK5060').classes(TEXT_FONT)
    label_third_row = ui.label('文件名字： fw.bin 已授权').classes(TEXT_FONT)
    label_fourth_row = ui.label('校验码： 4A33-76449996').classes(TEXT_FONT)

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
# 运行 NiceGUI 应用
ui.run()




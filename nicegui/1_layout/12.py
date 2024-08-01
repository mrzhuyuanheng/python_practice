from nicegui import ui

# 初始化 B 和 C 的值
value_b = 1
value_c = 100



# 创建按钮，点击按钮时修改 B 和 C 的值，并更新第一行的标签文本
def change_values():
    global value_b, value_c
    value_b = 3
    value_c = 100
    label_first_row.text = f'烧写信息: {value_b}/{value_c} 模式：烧写'

# 创建主容器，用于包含行布局和按钮
with ui.column().classes('w-8/12 p-4').style('text-align: left;'):

    # 创建第一行的标签，显示烧写信息和模式，并根据事件修改 B 和 C 的值
    label_first_row = ui.label(f'烧写信息: {value_b}/{value_c} 模式：烧写').classes('text-lg mb-4')

    # 创建第二行到第五行的文本
    label_second_row = ui.label('当前芯片： CSK5060').classes('text-lg mb-4')
    label_third_row = ui.label('文件名字： fw.bin 已授权').classes('text-lg mb-4')
    label_fourth_row = ui.label('校验码： 4A33-76449996').classes('text-lg mb-4')


    # 创建八行布局，每行包含一个编号、一个居中显示的文本标签和一个长度较长的进度条
    for i in range(1, 9):
        with ui.row().classes('items-center mb-4 relative'):
            # 显示编号
            ui.label(f'{i}').classes('text-lg mr-4')
            # 创建包含文本标签和进度条的容器，使其在同一行内显示
            with ui.column().classes('relative flex-grow h-12'):
                # 文本标签
                ui.label('Ready').classes('w-full h-full bg-transparent text-center relative z-10 flex items-center justify-center')
                # 进度条叠加在文本标签上，并设置不显示值和调长长度
                progress = ui.linear_progress(value=0.5, show_value=False).style('width: 1000%;').classes('absolute top-0 left-0 h-full')

ui.button('Change Values').on('click', change_values)
# 运行 NiceGUI 应用
ui.run()

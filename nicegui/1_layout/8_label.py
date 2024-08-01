from nicegui import ui

# 创建一个容器，使其在不同屏幕尺寸下具有不同的宽度，并使其水平居中
with ui.column().classes('relative sm:w-full md:w-8/12 lg:w-6/12 mx-auto p-4'):
    for i in range(1, 9):
        with ui.row().classes('items-center mb-4'):
            # 显示编号
            ui.label(f'{i}').classes('text-lg mr-4')
            # 包含文本框和进度条的容器
            with ui.column().classes('relative w-full h-12'):
                progress = ui.linear_progress(value=0.5).classes('absolute w-full h-full')
                text_input = ui.input(value='Ready').classes('absolute w-full h-full bg-transparent text-center')

# 运行 NiceGUI 应用
ui.run()

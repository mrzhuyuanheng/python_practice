from nicegui import ui

# 创建一个容器，使其在不同屏幕尺寸下具有不同的宽度，并使其水平居中
with ui.column().classes('w-8/12 mx-auto p-4'):
    for i in range(1, 9):
        with ui.row().classes('items-center mb-4'):
            # 显示编号
            ui.label(f'{i}').classes('text-lg mr-4')
            # 文本框
            ui.input(value='Ready').classes('bg-transparent text-center')

# 运行 NiceGUI 应用
ui.run()

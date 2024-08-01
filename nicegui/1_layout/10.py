from nicegui import ui

# 创建一个容器，使其在不同屏幕尺寸下具有不同的宽度，并使其水平居中
with ui.column().classes('w-8/12 mx-auto p-4'):
    for i in range(1, 9):
        with ui.row().classes('items-center mb-4 relative'):
            # 显示编号
            ui.label(f'{i}').classes('text-lg mr-4')
            # 创建包含文本标签和进度条的容器，使其在同一行内显示
            with ui.column().classes('relative flex-grow h-12'):
                # 文本标签
                ui.label('Ready').classes('w-full h-full bg-transparent text-center relative z-10 flex items-center justify-center')
                # 进度条叠加在文本标签上，并设置不显示值和调长长度
                progress = ui.linear_progress(value=0, show_value=False).style('width: 1000%;').classes('absolute top-0 left-0 h-full')

# 运行 NiceGUI 应用
ui.run()

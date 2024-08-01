from nicegui import ui

# 定义文件上传处理函数
def handle_upload(files):
    for file in files:
        with open(f'uploaded_files/{file.name}', 'wb') as f:
            f.write(file.content.read())
    ui.notify('Files uploaded successfully!')

# 创建上传组件，并应用 Tailwind CSS 类
ui.upload(on_upload=handle_upload, multiple=True).classes('my-4 max-w-full')

# 创建一个带有 Tailwind CSS 类的按钮
ui.button('Submit', on_click=lambda: ui.notify('Button clicked')).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')

# 启动 NiceGUI 应用
ui.run()

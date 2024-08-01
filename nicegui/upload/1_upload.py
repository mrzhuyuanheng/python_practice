from nicegui import ui
import os
from nicegui.events import UploadEventArguments

def handle_upload(e: UploadEventArguments):
    try:
        file_name = e.name
        file_content = e.content.read()

        # 确保文件名是唯一的
        base_name, extension = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(os.path.join('uploads', file_name)):
            file_name = f"{base_name}_{counter}{extension}"
            counter += 1

        file_path = os.path.join('uploads', file_name)

        # 直接写入文件
        with open(file_path, 'wb') as f:
            f.write(file_content)

        ui.notify(f'文件 {file_name} 已成功上传.')
        update_file_list()
    except Exception as err:
        ui.notify(f'上传文件时发生错误: {str(err)}', color='negative')
        print("详细错误信息:", str(err))

# 创建上传文件的文件夹
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# 创建NiceGUI应用
ui.label('上传文件到设备').classes('text-2xl')
ui.upload(on_upload=handle_upload, multiple=True).classes('my-4 max-w-full')

# 添加已上传文件列表
file_list = ui.html()

def update_file_list():
    files = os.listdir('uploads')
    file_list.set_content('<br>'.join(files) if files else '没有上传的文件')

ui.button('刷新文件列表', on_click=update_file_list)

# 初始化文件列表
update_file_list()

# 启动NiceGUI应用
ui.run(host='0.0.0.0', port=8080, title='烧录器部署')

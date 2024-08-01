from nicegui import ui

config_dict = {}  # 配置字典的定义
handle_upload = lambda files: None  # 上传处理函数的定义
download_file = lambda: None  # 下载处理函数的定义

with ui.card().classes('w-full border-2 border-gray-300 rounded-xl p-4 flex flex-col'):
    ui.label('文件信息').classes('text-xl font-bold mb-4')
    
    with ui.row().classes('w-full flex-1 flex'):
        with ui.card().classes('flex-1 border-2 border-gray-300 rounded-xl p-4 m-2 flex flex-col'):
            ui.label('本地上传').classes('text-l font-bold')
            ui.upload(label='上传本地文件到设备', auto_upload=True, on_upload=handle_upload, multiple=True).classes('w-full mb-4')
            ui.label().classes('w-full p-2 bg-gray-100 rounded').bind_text_from(config_dict, 'fw', backward=lambda l: f'烧录文件名字： {l}')
            ui.input('请输入文件MD5校验值').bind_value_to(config_dict, 'fw_check').classes('w-full')

        with ui.card().classes('flex-1 border-2 border-gray-300 rounded-xl p-4 m-2 flex flex-col'):
            ui.label('云端拉取').classes('text-l font-bold')
            ui.input(label='请输入云端下载链接').classes('w-full mb-4')
            ui.button('下载', on_click=download_file).classes('w-full')

ui.run()

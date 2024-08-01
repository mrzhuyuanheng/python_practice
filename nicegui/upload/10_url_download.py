from nicegui import ui
import requests
import os

def download_file():
    url = input_url.value
    if not url:
        ui.notify('请输入下载链接')
        return
    
    try:
        response = requests.get(url)
        filename = os.path.basename(url)
        
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        ui.notify(f'文件 {filename} 下载成功!')
    except Exception as e:
        ui.notify(f'下载失败: {str(e)}')

input_url = ui.input(label='输入下载链接')
ui.button('下载', on_click=download_file)

ui.run()

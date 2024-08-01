#!/usr/bin/env python3

"""
具备功能：
- 登陆
- 退出
- 保存config文件到路径, 调用对话框来显示部署成功，
- 上传文件，并校验，
    如果校验不通过，则显示校验错误，并删除文件
    如果通过，则更新文件名，文件校验值，文件更新时间
"""

#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

import os
from nicegui.events import UploadEventArguments

import hashlib

# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}
unrestricted_page_routes = {'/login'}

# 定义配置选项
config_dict = {
    'flash_load': False,
    'flash_empty': False,
    'flash_check': False,
    'flash_opt': False,
    'current': False,
    'audio': False,
    'chip': None,
    'fw': 'fw.bin',
    'fw_check': '1234567',
    'total': 0,
    'left': 0,
    'last_update_time': None
}

# 文件保存路径
FW_SAVE_PATH = '~/fw_release/'

def calculate_md5_binary(binary_data):
    # 创建MD5对象
    md5 = hashlib.md5()
    # 更新MD5对象
    md5.update(binary_data)
    # 获取十六进制的哈希值
    return md5.hexdigest()

@app.post('/disconnect')
async def disconnect(request: Request):
    app.storage.user.clear()
    return {"status": "success"}

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)

app.add_middleware(AuthMiddleware)

@ui.page('/')
def main_page() -> None:
    def handle_upload(e: UploadEventArguments):
        try:
            file_name = e.name
            file_content = e.content.read()

            md5_sum = calculate_md5_binary(file_content)

            # 确保文件名是唯一的
            base_name, extension = os.path.splitext(file_name)
            print(f"base_name={base_name}, extension={extension}")
            counter = 1
            while os.path.exists(os.path.join(FW_SAVE_PATH, file_name)):
                file_name = f"{base_name}_{counter}{extension}"
                counter += 1

            file_path = os.path.join(FW_SAVE_PATH, file_name)

            # 直接写入文件
            with open(file_path, 'wb') as f:
                f.write(file_content)

            ui.notify(f'芯片烧录固件 {file_name} 已成功上传.')
            update_file_list()
        except Exception as err:
            ui.notify(f'上传文件时发生错误: {str(err)}', color='negative')
            print("详细错误信息:", str(err))

    def update_file_list():
        files = os.listdir(FW_SAVE_PATH)
        file_list.set_content('<br>'.join(files) if files else '没有上传的文件')

    def save_config_dict():
        config_name = f"{config_dict['fw']}_md5sum.txt"
        config_path = os.path.join(FW_SAVE_PATH, config_name)
        with open(config_path, 'w') as file:
            for key in config_dict:
                value = config_dict[key]
                file.write(f'{key}: {value}\n')
        ui.notify('配置文件已经部署.txt')

    # 创建主界面
    ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
    with ui.card().classes('w-full'):
        ui.label('烧写选项').classes('text-xl font-bold')
        with ui.row().classes('items-center justify-between w-full'):
            ui.checkbox('烧写', value=False).bind_value_to(config_dict, 'flash_load')
            ui.checkbox('查空', value=False).bind_value_to(config_dict, 'flash_empty')
            ui.checkbox('校验', value=False).bind_value_to(config_dict, 'flash_check')
            ui.checkbox('OPT', value=False).bind_value_to(config_dict, 'flash_opt')
            ui.checkbox('电流检测', value=False).bind_value_to(config_dict, 'current')
            ui.checkbox('音频检测', value=False).bind_value_to(config_dict, 'audio')

    with ui.card().classes('w-full'):
        ui.label('文件信息').classes('text-xl font-bold')

        with ui.row().classes('w-full'):

            ui.upload(label='上传文件到设备', auto_upload=False, on_upload=handle_upload, multiple=True).classes('text-2xl my-4 w-[300px] h-[200px]').props('color=primary')
            
            with ui.column().classes('items-center'):
                file_label = ui.label().classes(' p-2 bg-gray-100 rounded')
                md5_label = ui.label().classes('w-64 p-2 bg-gray-100 rounded')

                # file_label = ui.label().classes(' p-2 bg-gray-100 rounded').bind_text(config_dict, 'fw',backward= lambda l: f'烧录文件名字： {l}')
                # md5_label = ui.label().classes('w-64 p-2 bg-gray-100 rounded').bind_text(config_dict, 'fw_check',backward= lambda l: f'文件校验码： {l}')

                md5_input = ui.input('请输入文件MD5校验值').bind_value_to(config_dict, 'fw_check')

    # with ui.card().classes('w-full sm:w-1/2 md:w-1/3 lg:w-1/4'):
    #     # ui.upload(label='上传文件到设备', auto_upload=False, on_upload=handle_upload, multiple=True).classes('text-2xl my-4 w-full h-full')
    #     ui.upload(label='上传文件到设备', auto_upload=False, on_upload=handle_upload, multiple=True).classes('text-2xl my-4 w-[300px] h-[200px]').props('color=red')

    # 创建上传文件的文件夹
    if not os.path.exists(FW_SAVE_PATH):
        os.makedirs(FW_SAVE_PATH)

    # 添加已上传文件列表
    file_list = ui.html()
    ui.button('刷新文件列表', on_click=update_file_list)

    ui.button('部署配置', on_click=save_config_dict)
    
    # logout需要的东西
    ui.button('退出登陆', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout')#.props('outline round')
    

    # 初始化文件列表
    update_file_list()

    ui.run_javascript('''
    window.addEventListener('beforeunload', function (e) {
        fetch('/disconnect', {method: 'POST', keepalive: true});
    });
    ''')


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None


ui.run(storage_secret='listenai', title='烧录器部署')
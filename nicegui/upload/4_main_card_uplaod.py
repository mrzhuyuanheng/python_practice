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

# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}

unrestricted_page_routes = {'/login'}


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
    # with ui.column().classes('absolute-center items-center'):
    #     ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
    #     ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout') \
    #         .props('outline round')

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

    def update_file_list():
        files = os.listdir('uploads')
        file_list.set_content('<br>'.join(files) if files else '没有上传的文件')

    # 创建主界面
    with ui.card().classes('w-full'):
        ui.label('烧写选项').classes('text-xl font-bold')
        with ui.row().classes('items-center justify-between w-full'):
            ui.checkbox('烧写')
            ui.checkbox('查空')
            ui.checkbox('校验')
            ui.checkbox('OPT')
            ui.checkbox('电流检测')
            ui.checkbox('音频检测')

    with ui.card().classes('w-full mt-4'):
        ui.label('文件信息').classes('text-xl font-bold')
        with ui.row().classes('items-center justify-between w-full'):
            ui.label('文件：')
            file_label = ui.label().classes('flex-grow p-2 bg-gray-100 rounded')
            ui.label('校验码：')
            md5_label = ui.label().classes('w-64 p-2 bg-gray-100 rounded')
            # ui.button('打开', on_click=open_file)

    # 创建上传文件的文件夹
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # 创建NiceGUI应用
    ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
    ui.label('上传文件到设备').classes('text-2xl')
    # ui.upload(on_upload=handle_upload, multiple=True).classes('my-4')
    ui.upload(label='pick a video file', auto_upload=False, on_upload=handle_upload, multiple=True).classes('my-4')

    # 添加已上传文件列表
    file_list = ui.html()
    ui.button('刷新文件列表', on_click=update_file_list)

    # logout需要的东西
    ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout') \
        .props('outline round')

    # 初始化文件列表
    update_file_list()


@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')


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


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
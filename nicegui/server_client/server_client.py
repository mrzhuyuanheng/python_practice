from nicegui import ui, app

@ui.page('/')
async def main():
    print('before label')
    ui.label('欢迎访问我的 NiceGUI 应用！')
    ui.button('点击我', on_click=lambda: ui.notify('你点击了按钮！'))
    print('after button')

@app.on_startup
async def startup():
    print("应用已启动，等待客户端连接...")
    print(f"请通过浏览器访问 http://[你的IP地址]:8080")

# if __name__ == '__main__':
    # app.config.run_mode = 'server'
ui.run(host='0.0.0.0', port=8080, show=False)

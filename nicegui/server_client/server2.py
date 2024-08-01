from nicegui import ui

@ui.page('/')
def home():
    ui.label('欢迎访问我的 NiceGUI 应用！')
    ui.button('点击我', on_click=lambda: ui.notify('你点击了按钮！'))

ui.run(host='0.0.0.0', port=8080, show=False)

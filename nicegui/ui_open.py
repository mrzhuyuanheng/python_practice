from nicegui import ui

# 定义一个页面
@ui.page('/mypage')
def my_page():
    ui.label('这是我的页面')
    ui.button('关闭', on_click=lambda: ui.open('/'))

# 主页面
@ui.page('/')
def homepage():
    ui.label('欢迎来到主页')
    ui.button('打开我的页面', on_click=lambda: ui.open('/mypage'))
    flash_load = ui.checkbox('烧写')
    ui.button('禁用烧写配置', on_click=lambda: flash_load.disable())
    ui.button('使能烧写配置', on_click=lambda: flash_load.enable())

# 启动 NiceGUI
ui.run()

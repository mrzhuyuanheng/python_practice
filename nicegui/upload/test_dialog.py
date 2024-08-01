from nicegui import ui

def open_dialog():
    dialog.open()

with ui.dialog() as dialog:
    with ui.card():
        dialog_msg_label = ui.label('消息')
        dialog_fw_label = ui.label('固件信息')
        dialog_md5_input_label = ui.label('MD5 校验')
        dialog_fw_check_label = ui.label('校验结果')
        
        # 使用 Flexbox 布局将按钮放置在中间
        with ui.row().classes('justify-center w-full mt-4'):
            ui.button('确定', on_click=dialog.close)

ui.button('打开对话框', on_click=open_dialog)

ui.run()

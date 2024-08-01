from nicegui import ui

file_list = []

select = ui.select(file_list, value=file_list[0], label='Empty Select')

# 运行NiceGUI应用
ui.run()
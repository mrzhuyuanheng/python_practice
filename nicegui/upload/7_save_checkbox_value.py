from nicegui import ui

# 定义复选框选项
checkbox_values = {
    'option1': False,
    'option2': False,
    'option3': False
}

# 创建复选框
checkbox_elements = {}
with ui.column():
    for key in checkbox_values:
        checkbox_elements[key] = ui.checkbox(key, value=checkbox_values[key])

# 定义保存函数
def save_values_to_file():
    with open('checkbox_values.txt', 'w') as file:
        for key in checkbox_elements:
            value = checkbox_elements[key].value
            file.write(f'{key}: {value}\n')
    ui.notify('Values saved to checkbox_values.txt')

# 创建按钮并绑定保存函数
ui.button('Save', on_click=save_values_to_file)

# 启动应用
ui.run()

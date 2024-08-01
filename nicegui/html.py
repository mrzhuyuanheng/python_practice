from nicegui import ui

# 假设你的字典a如下：
a = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3',
}

# 创建一个HTML组件并将字典a里面所有的key和value显示出来
html = ui.html()
for key, value in a.items():
    html.set_content(f'<p>{key}: {value}</p>')

# 运行NiceGUI应用
ui.run()

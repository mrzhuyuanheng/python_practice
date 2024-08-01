from nicegui import ui

# 创建一个带有行内样式的标签
ui.label('Hello, NiceGUI!').style('color: red; font-size: 24px;')

# 创建一个带有自定义属性的输入框
ui.input('Your name').props('placeholder=yhzhu').classes('border border-gray-300 rounded-lg p-2')

# 启动 NiceGUI 应用
ui.run()

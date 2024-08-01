from nicegui import ui

@ui.page('/')
def main_page() -> None:
    # 单一样式设置
    ui.button('Red Button').style('color: red')

    # 多个样式设置（字符串方式）
    ui.label('Styled Label').style('color: blue; font-size: 20px; font-weight: bold')

    # 多个样式设置（字典方式）
    # ui.card().style(
    #     width='200px',
    #     height='100px',
    #     background_color='#f0f0f0',
    #     border='1px solid black'
    # ).add(ui.label('Card Content'))

    # 使用 Python 变量动态设置样式
    color = 'green'
    size = '18px'
    ui.button('Dynamic Style').style(f'color: {color}; font-size: {size}')

    # 设置布局相关样式
    with ui.row().style('gap: 10px; justify-content: space-between'):
        ui.button('Button 1')
        ui.button('Button 2')
        ui.button('Button 3')

    # 设置动画和过渡效果
    ui.button('Hover Me').style('transition: all 0.3s; &:hover { transform: scale(1.1) }')

    # 响应式样式
    ui.div('Responsive Div').style('''
        width: 100%;
        background-color: #ddd;
        padding: 10px;
        text-align: center;
        @media (min-width: 600px) { width: 50%; background-color: #bbb; }
        @media (min-width: 1200px) { width: 33%; background-color: #999; }
    ''')

ui.run()

from nicegui import ui

@ui.page('/')
def main_page() -> None:
    ui.label('NiceGUI .props() Showcase').classes('text-h3 text-weight-bold')

    # 1. 表单输入控制
    with ui.card().classes('w-full'):
        ui.label('Form Input Control').classes('text-h5')
        name_input = ui.input().props('label="Name" clearable')
        email_input = ui.input().props('label="Email" type="email" :rules="[val => /.+@.+\..+/.test(val) || \'Please enter a valid email\']"')
        password_input = ui.input().props('label="Password" type="password" :rules="[val => val.length >= 8 || \'Password must be at least 8 characters\']"')
        ui.button('Submit').props('color=primary')

    ui.separator()

    # 2. 动态切换组件状态
    with ui.card().classes('w-full'):
        ui.label('Dynamic Component State').classes('text-h5')
        toggle_button = ui.button('Toggle Disable', color='primary')
        target_button = ui.button('Target Button')

        def toggle_disable():
            if hasattr(target_button, '_disabled'):
                delattr(target_button, '_disabled')
                target_button.props.pop('disabled', None)
                toggle_button.props('color=primary')
            else:
                setattr(target_button, '_disabled', True)
                target_button.props('disabled')
                toggle_button.props('color=warning')

        toggle_button.on('click', toggle_disable)

    ui.separator()

    # 3. 自定义选择器
    with ui.card().classes('w-full'):
        ui.label('Custom Selector').classes('text-h5')
        options = ['Option 1', 'Option 2', 'Option 3']
        ui.select(options).props('filled label="Custom Select" color="teal" style="width: 200px"')

    ui.separator()

    # 4. 高级表格配置
    with ui.card().classes('w-full'):
        ui.label('Advanced Table Configuration').classes('text-h5')
        data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True}
        ]

        ui.table(columns=columns, rows=data, row_key='name').props('pagination filter rows-per-page-options=[10]')


    ui.separator()

    # 5. 自定义对话框
    with ui.card().classes('w-full'):
        ui.label('Custom Dialog').classes('text-h5')
        def show_dialog():
            with ui.dialog().props('persistent') as dialog:
                ui.label('This is a custom dialog')
                ui.button('Close', on_click=dialog.close).props('color=negative')

        ui.button('Open Dialog', on_click=show_dialog)

    ui.separator()

    # 6. 日期选择器配置
    with ui.card().classes('w-full'):
        ui.label('Date Picker Configuration').classes('text-h5')
        ui.date().props('''
            landscape
            today-btn
            range
            color="green"
            :options="date => date >= '2023-01-01' && date <= '2023-12-31'"
        ''')

    ui.separator()

    # 7. 文件上传组件
    with ui.card().classes('w-full'):
        ui.label('File Upload Component').classes('text-h5')
        ui.upload(auto_upload=True).props('''
            accept=".pdf,.doc,.docx"
            label="Upload Document"
            max-file-size="5242880"
            max-files="3"
        ''')

    ui.separator()

    # 8. 自定义进度条
    with ui.card().classes('w-full'):
        ui.label('Custom Progress Bar').classes('text-h5')
        ui.linear_progress(value=0.7).props('rounded stripe color="orange" size="10px"')

    ui.separator()

    # 9. 响应式图像
    with ui.card().classes('w-full'):
        ui.label('Responsive Image').classes('text-h5')
        ui.image('https://picsum.photos/id/1/200/300').props('fit=cover transition-opacity duration-300 blur-transition')

    ui.separator()

    # 10. 高级列表
    with ui.card().classes('w-full'):
        ui.label('Advanced List').classes('text-h5')
        with ui.list().classes('bordered separator'):
            ui.icon('star')
            ui.label('Item 1').classes('clickable')
            ui.icon('favorite')
            ui.label('Item 2').classes('clickable')
            ui.icon('thumb_up')
            ui.label('Item 3').classes('clickable')


""""""
ui.run()

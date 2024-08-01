from nicegui import ui

@ui.page('/')
def main():
    ui.label('Custom Upload Component').classes('text-h5 q-mb-md')
    
    upload = ui.upload(multiple=True, auto_upload=False).props('max-files=5').classes('max-w-full')

    header_label = ui.label()
    header_spinner = ui.spinner(size='sm')
    header_spinner.set_visibility(False)

    def update_header():
        files = upload.value or []
        header_label.set_text(f'Files: {len(files)}')
        header_spinner.set_visibility(upload.props.get('uploading', False))

    def custom_header():
        ui.button('Pick Files', on_click=lambda: upload.run_method('pickFiles')).classes('q-mr-sm')
        ui.button('Upload', on_click=lambda: upload.run_method('upload')).classes('q-mr-sm')
        with ui.row().classes('items-center'):
            header_label
            header_spinner

    file_list = ui.element('div')

    def update_file_list():
        file_list.clear()
        files = upload.value or []
        for file in files:
            with file_list, ui.row().classes('items-center'):
                ui.icon('insert_drive_file')
                ui.label(file['name'])
                ui.button(icon='close', on_click=lambda f=file: upload.run_method('removeFile', f))

    upload.add_slot('header', custom_header)
    upload.add_slot('list', file_list)

    def handle_added():
        update_header()
        update_file_list()

    def handle_removed():
        update_header()
        update_file_list()

    def handle_upload_status():
        update_header()

    def handle_uploaded(e):
        ui.notify(f'Uploaded {len(e.files)} files successfully!')

    def handle_failed(e):
        ui.notify(f'Upload failed: {e.error}', color='negative')

    upload.on('added', handle_added)
    upload.on('removed', handle_removed)
    upload.on('start', handle_upload_status)
    upload.on('finish', handle_upload_status)
    upload.on('uploaded', handle_uploaded)
    upload.on('failed', handle_failed)

    # Initial update
    update_header()
    update_file_list()

ui.run()

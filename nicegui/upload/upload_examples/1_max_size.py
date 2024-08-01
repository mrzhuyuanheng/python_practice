from nicegui import ui

ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
          on_rejected=lambda: ui.notify('Rejected!'),
          max_file_size=1_000_000).classes('max-w-full')

ui.run()
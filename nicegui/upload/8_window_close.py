from nicegui import ui, app
from fastapi import Request

def on_client_disconnect():
    print("Client disconnected")

@ui.page('/')
def main():
    ui.label('Hello, NiceGUI!')
    ui.run_javascript('''
    window.addEventListener('beforeunload', function (e) {
        fetch('/disconnect', {method: 'POST', keepalive: true});
    });
    ''')

@app.post('/disconnect')
async def disconnect(request: Request):
    on_client_disconnect()
    return {"status": "success"}

ui.run()

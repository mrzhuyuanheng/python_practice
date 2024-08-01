from nicegui import app,ui
import asyncio

# Simulate Ui Class
class Demo:
    def __init__(self):
        self.number = 1
    
    def show_ui(self):
        v = ui.checkbox('visible', value=True)
        with ui.column().bind_visibility_from(v, 'value'):
            ui.slider(min=1, max=100).bind_value(self, 'number')
            ui.number().bind_value(self, 'number')


# Simulate UartBurn Class
class HeavyTask():
    def __init__(self):
        self.port = 0

    def mock_progress_changed(self, progress):
        self.cbProgress(progress)

    async def listen(self, cbProgress):
        self.cbProgress = cbProgress
        print(f"listening on port")


# Main Logical

def on_progress(progress, demo: Demo):
    print(f"on_progress, {progress}")
    demo.number = progress


async def simulate_burner():
    for i in range(0,51):
        await asyncio.sleep(0.2)
        heavyTask.mock_progress_changed(i)

async def init_burner() -> None:
    await heavyTask.listen(lambda progress: on_progress(progress, demo))
    asyncio.create_task(simulate_burner())


@ui.page('/')
def app_main_page():
    demo.show_ui()


demo = Demo()
heavyTask = HeavyTask()
app.on_startup(init_burner)


ui.run()

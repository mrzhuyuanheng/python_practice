from nicegui import ui
import asyncio

custom_style = """
<style>
.custom-progress .q-linear-progress__model {
    transition: width 0s linear !important;
}


</style>
"""

ui.add_head_html(custom_style)

progress = ui.linear_progress(value=0).classes("custom-progress")
progress2 = ui.linear_progress(value=0)

# 更新进度条的函数
def update_progress(value):
    progress.value = value
    progress2.value = value


# 模拟更新进度条的过程
async def simulate_progress():
    # progress.classes(remove='custom-progress-immediately')
    for i in range(101):
        update_progress(i / 100)
        await asyncio.sleep(0.01)

    if progress.value == 1:
        # progress.classes('custom-progress-immediately')
        progress.value = 0
        progress2.value = 0
    

# 启动模拟进度条更新
ui.button('Start Progress', on_click=simulate_progress)

ui.run()

from nicegui import ui
import asyncio

custom_style = """
<style>
.custom-progress .q-linear-progress__model {
    transition: width 0s linear;
}
</style>
"""

# 创建一个线性进度条
ui.add_head_html(custom_style)

progress = ui.linear_progress().classes('custom-progress')
# progress = ui.linear_progress().props()


# 更新进度条的函数
def update_progress(value):
    progress.value = value

# 模拟更新进度条的过程
async def simulate_progress():
    for i in range(101):
        update_progress(i / 100)
        await asyncio.sleep(0.06)

    update_progress(0)
    await asyncio.sleep(0.1)

# 启动模拟进度条更新
ui.button('Start Progress', on_click=simulate_progress)

ui.run()

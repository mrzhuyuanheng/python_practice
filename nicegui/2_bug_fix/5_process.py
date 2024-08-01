from nicegui import ui
import asyncio

progress = ui.linear_progress(value=0)
progress2 = ui.linear_progress(value=0)

# 更新进度条的函数
def update_progress(value):
    progress.value = value
    progress2.value = value


# 模拟更新进度条的过程
async def simulate_progress():
    progress.props('animation-speed="200" ')

    for i in range(101):
        update_progress(i / 100)
        await asyncio.sleep(0.06)

    progress.props('color=green')
    await asyncio.sleep(1)
    progress.props('animation-speed="0" color=primary')

    if progress.value == 1:
        progress.value = 0
        progress2.value = 0

        
    

# 启动模拟进度条更新
ui.button('Start Progress', on_click=simulate_progress)

ui.run()
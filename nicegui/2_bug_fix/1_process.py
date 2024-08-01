from nicegui import ui
import asyncio

ui.add_head_html('''
<style>
.q-linear-progress--indeterminate .q-linear-progress__track {
  animation: none !important;
}
.q-linear-progress__model {
  transition: width 5s linear !important;
}
</style>
''')

# ui.add_head_html('''
# <style>
# .q-linear-progress--indeterminate .q-linear-progress__track {
#   animation-duration: 3s !important;
# }
# .q-linear-progress__model {
#   transition: transform 3s linear !important;
# }
# </style>
# ''')

# 创建一个线性进度条
progress = ui.linear_progress().props('indeterminate=False')
# progress = ui.linear_progress().props()


# 更新进度条的函数
def update_progress(value):
    progress.value = value

# 模拟更新进度条的过程
async def simulate_progress():
    for i in range(101):
        update_progress(i / 100)
        await asyncio.sleep(0.1)

    update_progress(0)
    await asyncio.sleep(0.1)

# 启动模拟进度条更新
ui.button('Start Progress', on_click=simulate_progress)

ui.run()

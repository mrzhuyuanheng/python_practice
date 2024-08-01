from nicegui import ui
import hashlib

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def open_file():
    file_path = ui.open_file()
    if file_path:
        file_input.set_value(file_path)
        checksum = calculate_checksum(file_path)
        checksum_display.set_value(checksum)

# 创建烧写选项卡片
with ui.card():
    ui.label('烧写选项')
    with ui.row():
        ui.checkbox('烧写')
        ui.checkbox('查空')
        ui.checkbox('校验')
        ui.checkbox('OPT')
        ui.checkbox('电流检测')
        ui.checkbox('音频检测')

# 创建文件信息卡片
with ui.card():
    ui.label('文件信息')
    with ui.row():
        ui.label('文件：')
        file_input = ui.input().props('filled').style('width: 300px')
        ui.label('校验码：')
        checksum_display = ui.input().props('readonly filled').style('width: 300px')
        ui.button('打开').on('click', open_file)

# 运行NiceGUI应用
ui.run()

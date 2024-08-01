import sounddevice as sd
import re
import asyncio
import numpy as np
import scipy.io.wavfile as wav

from scipy.fft import rfft, rfftfreq

from nicegui import run, ui

from multiprocessing import Manager, Queue

CHANNELS = 1  # 通道数
RATE = 16000  # 采样率
DURATION = 3  # 录音时长(秒)

# 生成 1kHz 正弦波
sine_wave = [np.sin(2 * np.pi * 1000 * x / RATE) * 32768 for x in range(0, DURATION * RATE)]

def analyze_audio(frames):
    f = open('record.pcm', 'wb+')
    f.write(frames)
    f.close()

    """分析录制的音频频谱"""
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    fft_data = rfft(audio_data)
    print(f'record audio len: {len(audio_data)}')
    frequencies = rfftfreq(len(audio_data), 1 / RATE)

    # 找到最大幅值对应的频率
    max_freq_idx = np.argmax(np.abs(fft_data))
    print(f'max_freq_idx: {max_freq_idx}')
    freq = frequencies[max_freq_idx]
    print(f'freq: {freq}')

    if abs(freq - 1000) < 10:
        print('PASS')
        result = "PASS"
    else:
        print('FAILED')
        result = f"FAILED, frequency: {freq:.2f} Hz"

    print(f'result:{result}')
    return result

def play_and_record():
    myrecording = sd.playrec(sine_wave, RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    sd.stop()   

    print('play and record done')

    return myrecording

async def burn_firmware(port, file, baudrate, q: Queue):
    command = f"cskburn -s {port} -C 6 0x0 {file} -b {baudrate}"
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    buffer = ""

    while True:
        line = await process.stdout.read(10)
        if not line:
            break
        line = line.decode('utf-8')

        # Append the chunk to the buffer
        buffer += line

        # # Handle lines with carriage return '\r'
        while re.search(r'\r', buffer):
            line, buffer = re.split(r'\r', buffer, 1)
            if line.strip():
                last_output = line.strip()
                # print(f"[{port}] {last_output}")

            # # Check for progress information
            match = re.search(r'(\d+(\.\d+)?) KB / \d+(\.\d+)? KB \((\d+(\.\d+)?)%\)', last_output)
            if match:
                pro = match.group(4)
                a = int(float(pro)) / 100
                print(f"[{port}] Progress: {pro} {a}")
                q.put_nowait(a)

        # Process each line in the buffer
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            if line.strip():
                line = line.strip()
                print(f"[{port}] {line}")

    stdout, stderr = await process.communicate()

    if stdout:
        print(f'[{port}] stdout: {stdout.decode()}')
    if stderr:
        print(f'[{port}] stderr: {stderr.decode()}')

    return process.returncode

@ui.page('/')
def main_page():
    async def test_audio():
        record_buffer = await run.io_bound(play_and_record)

        result = await run.cpu_bound(analyze_audio, record_buffer)

        # ui.notify(f'analyze result: {result}')
        # print('notify')

        if(result == 'PASS'):
            button.style('background-color:green!important')
        else:
            button.style('background-color:red!important')
        print('set color done')           
        button.set_text(result)
        
        print('set text done')

    async def test_burn():
        ports = ['/dev/ttyACM0']
        file = 'zephyr.bin'
        baudrate = 1500000

        progressbar.visible = True

        # 创建烧录任务列表
        burn_tasks = [burn_firmware(port, file, baudrate, queue) for port in ports]

        # 并发执行烧录任务
        results = await asyncio.gather(*burn_tasks)

        # 打印烧录结果
        for port, result in zip(ports, results):
            print(f'Port {port} finished with return code {result}')

        progressbar.visible = False
        progressbar.set_value(0)


    button = ui.button("Audio Test", on_click=test_audio)
    burn_button = ui.button('burn Test', on_click=test_burn)

    queue = Manager().Queue()
    ui.timer(0.1, callback=lambda: progressbar.set_value(queue.get() if not queue.empty() else progressbar.value))
    progressbar = ui.linear_progress(value=0).props('instant-feedback')
    progressbar.visible = False

ui.run()

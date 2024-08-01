import sounddevice as sd
import struct
import numpy as np
import scipy.io.wavfile as wav

from scipy.fft import rfft, rfftfreq

from nicegui import ui

CHANNELS = 1  # 通道数
RATE = 16000  # 采样率
DURATION = 5  # 录音时长(秒)

# 生成 1kHz 正弦波
sine_wave = [np.sin(2 * np.pi * 1000 * x / RATE) * 32768 for x in range(0, DURATION * RATE)]

# data = struct.pack('h' * len(sine_wave), *[int(x * 32767) for x in sine_wave])

async def analyze_audio(frames):
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

# ui.button("Test", on_click=test_audio)

# state = {
#     'check': 'NONE',
# }
check='NONE'

@ui.page('/')
def main_page():
    async def test_audio():
        """测试音频"""
        # 播放音频，同时录音
        myrecording = sd.playrec(sine_wave, RATE, channels=CHANNELS, dtype='int16')
        sd.wait()
        sd.stop()
        print('aaaaaaaaaaaaaaaaaa')
        f = open('record.pcm', 'wb+')
        f.write(myrecording)
        f.close()
        print('bbbbbbbbbbbbbbbbbb')
        result = await analyze_audio(myrecording)
        print('cccccccccccccccccc')
        ui.notify(result)
        # label.set_text(f'check: {result}')
        # state.update(check=result)
        check=result
        print(f'check:{check}')
        # label = ui.label()
        # label.set_text(f'check: {result}')
        print('dddddddddddddddddd')

    # ui.timer(0.1, callback=lambda: label.set_text(f'check: {check}'))

    # ui.label().bind_text_from(state, 'check', backward=lambda a: f'CHECK: {a}')
    # label = ui.label()
    ui.button("Test", on_click=test_audio)

# 运行 NiceGUI 应用程序
ui.run()

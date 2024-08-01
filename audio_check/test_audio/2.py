import asyncio
import numpy as np
import pyaudio
import struct
from scipy.fft import rfft, rfftfreq

from nicegui import ui

# 设置音频参数
CHUNK = 1024  # 每次读取的音频数据块大小
FORMAT = pyaudio.paInt16  # 音频数据格式
CHANNELS = 1  # 通道数
RATE = 16000  # 采样率
RECORD_SECONDS = 10  # 录音时长(秒)

# 初始化 PyAudio 对象
print('before init')
p = pyaudio.PyAudio()
print('init')

# 创建音频流
print('before open play')
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                frames_per_buffer=CHUNK)
print('open play')

# 生成 1kHz 正弦波
sine_wave = [np.sin(2 * np.pi * 1000 * x / RATE) for x in range(0, RECORD_SECONDS * RATE)]

frames = []

def play_sine_wave(in_data, frame_count, time_info, status):
    """播放 1kHz 正弦波回调函数"""
    data = struct.pack('h' * len(sine_wave), *[int(x * 32767) for x in sine_wave])
    stream.write(data)
    return (None, pyaudio.paContinue)

def record_audio(in_data, frame_count, time_info, status):
    """录制音频回调函数"""
    frames.append(in_data)
    if len(frames) >= int(RATE / CHUNK * RECORD_SECONDS):
        return (None, pyaudio.paComplete)
    return (None, pyaudio.paContinue)

async def analyze_audio():
    """分析录制的音频频谱"""
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    fft_data = rfft(audio_data)
    frequencies = rfftfreq(len(audio_data), 1 / RATE)

    # 找到最大幅值对应的频率
    max_freq_idx = np.argmax(np.abs(fft_data))
    freq = frequencies[max_freq_idx]

    if abs(freq - 1000) < 10:
        result = "PASS"
    else:
        result = f"FAILED, frequency: {freq:.2f} Hz"

    ui.notify(result)

async def test_audio():
    """测试音频"""
    global frames
    frames = []
    stream.start_stream()
    loop = asyncio.get_event_loop()
    loop.call_soon(stream.write, struct.pack('h' * len(sine_wave), *[int(x * 32767) for x in sine_wave]))
    stream.add_callback(play_sine_wave, pyaudio.paContinue)
    stream.add_callback(record_audio, pyaudio.paContinue)
    await asyncio.sleep(RECORD_SECONDS + 1)
    stream.stop_stream()
    await analyze_audio()

# 创建 UI
with ui.row():
    ui.button("Test", on_click=test_audio)

# 运行 NiceGUI 应用程序
ui.run()

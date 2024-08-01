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
                frames_per_buffer=CHUNK)
print('open play')

# 生成 1kHz 正弦波
sine_wave = [np.sin(2 * np.pi * 1000 * x / RATE) for x in range(0, RECORD_SECONDS * RATE)]

async def play_sine_wave():
    """播放 1kHz 正弦波"""
    data = struct.pack('h' * len(sine_wave), *[int(x * 32767) for x in sine_wave])
    print('playing')
    stream.write(data)
    print('play done')

async def record_audio():
    """录制音频"""
    frames = []
    record_stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK)

    print("Recording...")
    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = record_stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")
    record_stream.stop_stream()
    record_stream.close()

    return frames

async def analyze_audio(frames):
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

    return result

async def test_audio():
    """测试音频"""
    await play_sine_wave()
    frames = await record_audio()
    result = await analyze_audio(frames)
    ui.notify(result)

# 创建 UI
with ui.row():
    ui.button("Test", on_click=test_audio)

# 运行 NiceGUI 应用程序
ui.run()

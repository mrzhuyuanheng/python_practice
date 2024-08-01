import sounddevice as sd
import struct
import numpy as np
import scipy.io.wavfile as wav

from scipy.fft import rfft, rfftfreq

from nicegui import run, ui

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


    button = ui.button("Audio Test", on_click=test_audio)

ui.run()

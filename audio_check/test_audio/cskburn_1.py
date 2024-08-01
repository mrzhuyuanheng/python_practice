import asyncio
import re

async def burn_firmware(port, file, baudrate):
    command = f"cskburn.exe -s {port} -C 6 0x0 {file} -b {baudrate}"
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
            match = re.search(r'(\d+(\.\d+)?) KB / \d+(\.\d+)? KB \((\d+(\.\d+)?%)\)', last_output)
            if match:
                progress = match.group(4)
                print(f"[{port}] Progress: {progress}")

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

async def main():
    ports = ['COM6', 'COM14']
    file = 'zephyr.bin'
    baudrate = 1500000

    # 创建烧录任务列表
    burn_tasks = [burn_firmware(port, file, baudrate) for port in ports]

    # 并发执行烧录任务
    results = await asyncio.gather(*burn_tasks)

    # 打印烧录结果
    for port, result in zip(ports, results):
        print(f'Port {port} finished with return code {result}')

# 运行主函数
asyncio.run(main())


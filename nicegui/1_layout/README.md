## UI的需求
- 开机UI
    - 聆思logo
    - 客户编号
    - 设备编号
    - 烧录器固件版本
- 烧录UI
    - 显示烧录模式
    - 显示芯片型号
    - 显示当前部署固件
    - 显固件校验值
    - 8个通道的烧录状况
    - 8个通道烧录进度条
    - 8个通道的各自烧录次数
    - 8个通道的异常值

## 烧录UI的技术需求
- 上电读取默认配置文件，并显示（烧录模式、芯片型号、当前部署固件、固件校验值； 可用烧录次数，剩余次数）
- 依次显示8个通道：默认显示READY，进度条进度默认为0, 进度条颜色为灰色
- 根据各个通道烧录进度反馈，实时显示进度条，进度条为蓝色
- 如果通道烧录成功，显示'success, total time: %d ms'，并设置进度条颜色为绿色
- 如果通道烧录失败，显示失败原因，并设置颜色为红色
- 收到start信号：然后UI恢复相应通道的进度条默认值为READY，默认颜色为灰色
- 根据各个通道烧录结果，实时显示：烧录成功次数/总烧录次数

- 显示UI的关键日志

## UI的接口
```c
/*
 * ui上电显示信息
 * mode: 烧录模式
 * chip: 芯片名字
 * fw: 烧录固件名字
 * check: 烧录固件校验信息
 * total: 可用次数
 * left: 剩余可用次数
*/ 
ui(mode, chip, fw, check, total, left);

/*
 * 启动ch的烧录或者检测
 * ch: 通道号[0,7]
*/ 
start(ch);

/*
 * 设置ch的烧录进度
 * ch: 通道号[0,7]
 * process: 进度值[0, 100]
*/ 
set_process(ch, process);

/*
 * 设置ch的状态为success
 * ch: 通道号[0,7]
 * successful_text: 具体的成功信息
*/ 
set_success(ch, successful_text);

/*
 * 设置ch的状态为failed
 * ch: 通道号[0,7]
 * failed_text: 具体的失败信息
*/ 
set_fail(ch, failed_text);

```

## UI的接口
```python

from nicegui import ui

CHANNELS = 8 # 通道数

class Ui_check:
    mode = None
    chip = None
    fw = None
    check = None
    total = None
    left = None


    def __init__(self, mode, chip, fw, check, total, left):
    
    def __del__(self):

    def start(self, ch):

    def set_process(self, ch, process):

    def set_success(self, ch):

    def set_failed(self, ch):

```

## UI的接口实现
```python

from nicegui import ui

CHANNELS = 8 # 通道数

class Ui_check:
    mode = None
    chip = None
    fw = None
    check = None
    total = None
    left = None


    def __init__(self, mode, chip, fw, check, total, left):
        Ui_check.mode = mode
        Ui_check.chip = chip
        Ui_check.check = check
        Ui_check.total = total
        Ui_check.left = left
    
    def __del__(self):

    def start(self, ch):

    def set_process(self, ch, process):

    def set_success(self, ch, text):

    def set_failed(self, ch, text):

```
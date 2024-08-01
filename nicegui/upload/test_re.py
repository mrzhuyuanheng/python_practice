import re

def validate_input(value):
    # 定义正则表达式，匹配 0 或者正整数
    pattern = r'^(0|[1-9]\d*)$'
    # 使用 re.match() 函数匹配输入值和正则表达式
    if re.match(pattern, value):
        return True
    else:
        return False

# 测试输入值
inputs = ['0', '1', '123', '-1', 'abc', '3.14']

for inp in inputs:
    if validate_input(inp):
        print(f'"{inp}" 是 0 或正整数')
    else:
        print(f'"{inp}" 不是 0 或正整数')

# https://www.jianshu.com/p/b5e347b3a17c

import asyncio
import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

start = now()

task = asyncio.create_task(do_some_work(5))

print('Task ret: ', task.result())
print('TIME: ', now() - start)  
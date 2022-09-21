import asyncio

async def do_ping(ip):
    proc = await asyncio.create_subprocess_shell(f'ping -c 1 -w 1 {ip} > /dev/null')
    await proc.communicate()
    if proc.returncode == 0:
        return ip

    return ''


async def main():
    tasks = []
    for i in range(1, 255):
        tasks.append(do_ping(f'192.168.4.{i}'))
    
    ret = await asyncio.gather(*tasks)
    ret = [i for i in ret if i]
    print(', '.join(ret))

import time
t1 = time.time()
asyncio.run(main())

print(time.time()-t1)

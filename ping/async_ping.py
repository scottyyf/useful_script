#!/usr/bin/env python
# coding=utf-8

import asyncio
import aioping

async def do_ping(ip: str, timeout=2) -> str:
    try:
        ret = await aioping.ping(ip, timeout=timeout)
    except TimeoutError:
        return ''
    else:
        return ip


async def main(ip_list: list) -> list:
    tasks = []
    for ip in ip_list:
        tasks.append(do_ping(ip))

    ret = await asyncio.gather(*tasks)
    return [ip for ip in ret if ip] 

if __name__ == '__main__':
    import time
    t1 = time.time()
    ret = asyncio.run(main([f'192.168.4.{i}' for i in range(1, 255)]))
    print(', '.join(ret))
    print('TOTAL TIME: ', time.time()-t1)

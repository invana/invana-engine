import aiohttp
import asyncio

async def async_processing():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://192.168.0.10:8182/gremlin') as ws:
            message =  b'!application/vnd.gremlin-v3.0+json{"requestId": {"@type": "g:UUID", "@value": "16f19ea9-3d61-45b5-b823-7f67199ff1b2"}, "processor": "traversal", "op": "bytecode", "args": {"gremlin": {"@type": "g:Bytecode", "@value": {"step": [["V", "98528"], ["valueMap", true]]}}, "aliases": {"g": "g"}}}'

            await ws.send_bytes(message)
            async for msg in ws:
                print("response", msg)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        await ws.send_str(msg.data + '/answer')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        #
    # async with session.get('http://httpbin.org/get') as resp:
    #     print(resp.status)
    #     print(await resp.text())
asyncio.get_event_loop().run_until_complete(asyncio.wait([
   async_processing()
]))

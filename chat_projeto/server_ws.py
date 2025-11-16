#!/usr/bin/env python3
import asyncio
import json
import websockets
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))  # Render define a PORT automaticamente

connected = {}  # websocket -> nick


async def handler(ws):
    try:
        raw = await ws.recv()
        obj = json.loads(raw)

        if obj.get("type") != "join" or not obj.get("nick"):
            await ws.send(json.dumps({
                "type": "system",
                "text": "Envie primeiro: {\"type\":\"join\",\"nick\":\"seu_nome\"}"
            }))
            return

        nick = obj["nick"][:32]
        connected[ws] = nick

        await broadcast({
            "type": "system",
            "text": f"** {nick} entrou **"
        })

        async for msg in ws:
            try:
                data = json.loads(msg)
            except:
                continue

            if data.get("type") == "msg":
                texto = f"[{nick}]: {data['msg']}"
                await broadcast({"type": "broadcast", "text": texto})
            else:
                await ws.send(json.dumps({
                    "type": "system",
                    "text": "Comando inválido"
                }))

    except:
        pass

    finally:
        if ws in connected:
            name = connected.pop(ws)
            await broadcast({
                "type": "system",
                "text": f"** {name} saiu **"
            })


async def broadcast(obj):
    if not connected:
        return
    message = json.dumps(obj, ensure_ascii=False)
    await asyncio.gather(*(safe_send(w, message) for w in list(connected)))


async def safe_send(ws, message):
    try:
        await ws.send(message)
    except:
        pass


async def main():
    print(f"Servidor WebSocket rodando em ws://0.0.0.0:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())

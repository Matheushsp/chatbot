#!/usr/bin/env python3
import asyncio
import json
import websockets

HOST = "0.0.0.0"
PORT = 6789

connected = {}  # websocket -> nick


async def handler(ws):
    try:
        # Primeiro pacote: JOIN
        raw = await ws.recv()
        obj = json.loads(raw)

        if obj.get("type") != "join" or not obj.get("nick"):
            await ws.send(json.dumps({
                "type": "system",
                "text": "Envie primeiro: {\"type\":\"join\",\"nick\":\"seu_nome\"}"
            }))
            return

        nick = obj["nick"][:32]  # limitar tamanho do nick
        connected[ws] = nick

        # Avisar entrada
        await broadcast({
            "type": "system",
            "text": f"** {nick} entrou **"
        })

        # Loop principal de mensagens
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

    except websockets.ConnectionClosed:
        pass

    finally:
        # Se o cliente estava conectado, remover
        if ws in connected:
            name = connected.pop(ws)
            await broadcast({
                "type": "system",
                "text": f"** {name} saiu **"
            })


async def broadcast(obj):
    """Envia mensagem para todos os clientes conectados."""
    if not connected:
        return

    message = json.dumps(obj, ensure_ascii=False)
    await asyncio.gather(*(safe_send(w, message) for w in list(connected)))


async def safe_send(ws, message):
    """Envia mensagem sem interromper em caso de erro."""
    try:
        await ws.send(message)
    except:
        pass


async def main():
    print(f"Servidor WebSocket rodando em ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # mantém servidor ativo


if __name__ == "__main__":
    asyncio.run(main())

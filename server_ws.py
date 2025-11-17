import os
import asyncio
import websockets
import json

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

connected = set()

async def handler(ws, path):
    connected.add(ws)
    try:
        async for msg in ws:
            try:
                data = json.loads(msg)
            except:
                continue

            # Mensagem de entrada
            if data.get("type") == "join":
                nick = data.get("nick", "Usuário")
                system_msg = {
                    "type": "system",
                    "text": f"** {nick} entrou no chat **"
                }
                await broadcast(system_msg, skip=None)

            # Mensagem normal
            elif data.get("type") == "msg":
                out = {
                    "type": "broadcast",
                    "text": f"{data.get('msg')}"
                }
                await broadcast(out, skip=None)

    except Exception as e:
        print("Erro:", e)
    finally:
        connected.remove(ws)


async def broadcast(message, skip=None):
    dead = []
    for ws in connected:
        if ws != skip:
            try:
                await ws.send(json.dumps(message))
            except:
                dead.append(ws)
    for ws in dead:
        connected.remove(ws)


async def main():
    print(f"Servidor WebSocket rodando em ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # Mantém rodando


if __name__ == "__main__":
    asyncio.run(main())

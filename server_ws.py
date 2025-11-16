import os
import asyncio
import websockets

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

connected = set()

async def handler(ws, path):
    connected.add(ws)
    try:
        async for msg in ws:
            # broadcast
            for c in connected:
                if c != ws:
                    await c.send(msg)
    finally:
        connected.remove(ws)

async def main():
    print(f"Iniciando servidor WebSocket em ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # mantém o servidor rodando

if __name__ == "__main__":
    asyncio.run(main())

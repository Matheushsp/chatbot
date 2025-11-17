#!/usr/bin/env python3
import socket, threading, json, traceback
HOST="0.0.0.0"; PORT=50000
clients_lock=threading.Lock(); clients={}
def recv_json_line(conn):
    buf=b""
    while True:
        try: ch=conn.recv(4096)
        except ConnectionResetError: return None
        if not ch: return None
        buf+=ch
        if b"\n" in buf:
            line, buf2 = buf.split(b"\n",1)
            try: return json.loads(line.decode().strip())
            except: return None
def send_json_line(conn,obj):
    conn.sendall((json.dumps(obj,ensure_ascii=False)+"\n").encode())
def broadcast(sender,msg):
    with clients_lock:
        for c in list(clients):
            if c is sender: continue
            try: send_json_line(c,{"broadcast":msg})
            except: remove_client(c)
def remove_client(conn):
    with clients_lock:
        if conn in clients:
            addr,nick=clients.pop(conn)
            try: conn.close()
            except: pass
            info=f"** {nick} saiu ({addr[0]}:{addr[1]}) **"
            print(info)
            for c in list(clients):
                try: send_json_line(c,{"system":info})
                except: pass
def handle_client(conn,addr):
    print(f"Conexão {addr}")
    obj=recv_json_line(conn)
    if not obj or "nick" not in obj: conn.close(); return
    nick=str(obj["nick"]).strip()
    if not nick: conn.close(); return
    with clients_lock: clients[conn]=(addr,nick)
    try: send_json_line(conn,{"system":f"** Bem-vindo {nick}! **"})
    except: remove_client(conn); return
    notice=f"** {nick} entrou ({addr[0]}:{addr[1]}) **"
    print(notice); broadcast(conn,notice)
    try:
        while True:
            obj=recv_json_line(conn)
            if obj is None: break
            if "msg" in obj:
                text=str(obj["msg"])
                formatted=f"[{nick}]: {text}"
                print(formatted); broadcast(conn,formatted)
            else:
                send_json_line(conn,{"system":"Formato inválido"})
    except: traceback.print_exc()
    finally: remove_client(conn)
def start():
    s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT)); s.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")
    try:
        while True:
            c,a=s.accept()
            threading.Thread(target=handle_client,args=(c,a),daemon=True).start()
    except KeyboardInterrupt: print("Finalizando...")
    finally:
        with clients_lock:
            for c in list(clients):
                try: c.close()
                except: pass
        s.close()
if __name__=="__main__": start()

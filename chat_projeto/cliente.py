#!/usr/bin/env python3
import socket, threading, json, sys
SERVER_HOST="127.0.0.1"; SERVER_PORT=50000
def recv_loop(sock):
    buf=b""
    try:
        while True:
            ch=sock.recv(4096)
            if not ch:
                print("[Servidor desconectou]"); break
            buf+=ch
            while b"\n" in buf:
                line, buf = buf.split(b"\n",1)
                if not line: continue
                try:
                    obj=json.loads(line.decode())
                    if "broadcast" in obj: print(obj["broadcast"])
                    elif "system" in obj: print(obj["system"])
                    else: print("[raw]",obj)
                except: print(line.decode(errors="ignore"))
    except: print("[Erro no recebimento]")
    finally:
        try: sock.close()
        except: pass
        sys.exit(0)
def send_json(sock,obj):
    sock.sendall((json.dumps(obj,ensure_ascii=False)+"\n").encode())
def main():
    host=SERVER_HOST; port=SERVER_PORT
    if len(sys.argv)>=2: host=sys.argv[1]
    if len(sys.argv)>=3: port=int(sys.argv[2])
    nick=input("Nick: ").strip()
    if not nick: return
    sock=socket.socket()
    try: sock.connect((host,port))
    except Exception as e:
        print("Falha:",e); return
    send_json(sock,{"nick":nick})
    threading.Thread(target=recv_loop,args=(sock,),daemon=True).start()
    print("Digite mensagens. /quit para sair.")
    while True:
        try: msg=input()
        except: break
        if msg.lower()=="/quit":
            sock.close(); break
        if msg.strip()=="":
            continue
        try: send_json(sock,{"msg":msg})
        except:
            print("Conexão perdida"); break
    try: sock.close()
    except: pass
if __name__=="__main__": main()

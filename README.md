📘 Sistema de Chat em Tempo Real

Este projeto implementa um chat online em tempo real utilizando WebSockets, permitindo que múltiplos usuários troquem mensagens instantaneamente através de um servidor central.

📌 Descrição Geral

O sistema consiste em:

Servidor WebSocket em Python, responsável por receber, interpretar e distribuir mensagens.

Cliente Web em HTML/JavaScript, que permite que usuários se conectem e conversem entre si.

Comunicação feita inteiramente via WebSockets em formato JSON, garantindo troca de mensagens rápida e contínua.

O projeto demonstra de forma simples a comunicação bidirecional entre cliente e servidor.

⚙️ Tecnologias Utilizadas

Python 3

websockets (biblioteca Python)

HTML5

CSS3

JavaScript

Render – para hospedar o servidor WebSocket

Vercel – para hospedar a interface web (opcional)

🧩 Funcionamento Geral
📡 Servidor WebSocket

O servidor:

mantém uma lista de usuários conectados;

recebe pacotes JSON dos clientes;

identifica ações como entrada (join) e envio de mensagens (msg);

envia mensagens de broadcast para todos os usuários conectados.

🖥️ Cliente Web

O cliente:

permite que o usuário informe um apelido;

se conecta ao servidor;

envia mensagens no formato JSON;

exibe mensagens próprias, de outros usuários e mensagens do sistema.

🔄 Comunicação Cliente ↔ Servidor

A comunicação é feita em JSON, com dois tipos principais:

✔ Entrada de usuário:
{
  "type": "join",
  "nick": "usuario"
}

✔ Mensagem enviada:
{
  "type": "msg",
  "msg": "Olá!"
}


O servidor recebe, interpreta e retransmite para todos os demais clientes.

🧱 Estrutura do Projeto
/
├── server_ws.py     # Servidor WebSocket
├── chat.html        # Cliente web
└── README.md        # Documentação do projeto

🎯 Objetivo do Projeto

Demonstrar de forma didática como funciona:

comunicação bidirecional contínua via WebSockets;

troca de mensagens em tempo real;

integração entre servidor Python e cliente web;

conceito básico de broadcast em aplicações online.

Este projeto pode servir como base para:

chats completos,

sistemas de monitoramento ao vivo,

dashboards em tempo real,

jogos multiplayer simples,

aplicações que exigem atualização constante de dados.

📄 Licença

Uso educacional e demonstrativo.

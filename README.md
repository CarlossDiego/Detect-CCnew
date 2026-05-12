🛡️ Sistema de Detecção de Movimento com Python, IoT e Nuvem
Este projeto foi desenvolvido como parte da disciplina de Python, IoT e Computação em Nuvem. O objetivo é demonstrar a integração entre visão computacional e protocolos de comunicação para monitoramento remoto.

🚀 Funcionalidades
Detecção em Tempo Real: Captura e processamento de vídeo via webcam.
Visão Computacional: Uso da biblioteca OpenCV para converter imagens em tons de cinza, aplicar desfoque e identificar diferenças entre frames.
Conectividade IoT: Envio de alertas automáticos para um Broker MQTT na nuvem toda vez que um movimento é detectado.
🛠️ Tecnologias Utilizadas
Linguagem: Python 3.
Bibliotecas: OpenCV, Paho-MQTT e NumPy.
Infraestrutura: Broker MQTT Público (HiveMQ).
⚙️ Arquitetura do Sistema
O fluxo de funcionamento do projeto segue a ordem: Câmera ➔ Processamento Python ➔ Detecção de Movimento ➔ Envio MQTT ➔ Nuvem

🔧 Como Executar
1.instale as dependências necessárias: pip install opencv-python numpy paho-mqtt

Execute o script principal: O sistema abrirá a câmera, processará os frames e enviará uma mensagem ao tópico "projeto/movimento" sempre que houver uma alteração significativa na imagem.
📈 Resultados Esperados
Detecção precisa de movimentos em tempo real.
Publicação instantânea de eventos no Broker MQTT.
Base para integração com dashboards ou notificações mobile.
Projeto desenvolvido em: 03/03/2026, por Carlos Diego e Carlos Eduardo.

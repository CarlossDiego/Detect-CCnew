import cv2
import numpy as np
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuração MQTT com a versão 2 ,  da API
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start() # Mantém a conexão ativa em segundo plano

camera = cv2.VideoCapture(1) 

# Captura inicial necessária para a primeira comparação [cite: 24]
ret, frame1 = camera.read()
ret, frame2 = camera.read()

# --- BLOCO DE INTRODUÇÃO ---
# Criar uma imagem preta de 480x640 (mesmo tamanho padrão da webcam)
intro = np.zeros((480, 640, 3), dtype=np.uint8)

# Configurações do Texto
fonte = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(intro, "SISTEMA DE DETECCAO IOT", (100, 200), fonte, 1, (255, 255, 255), 2)
cv2.putText(intro, "by: Carlos Diego and Carlos Eduardo", (85, 260), fonte, 0.8, (0, 255, 0), 2)
cv2.putText(intro, "Iniciando em 3 segundos...", (150, 400), fonte, 0.6, (200, 200, 200), 1)

# Exibir a Intro
cv2.imshow("Detector de Movimento", intro)
cv2.waitKey(1) # Necessário para o OpenCV renderizar a janela
time.sleep(3)  # Pausa de 3 segundos [cite: 33]
cv2.destroyWindow("Detector de Movimento") # Fecha a intro para abrir a camera
# ---------------------------

while camera.isOpened():
    # 1. Calcula a diferença e processa a imagem [cite: 24]
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    # 2. Encontra os contornos (movimento) [cite: 24]
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 5000: # Ajustei para 5000 para ser menos sensível
            continue

        # 1. Obtém as coordenadas do movimento (x, y, largura, altura)
        (x, y, w, h) = cv2.boundingRect(contour)

        # 2. Desenha o retângulo no frame original
        # Parâmetros: (imagem, ponto_inicial, ponto_final, cor_BGR, espessura)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 3. Adiciona um texto acima do retângulo
        cv2.putText(frame1, "STATUS: MOVIMENTO", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Log de detecção e envio para a nuvem [cite: 19, 25]
        print("Movimento Detectado!")
        mensagem = f"Movimento detectado em {datetime.now()}"
        client.publish("projeto/movimento", mensagem) 
        
        # Se chegou aqui, detectou movimento! [cite: 25]
        print("Movimento Detectado!")
        mensagem = f"Movimento detectado em {datetime.now()}"
        client.publish("projeto/seu_nome_aqui/movimento", mensagem)

    # 3. Exibe o resultado na tela
    cv2.imshow("Detector de Movimento", frame1)

    # 4. Atualiza os frames para a próxima comparação [cite: 25]
    frame1 = frame2
    ret, frame2 = camera.read()

    if not ret:
        break

    # Sai ao apertar ESC
    if cv2.waitKey(10) == 27:
        break

camera.release()
cv2.destroyAllWindows()
client.loop_stop()
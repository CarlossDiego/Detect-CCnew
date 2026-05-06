import cv2
import numpy as np
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# --- MELHORIA 1: CONEXÃO RÁPIDA (Não trava o início) ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect_async("broker.hivemq.com", 1883, 60)
client.loop_start() 

# --- BLOCO DE INTRODUÇÃO ---
intro = np.zeros((480, 640, 3), dtype=np.uint8)
fonte = cv2.FONT_HERSHEY_SIMPLEX

cv2.putText(intro, "SISTEMA DE DETECCAO IOT", (100, 200), fonte, 1, (255, 255, 255), 2)
cv2.putText(intro, "by: Carlos Diego and Carlos Eduardo", (85, 260), fonte, 0.8, (0, 255, 0), 2)
cv2.putText(intro, "Pressione ENTER no terminal para iniciar...", (100, 400), fonte, 0.6, (200, 200, 200), 1)

# Exibir a Intro
cv2.imshow("Detector de Movimento", intro)
cv2.waitKey(1) 

# --- MELHORIA 2: INÍCIO POR TECLADO ---
print("\n" + "="*40)
print("SISTEMA PRONTO: Aguardando comando...")
print("Aperte [ENTER] no terminal para ligar a camera.")
print("="*40)
input() # Pausa o código até você apertar Enter no terminal

# --- MELHORIA 3: ACELERADOR DE CÂMERA (CAP_DSHOW) ---
camera = cv2.VideoCapture(1, cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.destroyWindow("Detector de Movimento") 

# Captura inicial necessária para a primeira comparação
ret, frame1 = camera.read()
ret, frame2 = camera.read()

while camera.isOpened():
    # 1. Calcula a diferença e processa a imagem
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    # 2. Encontra os contornos (movimento)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 5000: 
            continue

        # Obtém as coordenadas do movimento
        (x, y, w, h) = cv2.boundingRect(contour)

        # Desenha o retângulo no frame original
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Adiciona um texto acima do retângulo
        cv2.putText(frame1, "STATUS: MOVIMENTO", (x, y - 10), 
                    fonte, 0.5, (0, 255, 0), 2)

        # Log de detecção e envio para a nuvem
        agora = datetime.now().strftime("%H:%M:%S")
        print(f"[{agora}] Movimento Detectado!")
        
        mensagem = f"Movimento detectado em {datetime.now()}"
        client.publish("projeto/movimento", mensagem) 
        client.publish("projeto/seu_nome_aqui/movimento", mensagem)

    # 3. Exibe o resultado na tela
    cv2.imshow("Monitoramento em Tempo Real", frame1)

    # 4. Atualiza os frames para a próxima comparação
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
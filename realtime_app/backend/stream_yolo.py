import cv2
import torch
import os
import time
from ultralytics import YOLO

def iniciar_stream_com_inferencia():
    # Limpa VRAM antes de iniciar
    torch.cuda.empty_cache()

    # 1. Carrega o modelo de DETECÇÃO (usando o caminho gerado pelo seu log de treino)
    # Lembre-se: Você precisa ter exportado o best.pt para best.engine antes!
    caminho_modelo = r"/home/jorgemetri/Desktop/Autonomous_Inspection_DroneDji/yolo_training/src/runs/detect/Inspecao_Avarias/YOLO11_Large_10242/weights/best.engine"
    model = YOLO(caminho_modelo, task="detect") 

    # 2. Conecta ao MediaMTX
    rtsp_url = "rtsp://localhost:8554/live/drone"
    cap = cv2.VideoCapture(rtsp_url)
    
    # CRÍTICO: Zera o buffer para ler sempre o frame atual e não criar atraso
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    print("Aguardando conexao com o fluxo do drone...")

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Aguardando sinal/imagem...")
            time.sleep(1)
            continue

        # 3. Inferência configurada para velocidade e alta resolução (1024)
        results = model.predict(
            source=frame,
            device=0,
            half=True,         # Ativa o FP16 na sua RTX 5070
            conf=0.6,          # Filtra falsos positivos
            imgsz=1024,        # Resolução do seu treino YOLO11 Large
            verbose=False      # Desliga o spam no terminal
        )

        # 4. Prevenção de Gargalo ao Pintar (Transferência para RAM)
        for r in results:
            r_cpu = r.cpu()
            # Desenha as caixas (bounding boxes) no frame
            frame_anotado = r_cpu.plot() 

        # 5. Exibe a imagem em tempo real
        cv2.imshow('Mavic 3E - Inspecao Autonoma', frame_anotado)

        # Aperte 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Limpeza
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_stream_com_inferencia()
    os._exit(0) # Força encerramento limpo
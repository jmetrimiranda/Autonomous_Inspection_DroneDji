import cv2
import torch
import os
import time
from ultralytics import YOLO

def iniciar_stream_com_inferencia():
    # FORÇA O PROTOCOLO TCP (Evita travamentos em redes Wi-Fi/4G)
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    
    torch.cuda.empty_cache()

    caminho_engine = "/home/jorgemetri/Desktop/Autonomous_Inspection_DroneDji/yolo_training/src/runs/detect/Inspecao_Avarias/YOLO11_Large_10242/weights/best.engine"
    
    print("Carregando modelo TensorRT...")
    model = YOLO(caminho_engine, task="detect") 

    rtsp_url = "rtsp://localhost:8554/live/drone"
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG) # Especifica o backend FFMPEG
    
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("Erro: Não foi possível abrir o fluxo RTSP. O MediaMTX está recebendo o sinal?")
        return

    print("Conexão estabelecida! Iniciando análise...")

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Aguardando sinal/imagem...")
            time.sleep(0.5)
            continue

        results = model.predict(
            source=frame,
            device=0,
            half=True,         
            conf=0.5,          
            imgsz=1024,        
            verbose=False      
        )

        frame_anotado = results[0].plot() 
        cv2.imshow('Mavic 3E - Inspeção Autônoma', frame_anotado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_stream_com_inferencia()
    os._exit(0)
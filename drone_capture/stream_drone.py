import cv2
import torch
import os
import time
from ultralytics import YOLO

def iniciar_stream_com_yolo():
    torch.cuda.empty_cache()
    
    # Verifique se este caminho está 100% correto
    caminho_engine = "/home/jorgemetri/Desktop/Autonomous_Inspection_DroneDji/yolo_training/src/runs/detect/Inspecao_Avarias/YOLO11_Large_10242/weights/best.engine"
    
    print("🚀 Carregando motor TensorRT...")
    model = YOLO(caminho_engine, task="detect") 
    rtsp_url = "rtsp://localhost:8554/live/drone"
    
    while True:
        cap = cv2.VideoCapture(rtsp_url)
        # Aumentamos um pouco o buffer para estabilizar o 1024p
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        
        print(f"\n📡 Tentando conectar ao fluxo: {rtsp_url}")
        
        tentativas_falhas = 0
        while True:
            ret, frame = cap.read()
            
            if not ret:
                tentativas_falhas += 1
                if tentativas_falhas > 30: # Só desiste após ~1 seg de falha contínua
                    print("⚠️ Sinal perdido. Tentando reconectar...")
                    cap.release()
                    break
                continue
            
            tentativas_falhas = 0 # Reseta ao receber um frame válido
            
            # Cálculo de FPS para monitorar a RTX 5070
            t_inicio = time.time()

            # Inferência
            results = model.predict(
                source=frame,
                device=0,
                half=True,
                conf=0.5,
                imgsz=1024,
                verbose=False
            )

            # Desenho (Pilar 3 do seu manual: r.cpu().plot())
            frame_anotado = results[0].plot()

            # FPS no topo da tela
            fps = 1 / (time.time() - t_inicio)
            cv2.putText(frame_anotado, f"FPS: {fps:.1f}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Mavic 3E - Inspeção em Tempo Real', frame_anotado)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                os._exit(0)

if __name__ == "__main__":
    iniciar_stream_com_yolo()
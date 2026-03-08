from ultralytics import YOLO

# Caminho absoluto ou relativo para o seu modelo treinado
caminho_modelo = "/home/jorgemetri/Desktop/Autonomous_Inspection_DroneDji/yolo_training/src/runs/detect/Inspecao_Avarias/YOLO11_Large_10242/weights/best.pt"

model = YOLO(caminho_modelo)

print("Iniciando a exportacao para TensorRT...")
print("A GPU vai aquecer e esse processo pode demorar alguns minutos. Aguarde!")

# Exporta ativando FP16 (metade da precisão, dobro da velocidade nas RTX)
model.export(
    format="engine", 
    device=0, 
    half=True, 
    imgsz=1024,
    workspace=4 # Reserva até 4GB de VRAM para otimização
)

print("Exportacao concluida com sucesso!")

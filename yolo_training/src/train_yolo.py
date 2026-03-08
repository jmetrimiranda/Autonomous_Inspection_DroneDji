import ssl
from ultralytics import YOLO

ssl._create_default_https_context = ssl._create_unverified_context

# Usando o modelo Medium para suportar a resolução 1024
model = YOLO("yolo26m.pt")  

results = model.train(
    task='detect',          
    data=r"/home/jorgemetri/Desktop/Autonomous_Inspection_DroneDji/yolo_training/dataset/Drone_GMU-4/data.yaml", 
    epochs=300,             
    patience=50,            
    imgsz=1024,             # Resolução alta mantida
    batch=4,                # Batch fixado manualmente
    device=0,               
    workers=4,              # Workers reduzidos para estabilidade
    amp=True,               
    optimizer='auto',       
    cos_lr=True,            
    close_mosaic=10,        
    mosaic=1.0,             
    mixup=0.1,              
    project="Inspecao_Avarias", 
    name="YOLO26_Medium_1024",
    plots=True              
)
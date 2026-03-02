├── .github/                 # Configurações de CI/CD para automação
├── drone_capture/           # PASSO 1: Comunicação com o DJI
│   ├── src/
│   │   └── dji_stream.py    # Conecta ao controle do drone e gera o stream (ex: RTSP)
│   └── requirements.txt
├── yolo_training/           # PASSO 2: Obtenção de Dados e Treinamento
│   ├── src/
│   │   ├── fetch_dataset.py # Script que consome a API do Roboflow e baixa as imagens/labels
│   │   └── train_yolo.py    # Script de fine-tuning do modelo YOLO escolhido
│   ├── dataset/             # Pasta local para os dados baixados do Roboflow (adicionar ao .gitignore)
│   ├── runs/                # Saída padrão do YOLO com os pesos (.pt) e métricas de cada treino
│   ├── yolo_config.yaml     # Arquivo YAML de configuração apontando para os paths do dataset
│   └── requirements.txt
├── inference_service/       # PASSO 3: Inferência no Stream
│   ├── src/
│   │   ├── engine.py        # Carrega o modelo exportado e otimizado (ex: TensorRT)
│   │   └── predictor.py     # Lê o stream do drone, roda a inferência e gera as coordenadas
│   ├── weights/             # Pesos finais escolhidos para deploy (.engine, .onnx)
│   └── requirements.txt
├── realtime_app/            # PASSO 4: Aplicação em Tempo Real
│   ├── backend/             # Servidor (FastAPI/Node) para distribuir o vídeo e gerenciar WebSockets
│   ├── frontend/            # Interface do usuário (React/Vue) com Canvas para desenhar as avarias
│   └── package.json / requirements.txt
├── .gitignore               # Deve ignorar datasets, logs pesados de treino e arquivos .pt/.engine
└── README.md

# Contexto do Projeto para Geração de Código Manim

**Objetivo:** Criar uma apresentação animada usando a biblioteca `manim` em Python para explicar um sistema de inspeção industrial. O sistema usa um drone que sobrevoa uma usina, captura imagens dos ativos, envia para um computador e processa as imagens usando uma Rede Neural para identificar falhas (detecção de objetos/anomalias).

**Estilo Visual:** Fundo escuro (padrão do Manim), animações fluidas, visual moderno e tecnológico.

---

## Cena 1: Arquitetura do Sistema e Conectividade (`SystemArchitecture`)

**Descrição da Animação:**
1. **O Drone:** Um ícone ou imagem de um drone aparece na tela (à esquerda).
2. **O Controle:** Um ícone de controle remoto aparece (no centro).
3. **O Computador:** Um ícone de um notebook/computador aparece (à direita).
4. **Conexões:**
   - Sinais de rádio (arcos pulsantes) saem do drone para o controle.
   - Uma linha de conexão (ou sinal Wi-Fi) liga o controle ao computador.
5. **Transição:** A tela faz um *zoom in* na tela do computador, indicando que agora vamos olhar para o software/processamento interno. Tudo desaparece (`FadeOut`) para iniciar a próxima cena.

**Requisitos Técnicos para o Manim (Cena 1):**
- Usar `SVGMobject` ou ícones simples construídos com primitivas geométricas para o drone, controle e PC, ou preparar o código para receber `ImageMobject` (ex: `drone_icon.png`).
- Usar `Succession` e `Create` para as animações de desenho.
- Para o sinal, usar `Arc` com opacidade variando para simular pulso.

---

## Cena 2: Fluxo de Dados e Rede Neural (`NeuralNetworkInference`)

**Descrição da Animação:**
1. **Entradas (Raw Images):** À esquerda da tela, aparecem 5 imagens (lado a lado verticalmente ou empilhadas em perspectiva). Estas são as imagens sem rótulos. *(Nota: Deixe o código pronto usando `ImageMobject` com caminhos de arquivo genéricos como `"img_in_1.jpg"`, etc.)*
2. **A Rede Neural (CNN/MLP):** No centro da tela, surge uma representação de uma Rede Neural.
   - Pode ser um conjunto de camadas com nós (círculos) e arestas (linhas).
   - *Animação:* As 5 imagens de entrada deslizam (`ApplyMethod(mobj.move_to)`) para a primeira camada da rede neural.
3. **Processamento (Forward Pass):** - Quando as imagens tocam a primeira camada, as arestas da rede neural começam a brilhar/piscar sequencialmente da esquerda para a direita (usando `ShowPassingFlash` ou mudando a cor das linhas momentaneamente para amarelo/verde).
   - Os nós também podem pulsar (`scale`).
4. **Saída (Labeled Image):** - Do lado direito da última camada da rede neural, emerge o resultado final.
   - O resultado é a imagem processada com as "Bounding Boxes" (caixas delimitadoras) destacando as falhas detectadas (como corrosão ou danos no duto). *(Usar caminho genérico como `"img_out_labeled.jpg"`)*.
5. **Destaque:** A imagem de saída vai para o centro da tela, fica maior (`scale`) e as caixas delimitadoras piscam para dar ênfase à detecção.

**Requisitos Técnicos para o Manim (Cena 2):**
- Criar uma classe auxiliar para desenhar a rede neural (ex: listas de nós por camada `[5, 8, 8, 4, 1]`).
- Usar `VGroup` para organizar as imagens de entrada.
- Fazer a animação de "Forward Pass" de forma sequencial com loops nas camadas.
- Garantir que o código seja modular e fácil de substituir os caminhos das imagens (`"path/to/image.jpg"`).

---

## Instruções para a IA Geradora:
Por favor, gere o código Python completo utilizando `manim` (versão Community). Divida o código claramente entre as duas classes (`SystemArchitecture` e `NeuralNetworkInference`). Inclua comentários explicando onde eu devo colocar os arquivos das minhas imagens reais.
"""
Apresentação Manim: Sistema de Inspeção Industrial com Drone
============================================================
Execução (a partir da pasta presentation/):
    manim -pql presentation.py SystemArchitecture
    manim -pql presentation.py NeuralNetworkInference
    manim -pqh presentation.py NeuralNetworkInference   # alta qualidade

Imagens de entrada (já presentes):
    assets/input_1.jpg ~ assets/input_4.jpg

Imagem de saída (adicionar quando o modelo YOLO estiver treinado):
    assets/output_labeled.jpg
    → Descomente o bloco ImageMobject na seção "Imagem de saída" abaixo.
"""

from manim import *

# ─────────────────────────────────────────────────────────────────────────────
# Helpers de ícones construídos com primitivas (substitua por ImageMobject
# quando tiver os arquivos reais em presentation/assets/)
# ─────────────────────────────────────────────────────────────────────────────

def make_drone(color=BLUE_C, scale=1.0) -> VGroup:
    """Drone simples: corpo central + 4 braços + hélices."""
    body = RoundedRectangle(corner_radius=0.15, width=0.7, height=0.35,
                            color=color, fill_opacity=0.9)
    arms = VGroup()
    for angle in [45, 135, 225, 315]:
        arm = Line(ORIGIN, rotate_vector(RIGHT * 0.55, angle * DEGREES),
                   color=GREY_B, stroke_width=3)
        rotor = Circle(radius=0.18, color=color, fill_opacity=0.3,
                       stroke_width=2)
        rotor.move_to(arm.get_end())
        arms.add(arm, rotor)
    camera = Circle(radius=0.08, color=YELLOW, fill_opacity=1).next_to(body, DOWN, buff=0.05)
    drone = VGroup(arms, body, camera).scale(scale)
    return drone


def make_remote(color=GREEN_C, scale=1.0) -> VGroup:
    """Controle remoto simples."""
    body = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.1,
                            color=color, fill_opacity=0.85)
    joystick_l = Circle(radius=0.13, color=WHITE, fill_opacity=0.6)
    joystick_r = Circle(radius=0.13, color=WHITE, fill_opacity=0.6)
    joystick_l.move_to(body.get_center() + LEFT * 0.2 + DOWN * 0.15)
    joystick_r.move_to(body.get_center() + RIGHT * 0.2 + DOWN * 0.15)
    antenna = Line(body.get_top(), body.get_top() + UP * 0.35, color=GREY_B, stroke_width=3)
    return VGroup(body, joystick_l, joystick_r, antenna).scale(scale)


def make_computer(color=BLUE_B, scale=1.0) -> VGroup:
    """Notebook simples."""
    screen = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.95,
                              color=color, fill_opacity=0.85)
    screen_inner = RoundedRectangle(corner_radius=0.05, width=1.1, height=0.7,
                                    color=BLACK, fill_opacity=1)
    screen_inner.move_to(screen.get_center())
    # tela com texto "AI"
    ai_text = Text("AI", font_size=22, color=GREEN_C, weight=BOLD)
    ai_text.move_to(screen_inner.get_center())
    base = RoundedRectangle(corner_radius=0.05, width=1.6, height=0.12,
                            color=GREY_D, fill_opacity=1)
    base.next_to(screen, DOWN, buff=0)
    return VGroup(screen, screen_inner, ai_text, base).scale(scale)


# ─────────────────────────────────────────────────────────────────────────────
# Cena 1 – Arquitetura do Sistema
# ─────────────────────────────────────────────────────────────────────────────

class SystemArchitecture(Scene):
    def construct(self):
        # ── Título ──────────────────────────────────────────────────────────
        title = Text("Sistema de Inspeção Industrial com Drone",
                     font_size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(0.5)

        # ── Ícones ──────────────────────────────────────────────────────────
        # Troque por ImageMobject("presentation/assets/drone_icon.png") etc.
        drone   = make_drone(scale=1.1).move_to(LEFT * 4.5)
        remote  = make_remote(scale=1.0).move_to(ORIGIN)
        pc      = make_computer(scale=1.0).move_to(RIGHT * 4.5)

        label_drone  = Text("Drone DJI", font_size=20, color=BLUE_C).next_to(drone,  DOWN, buff=0.3)
        label_remote = Text("Controle",  font_size=20, color=GREEN_C).next_to(remote, DOWN, buff=0.3)
        label_pc     = Text("PC / IA",   font_size=20, color=BLUE_B ).next_to(pc,     DOWN, buff=0.3)

        self.play(
            FadeIn(drone,   shift=RIGHT * 0.4),
            FadeIn(remote,  shift=UP    * 0.3),
            FadeIn(pc,      shift=LEFT  * 0.4),
            lag_ratio=0.3,
        )
        self.play(
            FadeIn(label_drone), FadeIn(label_remote), FadeIn(label_pc),
            lag_ratio=0.2,
        )
        self.wait(0.4)

        # ── Sinal de Rádio: Drone → Controle ────────────────────────────────
        radio_label = Text("Sinal de Rádio / RC", font_size=16, color=YELLOW)\
            .move_to(LEFT * 2.3 + UP * 1.3)
        self.play(FadeIn(radio_label))

        for _ in range(3):
            for r, op in [(0.25, 0.9), (0.45, 0.6), (0.65, 0.3)]:
                arc = Arc(radius=r, start_angle=-PI / 3, angle=2 * PI / 3,
                          color=YELLOW, stroke_width=2, stroke_opacity=op)
                arc.move_to(drone.get_right() + RIGHT * r)
                self.play(Create(arc), run_time=0.12)
                self.play(FadeOut(arc), run_time=0.08)

        # ── Linha: Controle → PC (Wi-Fi / cabo) ─────────────────────────────
        data_line = DashedLine(
            remote.get_right(), pc.get_left(),
            color=TEAL, dash_length=0.15, stroke_width=3,
        )
        wifi_label = Text("Wi-Fi / Ethernet", font_size=16, color=TEAL)\
            .move_to(RIGHT * 2.2 + UP * 0.65)
        self.play(Create(data_line), run_time=1.0)
        self.play(FadeIn(wifi_label))
        self.wait(0.5)

        # ── Seta de dados (pacote de imagens) viajando pelo fio ─────────────
        packet = Dot(color=ORANGE, radius=0.14).move_to(remote.get_right())
        self.play(FadeIn(packet))
        self.play(packet.animate.move_to(pc.get_left()), run_time=1.2,
                  rate_func=smooth)
        self.play(FadeOut(packet))

        # ── Destaque no PC ───────────────────────────────────────────────────
        zoom_rect = SurroundingRectangle(pc, color=GREEN_C, buff=0.2,
                                         corner_radius=0.1, stroke_width=3)
        self.play(Create(zoom_rect))
        self.play(zoom_rect.animate.scale(1.15), run_time=0.4)
        self.play(zoom_rect.animate.scale(1 / 1.15), run_time=0.4)
        self.wait(0.4)

        # ── Fade out tudo ────────────────────────────────────────────────────
        all_objs = VGroup(
            title, drone, remote, pc,
            label_drone, label_remote, label_pc,
            data_line, wifi_label, radio_label, zoom_rect,
        )
        self.play(FadeOut(all_objs), run_time=1.2)
        self.wait(0.3)


# ─────────────────────────────────────────────────────────────────────────────
# Helper – Rede Neural desenhada com primitivas
# ─────────────────────────────────────────────────────────────────────────────

class NeuralNetworkDiagram(VGroup):
    """
    Desenha uma MLP simples com as camadas definidas em `layer_sizes`.
    Retorna um VGroup com:
        .nodes   – lista de listas de Circle por camada
        .edges   – VGroup com todas as arestas
        .layers  – VGroup de cada coluna de nós
    """

    def __init__(self, layer_sizes=(5, 8, 8, 4, 1),
                 node_radius=0.12, h_spacing=1.2, v_spacing=0.38,
                 node_color=BLUE_C, edge_color=GREY, **kwargs):
        super().__init__(**kwargs)
        self.node_radius = node_radius
        self.node_color  = node_color
        self.edge_color  = edge_color
        self.nodes: list[list[Circle]] = []
        self.edges = VGroup()
        self.layers = VGroup()

        n_layers = len(layer_sizes)

        # Cria nós
        for i, n_nodes in enumerate(layer_sizes):
            col = VGroup()
            node_list = []
            total_h = (n_nodes - 1) * v_spacing
            for j in range(n_nodes):
                node = Circle(radius=node_radius, color=node_color,
                              fill_opacity=0.7, stroke_width=1.5)
                node.move_to(
                    RIGHT * i * h_spacing + UP * (total_h / 2 - j * v_spacing)
                )
                col.add(node)
                node_list.append(node)
            self.nodes.append(node_list)
            self.layers.add(col)

        # Cria arestas
        for i in range(n_layers - 1):
            for src in self.nodes[i]:
                for dst in self.nodes[i + 1]:
                    edge = Line(
                        src.get_center(), dst.get_center(),
                        color=edge_color, stroke_width=0.6, stroke_opacity=0.4,
                    )
                    self.edges.add(edge)

        self.add(self.edges, self.layers)
        self.center()


# ─────────────────────────────────────────────────────────────────────────────
# Cena 2 – Fluxo de Dados e Rede Neural
# ─────────────────────────────────────────────────────────────────────────────

class NeuralNetworkInference(Scene):
    def construct(self):
        # ── Título ──────────────────────────────────────────────────────────
        title = Text("Inferência com Rede Neural (YOLO)",
                     font_size=30, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=DOWN * 0.2))
        self.wait(0.4)

        # ── Imagens de entrada (reais) ───────────────────────────────────────
        # Usando as 4 imagens capturadas pelo drone (assets/input_1.jpg ... input_4.jpg)
        IMG_HEIGHT = 1.1   # altura de cada imagem na cena — ajuste se necessário
        input_imgs = Group(
            *[
                ImageMobject(f"assets/input_{i}.jpg").scale_to_fit_height(IMG_HEIGHT)
                for i in range(1, 5)
            ]
        )
        input_imgs.arrange(DOWN, buff=0.12)
        input_imgs.to_edge(LEFT, buff=0.4)

        # Borda azul em volta de cada imagem
        borders = VGroup(
            *[
                SurroundingRectangle(img, color=BLUE_D, buff=0.03, stroke_width=1.5)
                for img in input_imgs
            ]
        )

        input_label = Text("Imagens\nCapturadas", font_size=18, color=BLUE_C,
                           t2c={"Capturadas": BLUE_D})
        input_label.next_to(input_imgs, UP, buff=0.2)

        self.play(FadeIn(input_label))
        self.play(
            LaggedStart(
                *[FadeIn(img, shift=RIGHT * 0.3) for img in input_imgs],
                lag_ratio=0.2,
            )
        )
        self.play(Create(borders))
        self.wait(0.4)

        # ── Rede Neural ─────────────────────────────────────────────────────
        # Primeira camada = 4 nós (um por imagem de entrada)
        nn = NeuralNetworkDiagram(
            layer_sizes=(4, 8, 8, 4, 1),
            node_radius=0.13, h_spacing=1.15, v_spacing=0.36,
            node_color=TEAL_C, edge_color=GREY_B,
        )
        nn.move_to(ORIGIN + RIGHT * 0.5)
        nn_label = Text("CNN / YOLO", font_size=18, color=TEAL_C)\
            .next_to(nn, UP, buff=0.3)

        self.play(FadeIn(nn_label))
        self.play(
            LaggedStart(*[Create(layer) for layer in nn.layers], lag_ratio=0.25),
            run_time=1.5,
        )
        self.play(Create(nn.edges), run_time=0.8)
        self.wait(0.3)

        # ── Imagens "entram" na primeira camada ─────────────────────────────
        img_copies = input_imgs.copy()
        self.play(
            img_copies.animate
                .arrange(DOWN, buff=0.06)
                .scale_to_fit_height(nn.layers[0].height + 0.3)
                .move_to(nn.layers[0].get_center() + LEFT * 1.0),
            run_time=1.0,
        )
        self.play(FadeOut(img_copies), run_time=0.3)

        # ── Forward pass: arestas brilham camada a camada ───────────────────
        n_layers = len(nn.nodes)
        edges_per_layer: list[VGroup] = []
        edge_list = list(nn.edges)
        idx = 0
        nodes_per_layer = [len(col) for col in nn.nodes]
        for i in range(n_layers - 1):
            count = nodes_per_layer[i] * nodes_per_layer[i + 1]
            edges_per_layer.append(VGroup(*edge_list[idx: idx + count]))
            idx += count

        # Nós pulsam e arestas acendem
        for i in range(n_layers):
            # Pulsa coluna de nós
            col = nn.layers[i]
            self.play(
                col.animate.set_fill(YELLOW_C, opacity=0.95)
                           .set_stroke(YELLOW_A, width=2),
                run_time=0.25,
            )
            if i < n_layers - 1:
                flash_edges = edges_per_layer[i].copy()
                flash_edges.set_color(GREEN_C).set_stroke(width=1.8, opacity=0.9)
                self.play(FadeIn(flash_edges), run_time=0.2)
                self.play(FadeOut(flash_edges), run_time=0.15)
            self.play(
                col.animate.set_fill(TEAL_C, opacity=0.7)
                           .set_stroke(TEAL_C, width=1.5),
                run_time=0.2,
            )

        self.wait(0.3)

        # ── Imagens de saída (resultados YOLO: image0..3) ───────────────────
        # 4 thumbnails empilhados à direita da rede
        OUT_THUMB_H = 0.75
        out_thumbs = Group(
            *[
                ImageMobject(f"assets/image{i}.jpg").scale_to_fit_height(OUT_THUMB_H)
                for i in range(4)
            ]
        )
        out_thumbs.arrange(DOWN, buff=0.1)
        out_thumbs.next_to(nn.layers[-1], RIGHT, buff=0.6)

        out_borders = VGroup(
            *[
                SurroundingRectangle(img, color=RED_B, buff=0.03, stroke_width=2)
                for img in out_thumbs
            ]
        )

        out_label = Text("Detecções\nYOLO", font_size=18, color=RED_B,
                         t2c={"YOLO": ORANGE})
        out_label.next_to(out_thumbs, UP, buff=0.2)

        self.play(FadeIn(out_label))
        self.play(
            LaggedStart(
                *[FadeIn(img, shift=LEFT * 0.3) for img in out_thumbs],
                lag_ratio=0.2,
            )
        )
        self.play(Create(out_borders))
        self.wait(0.4)

        # ── Fade out da rede, deixa só as saídas ────────────────────────────
        self.play(FadeOut(nn, nn_label, input_imgs, borders, input_label, title))
        self.wait(0.2)

        # ── Cada imagem vai ao centro em sequência (carrossel) ──────────────
        final_msg = Text("Falha detectada automaticamente!",
                         font_size=26, color=GREEN_C, weight=BOLD)
        final_msg.to_edge(DOWN, buff=0.45)

        center_img = None
        highlight_rect = None

        for i, (thumb, border) in enumerate(zip(out_thumbs, out_borders)):
            # Cria versão grande centralizada
            big = ImageMobject(f"assets/image{i}.jpg").scale_to_fit_height(4.0)
            big.move_to(ORIGIN)
            h_rect = SurroundingRectangle(big, color=RED, buff=0.06, stroke_width=3)

            if i == 0:
                self.play(
                    FadeIn(big),
                    Create(h_rect),
                    out_label.animate.to_edge(UP, buff=0.4),
                    run_time=0.7,
                )
                self.play(Write(final_msg))
            else:
                self.play(
                    FadeOut(center_img),
                    FadeOut(highlight_rect),
                    FadeIn(big),
                    Create(h_rect),
                    run_time=0.6,
                )

            # Pisca borda de destaque 2x
            for _ in range(2):
                self.play(h_rect.animate.set_stroke(opacity=0.15), run_time=0.18)
                self.play(h_rect.animate.set_stroke(opacity=1.0),  run_time=0.18)

            self.wait(0.6)
            center_img = big
            highlight_rect = h_rect

        self.wait(0.5)
        self.play(
            FadeOut(center_img, highlight_rect, out_thumbs, out_borders,
                    out_label, final_msg),
            run_time=1.0,
        )
        self.wait(0.3)

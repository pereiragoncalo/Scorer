"""Striker — jogo de carreira de um avançado em Python/Kivy.


Controlos
---------
Os menus controlam a carreira, treino, agente e jogos completos.
ESPAÇO / clique na zona inferior durante uma oportunidade: rematar.
Clique/toque dentro da baliza: apontar diretamente e rematar.
Setas ou WASD: mover manualmente a mira.
C: voltar à mira automática.
R: repor as estatísticas.
ESC: sair.


A partida e o estádio usam o Canvas do Kivy. Os menus usam layouts Kivy
responsivos sem ficheiros KV. A carreira é guardada automaticamente.
"""


from __future__ import annotations


import json
import math
import random
import struct
import urllib.parse
import urllib.request
import wave
from datetime import date
from pathlib import Path
from typing import Iterable, Optional


from kivy.config import Config




Config.set("graphics", "minimum_width", "320")
Config.set("graphics", "minimum_height", "240")
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", "1")




from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import (
    ClearBuffers,
    ClearColor,
    Color,
    Ellipse,
    Fbo,
    Line,
    Mesh,
    PopMatrix,
    PushMatrix,
    Rectangle,
    Translate,
    Triangle,
)
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label as UiLabel
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from menu_ui import CareerMenu, MENU_VIEWS, FlowLabel, TouchButton, MatchNotice
from kivy.utils import platform




Window.clearcolor = (0.025, 0.055, 0.075, 1.0)




from career import GRAVITY, GOAL_WIDTH, GOAL_HEIGHT, GOAL_DEPTH, VEIL_TOP_DEPTH, VEIL_TOUCH_DEPTH, VEIL_SAG, VEIL_SLOPE_LENGTH, VEIL_PATH_LENGTH, NET_RIPPLE_DURATION, PHYSICS_STEP, POST_RADIUS, BALL_RADIUS, START_Y, GOALKEEPER_Y, GOALKEEPER_SCALE, PLAYER_SCALE, FIELD_PLAYER_SCALE, HEADER_BALL_HEIGHT, STAND_CONCRETE, STAND_RISER, STAND_TREAD, STAND_EDGE, STAND_RAIL, STAND_ROOF, STAND_ROWS, STAND_CORNER_X, STAND_FRONT_Y, STAND_ROW_DEPTH, STAND_TREAD_DEPTH, STAND_ROW_RISE, SHOT_ORIGINS, HEADER_ORIGINS, PENALTY_ORIGIN, FREE_KICK_ORIGINS, CAMERA_POSITION, CAMERA_VERTICAL_FOV, clamp, length3, dot3, subtract3, normalize3, CAMERA_FORWARD, CAMERA_RIGHT, CAMERA_UP, Ball, NetRipple, FieldPlayer, EUROPE_PYRAMID_DEPTH, EUROPE_COUNTRIES, WORLD_COUNTRIES, club_kit, poisson_goal, CareerClub, CareerMode

def force_android_landscape() -> None:
    """Pede landscape ao Android, tanto em APK como no Pydroid/Kivy Launcher."""
    if platform != "android":
        return


    # python-for-android expõe normalmente a Activity por este caminho.
    try:
        from android import mActivity


        mActivity.setRequestedOrientation(6)  # SENSOR_LANDSCAPE
        return
    except (ImportError, AttributeError):
        pass


    # Fallback para distribuições Android que só expõem a Activity via PyJNIus.
    try:
        from jnius import autoclass


        activity_info = autoclass("android.content.pm.ActivityInfo")
        python_activity = autoclass("org.kivy.android.PythonActivity")
        python_activity.mActivity.setRequestedOrientation(
            activity_info.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
        )
    except Exception:
        # O desenho mostra uma indicação para rodar o equipamento se o host
        # bloquear alterações de orientação.
        pass




class StrikerGame(Widget):
    """Widget principal: simulação, controlos e renderização."""


    STATE_AIMING = "aiming"
    STATE_SHOT = "shot"
    STATE_RESULT = "result"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.ball = Ball()
        self.shot_origin_x = 0.0
        self.shot_origin_y = START_Y
        self.last_origin_index = -1
        self.player_kick_progress = 0.0
        self.shot_type = "kick"
        self.one_on_one = False
        self.field_players: list[FieldPlayer] = []
        self.last_field_collision: Optional[tuple[str, float, float]] = None
        self.state = self.STATE_AIMING
        self.state_age = 0.0
        self.elapsed = 0.0


        self.aim_x = 0.0
        self.aim_z = 1.15
        self.aim_phase = 0.0
        self.power_phase = math.pi / 2.0
        self.power = 0.82
        self.auto_aim = True
        self.aim_direction = 1.0
        self.aim_horizontal_mix = 1.73
        self.aim_vertical_ratio = 0.67
        self.aim_vertical_mix = 1.31
        self.aim_horizontal_offset = 0.0
        self.aim_vertical_offset = 0.8
        self.aim_center_x = 0.0
        self.aim_center_z = GOAL_HEIGHT * 0.50
        self.aim_amplitude_x = self.goal_half_width + 0.48
        self.aim_amplitude_z = (GOAL_HEIGHT + 0.40) * 0.50
        self.aim_speed_pulse = 0.0


        self.goalkeeper_x = 0.0
        self.goalkeeper_target_x = 0.0
        self.goalkeeper_reaction = 0.0
        self.goalkeeper_dive_start_x = 0.0
        self.goalkeeper_dive_progress = 0.0
        self.goalkeeper_dive_sign = 1.0
        self.goalkeeper_dive_amount = 0.0
        self.goalkeeper_is_diving = False
        self.goalkeeper_should_dive = False
        self.goalkeeper_high_reach = 0.0
        self.goalkeeper_dive_age = 0.0
        self.goalkeeper_dive_speed = 2.2
        self.goalkeeper_read_error = 0.0
        self.goalkeeper_vx = 0.0
        self.shot_distance_factor = 0.5


        self.attempts = 0
        self.goals = 0
        self.saves = 0
        self.misses = 0
        self.result_text = ""
        self.result_color = (1.0, 1.0, 1.0, 1.0)
        self.outcome_registered = False
        self.last_goal_line_point: Optional[tuple[float, float]] = None


        self.ripples: list[NetRipple] = []
        self._crowd_specs: Optional[list[tuple[float, float, float, int]]] = None
        self._crowd_mesh_cache_key: Optional[tuple[float, float, float, float]] = None
        self._crowd_mesh_cache: list[
            tuple[tuple[float, float, float, float], list[float], list[int], int]
        ] = []
        self._stand_mesh_cache_key: Optional[
            tuple[float, float, float, float]
        ] = None
        self._stand_mesh_cache: list[
            tuple[tuple[float, float, float, float], list[float], list[int]]
        ] = []
        self._stand_mesh_builders: Optional[
            dict[
                tuple[str, tuple[float, float, float, float]],
                tuple[list[float], list[int]],
            ]
        ] = None
        self._stand_cache_section = ""
        self._static_layer_key: Optional[tuple[float, float, float, float]] = None
        self._static_fbo: Optional[Fbo] = None
        self._fbo_disabled = False
        self._text_texture_cache: dict[
            tuple[str, int, tuple[float, float, float, float]], object
        ] = {}
        self.crowd_total = 0
        self.crowd_visible = 0


        self._menu = None
        self._match_notice = None
        self._exit_popup = None
        self._new_game_popup = None
        self._career_started = False
        self._profile_return = "offers"
        self.career = CareerMode(autoload=False)
        self.view = "splash"
        self.shot_context = "career"
        self.ui_buttons: list[tuple[float, float, float, float, str, object]] = []
        self.table_page = 0
        self.world_page = 0
        self.training_shots_left = 0
        self.training_goals = 0
        self.training_completed = False
        self.training_stamina_before = self.career.stamina
        self.training_gain = 0.0
        self.training_summary = ""
        self.match_minute = 0.0
        self.match_stoppage = 1
        self.match_first_stoppage = 1
        self.match_half = 1
        self.match_halftime = False
        self.scoreboard_flash_until = 0.0
        self._match_shot_goal_counted = False
        self.match_chance_minutes: list[int] = []
        self.match_chance_index = 0
        self.match_easy_chance_index = -1
        self.current_chance_difficulty = "standard"
        self.match_player_goals = 0
        self.match_player_misses = 0
        self.match_home_score = 0
        self.match_away_score = 0
        self.match_goal_events: list[tuple[int, str]] = []
        self.match_goal_event_index = 0
        self.match_home: Optional[CareerClub] = None
        self.match_away: Optional[CareerClub] = None
        self.match_is_international = False
        self.match_is_cup = False
        self.match_competition = "league"
        self.match_finished = False
        self.match_summary = ""
        self.awaiting_chance = False
        self.shot_time_limit = 0.0
        self.shot_time_left = 0.0
        self.current_aim_speed = 2.20
        self._chance_sound = None
        self._chance_sound_attempted = False
        self._ai_goal_sound = None
        self._ai_goal_sound_attempted = False
        self._goal_crowd_sound = None
        self._goal_crowd_sound_attempted = False
        self._club_badge_textures: dict[str, object] = {}
        self._club_badge_loading: set[str] = set()
        self._choose_shot_origin()


        Window.bind(on_key_down=self._on_key_down)
        self.bind(pos=lambda *_: self.draw(), size=lambda *_: self.draw())
        # Zero significa uma chamada por frame gráfico. A física continua com
        # o seu passo próprio e não fica dependente da taxa do ecrã.
        Clock.schedule_interval(self.update, 0.0)


    # ------------------------------------------------------------------
    # Geometria e projeção 2.5D
    # ------------------------------------------------------------------
    @property
    def goal_half_width(self) -> float:
        return GOAL_WIDTH / 2.0


    @staticmethod
    def _veil_profile(amount: float) -> tuple[float, float]:
        """Perfil do teto curto e da queda do véu, medido pela malha."""
        distance = clamp(amount, 0.0, 1.0) * VEIL_PATH_LENGTH
        if distance <= VEIL_TOP_DEPTH:
            return -distance, GOAL_HEIGHT


        if distance <= VEIL_TOP_DEPTH + VEIL_SLOPE_LENGTH:
            slope_amount = (distance - VEIL_TOP_DEPTH) / VEIL_SLOPE_LENGTH
            return (
                -VEIL_TOP_DEPTH
                - (VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH) * slope_amount,
                GOAL_HEIGHT * (1.0 - slope_amount)
                - VEIL_SAG * math.sin(math.pi * slope_amount),
            )


        # A malha não termina esticada no primeiro contacto com o relvado:
        # sobra uma faixa pousada no chão, como tecido com folga.
        ground_amount = distance - VEIL_TOP_DEPTH - VEIL_SLOPE_LENGTH
        return -VEIL_TOUCH_DEPTH - ground_amount, 0.0


    @staticmethod
    def _veil_height_at_y(y: float) -> float:
        """Altura superior da rede num corte lateral da baliza."""
        depth = clamp(-y, 0.0, GOAL_DEPTH)
        if depth <= VEIL_TOP_DEPTH:
            return GOAL_HEIGHT
        if depth >= VEIL_TOUCH_DEPTH:
            return 0.0
        slope_amount = (depth - VEIL_TOP_DEPTH) / (
            VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH
        )
        return (
            GOAL_HEIGHT * (1.0 - slope_amount)
            - VEIL_SAG * math.sin(math.pi * slope_amount)
        )


    @classmethod
    def _veil_amount_at_y(cls, y: float) -> float:
        """Converte profundidade física na coordenada contínua da malha."""
        depth = clamp(-y, 0.0, GOAL_DEPTH)
        if depth <= VEIL_TOP_DEPTH:
            distance = depth
        elif depth >= VEIL_TOUCH_DEPTH:
            distance = (
                VEIL_TOP_DEPTH
                + VEIL_SLOPE_LENGTH
                + depth
                - VEIL_TOUCH_DEPTH
            )
        else:
            slope_amount = (depth - VEIL_TOP_DEPTH) / (
                VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH
            )
            distance = VEIL_TOP_DEPTH + slope_amount * VEIL_SLOPE_LENGTH
        return clamp(distance / VEIL_PATH_LENGTH, 0.0, 1.0)


    @classmethod
    def _veil_depth_at_height(cls, z: float) -> float:
        """Profundidade onde uma fiada horizontal encontra o véu curvo."""
        if z >= GOAL_HEIGHT:
            return VEIL_TOP_DEPTH
        if z <= 0.0:
            return VEIL_TOUCH_DEPTH


        low = VEIL_TOP_DEPTH
        high = VEIL_TOUCH_DEPTH
        for _ in range(26):
            middle = (low + high) * 0.5
            if cls._veil_height_at_y(-middle) > z:
                low = middle
            else:
                high = middle
        return (low + high) * 0.5


    def camera_values(self) -> tuple[float, float, float]:
        """Centro ótico e distância focal da câmara da bancada."""
        center_x = self.x + self.width * 0.50
        center_y = self.y + self.height * 0.52
        focal = self.height / (
            2.0 * math.tan(math.radians(CAMERA_VERTICAL_FOV) / 2.0)
        )
        return center_x, center_y, focal


    @staticmethod
    def camera_depth(x: float, y: float, z: float) -> float:
        relative = (
            x - CAMERA_POSITION[0],
            y - CAMERA_POSITION[1],
            z - CAMERA_POSITION[2],
        )
        return dot3(relative, CAMERA_FORWARD)


    def project(self, x: float, y: float, z: float) -> tuple[float, float]:
        """Projeção perspetiva vista da bancada central elevada."""
        center_x, center_y, focal = self.camera_values()
        relative = (
            x - CAMERA_POSITION[0],
            y - CAMERA_POSITION[1],
            z - CAMERA_POSITION[2],
        )
        depth = max(0.05, dot3(relative, CAMERA_FORWARD))
        return (
            center_x + focal * dot3(relative, CAMERA_RIGHT) / depth,
            center_y + focal * dot3(relative, CAMERA_UP) / depth,
        )


    def unproject_goal(self, sx: float, sy: float) -> tuple[float, float]:
        """Converte um toque no ecrã num ponto do plano frontal da baliza."""
        center_x, center_y, focal = self.camera_values()
        horizontal = (sx - center_x) / focal
        vertical = (sy - center_y) / focal
        ray = (
            CAMERA_FORWARD[0]
            + CAMERA_RIGHT[0] * horizontal
            + CAMERA_UP[0] * vertical,
            CAMERA_FORWARD[1]
            + CAMERA_RIGHT[1] * horizontal
            + CAMERA_UP[1] * vertical,
            CAMERA_FORWARD[2]
            + CAMERA_RIGHT[2] * horizontal
            + CAMERA_UP[2] * vertical,
        )
        if abs(ray[1]) < 1e-8:
            return 0.0, 0.0
        distance = -CAMERA_POSITION[1] / ray[1]
        return (
            CAMERA_POSITION[0] + ray[0] * distance,
            CAMERA_POSITION[2] + ray[2] * distance,
        )


    def pixels_per_meter(self, x: float, y: float, z: float) -> float:
        """Escala aparente num ponto, usada para a bola, alvo e sombras."""
        _, _, focal = self.camera_values()
        return focal / max(0.05, self.camera_depth(x, y, z))


    @staticmethod
    def _is_generated_club(club_name: str) -> bool:
        return club_name.endswith(" FC") and "-" in club_name


    def _request_club_badge(self, club_name: str) -> None:
        """Official badge downloads are disabled in shipped builds.

        The renderer deliberately falls back to generated geometric markers so the
        app ships no third-party club logos or remote media.
        """
        return


    def _download_club_badge(self, club_name: str, cache_path: Path) -> None:
        try:
            search_name = (
                f"{club_name} national football team"
                if club_name in WORLD_COUNTRIES
                else f"{club_name} football club"
            )
            query = urllib.parse.urlencode({
                "action": "query",
                "generator": "search",
                "gsrsearch": search_name,
                "gsrnamespace": 0,
                "gsrlimit": 1,
                "prop": "pageimages",
                "piprop": "thumbnail",
                "pithumbsize": 160,
                "format": "json",
                "formatversion": 2,
            })
            request = urllib.request.Request(
                f"https://en.wikipedia.org/w/api.php?{query}",
                headers={"User-Agent": "StrikerCareerGame/1.0"},
            )
            with urllib.request.urlopen(request, timeout=7.0) as response:
                payload = json.loads(response.read().decode("utf-8"))
            pages = payload.get("query", {}).get("pages", [])
            image_url = (
                pages[0].get("thumbnail", {}).get("source") if pages else None
            )
            if not image_url:
                raise ValueError("badge not found")
            image_request = urllib.request.Request(
                str(image_url),
                headers={"User-Agent": "StrikerCareerGame/1.0"},
            )
            with urllib.request.urlopen(image_request, timeout=8.0) as response:
                image_data = response.read(1_500_001)
            if not 256 <= len(image_data) <= 1_500_000:
                raise ValueError("invalid badge size")
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = cache_path.with_suffix(".tmp")
            temporary_path.write_bytes(image_data)
            temporary_path.replace(cache_path)
            Clock.schedule_once(
                lambda _dt: self._load_club_badge(club_name, cache_path), 0
            )
        except Exception:
            Clock.schedule_once(
                lambda _dt: self._club_badge_loading.discard(club_name), 0
            )


    def _load_club_badge(self, club_name: str, cache_path: Path) -> None:
        try:
            source_texture = CoreImage(str(cache_path)).texture
            self._club_badge_textures[club_name] = self._clean_badge_texture(
                source_texture
            )
        except Exception:
            pass
        self._club_badge_loading.discard(club_name)


    @staticmethod
    def _clean_badge_texture(source_texture):
        """Remove o fundo ligado às margens e recorta o emblema.


        Algumas miniaturas chegam como RGB sobre um quadrado branco, apesar de
        o símbolo original ser recortado. O algoritmo só torna transparentes
        píxeis semelhantes ao fundo que estejam ligados à borda da imagem; por
        isso, o branco que faça parte do interior do emblema é preservado.
        """
        width = int(getattr(source_texture, "width", 0))
        height = int(getattr(source_texture, "height", 0))
        raw = bytes(getattr(source_texture, "pixels", b""))
        if width < 2 or height < 2 or len(raw) != width * height * 4:
            return source_texture


        pixels = bytearray(raw)
        border_indices = []
        for x in range(width):
            border_indices.extend((x, (height - 1) * width + x))
        for y in range(1, height - 1):
            border_indices.extend((y * width, y * width + width - 1))


        # A cor dominante da moldura é o fundo mais provável.
        buckets: dict[tuple[int, int, int], list[int]] = {}
        for index in border_indices:
            offset = index * 4
            if pixels[offset + 3] < 20:
                continue
            key = (
                pixels[offset] // 16,
                pixels[offset + 1] // 16,
                pixels[offset + 2] // 16,
            )
            buckets.setdefault(key, []).append(index)


        if buckets:
            dominant = max(buckets.values(), key=len)
            coverage = len(dominant) / max(1, len(border_indices))
            if coverage >= 0.42:
                red = sum(pixels[index * 4] for index in dominant) / len(dominant)
                green = sum(pixels[index * 4 + 1] for index in dominant) / len(dominant)
                blue = sum(pixels[index * 4 + 2] for index in dominant) / len(dominant)
                visited = bytearray(width * height)
                pending = list(dict.fromkeys(border_indices))
                while pending:
                    index = pending.pop()
                    if visited[index]:
                        continue
                    visited[index] = 1
                    offset = index * 4
                    distance = (
                        abs(pixels[offset] - red)
                        + abs(pixels[offset + 1] - green)
                        + abs(pixels[offset + 2] - blue)
                    )
                    if pixels[offset + 3] < 20 or distance <= 58:
                        pixels[offset + 3] = 0
                        x = index % width
                        y = index // width
                        if x:
                            pending.append(index - 1)
                        if x + 1 < width:
                            pending.append(index + 1)
                        if y:
                            pending.append(index - width)
                        if y + 1 < height:
                            pending.append(index + width)


        visible = [
            index for index in range(width * height) if pixels[index * 4 + 3] >= 20
        ]
        if not visible:
            return source_texture
        min_x = max(0, min(index % width for index in visible) - 2)
        max_x = min(width - 1, max(index % width for index in visible) + 2)
        min_y = max(0, min(index // width for index in visible) - 2)
        max_y = min(height - 1, max(index // width for index in visible) + 2)
        crop_width = max_x - min_x + 1
        crop_height = max_y - min_y + 1
        if crop_width == width and crop_height == height and not buckets:
            return source_texture


        cropped = bytearray(crop_width * crop_height * 4)
        for row in range(crop_height):
            source_start = ((min_y + row) * width + min_x) * 4
            source_end = source_start + crop_width * 4
            target_start = row * crop_width * 4
            cropped[target_start:target_start + crop_width * 4] = pixels[
                source_start:source_end
            ]
        cleaned = Texture.create(size=(crop_width, crop_height), colorfmt="rgba")
        cleaned.blit_buffer(bytes(cropped), colorfmt="rgba", bufferfmt="ubyte")
        return cleaned


    def _draw_club_badge(
        self, club_name: str, center_x: float, center_y: float, size: float
    ) -> None:
        texture = self._club_badge_textures.get(club_name)
        if texture is not None:
            texture_width = max(1.0, float(getattr(texture, "width", size)))
            texture_height = max(1.0, float(getattr(texture, "height", size)))
            scale = min(size / texture_width, size / texture_height)
            width = texture_width * scale
            height = texture_height * scale
            Color(1.0, 1.0, 1.0, 1.0)
            Rectangle(
                texture=texture,
                pos=(center_x - width / 2, center_y - height / 2),
                size=(width, height),
            )
            return
        shirt, _shorts, _socks, trim = club_kit(club_name)
        shield_width = size * 0.72
        shield_height = size * 0.82
        Color(*shirt)
        Rectangle(
            pos=(center_x - shield_width / 2, center_y - shield_height * 0.32),
            size=(shield_width, shield_height * 0.64),
        )
        Triangle(points=[
            center_x - shield_width / 2,
            center_y - shield_height * 0.32,
            center_x + shield_width / 2,
            center_y - shield_height * 0.32,
            center_x,
            center_y - shield_height * 0.58,
        ])
        Color(*trim)
        Line(
            rectangle=(
                center_x - shield_width / 2,
                center_y - shield_height * 0.32,
                shield_width,
                shield_height * 0.64,
            ),
            width=1.2,
        )
        initials = "".join(word[0] for word in club_name.split()[:3]).upper()
        self._draw_text(
            initials,
            center_x,
            center_y,
            max(7, int(size * 0.22)),
            trim,
            "center",
            max_width=shield_width - 4,
        )


    def _match_outfield_kits(self):
        player_name = "Portugal" if self.match_is_international else self.career.club_name
        opponent_name = "Opponent"
        if self.match_home and self.match_away:
            opponent_name = (
                self.match_away.name
                if self.match_home.name == player_name
                else self.match_home.name
            )
        player_kit = club_kit(player_name)
        opponent_kit = club_kit(opponent_name)
        colour_distance = sum(
            abs(player_kit[0][index] - opponent_kit[0][index])
            for index in range(3)
        )
        if colour_distance < 0.42:
            opponent_kit = (
                opponent_kit[3],
                opponent_kit[1],
                opponent_kit[2],
                opponent_kit[0],
            )
        return player_kit, opponent_kit


    def _goalkeeper_kit(self):
        player_kit, opponent_kit = self._match_outfield_kits()
        candidates = (
            ((0.42, 0.88, 0.16, 1.0), (0.10, 0.22, 0.08, 1.0)),
            ((0.62, 0.22, 0.86, 1.0), (0.18, 0.06, 0.28, 1.0)),
            ((0.10, 0.78, 0.86, 1.0), (0.04, 0.20, 0.25, 1.0)),
            ((0.96, 0.46, 0.10, 1.0), (0.30, 0.10, 0.03, 1.0)),
        )
        outfield_colours = (player_kit[0], opponent_kit[0])
        return max(
            candidates,
            key=lambda candidate: min(
                sum(abs(candidate[0][index] - colour[index]) for index in range(3))
                for colour in outfield_colours
            ),
        )


    # ------------------------------------------------------------------
    # Ciclo de jogo
    # ------------------------------------------------------------------
    def start_career_match(self) -> None:
        """Cria um jogo completo com relógio e oportunidades interativas."""
        if not self.career.trained_this_week:
            self.career.message = 'Complete this week’s training to unlock Play.'
            self.view = 'hub'
            self.draw()
            return
        self.match_is_international = self.career.called_up
        self.match_is_cup = False
        self.match_competition = "international" if self.match_is_international else "league"
        if self.match_is_international:
            opponents = (
                "Spain", "France", "Germany", "Italy", "Netherlands",
                "Belgium", "Croatia", "Denmark", "Switzerland", "Poland",
            )
            opponent = self.career.rng.choice(opponents)
            self.match_home = CareerClub("Portugal", "Portugal", "National Team", 1, 89)
            self.match_away = CareerClub(opponent, opponent, "National Team", 1, 84)
            self.career.called_up = False
        else:
            scheduled = self.career.next_match()
            if scheduled is None:
                self.career.message = 'The season has ended. Talk to your agent or start the new season.'
                self.view = "hub"
                return
            self.match_competition, self.match_home, self.match_away = scheduled
            self.match_is_cup = self.match_competition == "cup"


        self._request_club_badge(self.match_home.name)
        self._request_club_badge(self.match_away.name)
        self.match_minute = 0.0
        self.match_stoppage = self.career.rng.randint(1, 8)
        self.match_first_stoppage = self.career.rng.randint(1, 4)
        self.match_half = 1
        self.match_halftime = False
        self.scoreboard_flash_until = 0.0
        player_home = self.match_is_international or self.match_home.name == self.career.club_name
        opponent = self.match_away if player_home else self.match_home
        chance_profile = self.career.opponent_chance_profile(opponent)
        chance_total = self.career.chance_count(opponent)
        final_minute = 90 + self.match_first_stoppage + self.match_stoppage
        self.match_chance_minutes = sorted(
            self.career.rng.sample(range(3, final_minute), min(chance_total, final_minute - 3))
        )
        self.match_chance_index = 0
        self.match_easy_chance_index = self.career.rng.randrange(len(self.match_chance_minutes)) if self.match_chance_minutes and self.career.rng.random() < chance_profile.clear_chance_probability else -1
        self.current_chance_difficulty = "standard"
        self.match_player_goals = 0
        self.match_player_misses = 0
        self.match_home_score = 0
        self.match_away_score = 0
        self.match_goal_event_index = 0
        if self.match_is_international:
            rating_difference = (self.match_home.rating - self.match_away.rating) / 18.0
            home_mean = clamp(1.42 + rating_difference, 0.30, 3.20)
            away_mean = clamp(1.08 - rating_difference, 0.22, 3.00)
            home_ai = poisson_goal(self.career.rng, home_mean * 0.58)
            away_ai = poisson_goal(self.career.rng, away_mean)
        elif self.match_is_cup:
            rating_difference = (self.match_home.rating - self.match_away.rating) / 18.0
            home_mean = clamp(1.42 + rating_difference, 0.24, 3.35)
            away_mean = clamp(1.08 - rating_difference, 0.20, 3.10)
            player_home = self.match_home.name == self.career.club_name
            if player_home:
                home_mean *= 0.58
            else:
                away_mean *= 0.58
            home_ai = poisson_goal(self.career.rng, home_mean)
            away_ai = poisson_goal(self.career.rng, away_mean)
        else:
            player_home = bool(
                self.match_home and self.match_home.name == self.career.club_name
            )
            home_mean, away_mean = self.career.fixture_goal_means(
                self.match_home, self.match_away
            )
            # A parte ofensiva da equipa do jogador é reduzida porque os seus
            # próprios remates são acrescentados interativamente. O adversário
            # usa o valor completo, fortemente influenciado pela classificação.
            if player_home:
                home_mean *= 0.58
            else:
                away_mean *= 0.58
            home_ai = poisson_goal(self.career.rng, home_mean)
            away_ai = poisson_goal(self.career.rng, away_mean)
        goal_events = [
            (self.career.rng.randint(2, final_minute), "home")
            for _ in range(home_ai)
        ] + [
            (self.career.rng.randint(2, final_minute), "away")
            for _ in range(away_ai)
        ]
        self.match_goal_events = sorted(goal_events, key=lambda event: event[0])
        self.match_finished = False
        self.match_summary = ""
        self.awaiting_chance = False
        self.view = "match"
        self.state = self.STATE_AIMING


    @property
    def match_clock_text(self) -> str:
        # Timeline includes both periods of added time; the second-half clock
        # resumes at 45:00 without counting first-half added time twice.
        minute = self.match_minute - (self.match_first_stoppage if self.match_half == 2 else 0)
        seconds = max(0, int(minute * 60 + 1e-6))
        whole, second = divmod(seconds, 60)
        boundary = 45 if self.match_half == 1 else 90
        return (f"{boundary}+{whole - boundary:02d}:{second:02d}"
                if whole >= boundary else f"{whole:02d}:{second:02d}")

    def _flash_scoreboard(self) -> None:
        self.scoreboard_flash_until = self.elapsed + 1.0

    def _record_player_match_goal(self) -> None:
        if self._match_shot_goal_counted:
            return
        self._match_shot_goal_counted = True
        self.match_player_goals += 1
        if self.match_home and self.match_home.name in (self.career.club_name, "Portugal"):
            self.match_home_score += 1
        else:
            self.match_away_score += 1
        self._flash_scoreboard()

    def _resume_second_half(self) -> None:
        if not self.match_halftime or self.match_finished:
            return
        self.match_halftime = False
        self.match_half = 2
        self.draw()

    def _update_career_match(self, dt: float) -> None:
        if self.match_finished or self.awaiting_chance or self.match_halftime:
            return
        final_minute = 90 + self.match_first_stoppage + self.match_stoppage
        boundary = 45 + self.match_first_stoppage if self.match_half == 1 else final_minute
        target = min(boundary, self.match_minute + max(0.0, dt) * 3.0)
        if self.match_chance_index < len(self.match_chance_minutes):
            target = min(target, float(self.match_chance_minutes[self.match_chance_index]))
        self.match_minute = target
        while self.match_goal_event_index < len(self.match_goal_events):
            event_minute, side = self.match_goal_events[self.match_goal_event_index]
            if event_minute > self.match_minute:
                break
            if side == "home":
                self.match_home_score += 1
            else:
                self.match_away_score += 1
            self._flash_scoreboard()
            self._play_ai_goal_sound()
            self.match_goal_event_index += 1
        if self.match_chance_index < len(self.match_chance_minutes):
            if self.match_minute >= self.match_chance_minutes[self.match_chance_index]:
                self.awaiting_chance = True
                self._play_chance_sound()
                return
        if self.match_minute >= boundary:
            if self.match_half == 1:
                self.match_halftime = True
            else:
                self._finish_career_match()


    def _finish_career_match(self) -> None:
        if self.match_finished or self.match_home is None or self.match_away is None:
            return
        score = self.career.finish_match(
            self.match_home,
            self.match_away,
            self.match_player_goals,
            self.match_player_misses,
            self.match_is_international,
            (self.match_home_score, self.match_away_score),
            self.match_competition,
        )
        self.match_finished = True
        self.awaiting_chance = False
        self.match_summary = f"FINAL  {self.career.last_result}"


    def _begin_pending_chance(self) -> None:
        if not self.awaiting_chance or self.match_finished or self.match_halftime:
            return
        self.awaiting_chance = False
        self.current_chance_difficulty = "easy" if self.match_chance_index == self.match_easy_chance_index else "hard"
        self.match_chance_index += 1
        self.shot_context = "match"
        self.view = "shot"
        self.shot_time_limit, self.current_aim_speed = self.career.difficulty_profile(
            self.match_is_international
        )
        if self.match_is_cup:
            self.shot_time_limit = max(3.0, self.shot_time_limit - 0.20)
            self.current_aim_speed += 0.10
        if self.current_chance_difficulty == "hard":
            self.shot_time_limit = max(2.7, self.shot_time_limit * 0.60)
            self.current_aim_speed *= 1.55
        self.shot_time_left = self.shot_time_limit
        self._prepare_next_shot()


    def _play_chance_sound(self) -> None:
        """Toca Do-Re-Mi-Fa-Sol; falhas de áudio nunca bloqueiam o jogo."""
        try:
            if not self._chance_sound_attempted:
                self._chance_sound_attempted = True
                sound_path = Path(__file__).resolve().parent / "striker_chance.wav"
                if not sound_path.exists():
                    sample_rate = 22050
                    samples: list[int] = []
                    for frequency in (261.63, 293.66, 329.63, 349.23, 392.00):
                        tone_length = int(sample_rate * 0.105)
                        for index in range(tone_length):
                            envelope = min(1.0, index / 100.0) * min(
                                1.0, (tone_length - index) / 130.0
                            )
                            samples.append(
                                int(
                                    10500
                                    * envelope
                                    * math.sin(2.0 * math.pi * frequency * index / sample_rate)
                                )
                            )
                        samples.extend([0] * int(sample_rate * 0.025))
                    with wave.open(str(sound_path), "wb") as sound_file:
                        sound_file.setnchannels(1)
                        sound_file.setsampwidth(2)
                        sound_file.setframerate(sample_rate)
                        sound_file.writeframes(
                            struct.pack("<" + "h" * len(samples), *samples)
                        )
                self._chance_sound = SoundLoader.load(str(sound_path))
            if self._chance_sound is not None:
                self._chance_sound.stop()
                self._chance_sound.play()
        except Exception:
            self._chance_sound = None


    def _play_ai_goal_sound(self) -> None:
        """Beep curto para cada golo que não é marcado pelo jogador."""
        try:
            if not self._ai_goal_sound_attempted:
                self._ai_goal_sound_attempted = True
                sound_path = Path(__file__).resolve().parent / "striker_ai_goal.wav"
                if not sound_path.exists():
                    sample_rate = 22050
                    samples: list[int] = []
                    for frequency, duration in ((740.0, 0.12), (980.0, 0.16)):
                        count = int(sample_rate * duration)
                        for index in range(count):
                            envelope = min(1.0, index / 80.0) * min(
                                1.0, (count - index) / 120.0
                            )
                            samples.append(int(12500 * envelope * math.sin(
                                2.0 * math.pi * frequency * index / sample_rate
                            )))
                        samples.extend([0] * int(sample_rate * 0.035))
                    with wave.open(str(sound_path), "wb") as sound_file:
                        sound_file.setnchannels(1)
                        sound_file.setsampwidth(2)
                        sound_file.setframerate(sample_rate)
                        sound_file.writeframes(struct.pack("<" + "h" * len(samples), *samples))
                self._ai_goal_sound = SoundLoader.load(str(sound_path))
            if self._ai_goal_sound is not None:
                self._ai_goal_sound.stop()
                self._ai_goal_sound.play()
        except Exception:
            self._ai_goal_sound = None


    def _play_goal_crowd_sound(self) -> None:
        """Celebração de bancada sintetizada, sem ficheiros externos."""
        try:
            if not self._goal_crowd_sound_attempted:
                self._goal_crowd_sound_attempted = True
                sound_path = Path(__file__).resolve().parent / "striker_goal_crowd.wav"
                if not sound_path.exists():
                    sample_rate = 22050
                    duration = 2.35
                    count = int(sample_rate * duration)
                    rng = random.Random(92831)
                    samples: list[int] = []
                    smooth = 0.0
                    for index in range(count):
                        t = index / sample_rate
                        raw = rng.uniform(-1.0, 1.0)
                        smooth = smooth * 0.86 + raw * 0.14
                        voices = (
                            0.34 * math.sin(2.0 * math.pi * 176.0 * t + 0.3)
                            + 0.25 * math.sin(2.0 * math.pi * 223.0 * t + 1.7)
                            + 0.18 * math.sin(2.0 * math.pi * 287.0 * t + 2.4)
                        )
                        attack = min(1.0, t / 0.11)
                        decay = max(0.0, 1.0 - max(0.0, t - 0.55) / 2.0)
                        pulse = 0.82 + 0.18 * math.sin(2.0 * math.pi * 3.2 * t)
                        value = (smooth * 0.78 + voices) * attack * decay * pulse
                        samples.append(int(clamp(value, -1.0, 1.0) * 14500))
                    with wave.open(str(sound_path), "wb") as sound_file:
                        sound_file.setnchannels(1)
                        sound_file.setsampwidth(2)
                        sound_file.setframerate(sample_rate)
                        sound_file.writeframes(struct.pack("<" + "h" * len(samples), *samples))
                self._goal_crowd_sound = SoundLoader.load(str(sound_path))
            if self._goal_crowd_sound is not None:
                self._goal_crowd_sound.stop()
                self._goal_crowd_sound.play()
        except Exception:
            self._goal_crowd_sound = None


    def start_training(self) -> None:
        if self.view == "shot" and self.shot_context == "training":
            return
        if not self.career.begin_training():
            self.view = "training"
            self.draw()
            return
        self.training_completed = False
        self.training_stamina_before = self.career.stamina
        self.training_gain = 0.0
        self.training_summary = ""
        self.training_shots_left = 3 - self.career.training_shots_taken
        self.training_goals = self.career.training_session_goals
        if self.training_shots_left == 0:
            self.training_gain = self.career.complete_training(self.training_goals)
            self.training_completed = self.career.trained_this_week
            self.view = 'training'
            self.draw()
            return
        self.shot_context = "training"
        self.view = "shot"
        self.reset_statistics()


    def _advance_after_shot(self) -> None:
        scored = self.result_text == "GOAL!"
        if self.shot_context == "training":
            if not self.career.record_training_shot(scored):
                self.training_completed = False
                self.view = 'training'
                self.shot_context = 'career'
                return
            self.training_goals = self.career.training_session_goals
            self.training_shots_left = 3 - self.career.training_shots_taken
            if self.training_shots_left <= 0:
                self.training_gain = self.career.complete_training(self.training_goals)
                self.training_completed = self.career.trained_this_week
                self.training_summary = (
                    f"{self.training_goals}/3 goals  |  "
                    f"energy +{self.training_gain:.2f}"
                )
                self.view = "training"
                self.shot_context = "career"
                self._prepare_next_shot()
            else:
                self._prepare_next_shot()
            return


        if self.shot_context == "match":
            if scored:
                self._record_player_match_goal()
            else:
                self.match_player_misses += 1
            self.view = "match"
            self.shot_context = "career"
            self._prepare_next_shot()
            return


        self._prepare_next_shot()


    def update(self, dt: float) -> None:
        # Não deita fora tempo quando o desenho demora mais num telemóvel.
        # O limite evita saltos gigantes ao regressar de segundo plano; a
        # física continua dividida em passos de 1/60 s para não atravessar
        # jogadores, postes ou redes entre duas atualizações.
        if self._exit_popup is not None:
            return
        frame_dt = clamp(dt, 0.0, 0.12)
        self.elapsed += frame_dt
        self.state_age += frame_dt


        if self.view == "match":
            self._update_career_match(frame_dt)
            self.draw()
            return
        if self.view != "shot":
            self.draw()
            return


        if self.state == self.STATE_AIMING:
            self.player_kick_progress = 0.0
            if self.shot_context == "match":
                self.shot_time_left = max(0.0, self.shot_time_left - frame_dt)
                if self.shot_time_left <= 0.0:
                    self._expire_shot()
        else:
            self.player_kick_progress = clamp(
                self.player_kick_progress + frame_dt * 3.4, 0.0, 1.0
            )


        if self.state == self.STATE_AIMING:
            self._update_aim(frame_dt)
            self._update_goalkeeper_idle(frame_dt)
        else:
            remaining = frame_dt
            while remaining > 1e-8:
                physics_dt = min(PHYSICS_STEP, remaining)
                self._update_goalkeeper_shot(physics_dt)
                if self.ball.active:
                    self._update_ball(physics_dt)
                remaining -= physics_dt


        for ripple in self.ripples:
            ripple.age += frame_dt
        self.ripples = [
            ripple for ripple in self.ripples
            if ripple.age < NET_RIPPLE_DURATION
        ]


        if self.state == self.STATE_RESULT and self.state_age > 2.55:
            self._advance_after_shot()


        # O callback já ocorre uma vez por frame. Desenhar sempre evita o
        # padrão 60/30/60 fps causado por arredondamentos do relógio.
        self.draw()


    def _randomize_aim_pattern(self) -> None:
        rng = self.career.rng
        self.aim_phase = rng.uniform(0.0, math.tau)
        self.aim_direction = rng.choice((-1.0, 1.0))
        self.aim_horizontal_mix = rng.uniform(1.35, 2.25)
        self.aim_vertical_ratio = rng.uniform(0.43, 1.17)
        self.aim_vertical_mix = rng.uniform(1.28, 2.05)
        self.aim_horizontal_offset = rng.uniform(0.0, math.tau)
        self.aim_vertical_offset = rng.uniform(0.0, math.tau)
        self.aim_center_x = rng.uniform(-0.34, 0.34)
        self.aim_center_z = rng.uniform(0.94, 1.38)
        self.aim_amplitude_x = self.goal_half_width + rng.uniform(0.30, 0.82)
        self.aim_amplitude_z = rng.uniform(1.22, 1.58)
        self.aim_speed_pulse = rng.uniform(0.0, math.tau)
        self._apply_aim_pattern()


    def _apply_aim_pattern(self) -> None:
        phase = self.aim_phase
        horizontal = (
            0.62 * math.sin(phase + self.aim_horizontal_offset)
            + 0.26 * math.sin(
                phase * self.aim_horizontal_mix + self.aim_vertical_offset
            )
            + 0.12 * math.cos(phase * 0.37 - self.aim_vertical_offset)
        )
        vertical = (
            0.58 * math.sin(
                phase * self.aim_vertical_ratio + self.aim_vertical_offset
            )
            + 0.28 * math.sin(
                phase * self.aim_vertical_mix - self.aim_horizontal_offset
            )
            + 0.14 * math.cos(phase * 0.51 + self.aim_horizontal_offset)
        )
        self.aim_x = self.aim_center_x + horizontal * self.aim_amplitude_x
        self.aim_z = self.aim_center_z + vertical * self.aim_amplitude_z


    def _update_aim(self, dt: float) -> None:
        self.power_phase += dt * 2.15
        self.power = 0.58 + 0.42 * (0.5 + 0.5 * math.sin(self.power_phase))


        if self.auto_aim:
            aim_speed = (
                self.current_aim_speed
                if self.shot_context == "match"
                else 2.20
            )
            pulse = 0.82 + 0.30 * (
                0.5 + 0.5 * math.sin(self.aim_phase * 0.61 + self.aim_speed_pulse)
            )
            self.aim_phase += dt * aim_speed * self.aim_direction * pulse
            self._apply_aim_pattern()


    def _choose_shot_origin(self) -> None:
        if self.shot_context == "match" and self.current_chance_difficulty in ("easy", "hard"):
            rng = self.career.rng
            easy = self.current_chance_difficulty == "easy"
            self.one_on_one = easy
            self.shot_type = "kick"
            self.last_origin_index = -4 if easy else -5
            if easy:
                self.shot_type = rng.choices(("kick", "penalty", "header"), weights=(70, 15, 15), k=1)[0]
                self.shot_origin_x = rng.uniform(-1.8, 1.8)
                self.shot_origin_y = rng.uniform(8.0, 11.0)
                if self.shot_type == "penalty":
                    self.shot_origin_x, self.shot_origin_y = PENALTY_ORIGIN
                elif self.shot_type == "header":
                    self.one_on_one = False
                    self.shot_origin_y = rng.uniform(4.3, 5.1)
            else:
                self.shot_origin_x = rng.choice((-1, 1)) * rng.uniform(4.5, 8.0)
                self.shot_origin_y = rng.uniform(16.5, 21.0)
                # The fixed stadium camera can crop the near touchline on
                # narrower landscape displays. Mirror the same difficult
                # angle to the visible side rather than hiding the shooter.
                screen_x, _ = self.project(self.shot_origin_x, self.shot_origin_y, 0)
                if not self.x + self.width * 0.08 <= screen_x <= self.right - self.width * 0.08:
                    self.shot_origin_x = -abs(self.shot_origin_x)
                if rng.random() < 0.20:
                    self.shot_type = "free_kick"
            self.ball.reset(self.shot_origin_x, self.shot_origin_y, HEADER_BALL_HEIGHT if self.shot_type == "header" else None)
            self.player_kick_progress = 0.0
            self.last_field_collision = None
            self._generate_field_players()
            self.goalkeeper_x = self._aligned_goalkeeper_x()
            self.goalkeeper_vx = 0.0
            return
        # Os cabeceamentos surgem apenas dentro da pequena área. Nos restantes
        # lances, o rematador pode aparecer em qualquer zona ou ângulo útil.
        if self.shot_context == "match" and random.random() < 0.035:
            self.one_on_one = True
            self.shot_type = "penalty"
            self.last_origin_index = -2
            self.shot_origin_x = PENALTY_ORIGIN[0]
            self.shot_origin_y = PENALTY_ORIGIN[1]
            self.ball.reset(self.shot_origin_x, self.shot_origin_y)
            self.player_kick_progress = 0.0
            self.last_field_collision = None
            self._generate_field_players()
            self.goalkeeper_x = 0.0
            self.goalkeeper_vx = 0.0
            return
        # Livres diretos fora da área. A barreira é sempre de quatro jogadores
        # e fica aproximadamente à distância regulamentar de 9,15 m da bola.
        if self.shot_context == "match" and random.random() < 0.12:
            self.one_on_one = False
            self.shot_type = "free_kick"
            self.last_origin_index = -3
            base_x, base_y = random.choice(FREE_KICK_ORIGINS)
            self.shot_origin_x = base_x + random.uniform(-0.45, 0.45)
            self.shot_origin_y = base_y + random.uniform(-0.35, 0.35)
            self.ball.reset(self.shot_origin_x, self.shot_origin_y)
            self.player_kick_progress = 0.0
            self.last_field_collision = None
            self._generate_field_players()
            self.goalkeeper_x = self._aligned_goalkeeper_x()
            self.goalkeeper_vx = 0.0
            return


        self.one_on_one = random.random() < 0.18
        use_header = not self.one_on_one and random.random() < 0.28
        if use_header:
            offset = len(SHOT_ORIGINS)
            choices = [
                i for i in range(len(HEADER_ORIGINS))
                if offset + i != self.last_origin_index
            ]
            index = random.choice(choices)
            self.last_origin_index = offset + index
            base_x, base_y = HEADER_ORIGINS[index]
            self.shot_type = "header"
            jitter_x, jitter_y = 0.38, 0.24
        else:
            choices = [
                i for i in range(len(SHOT_ORIGINS))
                if i != self.last_origin_index
            ]
            index = random.choice(choices)
            self.last_origin_index = index
            base_x, base_y = SHOT_ORIGINS[index]
            self.shot_type = "kick"
            jitter_x, jitter_y = 0.65, 0.45


        self.shot_origin_x = base_x + random.uniform(-jitter_x, jitter_x)
        self.shot_origin_y = base_y + random.uniform(-jitter_y, jitter_y)
        start_z = HEADER_BALL_HEIGHT if self.shot_type == "header" else None
        self.ball.reset(self.shot_origin_x, self.shot_origin_y, start_z)
        self.player_kick_progress = 0.0
        self.last_field_collision = None
        self._generate_field_players()
        self.goalkeeper_x = self._aligned_goalkeeper_x()
        self.goalkeeper_vx = 0.0


    def _generate_field_players(self) -> None:
        """Cria equipas variáveis, com no máximo cinco jogadores de cada lado."""
        defenders = (
            (-8.7, 3.0),
            (-5.5, 5.1),
            (-1.9, 4.2),
            (1.9, 4.4),
            (5.5, 5.0),
            (8.7, 3.1),
            (-3.8, 8.4),
            (3.8, 8.6),
        )
        attackers = (
            (-8.0, 6.4),
            (-4.4, 6.9),
            (-1.2, 5.8),
            (2.7, 6.4),
            (6.5, 5.9),
            (0.4, 9.5),
        )


        if self.shot_type == "free_kick":
            distance = max(0.1, math.hypot(self.shot_origin_x, self.shot_origin_y))
            to_goal_x = -self.shot_origin_x / distance
            to_goal_y = -self.shot_origin_y / distance
            wall_center_x = self.shot_origin_x + to_goal_x * 9.15
            wall_center_y = self.shot_origin_y + to_goal_y * 9.15
            perp_x, perp_y = -to_goal_y, to_goal_x
            spacing = 0.72
            self.field_players = [
                FieldPlayer(
                    wall_center_x + perp_x * spacing * offset,
                    wall_center_y + perp_y * spacing * offset,
                    "defender",
                    random.uniform(0.0, math.tau),
                )
                for offset in (-1.5, -0.5, 0.5, 1.5)
            ]
            return


        if self.shot_context == "match" and self.current_chance_difficulty == "hard":
            # Keep normal physical defenders, including one marking the central
            # shooting lane. Corners and gaps remain available to a good shot.
            lane_y = self.shot_origin_y * 0.48
            lane_x = self.shot_origin_x * 0.48 + self.career.rng.uniform(-0.65, 0.65)
            positions = [(lane_x, lane_y)] + random.sample(list(defenders), 3)
            self.field_players = [FieldPlayer(x, y, "defender", random.uniform(0.0, math.tau)) for x, y in positions]
            return
        if self.one_on_one:
            # A genuine one-on-one contains only the shooter and goalkeeper.
            # _choose_shot_origin also forces these opportunities to be kicks.
            supporting_attacker_count = 0
            defender_count = 0
        else:
            # The shooter counts as one attacker. Smaller groups remain more
            # common, but every non-one-on-one play has at least as many
            # opponents as players from the shooter's team.
            supporting_attacker_count = random.choices(
                (0, 1, 2, 3, 4),
                weights=(42, 28, 17, 9, 4),
                k=1,
            )[0]
            attacking_team_count = 1 + supporting_attacker_count
            possible_defender_counts = tuple(range(attacking_team_count, 6))
            defender_count = random.choices(
                possible_defender_counts,
                weights=tuple(
                    max(1, 6 - 2 * offset)
                    for offset in range(len(possible_defender_counts))
                ),
                k=1,
            )[0]
        available_defenders = [
            position for position in defenders
            if math.hypot(
                position[0] - self.shot_origin_x,
                position[1] - self.shot_origin_y,
            ) >= 1.90
        ]
        available_attackers = [
            position for position in attackers
            if math.hypot(
                position[0] - self.shot_origin_x,
                position[1] - self.shot_origin_y,
            ) >= 1.90
        ]
        if len(available_defenders) < defender_count:
            available_defenders = list(defenders)
        if len(available_attackers) < supporting_attacker_count:
            available_attackers = list(attackers)
        team_selections = (
            (
                "defender",
                random.sample(
                    available_defenders,
                    min(defender_count, len(available_defenders)),
                ),
            ),
            (
                "attacker",
                random.sample(
                    available_attackers,
                    min(supporting_attacker_count, len(available_attackers)),
                ),
            ),
        )


        players: list[FieldPlayer] = []
        for team, formation in team_selections:
            for base_x, base_y in formation:
                x = base_x + random.uniform(-0.48, 0.48)
                y = base_y + random.uniform(-0.38, 0.38)
                # Deixa espaço para o gesto do rematador, sem abrir
                # artificialmente o corredor entre a bola e a baliza.
                players.append(
                    FieldPlayer(x, y, team, random.uniform(0.0, math.tau))
                )
        self.field_players = players


    def _aligned_goalkeeper_x(self) -> float:
        """Posição na linha entre a bola e o centro da baliza."""
        if self.ball.y > GOALKEEPER_Y + 0.05:
            aligned = self.ball.x * GOALKEEPER_Y / self.ball.y
        else:
            aligned = self.ball.x
        return clamp(
            aligned,
            -self.goal_half_width + 0.42,
            self.goal_half_width - 0.42,
        )


    def _update_goalkeeper_idle(self, dt: float) -> None:
        # Pequenos passos laterais em vez de saltar diretamente para o eixo.
        self._move_goalkeeper_towards(
            self._aligned_goalkeeper_x(), dt, max_speed=1.65, acceleration=8.2
        )
        self.goalkeeper_dive_progress = 0.0
        self.goalkeeper_dive_amount = 0.0
        self.goalkeeper_is_diving = False
        self.goalkeeper_should_dive = False
        self.goalkeeper_high_reach = 0.0
        self.goalkeeper_dive_age = 0.0


    def _move_goalkeeper_towards(
        self,
        target: float,
        dt: float,
        max_speed: float,
        acceleration: float,
    ) -> None:
        """Deslocação lateral com aceleração, travagem e mudança de apoio."""
        low = -self.goal_half_width + 0.42
        high = self.goal_half_width - 0.42
        target = clamp(target, low, high)
        gap = target - self.goalkeeper_x
        desired_speed = clamp(gap * 7.0, -max_speed, max_speed)
        speed_change = acceleration * dt
        self.goalkeeper_vx += clamp(
            desired_speed - self.goalkeeper_vx,
            -speed_change,
            speed_change,
        )
        next_x = self.goalkeeper_x + self.goalkeeper_vx * dt
        if (target - self.goalkeeper_x) * (target - next_x) <= 0.0:
            next_x = target
            self.goalkeeper_vx *= 0.32
        self.goalkeeper_x = clamp(next_x, low, high)
        if abs(gap) < 0.012 and abs(self.goalkeeper_vx) < 0.08:
            self.goalkeeper_x = target
            self.goalkeeper_vx = 0.0


    def _update_goalkeeper_shot(self, dt: float) -> None:
        prediction = self._predict_ball_at_y(GOALKEEPER_Y)


        # Depois do impulso, o GR já não muda de ideia no ar.
        if self.goalkeeper_is_diving:
            self.goalkeeper_dive_age += dt
            self.goalkeeper_dive_progress = clamp(
                self.goalkeeper_dive_progress + dt * self.goalkeeper_dive_speed,
                0.0,
                1.0,
            )
            progress = self.goalkeeper_dive_progress
            ease = 1.0 - math.pow(1.0 - progress, 3.0)
            self.goalkeeper_x = (
                self.goalkeeper_dive_start_x
                + (self.goalkeeper_target_x - self.goalkeeper_dive_start_x) * ease
            )
            self.goalkeeper_vx = 0.0
            return


        if self.goalkeeper_reaction > 0.0:
            # Enquanto lê a trajetória, ajusta os apoios e mantém-se alinhado
            # com a posição lateral atual da bola.
            reading_target = self._aligned_goalkeeper_x()
            self._move_goalkeeper_towards(
                reading_target,
                dt,
                max_speed=1.55,
                acceleration=8.0,
            )
            self.goalkeeper_dive_start_x = self.goalkeeper_x
            self.goalkeeper_reaction -= dt
            return


        if prediction is None:
            self.goalkeeper_should_dive = False
            return


        time_to_keeper, intercept_x, intercept_z = prediction
        threatens_goal = (
            abs(intercept_x) <= self.goal_half_width + 0.20
            and -0.10 <= intercept_z <= GOAL_HEIGHT + 0.20
        )
        horizontal_gap = intercept_x - self.goalkeeper_x


        # Uma bola exterior ou dirigida ao corpo não justifica um mergulho.
        # O GR acompanha-a com passos curtos, mantendo os pés no relvado.
        # Uma bola a cerca de meio metro do eixo já merece um gesto curto de
        # defesa; anteriormente algumas passavam rente ao braço sem mergulho.
        body_width = 0.49 if intercept_z < 1.65 else 0.39
        needs_high_jump = intercept_z > 1.68
        self.goalkeeper_should_dive = threatens_goal and (
            abs(horizontal_gap) > body_width or needs_high_jump
        )
        if not self.goalkeeper_should_dive:
            target = clamp(
                intercept_x if threatens_goal else self._aligned_goalkeeper_x(),
                -self.goal_half_width + 0.42,
                self.goal_half_width - 0.42,
            )
            self._move_goalkeeper_towards(
                target,
                dt,
                max_speed=1.78,
                acceleration=10.0,
            )
            self.goalkeeper_dive_start_x = self.goalkeeper_x
            self.goalkeeper_dive_progress = 0.0
            self.goalkeeper_is_diving = False
            return


        # Continua a ajustar os apoios e compromete-se nos últimos 0,30 s.
        # Em bolas cruzadas, este cálculo é feito no plano do GR, não no fundo
        # da baliza, evitando lançamentos precoces e deslocações impossíveis.
        if time_to_keeper > 0.30:
            step_target = clamp(
                intercept_x,
                -self.goal_half_width + 0.42,
                self.goal_half_width - 0.42,
            )
            self._move_goalkeeper_towards(
                step_target,
                dt,
                max_speed=2.75 if self.shot_context == "match" and self.current_chance_difficulty == "hard" else 1.95,
                acceleration=13.0 if self.shot_context == "match" and self.current_chance_difficulty == "hard" else 10.5,
            )
            self.goalkeeper_dive_start_x = self.goalkeeper_x
            return


        self.goalkeeper_is_diving = True
        self.goalkeeper_vx = 0.0
        self.goalkeeper_dive_start_x = self.goalkeeper_x
        self.goalkeeper_dive_age = 0.0
        self.goalkeeper_high_reach = clamp(
            (intercept_z - 1.52) / 0.82,
            0.0,
            1.0,
        )
        dive_delta = intercept_x + self.goalkeeper_read_error - self.goalkeeper_x
        # Um mergulho desloca o centro de massa no máximo cerca de 1,72 m.
        # A limitação é ainda mais importante nas trajetórias muito cruzadas.
        crossing_ratio = abs(self.ball.vx) / max(0.1, abs(self.ball.vy))
        maximum_reach = 1.72 - 0.25 * clamp(crossing_ratio / 1.2, 0.0, 1.0)
        dive_delta = clamp(dive_delta, -maximum_reach, maximum_reach)
        self.goalkeeper_target_x = clamp(
            self.goalkeeper_x + dive_delta,
            -self.goal_half_width + 0.48,
            self.goal_half_width - 0.48,
        )
        self.goalkeeper_dive_sign = 1.0 if dive_delta >= 0.0 else -1.0
        lateral_dive = clamp((abs(dive_delta) - 0.18) / 1.10, 0.0, 1.0)
        if abs(dive_delta) > 0.42:
            lateral_dive = max(0.34, lateral_dive)
        self.goalkeeper_dive_amount = lateral_dive


    def _predict_ball_at_y(
        self,
        target_y: float,
    ) -> Optional[tuple[float, float, float]]:
        """Prevê tempo, posição lateral e altura no plano indicado."""
        ball = self.ball
        if ball.vy >= -0.01 or ball.y <= target_y:
            return None
        time = (ball.y - target_y) / -ball.vy
        return (
            time,
            ball.x + ball.vx * time,
            ball.z + ball.vz * time - 0.5 * GRAVITY * time * time,
        )


    def shoot(self, x: Optional[float] = None, z: Optional[float] = None) -> None:
        if self.state != self.STATE_AIMING:
            return


        if x is not None and z is not None:
            self.auto_aim = False
            self.aim_x = clamp(x, -self.goal_half_width + 0.16, self.goal_half_width - 0.16)
            self.aim_z = clamp(z, 0.18, GOAL_HEIGHT - 0.10)


        self.attempts += 1
        self.state = self.STATE_SHOT
        self.state_age = 0.0
        self.outcome_registered = False
        self.result_text = ""
        self.last_goal_line_point = None


        start_z = HEADER_BALL_HEIGHT if self.shot_type == "header" else None
        self.ball.reset(self.shot_origin_x, self.shot_origin_y, start_z)
        self.ball.active = True
        self.goalkeeper_x = self._aligned_goalkeeper_x()
        self.player_kick_progress = 0.0
        self.last_field_collision = None
        self.goalkeeper_high_reach = 0.0
        self.goalkeeper_dive_age = 0.0


        # Distância medida à linha de golo: de perto o remate é mais preciso
        # e o GR tem menos tempo; de longe há mais dispersão e melhor leitura.
        self.shot_distance_factor = clamp(
            (self.shot_origin_y - 6.0) / 12.0, 0.0, 1.0
        )
        spread = (
            0.018
            + 0.20 * self.shot_distance_factor
            + (1.0 - self.power) * (0.05 + 0.08 * self.shot_distance_factor)
        )
        destination_x = self.aim_x + random.uniform(-spread, spread)
        destination_z = self.aim_z + random.uniform(-spread, spread)


        # O tempo de voo adapta-se à distância e à potência do remate.
        horizontal_distance = math.hypot(
            destination_x - self.ball.x, self.ball.y
        )
        if self.shot_type == "header":
            shot_speed = 17.0 + self.power * 8.0
            flight_time = clamp(horizontal_distance / shot_speed, 0.28, 0.82)
        else:
            shot_speed = 24.0 + self.power * 11.0
            flight_time = clamp(horizontal_distance / shot_speed, 0.20, 0.78)


        self.ball.vx = (destination_x - self.ball.x) / flight_time
        self.ball.vy = -self.ball.y / flight_time
        self.ball.vz = (
            destination_z
            - self.ball.z
            + 0.5 * GRAVITY * flight_time * flight_time
        ) / flight_time


        # Perto, o GR reage tarde e adivinha pior; de longe lê melhor a bola.
        goalkeeper_error = 0.88 - 0.76 * self.shot_distance_factor
        ability_error = random.gauss(0.0, goalkeeper_error)
        self.goalkeeper_read_error = ability_error
        self.goalkeeper_target_x = clamp(
            destination_x + ability_error,
            -self.goal_half_width + 0.62,
            self.goal_half_width - 0.62,
        )
        reaction_low = 0.22 - 0.06 * self.shot_distance_factor
        reaction_high = 0.34 - 0.09 * self.shot_distance_factor
        hard = self.shot_context == "match" and self.current_chance_difficulty == "hard"
        if hard:
            self.goalkeeper_read_error = random.gauss(0.0, 0.09)
            reaction_low, reaction_high = 0.07, 0.13
        self.goalkeeper_reaction = random.uniform(reaction_low, reaction_high)
        self.goalkeeper_dive_speed = 5.8 if hard else 3.90 + 0.80 * self.shot_distance_factor
        dive_delta = self.goalkeeper_target_x - self.goalkeeper_x
        self.goalkeeper_should_dive = (
            abs(destination_x - self.goalkeeper_x) > 0.58
        )
        self.goalkeeper_dive_start_x = self.goalkeeper_x
        self.goalkeeper_dive_progress = 0.0
        self.goalkeeper_dive_sign = 1.0 if dive_delta >= 0.0 else -1.0
        self.goalkeeper_dive_amount = (
            clamp((abs(dive_delta) - 0.18) / 1.30, 0.0, 1.0)
            if self.goalkeeper_should_dive
            else 0.0
        )
        self.goalkeeper_is_diving = False
        self.goalkeeper_vx = 0.0


    def _update_ball(self, dt: float) -> None:
        ball = self.ball
        old_x = ball.x
        old_y = ball.y
        old_z = ball.z


        ball.post_cooldown = max(0.0, ball.post_cooldown - dt)
        ball.player_cooldown = max(0.0, ball.player_cooldown - dt)
        ball.net_cooldown = max(0.0, ball.net_cooldown - dt)
        ball.vz -= GRAVITY * dt
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        ball.z += ball.vz * dt


        # Resistência do ar suave.
        drag = math.pow(0.996, dt * 60.0)
        ball.vx *= drag
        ball.vy *= drag
        ball.vz *= drag


        self._collide_field_players(old_x, old_y, old_z)
        self._collide_goal_frame()
        saved = self._collide_goalkeeper()


        if (
            not ball.crossed_goal
            and not saved
            and old_y > 0.0 >= ball.y
        ):
            # Usa a interseção exata da trajetória com y=0. Verificar a posição
            # já atrás da linha podia transformar um remate exterior em golo.
            crossing = clamp(old_y / max(1e-9, old_y - ball.y), 0.0, 1.0)
            goal_line_x = old_x + (ball.x - old_x) * crossing
            goal_line_z = old_z + (ball.z - old_z) * crossing
            self.last_goal_line_point = (goal_line_x, goal_line_z)
            ball.crossed_goal = True
            # A decisão segue o centro da bola no instante em que cruza a linha.
            # Assim, um remate junto ao poste que entra visualmente conta como
            # golo, sem usar a posição posterior da bola para falsear o lance.
            if (
                abs(goal_line_x) < self.goal_half_width
                and 0.0 < goal_line_z < GOAL_HEIGHT
            ):
                self._register_goal()
            else:
                self._register_non_goal()


        # A rede interior só prende bolas que entraram legalmente. Um remate
        # exterior junto ao poste não pode ser puxado para dentro pela malha e
        # parecer golo depois de já ter sido classificado como falhado.
        if (
            ball.y < 0.0
            and self.result_text == "GOAL!"
            and abs(ball.x) <= self.goal_half_width + 0.35
        ):
            self._collide_net(old_x, old_y, old_z)


        # Relvado: a bola perde energia a cada ressalto.
        if ball.z < ball.radius:
            ball.z = ball.radius
            if ball.vz < 0.0:
                inside_net = self.result_text == "GOAL!" and ball.y < 0.0
                ball.vz = -ball.vz * (0.27 if inside_net else 0.48)
                ground_drag = 0.74 if inside_net else 0.82
                ball.vx *= ground_drag
                ball.vy *= ground_drag


        # Bola que saiu claramente da zona útil.
        if not self.outcome_registered:
            if (
                ball.y < -GOAL_DEPTH - 1.2
                or abs(ball.x) > 22.0
                or ball.y > self.shot_origin_y + 4.0
            ):
                self._register_non_goal()


        if ball.speed < 0.42 and ball.z <= ball.radius + 0.01:
            if not self.outcome_registered:
                self._register_non_goal()
            ball.active = False


        if self.outcome_registered and self.state == self.STATE_SHOT:
            self.state = self.STATE_RESULT
            self.state_age = 0.0


    # ------------------------------------------------------------------
    # Colisões
    # ------------------------------------------------------------------
    def _field_player_position(self, player: FieldPlayer) -> tuple[float, float]:
        """Pequenos ajustes de apoio, partilhados pelo desenho e colisões."""
        elapsed = getattr(self, "elapsed", 0.0)
        return (
            player.x + math.sin(elapsed * 1.15 + player.phase) * 0.07,
            player.y + math.cos(elapsed * 0.92 + player.phase) * 0.045,
        )


    def _collide_field_players(
        self,
        old_x: float,
        old_y: float,
        old_z: float,
    ) -> bool:
        """Deteta o primeiro impacto varrido e desvia a bola nesse ponto."""
        ball = self.ball
        if ball.player_cooldown > 0.0:
            return False


        start = (old_x, old_y, old_z)
        movement = (ball.x - old_x, ball.y - old_y, ball.z - old_z)
        movement_size_sq = dot3(movement, movement)
        if movement_size_sq < 1e-9:
            return False


        # Três volumes representam pernas, tronco e cabeça. A interseção é
        # calculada ao longo de todo o passo para não atravessar jogadores em
        # remates rápidos num telemóvel que esteja a renderizar a 30 fps.
        body_parts = (
            (0.43 * FIELD_PLAYER_SCALE, 0.25 * FIELD_PLAYER_SCALE),
            (1.08 * FIELD_PLAYER_SCALE, 0.34 * FIELD_PLAYER_SCALE),
            (1.73 * FIELD_PLAYER_SCALE, 0.22 * FIELD_PLAYER_SCALE),
        )
        earliest: Optional[
            tuple[float, FieldPlayer, tuple[float, float, float]]
        ] = None


        for player in self.field_players:
            player_x, player_y = self._field_player_position(player)
            for center_z, body_radius in body_parts:
                center = (player_x, player_y, center_z)
                relative = subtract3(start, center)
                radius = ball.radius + body_radius
                quadratic_b = 2.0 * dot3(relative, movement)
                quadratic_c = dot3(relative, relative) - radius * radius
                discriminant = (
                    quadratic_b * quadratic_b
                    - 4.0 * movement_size_sq * quadratic_c
                )
                if discriminant < 0.0:
                    continue
                root = math.sqrt(discriminant)
                t0 = (-quadratic_b - root) / (2.0 * movement_size_sq)
                t1 = (-quadratic_b + root) / (2.0 * movement_size_sq)
                valid = [amount for amount in (t0, t1) if 0.0 <= amount <= 1.0]
                if quadratic_c <= 0.0:
                    valid.append(0.0)
                if not valid:
                    continue
                amount = min(valid)
                if earliest is None or amount < earliest[0]:
                    earliest = (amount, player, center)


        if earliest is None:
            return False


        amount, player, center = earliest
        impact = (
            old_x + movement[0] * amount,
            old_y + movement[1] * amount,
            old_z + movement[2] * amount,
        )
        normal = subtract3(impact, center)
        normal_size = length3(*normal)
        if normal_size < 1e-6:
            normal = normalize3((-ball.vx, -ball.vy, -ball.vz))
        else:
            normal = (
                normal[0] / normal_size,
                normal[1] / normal_size,
                normal[2] / normal_size,
            )


        approach = ball.vx * normal[0] + ball.vy * normal[1] + ball.vz * normal[2]
        if approach >= 0.0:
            return False


        # Reflexão amortecida: um bloco tira velocidade, mas conserva uma
        # trajetória suficientemente viva para haver ressaltos e autogolos.
        restitution = 1.34
        ball.vx = (ball.vx - restitution * approach * normal[0]) * 0.76
        ball.vy = (ball.vy - restitution * approach * normal[1]) * 0.76
        ball.vz = (ball.vz - restitution * approach * normal[2]) * 0.76
        ball.x = impact[0] + normal[0] * 0.008
        ball.y = impact[1] + normal[1] * 0.008
        ball.z = max(ball.radius, impact[2] + normal[2] * 0.008)
        ball.player_cooldown = 0.10
        self.last_field_collision = (player.team, ball.x, ball.y)
        return True


    def _collide_goal_frame(self) -> bool:
        if self.ball.post_cooldown > 0.0:
            return False


        hw = self.goal_half_width
        segments = (
            ((-hw, 0.0, 0.0), (-hw, 0.0, GOAL_HEIGHT)),
            ((hw, 0.0, 0.0), (hw, 0.0, GOAL_HEIGHT)),
            ((-hw, 0.0, GOAL_HEIGHT), (hw, 0.0, GOAL_HEIGHT)),
        )
        for start, end in segments:
            if self._collide_segment(start, end, POST_RADIUS):
                self.ball.post_cooldown = 0.055
                if not self.outcome_registered:
                    self.result_text = "OFF THE POST!"
                    self.result_color = (1.0, 0.78, 0.18, 1.0)
                return True
        return False


    def _collide_segment(
        self,
        start: tuple[float, float, float],
        end: tuple[float, float, float],
        segment_radius: float,
    ) -> bool:
        px, py, pz = self.ball.x, self.ball.y, self.ball.z
        ax, ay, az = start
        bx, by, bz = end
        abx, aby, abz = bx - ax, by - ay, bz - az
        apx, apy, apz = px - ax, py - ay, pz - az
        denom = abx * abx + aby * aby + abz * abz
        t = clamp((apx * abx + apy * aby + apz * abz) / denom, 0.0, 1.0)
        cx, cy, cz = ax + abx * t, ay + aby * t, az + abz * t
        nx, ny, nz = px - cx, py - cy, pz - cz
        distance = length3(nx, ny, nz)
        minimum = self.ball.radius + segment_radius
        if distance >= minimum:
            return False


        if distance < 1e-6:
            nx, ny, nz, distance = 0.0, 1.0, 0.0, 1.0
        nx, ny, nz = nx / distance, ny / distance, nz / distance
        correction = minimum - distance + 0.002
        self.ball.x += nx * correction
        self.ball.y += ny * correction
        self.ball.z += nz * correction


        dot = self.ball.vx * nx + self.ball.vy * ny + self.ball.vz * nz
        if dot < 0.0:
            restitution = 1.78
            self.ball.vx -= restitution * dot * nx
            self.ball.vy -= restitution * dot * ny
            self.ball.vz -= restitution * dot * nz
            self.ball.vx *= 0.88
            self.ball.vy *= 0.88
            self.ball.vz *= 0.88
        return True


    def _collide_goalkeeper(self) -> bool:
        ball = self.ball
        if (
            ball.vy >= 0.0
            or ball.y < GOALKEEPER_Y - 0.36
            or ball.y > GOALKEEPER_Y + 0.36
        ):
            return False


        pose = self._goalkeeper_pose()
        segments = (
            (pose["hand_l"], pose["shoulder_l"], 0.24 * GOALKEEPER_SCALE),
            (pose["hand_r"], pose["shoulder_r"], 0.24 * GOALKEEPER_SCALE),
            (pose["shoulder_l"], pose["hip_l"], 0.27 * GOALKEEPER_SCALE),
            (pose["shoulder_r"], pose["hip_r"], 0.27 * GOALKEEPER_SCALE),
            (pose["shoulder_l"], pose["shoulder_r"], 0.25 * GOALKEEPER_SCALE),
            (pose["hip_l"], pose["foot_l"], 0.19 * GOALKEEPER_SCALE),
            (pose["hip_r"], pose["foot_r"], 0.19 * GOALKEEPER_SCALE),
        )
        saved = any(
            self._distance_to_segment_2d(
                ball.x, ball.z, start[0], start[1], end[0], end[1]
            )
            <= ball.radius + body_radius
            for start, end, body_radius in segments
        )
        head = pose["head"]
        saved = saved or math.hypot(
            ball.x - head[0], ball.z - head[1]
        ) <= ball.radius + 0.25 * GOALKEEPER_SCALE
        if not saved:
            return False


        ball.y = GOALKEEPER_Y + 0.32
        # A luva amortece e desvia a bola para fora do corpo. Defesas baixas
        # seguem mais rasas; bolas altas não sobem de novo artificialmente.
        side = 1.0 if ball.x >= pose["center"][0] else -1.0
        contact_height = clamp(ball.z / GOAL_HEIGHT, 0.0, 1.0)
        ball.vy = abs(ball.vy) * (0.40 - 0.08 * contact_height)
        ball.vx = ball.vx * 0.34 + side * (2.0 + 1.4 * contact_height)
        if contact_height < 0.30:
            ball.vz = max(0.38, abs(ball.vz) * 0.22)
        else:
            ball.vz = max(0.18, ball.vz * 0.16)
        # O toque não encerra a jogada: se a bola entrar depois da defesa,
        # continua a ser golo. A defesa só é confirmada quando ela não entra.
        ball.goalkeeper_touched = True
        return True


    @staticmethod
    def _distance_to_segment_2d(
        px: float,
        pz: float,
        ax: float,
        az: float,
        bx: float,
        bz: float,
    ) -> float:
        abx, abz = bx - ax, bz - az
        denominator = abx * abx + abz * abz
        if denominator < 1e-9:
            return math.hypot(px - ax, pz - az)
        amount = clamp(((px - ax) * abx + (pz - az) * abz) / denominator, 0.0, 1.0)
        closest_x = ax + abx * amount
        closest_z = az + abz * amount
        return math.hypot(px - closest_x, pz - closest_z)


    def _goalkeeper_pose(self) -> dict[str, tuple[float, float]]:
        """Esqueleto do GR: preparação, impulsão, voo e queda no relvado."""
        raw = clamp(self.goalkeeper_dive_progress, 0.0, 1.0)
        smooth = raw * raw * (3.0 - 2.0 * raw)
        dive = smooth * self.goalkeeper_dive_amount
        high = clamp(self.goalkeeper_high_reach, 0.0, 1.0)


        # O centro de massa sobe e volta a descer. A versão anterior ficava
        # suspensa no ponto alto durante todo o ecrã de resultado.
        flight_duration = 0.66 + 0.10 * high
        flight_phase = clamp(self.goalkeeper_dive_age / flight_duration, 0.0, 1.0)
        flight = math.sin(flight_phase * math.pi)
        landing_raw = clamp(
            (self.goalkeeper_dive_age - flight_duration * 0.72) / 0.42,
            0.0,
            1.0,
        )
        landing = landing_raw * landing_raw * (3.0 - 2.0 * landing_raw)


        moving = clamp(abs(self.goalkeeper_vx) / 1.55, 0.0, 1.0)
        ready_crouch = (0.15 if self.state == self.STATE_SHOT else 0.09) + 0.05 * moving
        angle = self.goalkeeper_dive_sign * math.radians(82.0) * dive
        cosine, sine = math.cos(angle), math.sin(angle)
        center_x = self.goalkeeper_x
        center_z = GOALKEEPER_SCALE * (
            0.89 - ready_crouch - 0.29 * dive - 0.10 * landing * dive
        )
        center_z += GOALKEEPER_SCALE * flight * (0.34 + 0.34 * high)


        def transform(local_x: float, local_z: float) -> tuple[float, float]:
            local_x *= GOALKEEPER_SCALE
            local_z *= GOALKEEPER_SCALE
            return (
                center_x + local_x * cosine + local_z * sine,
                center_z - local_x * sine + local_z * cosine,
            )


        step = math.sin(self.elapsed * 9.2)
        left_lift = max(0.0, step) * 0.075 * moving
        right_lift = max(0.0, -step) * 0.075 * moving
        stance = 0.28 + 0.055 * moving
        pose = {
            "center": (center_x, center_z),
            "head": transform(0.0, 0.86),
            "shoulder_l": transform(-0.32, 0.50),
            "shoulder_r": transform(0.32, 0.50),
            "hip_l": transform(-0.19, -0.18),
            "hip_r": transform(0.19, -0.18),
            "foot_l": transform(-stance, -0.88 + left_lift),
            "foot_r": transform(stance, -0.88 + right_lift),
            "hand_l": transform(-0.68, 0.17 - ready_crouch * 0.35),
            "hand_r": transform(0.68, 0.17 - ready_crouch * 0.35),
        }


        # A perna do lado oposto dá o último impulso e a outra fica a arrastar
        # durante o voo, evitando a antiga rotação rígida de todo o corpo.
        if dive > 0.0 or high > 0.0:
            launch = clamp(max(dive, high * smooth) * 1.28, 0.0, 1.0)
            reach_x = center_x + self.goalkeeper_dive_sign * GOALKEEPER_SCALE * (
                0.76 + 0.82 * dive
            )
            reach_z = center_z + GOALKEEPER_SCALE * (
                0.24 + 0.88 * high + 0.12 * flight
            )
            lead = "hand_r" if self.goalkeeper_dive_sign > 0.0 else "hand_l"
            trail = "hand_l" if lead == "hand_r" else "hand_r"
            for key, lag, vertical_offset in (
                (lead, 0.0, 0.08),
                (trail, 0.15, -0.08),
            ):
                old_x, old_z = pose[key]
                blend = clamp(launch - lag, 0.0, 1.0)
                pose[key] = (
                    old_x + (reach_x - old_x) * blend,
                    old_z + (
                        reach_z + vertical_offset * GOALKEEPER_SCALE - old_z
                    ) * blend,
                )


            push_key = "foot_l" if self.goalkeeper_dive_sign > 0.0 else "foot_r"
            trail_key = "foot_r" if push_key == "foot_l" else "foot_l"
            push_x, push_z = pose[push_key]
            trail_x, trail_z = pose[trail_key]
            pose[push_key] = (
                push_x - self.goalkeeper_dive_sign * 0.10 * GOALKEEPER_SCALE * smooth,
                max(0.02, push_z - 0.12 * GOALKEEPER_SCALE * smooth),
            )
            pose[trail_key] = (
                trail_x - self.goalkeeper_dive_sign * 0.18 * GOALKEEPER_SCALE * smooth,
                trail_z + 0.10 * GOALKEEPER_SCALE * flight,
            )
        return pose


    def _goalkeeper_world_pose(
        self,
        flat_pose: Optional[dict[str, tuple[float, float]]] = None,
    ) -> dict[str, tuple[float, float, float]]:
        """Roda o plano do corpo para o GR ficar sempre virado para a bola."""
        if flat_pose is None:
            flat_pose = self._goalkeeper_pose()


        target_x = self.ball.x if self.ball.active else self.shot_origin_x
        target_y = self.ball.y if self.ball.active else self.shot_origin_y
        facing_x = target_x - self.goalkeeper_x
        facing_y = target_y - GOALKEEPER_Y
        facing_size = max(1e-6, math.hypot(facing_x, facing_y))
        facing_x /= facing_size
        facing_y /= facing_size
        # O tronco acompanha a bola, mas não roda os membros quase 90 graus
        # em remates de ângulo fechado. Esse excesso fazia os mergulhos
        # cruzados parecerem uma cambalhota em profundidade.
        yaw = clamp(
            math.atan2(facing_x, max(0.08, facing_y)),
            math.radians(-52.0),
            math.radians(52.0),
        )
        # Eixo dos ombros, perpendicular à direção da bola.
        side_x, side_y = math.cos(yaw), -math.sin(yaw)


        world_pose: dict[str, tuple[float, float, float]] = {}
        for key, point in flat_pose.items():
            lateral = point[0] - self.goalkeeper_x
            world_pose[key] = (
                self.goalkeeper_x + side_x * lateral,
                GOALKEEPER_Y + side_y * lateral,
                max(0.02, point[1]),
            )
        return world_pose


    def _collide_net(
        self,
        old_x: Optional[float] = None,
        old_y: Optional[float] = None,
        old_z: Optional[float] = None,
    ) -> None:
        ball = self.ball
        hw = self.goal_half_width
        impact_speed = max(1.0, ball.speed)


        # Fast shots can travel farther than the ball's diameter in one
        # physics step. Sweep the travelled segment in short intervals and
        # stop at the first contact with the sloping veil, instead of testing
        # only the final position and allowing the ball to tunnel through.
        if old_x is not None and old_y is not None and old_z is not None:
            travel = length3(
                ball.x - old_x,
                ball.y - old_y,
                ball.z - old_z,
            )
            sweep_steps = max(1, math.ceil(travel / (ball.radius * 0.55)))
            previous_gap: Optional[float] = None
            previous_valid = False
            for sweep_index in range(sweep_steps + 1):
                amount = sweep_index / sweep_steps
                sample_x = old_x + (ball.x - old_x) * amount
                sample_y = old_y + (ball.y - old_y) * amount
                sample_z = old_z + (ball.z - old_z) * amount
                valid = (
                    -VEIL_TOUCH_DEPTH <= sample_y <= -VEIL_TOP_DEPTH
                    and abs(sample_x) <= hw + ball.radius
                )
                if valid:
                    slope_run = VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH
                    slope_amount = clamp(
                        (-sample_y - VEIL_TOP_DEPTH) / slope_run,
                        0.0,
                        1.0,
                    )
                    derivative = (
                        GOAL_HEIGHT
                        + VEIL_SAG
                        * math.pi
                        * math.cos(math.pi * slope_amount)
                    ) / slope_run
                    normal_size = math.sqrt(derivative * derivative + 1.0)
                    gap = (
                        sample_z - self._veil_height_at_y(sample_y)
                    ) / normal_size + ball.radius
                    approach = (
                        ball.vy * (-derivative / normal_size)
                        + ball.vz * (1.0 / normal_size)
                    )
                    if (
                        previous_valid
                        and previous_gap is not None
                        and previous_gap < 0.0 <= gap
                        and approach > 0.0
                    ):
                        ball.x = sample_x
                        ball.y = sample_y
                        ball.z = sample_z + 0.002
                        break
                    previous_gap = gap
                else:
                    previous_gap = None
                previous_valid = valid


        # Primeiro existe um pequeno teto horizontal, sustentado pelos ferros
        # dos cantos. Só depois desse recuo começa a queda inclinada do véu.
        within_width = abs(ball.x) <= hw + ball.radius
        if (
            -VEIL_TOP_DEPTH <= ball.y <= 0.0
            and within_width
            and ball.z >= GOAL_HEIGHT - ball.radius
            and ball.vz > 0.0
        ):
            ball.z = GOAL_HEIGHT - ball.radius
            ball.vz = -abs(ball.vz) * 0.20
            ball.vx *= 0.64
            ball.vy *= 0.64
            path_v = self._veil_amount_at_y(ball.y)
            self._add_ripple(
                "back",
                (ball.x + hw) / GOAL_WIDTH,
                path_v,
                impact_speed,
            )


        if (
            -VEIL_TOUCH_DEPTH <= ball.y <= -VEIL_TOP_DEPTH
            and within_width
        ):
            slope_run = VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH
            slope_amount = clamp(
                (-ball.y - VEIL_TOP_DEPTH) / slope_run, 0.0, 1.0
            )
            profile_z = self._veil_height_at_y(ball.y)
            derivative = (
                GOAL_HEIGHT
                + VEIL_SAG * math.pi * math.cos(math.pi * slope_amount)
            ) / slope_run
            normal_size = math.sqrt(derivative * derivative + 1.0)
            normal_y = -derivative / normal_size
            normal_z = 1.0 / normal_size
            signed_distance = (ball.z - profile_z) / normal_size
            approach = ball.vy * normal_y + ball.vz * normal_z
            if signed_distance > -ball.radius and approach > 0.0:
                correction = signed_distance + ball.radius + 0.002
                ball.y -= normal_y * correction
                ball.z -= normal_z * correction
                ball.vy -= 1.22 * approach * normal_y
                ball.vz -= 1.22 * approach * normal_z
                ball.vx *= 0.62
                ball.vy *= 0.58
                ball.vz *= 0.58
                self._add_ripple(
                    "back",
                    (ball.x + hw) / GOAL_WIDTH,
                    self._veil_amount_at_y(ball.y),
                    impact_speed,
                )


        # As laterais seguem o perfil poste–ferro curto–queda do véu.
        veil_height = self._veil_height_at_y(ball.y)
        within_side = (
            -GOAL_DEPTH <= ball.y <= 0.0
            and 0.0 <= ball.z <= veil_height + ball.radius
        )
        if within_side and ball.x <= -hw + ball.radius and ball.vx < 0.0:
            ball.x = -hw + ball.radius
            # A malha ampara o impacto, deixa a bola cair e encaminha-a para
            # o centro/fundo da baliza em vez de a fazer ressaltar para fora.
            ball.vx = clamp(abs(ball.vx) * 0.11, 0.38, 1.45)
            ball.vy = min(ball.vy * 0.30, -0.42)
            ball.vz = min(ball.vz * 0.16, -0.58)
            self._add_ripple(
                "left",
                self._veil_amount_at_y(ball.y),
                ball.z / GOAL_HEIGHT,
                impact_speed,
            )
        elif within_side and ball.x >= hw - ball.radius and ball.vx > 0.0:
            ball.x = hw - ball.radius
            ball.vx = -clamp(abs(ball.vx) * 0.11, 0.38, 1.45)
            ball.vy = min(ball.vy * 0.30, -0.42)
            ball.vz = min(ball.vz * 0.16, -0.58)
            self._add_ripple(
                "right",
                self._veil_amount_at_y(ball.y),
                ball.z / GOAL_HEIGHT,
                impact_speed,
            )


    def _add_ripple(self, surface: str, u: float, v: float, speed: float) -> None:
        if self.ball.net_cooldown > 0.0:
            return
        self.ball.net_cooldown = 0.075
        # O véu principal cede mais; as laterais acompanham a deformação.
        max_radii = 8.8 if surface == "back" else 6.3
        gain = 0.074 if surface == "back" else 0.075
        amplitude = min(max_radii * BALL_RADIUS, speed * gain)
        self.ripples.append(
            NetRipple(surface, clamp(u, 0.0, 1.0), clamp(v, 0.0, 1.0), amplitude)
        )


    # ------------------------------------------------------------------
    # Resultados e reinício
    # ------------------------------------------------------------------
    def _register_goal(self) -> None:
        if self.outcome_registered:
            return
        self.outcome_registered = True
        self.goals += 1
        self.result_text = "GOAL!"
        self.result_color = (0.25, 1.0, 0.50, 1.0)
        if self.shot_context == "match":
            self._record_player_match_goal()
            self._play_goal_crowd_sound()


    def _register_save(self) -> None:
        if self.outcome_registered:
            return
        self.outcome_registered = True
        self.saves += 1
        self.result_text = "SAVED!"
        self.result_color = (0.25, 0.78, 1.0, 1.0)


    def _register_non_goal(self) -> None:
        """Distingue uma defesa confirmada de um remate sem toque do GR."""
        if self.ball.goalkeeper_touched:
            self._register_save()
        else:
            self._register_miss("MISS!")


    def _register_miss(self, text: str) -> None:
        if self.outcome_registered:
            return
        self.outcome_registered = True
        self.misses += 1
        self.result_text = text
        self.result_color = (1.0, 0.36, 0.28, 1.0)


    def _expire_shot(self) -> None:
        if self.state != self.STATE_AIMING or self.outcome_registered:
            return
        self.attempts += 1
        self.ball.active = False
        self._register_miss("TOO LATE!")
        self.state = self.STATE_RESULT
        self.state_age = 0.0


    def _prepare_next_shot(self) -> None:
        self._randomize_aim_pattern()
        self._choose_shot_origin()
        self.ripples.clear()
        self.state = self.STATE_AIMING
        self.state_age = 0.0
        self.result_text = ""
        self.outcome_registered = False
        self._match_shot_goal_counted = False
        self.auto_aim = True
        self.goalkeeper_dive_progress = 0.0
        self.goalkeeper_dive_amount = 0.0
        self.goalkeeper_is_diving = False
        self.goalkeeper_should_dive = False
        self.goalkeeper_high_reach = 0.0
        self.goalkeeper_dive_age = 0.0
        self.goalkeeper_vx = 0.0


    def reset_statistics(self) -> None:
        self.attempts = self.goals = self.saves = self.misses = 0
        self._prepare_next_shot()


    # ------------------------------------------------------------------
    # Controlos
    # ------------------------------------------------------------------
    def _request_new_game(self):
        if self.view != "start" or self._new_game_popup is not None:
            return
        if not self.career.save_path.exists():
            self._start_new_career()
            return
        content = BoxLayout(orientation="vertical", spacing=dp(12), padding=dp(12))
        content.add_widget(FlowLabel(text="You already have a career. Start again? "
                                    "Your previous career will be backed up locally before it is replaced."))
        buttons = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(12))
        popup = Popup(title='Start a new career?', content=content,
                      size_hint=(0.9, None), height=min(Window.height - dp(16), dp(300)),
                      auto_dismiss=False)
        buttons.add_widget(TouchButton('CANCEL', popup.dismiss))
        buttons.add_widget(TouchButton('NEW GAME', self._start_new_career, accent=True))
        content.add_widget(buttons)
        popup.bind(on_dismiss=lambda *_: setattr(self, "_new_game_popup", None))
        self._new_game_popup = popup
        popup.open()

    def _start_new_career(self):
        if self.view != "start":
            return
        if not self.career.backup_before_new_game():
            if self._new_game_popup is not None:
                self._new_game_popup.dismiss()
            self.draw()
            return
        if self._new_game_popup is not None:
            self._new_game_popup.dismiss()
        self.career = CareerMode(autoload=False)
        self._career_started = False
        self.training_completed = False
        self.training_goals = 0
        self.match_finished = False
        self.awaiting_chance = False
        self._profile_return = "offers"
        self.view = "profile"
        self.draw()

    def _load_career(self):
        if self.view != "start":
            return
        if self.career.load():
            self._career_started = True
            self.view = "hub"
        else:
            self.career.message = 'Unable to load this career. Your previous save has been preserved.'
        self.draw()

    def _request_exit(self):
        if self._exit_popup is not None or self.view not in ("hub", "offers", "start"):
            return
        content = BoxLayout(orientation="vertical", spacing=dp(12), padding=dp(12))
        message = 'Your career will be saved before you exit.'
        if self.view in ("match", "shot"):
            message += ' The current match will need to be replayed. A started training session remains used.'
        from kivy.uix.scrollview import ScrollView
        message_scroll = ScrollView(do_scroll_x=False)
        message_scroll.add_widget(FlowLabel(text=message))
        content.add_widget(message_scroll)
        buttons = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(56))
        popup = Popup(title='Exit Scorer?', content=content,
                      size_hint=(0.9, None), height=min(Window.height - dp(16), dp(280)),
                      auto_dismiss=False)
        buttons.bind(minimum_height=buttons.setter("height"))
        buttons.add_widget(TouchButton('CONTINUE', popup.dismiss))
        buttons.add_widget(TouchButton('SAVE AND EXIT', self._confirm_exit, accent=True))
        content.add_widget(buttons)
        popup.bind(on_dismiss=lambda *_: setattr(self, "_exit_popup", None))
        self._exit_popup = popup
        popup.open()

    def _confirm_exit(self):
        if self.career.save() is False:
            if self._exit_popup is not None:
                self._exit_popup.dismiss()
            self.draw()
            return
        app = App.get_running_app()
        if app is not None:
            app.stop()

    def _on_key_down(self, _window, key, _scancode, codepoint, _modifiers):
        if self.view == "splash":
            return True
        if key == 27:  # ESC
            if self.view not in ("hub", "offers", "start") and self.career.club_name:
                self.view = "hub"
                return True
            self._request_exit()
            return True
        if key == 32:  # ESPAÇO
            if self.view == "shot":
                self.shoot()
            return True
        if codepoint and codepoint.lower() == "r":
            self.reset_statistics()
            return True
        if codepoint and codepoint.lower() == "c":
            self.auto_aim = True
            return True


        if self.view != "shot" or self.state != self.STATE_AIMING:
            return False


        step_x, step_z = 0.16, 0.10
        movement = False
        if key in (276, 97):  # esquerda / A
            self.aim_x -= step_x
            movement = True
        elif key in (275, 100):  # direita / D
            self.aim_x += step_x
            movement = True
        elif key in (273, 119):  # cima / W
            self.aim_z += step_z
            movement = True
        elif key in (274, 115):  # baixo / S
            self.aim_z -= step_z
            movement = True


        if movement:
            self.auto_aim = False
            self.aim_x = clamp(self.aim_x, -self.goal_half_width + 0.16, self.goal_half_width - 0.16)
            self.aim_z = clamp(self.aim_z, 0.18, GOAL_HEIGHT - 0.10)
            return True
        return False


    def on_touch_down(self, touch):
        if self._menu is not None or self._match_notice is not None:
            super().on_touch_down(touch)
            return True
        for x, y, width, height, action, value in reversed(self.ui_buttons):
            if x <= touch.x <= x + width and y <= touch.y <= y + height:
                self._activate_ui(action, value)
                return True


        if self.view == "match" and self.awaiting_chance:
            self._begin_pending_chance()
            return True


        if self.view != "shot":
            return True


        # A tap on a visible result advances immediately and must not also
        # trigger the following shot.
        if self.state == self.STATE_RESULT or (
            self.outcome_registered and self.result_text
        ):
            self._advance_after_shot()
            return True


        if self.state != self.STATE_AIMING:
            return True


        world_x, world_z = self.unproject_goal(touch.x, touch.y)
        inside_goal = (
            -self.goal_half_width <= world_x <= self.goal_half_width
            and 0.0 <= world_z <= GOAL_HEIGHT
        )
        if inside_goal:
            self.shoot(world_x, world_z)
        else:
            self.shoot()
        return True


    def _activate_ui(self, action: str, value: object = None) -> None:
        if action == "splash_continue" and self.view == "splash":
            self.view = "start"
        elif action == "new_game" and self.view == "start":
            self._request_new_game()
        elif action == "load_game":
            self._load_career()
        elif action == "profile" and self.view == "hub":
            self._profile_return = "hub"
            self.view = "profile"
        elif action == "save_profile" and self.view == "profile":
            try:
                if self.career.set_player_name(value):
                    self.view = self._profile_return
            except ValueError as error:
                self.career.message = str(error) if "scorer" in str(error) else 'Enter a name with at least 2 characters.'
        elif action == "cancel_profile" and self.view == "profile":
            self.view = "hub" if self._profile_return == "hub" else "start"
        elif action == "exit":
            self._request_exit()
        elif action == "accept_offer":
            self.career.accept_starting_offer(str(value))
            self._career_started = bool(self.career.club_name)
            self.view = "hub"
        elif action == "hub":
            self.view = "hub"
        elif action == "play":
            self.start_career_match()
        elif action == "training":
            self.training_completed = False
            self.training_summary = ""
            self.view = "training"
        elif action == "training_start":
            self.start_training()
        elif action == "standings":
            self.table_page = 0
            self.view = "standings"
        elif action == "scorers":
            self.view = "scorers"
        elif action == "calendar":
            self.view = "calendar"
        elif action == "agent":
            if not self.career.agent_offers:
                self.career.generate_agent_offers()
            self.view = "agent"
        elif action == "agent_refresh":
            self.career.generate_agent_offers()
        elif action == "transfer" and isinstance(value, tuple):
            club_name, league_key = value
            self.career.accept_transfer(str(club_name), str(league_key))
            self.view = "hub"
        elif action == "world":
            if self.career.world_unlocked:
                self.view = "world"
            else:
                self.career.message = 'Scorer World will be a separate app. This edition has one division.'
                self.view = "hub"
        elif action == "editor":
            if self.career.world_unlocked:
                self._open_local_editor()
        elif action == "table_prev":
            self.table_page = max(0, self.table_page - 1)
        elif action == "table_next":
            rows = len(self.career.current_league.clubs)
            self.table_page = min(max(0, (rows - 1) // 11), self.table_page + 1)
        elif action == "world_prev":
            self.world_page = max(0, self.world_page - 1)
        elif action == "world_next":
            pages = max(0, (len(EUROPE_COUNTRIES) - 1) // 9)
            self.world_page = min(pages, self.world_page + 1)
        elif action == "match_continue":
            self.view = "hub"


    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------
    def draw(self) -> None:
        # Keep touch grabs and the widget tree stable while a notice is visible.
        show_notice = self.view == "match" and (self.match_finished or self.awaiting_chance or self.match_halftime)
        if self._match_notice is not None and self._match_notice.parent is self and not show_notice:
            self.remove_widget(self._match_notice)
        if self.view in MENU_VIEWS:
            self.ui_buttons.clear()
            if self._menu is None:
                self.canvas.clear()
                self._menu = CareerMenu(self)
                self.add_widget(self._menu)
            self._menu.sync()
            return
        if self._menu is not None:
            self.remove_widget(self._menu)
            self._menu = None
        self.ui_buttons.clear()
        landscape = self.width >= self.height


        self.canvas.clear()
        with self.canvas:
            # Nunca comprime o jogo numa faixa vertical. A orientação é pedida
            # automaticamente; esta mensagem é apenas o fallback para hosts
            # Android que bloqueiem a rotação.
            if not landscape:
                self._draw_background()
                self._draw_text(
                    "ROTATE YOUR PHONE",
                    self.center_x,
                    self.center_y + 22,
                    font_size=max(28, int(self.width * 0.055)),
                    color=(0.96, 0.98, 1.0, 1.0),
                    anchor="center",
                )
                self._draw_text(
                    "SCORER IS DESIGNED FOR LANDSCAPE",
                    self.center_x,
                    self.center_y - 32,
                    font_size=max(13, int(self.width * 0.025)),
                    color=(0.55, 0.78, 0.82, 1.0),
                    anchor="center",
                )
                return


            self.ui_buttons.clear()
            if self.view in ("offers", "hub", "training", "standings", "scorers", "calendar", "agent", "world"):
                self._draw_career_screen()
                return


            # O cenário é suficientemente leve para ser desenhado diretamente.
            # Em alguns GPUs Android, a textura FBO alterava as cores e fazia
            # linhas finas da bancada aparecerem como faixas ou pilares.
            self._draw_background()
            self._draw_stadium_stands()


            self._draw_pitch()
            # A rede é sempre desenhada diretamente. Além de preservar a
            # animação, evita a textura transparente que causava a névoa
            # branca antes do remate no Pydroid.
            self._draw_goal_net()


            if self.view == "shot":
                # Dentro da baliza, a bola fica visualmente atrás do ferro e do GR.
                if self.ball.active and self.ball.y < 0.0:
                    self._draw_ball()


                self._draw_field_players()
                self._draw_player()
                self._draw_goal_frame()
                # O GR está 85 cm à frente da linha de golo e, por isso, é
                # desenhado depois dos postes em vez de parecer escondido atrás.
                self._draw_goalkeeper()
                if not (self.ball.active and self.ball.y < 0.0):
                    self._draw_ball()


                self._draw_aim_marker()
                self._draw_hud()
            else:
                # Entre oportunidades vê-se o campo limpo, sem jogadores nem bola.
                self._draw_goal_frame()


            if self.view == "match":
                self._draw_match_overlay()
        if self.view == "match" and (self.match_finished or self.awaiting_chance or self.match_halftime):
            if self._match_notice is None:
                self._match_notice = MatchNotice(self)
            self._match_notice.sync()
            if self._match_notice.parent is not self:
                self.add_widget(self._match_notice)
            elif self._match_notice.canvas not in self.canvas.children:
                self.canvas.add(self._match_notice.canvas)
        else:
            self._match_notice = None


    def _draw_career_screen(self) -> None:
        """Menus desenhados no mesmo Canvas para funcionar sem ficheiros KV."""
        self._draw_background()
        Color(0.025, 0.065, 0.080, 1.0)
        Rectangle(pos=self.pos, size=self.size)
        Color(0.03, 0.12, 0.12, 1.0)
        Rectangle(pos=(self.x, self.y), size=(self.width, self.height * 0.18))
        Color(0.10, 0.55, 0.35, 0.22)
        Triangle(points=[self.x, self.y, self.right, self.y, self.right, self.top])


        self._draw_text(
            "SCORER  CAREER",
            self.x + 34,
            self.top - 42,
            font_size=max(22, int(self.height * 0.043)),
            color=(0.92, 1.0, 0.96, 1.0),
        )
        if self.view == "offers":
            self._draw_offers_screen()
        elif self.view == "hub":
            self._draw_hub_screen()
        elif self.view == "training":
            self._draw_training_screen()
        elif self.view == "standings":
            self._draw_standings_screen()
        elif self.view == "scorers":
            self._draw_scorers_screen()
        elif self.view == "calendar":
            self._draw_calendar_screen()
        elif self.view == "agent":
            self._draw_agent_screen()
        elif self.view == "world":
            self._draw_world_screen()


    def _ui_button(
        self,
        label: str,
        x: float,
        y: float,
        width: float,
        height: float,
        action: str,
        value: object = None,
        accent: bool = False,
    ) -> None:
        Color(*(0.10, 0.58, 0.36, 0.96) if accent else (0.055, 0.16, 0.18, 0.96))
        Rectangle(pos=(x, y), size=(width, height))
        Color(0.26, 0.82, 0.56, 0.80)
        Line(rectangle=(x, y, width, height), width=1.1)
        self._draw_text(
            label,
            x + width / 2,
            y + height / 2,
            font_size=max(12, int(height * 0.28)),
            color=(0.94, 1.0, 0.97, 1.0),
            anchor="center",
            max_width=max(20.0, width - 20.0),
        )
        self.ui_buttons.append((x, y, width, height, action, value))


    def _panel(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        accent: bool = False,
    ) -> None:
        Color(*(0.035, 0.13, 0.135, 0.96) if accent else (0.025, 0.085, 0.095, 0.94))
        Rectangle(pos=(x, y), size=(width, height))
        Color(0.19, 0.55, 0.40, 0.72)
        Line(rectangle=(x, y, width, height), width=1.0)


    def _draw_value_bar(
        self, label: str, value: float, x: float, y: float, width: float
    ) -> None:
        label_width = min(100.0, width * 0.30)
        bar_x = x + label_width
        bar_width = max(60.0, width - label_width)
        self._draw_text(label, x, y + 12, max(11, int(self.height * 0.020)), (0.78, 0.88, 0.88, 1.0), max_width=label_width - 8)
        Color(0.02, 0.07, 0.08, 1.0)
        Rectangle(pos=(bar_x, y), size=(bar_width, 24))
        Color(0.20, 0.78, 0.43, 1.0)
        Rectangle(pos=(bar_x, y), size=(bar_width * clamp(value / 20.0, 0, 1), 24))
        self._draw_text(f"{value:.1f}/20", bar_x + bar_width / 2, y + 12, max(10, int(self.height * 0.018)), (1, 1, 1, 1), "center", max_width=bar_width - 8)


    def _draw_offers_screen(self) -> None:
        self._draw_text(
            'FIRST CONTRACT',
            self.center_x,
            self.top - 105,
            max(22, int(self.height * 0.040)),
            (0.35, 1.0, 0.66, 1.0),
            "center",
        )
        self._draw_text(
            f"You received {len(self.career.offers)} contract offer(s). Choose your club:",
            self.center_x,
            self.top - 150,
            max(13, int(self.height * 0.023)),
            (0.82, 0.91, 0.91, 1.0),
            "center",
        )
        button_w = min(520.0, self.width * 0.58)
        button_h = min(58.0, self.height * 0.085)
        start_y = self.top - 215
        for index, club in enumerate(self.career.offers):
            self._ui_button(
                club,
                self.center_x - button_w / 2,
                start_y - index * (button_h + 10),
                button_w,
                button_h,
                "accept_offer",
                club,
                accent=index == 0,
            )


    def _open_local_editor(self) -> None:
        """Small local-only editor for club and competition display names."""
        career = self.career
        club = career.club
        if club is None:
            career.message = 'Editor unavailable without an active club.'
            return

        layout = BoxLayout(orientation="vertical", spacing=8, padding=12)
        layout.add_widget(UiLabel(text='Local names — on this device only', size_hint_y=None, height=36))
        club_input = TextInput(text=club.name, multiline=False, hint_text='Club name')
        league_input = TextInput(text=career.current_league.name, multiline=False, hint_text='Competition name')
        layout.add_widget(club_input)
        layout.add_widget(league_input)
        controls = BoxLayout(size_hint_y=None, height=46, spacing=8)
        save_button = Button(text='SAVE')
        cancel_button = Button(text='CANCEL')
        controls.add_widget(save_button)
        controls.add_widget(cancel_button)
        layout.add_widget(controls)
        popup = Popup(title='LOCAL EDITOR', content=layout, size_hint=(0.72, 0.62), auto_dismiss=False)

        def save_names(_button) -> None:
            try:
                career.rename_current_club(club_input.text)
                career.rename_current_competition(league_input.text)
                popup.dismiss()
            except ValueError as exc:
                career.message = f"Invalid name: {exc}."

        save_button.bind(on_release=save_names)
        cancel_button.bind(on_release=lambda _button: popup.dismiss())
        popup.open()


    def _draw_hub_screen(self) -> None:
        career = self.career
        league = career.current_league
        season_text = f"{career.season}/{str(career.season + 1)[-2:]}"
        margin = max(28.0, self.width * 0.035)
        gap = max(14.0, self.width * 0.012)
        content_top = self.top - dp(64)
        content_bottom = self.y + 92
        content_height = content_top - content_bottom
        usable_width = self.width - margin * 2 - gap
        left_width = usable_width * 0.39
        right_width = usable_width - left_width
        left_x = self.x + margin
        right_x = left_x + left_width + gap
        vertical_scale = clamp(content_height / 520.0, 0.68, 1.0)
        self._panel(left_x, content_bottom, left_width, content_height, accent=True)
        self._panel(right_x, content_bottom, right_width, content_height)


        self._draw_text(
            f"{career.player_name.upper()}  |  {career.club_name}",
            left_x + 20,
            content_top - 34 * vertical_scale,
            max(17, int(self.height * 0.031)),
            (0.35, 1.0, 0.66, 1.0),
            max_width=left_width - 40,
        )
        self._draw_text(
            f"{league.name}  |  {career.format_date(career.current_date)}  |  Season {season_text}",
            left_x + 20,
            content_top - 72 * vertical_scale,
            max(12, int(self.height * 0.021)),
            (0.78, 0.88, 0.90, 1.0),
            max_width=left_width - 40,
        )
        bar_width = left_width - 40
        self._draw_value_bar('ENERGY', career.stamina, left_x + 20, content_top - 132 * vertical_scale, bar_width)
        self._draw_value_bar('MORALE', career.morale, left_x + 20, content_top - 174 * vertical_scale, bar_width)
        self._draw_text(
            f"MATCHES  {career.matches:02d}     GOALS  {career.goals:02d}",
            left_x + 20,
            content_top - 222 * vertical_scale,
            max(12, int(self.height * 0.021)),
            (0.90, 0.95, 0.94, 1.0),
            max_width=left_width - 40,
        )
        self._draw_text(
            f"PORTUGAL  {career.international_caps:02d} matches / {career.international_goals:02d} goals",
            left_x + 20,
            content_top - 258 * vertical_scale,
            max(12, int(self.height * 0.021)),
            (0.90, 0.95, 0.94, 1.0),
            max_width=left_width - 40,
        )
        window_text = 'WINDOW OPEN' if career.transfer_window_open else 'WINDOW CLOSED'
        training_text = 'TRAINING COMPLETE' if career.trained_this_week else 'NO TRAINING THIS WEEK'
        self._draw_text(
            f"{window_text}  |  {training_text}",
            left_x + 20,
            content_top - 294 * vertical_scale,
            max(10, int(self.height * 0.018)),
            (0.42, 1.0, 0.69, 1.0) if career.transfer_window_open else (0.72, 0.82, 0.80, 1.0),
            max_width=left_width - 40,
        )


        scheduled = career.next_match()
        if career.called_up:
            next_text = 'NEXT: PORTUGAL - INTERNATIONAL MATCH'
        elif scheduled:
            competition, home, away = scheduled
            prefix = career.cup_name if competition == "cup" else league.name
            next_text = f"NEXT: {prefix} | {home.name}  vs  {away.name}"
        else:
            next_text = 'SEASON COMPLETE'
        self._draw_text('NEXT MATCH', left_x + 20, content_bottom + 100, dp(12), (0.58, 0.72, 0.70, 1.0))
        self._draw_text(next_text.replace('NEXT: ', ""), left_x + 20, content_bottom + 66, max(13, int(self.height * 0.022)), (1.0, 0.86, 0.38, 1.0), max_width=left_width - 40)


        self._draw_text("MENU", right_x + 22, content_top - 34, max(13, int(self.height * 0.022)), (0.62, 0.78, 0.74, 1.0))
        inner_gap = clamp(right_width * 0.018, 12.0, 20.0)
        button_x = right_x + 20
        button_width = (right_width - 40 - inner_gap) / 2
        button_area_top = content_top - 66
        button_area_bottom = content_bottom + 20
        button_height = max(
            54.0,
            (button_area_top - button_area_bottom - inner_gap * 3) / 4,
        )
        row_y = [
            button_area_top - button_height - row * (button_height + inner_gap)
            for row in range(4)
        ]
        self._ui_button('PLAY', button_x, row_y[0], button_width, button_height, "play", accent=True)
        self._ui_button('TRAINING (3 SHOTS)', button_x + button_width + inner_gap, row_y[0], button_width, button_height, "training")
        self._ui_button('STANDINGS', button_x, row_y[1], button_width, button_height, "standings")
        self._ui_button('TOP SCORERS', button_x + button_width + inner_gap, row_y[1], button_width, button_height, "scorers")
        self._ui_button('FIXTURES', button_x, row_y[2], button_width, button_height, "calendar")
        self._ui_button('TALK TO AGENT', button_x + button_width + inner_gap, row_y[2], button_width, button_height, "agent")
        world_label = (
            'WORLD FOOTBALL'
            if self.career.world_unlocked
            else 'SCORER WORLD — LOCKED'
        )
        self._ui_button(world_label, button_x, row_y[3], button_width, button_height, "world")
        self._ui_button('LOCAL EDITOR', button_x + button_width + inner_gap, row_y[3], button_width, button_height, "editor")


        Color(0.02, 0.075, 0.085, 0.92)
        Rectangle(pos=(self.x + margin, self.y + 24), size=(self.width - margin * 2, 50))
        self._draw_text(career.message, self.center_x, self.y + 49, max(11, int(self.height * 0.020)), (0.82, 0.93, 0.90, 1.0), "center", max_width=self.width - margin * 2 - 24)


    def _draw_training_screen(self) -> None:
        panel_width = min(760.0, self.width * 0.72)
        panel_x = self.center_x - panel_width / 2
        panel_top = self.top - 126
        panel_bottom = self.y + 92
        panel_height = panel_top - panel_bottom
        self._draw_text(
            'FINISHING PRACTICE',
            self.center_x,
            self.top - 96,
            dp(20),
            (0.35, 1.0, 0.66, 1.0),
            "center",
        )
        self._panel(panel_x, panel_bottom, panel_width, panel_height, accent=True)


        content_x = panel_x + 42
        content_width = panel_width - 84
        if self.training_completed:
            self._draw_text(
                'TRAINING COMPLETE',
                self.center_x,
                panel_top - 58,
                max(20, int(self.height * 0.036)),
                (1.0, 0.86, 0.38, 1.0),
                "center",
            )
            self._draw_text(
                f"GOALS  {self.training_goals}/3",
                self.center_x,
                panel_top - 112,
                max(16, int(self.height * 0.028)),
                (0.94, 1.0, 0.97, 1.0),
                "center",
            )
            self._draw_text(
                f"STAMINA  {self.training_stamina_before:.1f}  >  {self.career.stamina:.1f}",
                self.center_x,
                panel_top - 154,
                max(14, int(self.height * 0.024)),
                (0.82, 0.93, 0.90, 1.0),
                "center",
            )
            self._draw_value_bar(
                'ENERGY',
                self.career.stamina,
                content_x,
                panel_top - 212,
                content_width,
            )
            self._draw_text(
                f"GAIN  +{self.training_gain:.2f}",
                self.center_x,
                panel_top - 260,
                max(13, int(self.height * 0.023)),
                (0.42, 1.0, 0.69, 1.0),
                "center",
            )
            button_label = 'TRAINING'
        else:
            self._draw_text(
                '3 SHOTS AT GOAL',
                self.center_x,
                panel_top - 62,
                max(20, int(self.height * 0.036)),
                (1.0, 0.86, 0.38, 1.0),
                "center",
            )
            self._draw_text(
                'Take three shots. Training improves energy and goals give a small bonus.',
                self.center_x,
                panel_top - 118,
                max(13, int(self.height * 0.023)),
                (0.82, 0.93, 0.90, 1.0),
                "center",
                max_width=content_width,
            )
            self._draw_value_bar(
                'ENERGY',
                self.career.stamina,
                content_x,
                panel_top - 190,
                content_width,
            )
            self._draw_text(
                'One training session per career week, used when you start.',
                self.center_x,
                panel_top - 242,
                max(12, int(self.height * 0.021)),
                (0.62, 0.78, 0.74, 1.0),
                "center",
                max_width=content_width,
            )
            button_label = 'START TRAINING'


        button_width = min(360.0, panel_width - 84)
        self._ui_button(
            button_label,
            self.center_x - button_width / 2,
            panel_bottom + 34,
            button_width,
            58,
            "training_start",
            accent=True,
        )
        self._ui_button(
            'BACK',
            self.x + max(30.0, self.width * 0.055),
            self.y + 24,
            150,
            48,
            "hub",
        )


    def _draw_standings_screen(self) -> None:
        league = self.career.current_league
        table = league.table()
        start = self.table_page * 11
        rows = table[start:start + 11]
        self._draw_text(f"STANDINGS  -  {league.name}", self.center_x, self.top - 95, max(18, int(self.height * 0.032)), (0.35, 1.0, 0.66, 1.0), "center")
        margin = max(32.0, self.width * 0.055)
        panel_x = self.x + margin
        panel_width = self.width - margin * 2
        panel_top = self.top - 126
        panel_bottom = self.y + 90
        self._panel(panel_x, panel_bottom, panel_width, panel_top - panel_bottom)
        header_y = panel_top - 25
        Color(0.045, 0.17, 0.17, 1.0)
        Rectangle(pos=(panel_x, panel_top - 50), size=(panel_width, 50))
        number_columns = (0.56, 0.62, 0.68, 0.74, 0.80, 0.86, 0.92, 0.975)
        headers = ('P', 'W', 'D', 'L', 'GF', 'GA', 'GD', "PTS")
        self._draw_text("POS", panel_x + panel_width * 0.040, header_y, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0), "center")
        self._draw_text('CLUB', panel_x + panel_width * 0.075, header_y, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0))
        for fraction, header in zip(number_columns, headers):
            self._draw_text(header, panel_x + panel_width * fraction, header_y, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0), "center")
        row_height = (panel_top - panel_bottom - 50) / 11
        for offset, club in enumerate(rows):
            position = start + offset + 1
            is_player = club.name == self.career.club_name
            row_y = panel_top - 50 - (offset + 1) * row_height
            if is_player:
                Color(0.08, 0.34, 0.24, 0.90)
                Rectangle(pos=(panel_x + 1, row_y), size=(panel_width - 2, row_height))
            elif offset % 2:
                Color(0.04, 0.115, 0.12, 0.72)
                Rectangle(pos=(panel_x + 1, row_y), size=(panel_width - 2, row_height))
            center_y = row_y + row_height / 2
            color = (0.42, 1.0, 0.69, 1.0) if is_player else (0.90, 0.95, 0.94, 1.0)
            font = max(9, int(self.height * 0.0175))
            self._draw_text(f"{position:02d}", panel_x + panel_width * 0.040, center_y, font, color, "center")
            self._draw_text(club.name, panel_x + panel_width * 0.075, center_y, font, color, max_width=panel_width * 0.455)
            values = (club.played, club.won, club.drawn, club.lost, club.goals_for, club.goals_against, f"{club.goal_difference:+d}", club.points)
            for fraction, value in zip(number_columns, values):
                self._draw_text(str(value), panel_x + panel_width * fraction, center_y, font, color, "center", max_width=panel_width * 0.05)
        button_y = self.y + 24
        self._ui_button('BACK', self.x + margin, button_y, 150, 48, "hub")
        self._ui_button("<", self.right - margin - 180, button_y, 80, 48, "table_prev")
        self._ui_button(">", self.right - margin - 80, button_y, 80, 48, "table_next")


    def _draw_scorers_screen(self) -> None:
        league = self.career.current_league
        scorers = dict(league.scorer_goals)
        scorers[self.career.player_name] = self.career.goals
        ranking = sorted(scorers.items(), key=lambda item: (item[1], item[0]), reverse=True)[:12]
        self._draw_text(f"TOP SCORERS  -  {league.name}", self.center_x, self.top - 95, max(18, int(self.height * 0.032)), (0.35, 1.0, 0.66, 1.0), "center")
        panel_width = min(self.width * 0.68, 850.0)
        panel_x = self.center_x - panel_width / 2
        panel_top = self.top - 126
        panel_bottom = self.y + 90
        self._panel(panel_x, panel_bottom, panel_width, panel_top - panel_bottom)
        Color(0.045, 0.17, 0.17, 1.0)
        Rectangle(pos=(panel_x, panel_top - 46), size=(panel_width, 46))
        self._draw_text("POS", panel_x + panel_width * 0.08, panel_top - 23, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0), "center")
        self._draw_text('PLAYER / CLUB', panel_x + panel_width * 0.16, panel_top - 23, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0))
        self._draw_text('GOALS', panel_x + panel_width * 0.92, panel_top - 23, max(10, int(self.height * 0.018)), (0.65, 0.78, 0.79, 1.0), "center")
        if not ranking:
            self._draw_text('The season has not started yet.', self.center_x, self.center_y, max(16, int(self.height * 0.028)), (0.85, 0.92, 0.91, 1.0), "center")
        row_height = (panel_top - panel_bottom - 46) / 12
        for index, (name, goals) in enumerate(ranking):
            is_player = name == self.career.player_name
            row_y = panel_top - 46 - (index + 1) * row_height
            if is_player:
                Color(0.08, 0.34, 0.24, 0.90)
                Rectangle(pos=(panel_x + 1, row_y), size=(panel_width - 2, row_height))
            elif index % 2:
                Color(0.04, 0.115, 0.12, 0.72)
                Rectangle(pos=(panel_x + 1, row_y), size=(panel_width - 2, row_height))
            center_y = row_y + row_height / 2
            color = (0.42, 1.0, 0.69, 1.0) if is_player else (0.90, 0.95, 0.94, 1.0)
            font = max(9, int(self.height * 0.018))
            self._draw_text(f"{index + 1:02d}", panel_x + panel_width * 0.08, center_y, font, color, "center")
            self._draw_text(name, panel_x + panel_width * 0.16, center_y, font, color, max_width=panel_width * 0.66)
            self._draw_text(f"{goals:02d}", panel_x + panel_width * 0.92, center_y, font, color, "center")
        self._ui_button('BACK', self.x + max(30.0, self.width * 0.055), self.y + 24, 150, 48, "hub")


    def _draw_calendar_screen(self) -> None:
        entries = self.career.calendar_entries()
        self._draw_text(
            f"FIXTURES  |  {self.career.format_date(self.career.current_date)}",
            self.center_x,
            self.top - 95,
            dp(20),
            (0.35, 1.0, 0.66, 1.0),
            "center",
        )
        margin = max(32.0, self.width * 0.050)
        panel_x = self.x + margin
        panel_width = self.width - margin * 2
        panel_top = self.top - 126
        panel_bottom = self.y + 90
        self._panel(panel_x, panel_bottom, panel_width, panel_top - panel_bottom)
        Color(0.045, 0.17, 0.17, 1.0)
        Rectangle(pos=(panel_x, panel_top - 46), size=(panel_width, 46))
        columns = (0.08, 0.25, 0.49, 0.92)
        for fraction, label, anchor in (
            (columns[0], 'DATE', "center"),
            (columns[1], 'COMPETITION', "center"),
            (columns[2], 'MATCH', "center"),
            (columns[3], 'STATUS', "center"),
        ):
            self._draw_text(
                label,
                panel_x + panel_width * fraction,
                panel_top - 23,
                max(10, int(self.height * 0.018)),
                (0.65, 0.78, 0.79, 1.0),
                anchor,
            )
        visible = entries[-12:]
        row_height = (panel_top - panel_bottom - 46) / max(12, len(visible))
        for index, entry in enumerate(visible):
            row_y = panel_top - 46 - (index + 1) * row_height
            played = bool(entry.get("played", False))
            if index % 2:
                Color(0.04, 0.115, 0.12, 0.72)
                Rectangle(pos=(panel_x + 1, row_y), size=(panel_width - 2, row_height))
            center_y = row_y + row_height / 2
            try:
                shown_date = self.career.format_date(
                    date.fromisoformat(str(entry.get("date", "")))
                )
            except ValueError:
                shown_date = str(entry.get("date", ""))
            match_text = f"{entry.get('home', '')}  vs  {entry.get('away', '')}"
            color = (0.62, 0.78, 0.74, 1.0) if played else (0.92, 0.97, 0.95, 1.0)
            font = max(9, int(self.height * 0.017))
            self._draw_text(shown_date, panel_x + panel_width * columns[0], center_y, font, color, "center", max_width=panel_width * 0.14)
            self._draw_text(str(entry.get("competition", "")), panel_x + panel_width * columns[1], center_y, font, color, "center", max_width=panel_width * 0.20)
            self._draw_text(match_text, panel_x + panel_width * columns[2], center_y, font, color, "center", max_width=panel_width * 0.42)
            self._draw_text(str(entry.get("status", "")), panel_x + panel_width * columns[3], center_y, font, color, "center", max_width=panel_width * 0.13)
        self._ui_button('BACK', self.x + margin, self.y + 24, 150, 48, "hub")


    def _draw_agent_screen(self) -> None:
        window_state = 'WINDOW OPEN' if self.career.transfer_window_open else 'WINDOW CLOSED'
        self._draw_text(f"TALK TO AGENT  |  {window_state}", self.center_x, self.top - 95, dp(20), (0.35, 1.0, 0.66, 1.0), "center")
        panel_width = min(680.0, self.width * 0.66)
        panel_x = self.center_x - panel_width / 2
        panel_top = self.top - 125
        panel_bottom = self.y + 90
        self._panel(panel_x, panel_bottom, panel_width, panel_top - panel_bottom)
        Color(0.045, 0.17, 0.17, 1.0)
        Rectangle(pos=(panel_x, panel_top - 52), size=(panel_width, 52))
        self._draw_text(self.career.message, self.center_x, panel_top - 26, max(12, int(self.height * 0.022)), (0.83, 0.91, 0.91, 1.0), "center", max_width=panel_width - 30)
        bw = panel_width - 40
        bh = min(56.0, self.height * 0.078)
        for index, (club_name, league_key) in enumerate(self.career.agent_offers[:5]):
            league = self.career.leagues[league_key]
            label = f"{club_name}  -  {league.name} ({league.country})"
            self._ui_button(label, panel_x + 20, panel_top - 75 - bh - index * (bh + 8), bw, bh, "transfer", (club_name, league_key), accent=index == 0)
        margin = max(30.0, self.width * 0.055)
        self._ui_button('BACK', self.x + margin, self.y + 24, 150, 48, "hub")
        refresh_label = 'FIND NEW OFFERS' if self.career.transfer_window_open else 'JUL–AUG / JAN–FEB'
        self._ui_button(refresh_label, self.right - margin - 300, self.y + 24, 300, 48, "agent_refresh")


    def _draw_world_screen(self) -> None:
        league_count = len(self.career.leagues)
        self._draw_text(
            f"WORLD FOOTBALL  |  {len(WORLD_COUNTRIES)} associations  |  {league_count} leagues",
            self.center_x,
            self.top - 92,
            max(16, int(self.height * 0.029)),
            (0.35, 1.0, 0.66, 1.0),
            "center",
        )
        margin = max(32.0, self.width * 0.055)
        gap = max(16.0, self.width * 0.018)
        panel_width = (self.width - margin * 2 - gap) / 2
        panel_top = self.top - 125
        panel_bottom = self.y + 90
        x_left = self.x + margin
        x_right = x_left + panel_width + gap
        self._panel(x_left, panel_bottom, panel_width, panel_top - panel_bottom)
        self._panel(x_right, panel_bottom, panel_width, panel_top - panel_bottom)
        Color(0.045, 0.17, 0.17, 1.0)
        Rectangle(pos=(x_left, panel_top - 48), size=(panel_width, 48))
        Rectangle(pos=(x_right, panel_top - 48), size=(panel_width, 48))
        self._draw_text('INTERNATIONAL COMPETITIONS', x_left + 18, panel_top - 24, max(13, int(self.height * 0.023)), (1.0, 0.86, 0.38, 1.0), max_width=panel_width - 36)
        for index, (name, status) in enumerate(self.career.international_status.items()):
            row_y = panel_top - 76 - index * self.height * 0.062
            self._draw_text(name, x_left + 18, row_y, max(9, int(self.height * 0.017)), (0.62, 0.78, 0.74, 1.0), max_width=panel_width * 0.46)
            self._draw_text(status, x_left + panel_width - 18, row_y, max(9, int(self.height * 0.017)), (0.88, 0.94, 0.93, 1.0), "right", max_width=panel_width * 0.47)
        cup_row_y = panel_top - 76 - len(self.career.international_status) * self.height * 0.062
        cup_winner = self.career.national_cup_winners.get(self.career.current_league.country)
        if cup_winner:
            cup_status = f"Last winner: {cup_winner}"
        elif self.career.cup_active:
            cup_status = self.career.cup_round_label
        else:
            cup_status = 'Eliminated'
        self._draw_text(self.career.cup_name, x_left + 18, cup_row_y, max(9, int(self.height * 0.017)), (0.62, 0.78, 0.74, 1.0), max_width=panel_width * 0.46)
        self._draw_text(cup_status, x_left + panel_width - 18, cup_row_y, max(9, int(self.height * 0.017)), (0.88, 0.94, 0.93, 1.0), "right", max_width=panel_width * 0.47)


        self._draw_text('EUROPEAN LEAGUE PYRAMIDS', x_right + 18, panel_top - 24, max(13, int(self.height * 0.023)), (1.0, 0.86, 0.38, 1.0), max_width=panel_width - 36)
        start = self.world_page * 9
        for index, country in enumerate(EUROPE_COUNTRIES[start:start + 9]):
            depth = EUROPE_PYRAMID_DEPTH[country]
            row_y = panel_top - 76 - index * self.height * 0.050
            self._draw_text(country, x_right + 18, row_y, max(9, int(self.height * 0.017)), (0.88, 0.94, 0.93, 1.0), max_width=panel_width * 0.65)
            self._draw_text(f"{depth} divisions", x_right + panel_width - 18, row_y, max(9, int(self.height * 0.017)), (0.62, 0.78, 0.74, 1.0), "right", max_width=panel_width * 0.28)
        self._ui_button('BACK', self.x + margin, self.y + 24, 150, 48, "hub")
        self._ui_button("<", self.right - margin - 180, self.y + 24, 80, 48, "world_prev")
        self._ui_button(">", self.right - margin - 80, self.y + 24, 80, 48, "world_next")


    def _scoreboard_bounds(self):
        return (self.x + dp(8), self.top - dp(54),
                min(dp(280), self.width - dp(16)), dp(46))

    def _shot_timer_bounds(self):
        x, y, width, _ = self._scoreboard_bounds()
        height = dp(22)
        return x, y - height, width, height

    def _draw_match_overlay(self) -> None:
        if self.match_home is None or self.match_away is None:
            return
        x, y, width, height = self._scoreboard_bounds()
        teams_width = width * 0.68
        remaining = max(0.0, self.scoreboard_flash_until - self.elapsed)
        pulse = math.sin(math.pi * min(1.0, remaining))
        Color(0.015 + pulse * 0.08, 0.04 + pulse * 0.32, 0.05 + pulse * 0.16, 0.96)
        Rectangle(pos=(x, y), size=(width, height))
        Color(0.30, 0.90, 0.65, 0.65 + pulse * 0.35)
        Line(rectangle=(x, y, width, height), width=1.0)
        Line(points=[x + teams_width, y, x + teams_width, y + height], width=1)
        for club, score, row in ((self.match_home, self.match_home_score, 0.73),
                                 (self.match_away, self.match_away_score, 0.27)):
            cy = y + height * row
            self._draw_club_badge(club.name, x + dp(12), cy, dp(15))
            self._draw_text(club.name, x + dp(24), cy, dp(11),
                            (0.94, 0.98, 0.97, 1), max_width=teams_width - dp(50))
            self._draw_text(str(score), x + teams_width - dp(14), cy, dp(14),
                            (0.36, 1.0, 0.66, 1), "center", max_width=dp(24))
        clock_x = x + teams_width + (width - teams_width) / 2
        self._draw_text(self.match_clock_text, clock_x, y + height * 0.64, dp(13),
                        (1.0, 0.91, 0.65, 1), "center", max_width=width - teams_width - dp(8))
        status = "Full time" if self.match_finished else "Half time" if self.match_halftime else "First half" if self.match_half == 1 else "Second half"
        self._draw_text(status, clock_x, y + height * 0.26, dp(9),
                        (0.65, 0.81, 0.80, 1), "center")


    def _ensure_static_layers(self) -> None:
        """Guarda apenas o cenário opaco numa textura reutilizável."""
        if self._fbo_disabled or self.width < 2.0 or self.height < 2.0:
            return
        key = (self.x, self.y, self.width, self.height)
        if key == self._static_layer_key:
            return


        try:
            fbo_size = (max(2, int(self.width)), max(2, int(self.height)))
            static_fbo = Fbo(size=fbo_size, with_stencilbuffer=False)
            with static_fbo:
                ClearColor(0.0, 0.0, 0.0, 0.0)
                ClearBuffers()
                PushMatrix()
                Translate(-self.x, -self.y, 0.0)
                self._draw_background()
                self._draw_stadium_stands(draw_crowd=False)
                PopMatrix()
            static_fbo.draw()


            self._static_fbo = static_fbo
            self._static_layer_key = key
        except Exception:
            # Pydroid/Kivy antigos podem não ter FBO funcional. O jogo mantém
            # o desenho normal em vez de falhar no arranque.
            self._static_fbo = None
            self._fbo_disabled = True


    def _draw_background(self) -> None:
        Color(0.025, 0.055, 0.075, 1.0)
        Rectangle(pos=self.pos, size=self.size)


        # Bancada distante estilizada.
        Color(0.06, 0.10, 0.13, 1.0)
        Rectangle(pos=(self.x, self.y + self.height * 0.68), size=(self.width, self.height * 0.32))
        Color(0.11, 0.18, 0.20, 1.0)
        for row in range(4):
            yy = self.y + self.height * (0.72 + row * 0.055)
            Line(points=[self.x, yy, self.right, yy], width=1.0)


    def _draw_stadium_stands(self, draw_crowd: bool = True) -> None:
        """Bancada oposta composta por degraus tridimensionais reais."""
        cache_key = (self.x, self.y, self.width, self.height)
        rebuild = (
            cache_key != self._stand_mesh_cache_key
            or cache_key != self._crowd_mesh_cache_key
        )
        if rebuild:
            self._crowd_specs = []
            self._stand_mesh_builders = {}


            # Cada fila é geometria 3D real: espelho vertical e patamar
            # horizontal. A geometria é calculada só quando o ecrã muda.
            self._stand_cache_section = "goal"
            self._draw_behind_goal_stand()
            self._stand_cache_section = "corner"
            self._draw_corner_stands((1.0,))
            self._stand_cache_section = "side"
            self._draw_touchline_stand(1.0)


            self._stand_mesh_cache = [
                (color, vertices, indices)
                for (_, color), (vertices, indices) in (
                    self._stand_mesh_builders or {}
                ).items()
                if indices
            ]
            self._stand_mesh_builders = None
            self._stand_mesh_cache_key = cache_key
            self._rebuild_crowd_mesh(self._crowd_specs or [])
            self._crowd_mesh_cache_key = cache_key
            self._crowd_specs = None


        self._draw_stand_meshes()


        if draw_crowd:
            self._draw_crowd_meshes(celebrating=self.result_text == "GOAL!")


    def _draw_stand_meshes(self) -> None:
        """Desenha toda a bancada em poucos lotes gráficos já projetados."""
        for color, vertices, indices in self._stand_mesh_cache:
            Color(*color)
            Mesh(vertices=vertices, indices=indices, mode="triangles")


    def _draw_continuous_grandstand(self) -> None:
        """Bancada coberta, com degraus legíveis e seis sectores regulares."""
        left = self.x - 8.0
        right = self.right + 8.0
        width = right - left


        # O topo e a frente convergem suavemente para a direita, de acordo com
        # as linhas do campo, mas sem a inclinação exagerada da versão anterior.
        back_left = self.y + self.height * 0.790
        back_right = self.y + self.height * 0.715
        front_left = self.y + self.height * 0.590
        front_right = self.y + self.height * 0.445


        back_l = (left, back_left)
        back_r = (right, back_right)
        front_l = (left, front_left)
        front_r = (right, front_right)


        Color(*STAND_CONCRETE)
        Triangle(points=[*back_l, *back_r, *front_r])
        Triangle(points=[*back_l, *front_r, *front_l])


        # Cobertura independente e fina. É estruturalmente escura, mas não
        # divide o betão da bancada em tons diferentes.
        roof_l = (left, back_left + self.height * 0.026)
        roof_r = (right, back_right + self.height * 0.026)
        Color(*STAND_ROOF)
        Triangle(points=[*roof_l, *roof_r, *back_r])
        Triangle(points=[*roof_l, *back_r, *back_l])


        def row_y(screen_x: float, amount: float) -> float:
            horizontal = clamp((screen_x - left) / width, 0.0, 1.0)
            back = back_left + (back_right - back_left) * horizontal
            front = front_left + (front_right - front_left) * horizontal
            return back + (front - back) * amount


        # Arestas horizontais dos degraus: finas, regulares e sem blocos.
        Color(*STAND_EDGE)
        for row in range(STAND_ROWS + 1):
            amount = row / STAND_ROWS
            Line(
                points=[left, row_y(left, amount), right, row_y(right, amount)],
                width=0.78,
            )


        # Escadas reais: pequenos patamares em cada fila. Não há linhas
        # verticais contínuas que possam parecer pilares.
        Color(*STAND_RAIL)
        for sector in range(1, 6):
            aisle_x = left + width * sector / 6.0
            for row in range(STAND_ROWS):
                amount = (row + 0.76) / STAND_ROWS
                step_y = row_y(aisle_x, amount)
                Line(
                    points=[aisle_x - 4.6, step_y, aisle_x + 4.6, step_y],
                    width=0.82,
                )


        # Corrimão frontal e cobertura superior muito fina.
        Line(points=[*front_l, *front_r], width=1.45)
        Line(points=[*back_l, *back_r], width=1.65)


        if self._crowd_specs is None:
            return


        columns_per_sector = 18
        for row in range(STAND_ROWS):
            amount = (row + 0.48) / STAND_ROWS
            person_height = self.height * (0.0086 + amount * 0.0062)
            for sector in range(6):
                sector_left = left + width * sector / 6.0
                sector_right = left + width * (sector + 1) / 6.0
                margin = width * 0.0105
                for column in range(columns_per_sector):
                    fraction = (column + 0.5) / columns_per_sector
                    screen_x = (
                        sector_left
                        + margin
                        + fraction * (sector_right - sector_left - 2.0 * margin)
                    )
                    code = row * 193 + sector * 47 + column * 29
                    # Falhas pequenas e determinísticas deixam o público
                    # natural sem criar manchas vazias ou listas coloridas.
                    if code % 23 in (0, 1) or code % 47 == 7:
                        continue
                    jitter_x = ((code * 7) % 5 - 2) * self.width * 0.00028
                    jitter_y = ((code * 11) % 5 - 2) * self.height * 0.00023
                    screen_y = row_y(screen_x, amount) + jitter_y
                    self._crowd_specs.append(
                        (screen_x + jitter_x, screen_y, person_height, code, True)
                    )


    def _draw_crowd_meshes(self, celebrating: bool) -> None:
        """Desenha o público já agrupado em poucos lotes gráficos."""
        for color, vertices, indices, jump_group in self._crowd_mesh_cache:
            Color(*color)
            jump = 0.0
            if celebrating:
                phase = self.state_age * 11.5 + jump_group * 1.25
                jump = max(0.0, math.sin(phase)) * (7.0 + jump_group * 1.4)
            if jump > 0.0:
                PushMatrix()
                Translate(0.0, jump, 0.0)
                Mesh(vertices=vertices, indices=indices, mode="triangles")
                PopMatrix()
            else:
                Mesh(vertices=vertices, indices=indices, mode="triangles")


    def _draw_spectator(
        self,
        world_x: float,
        world_y: float,
        seat_z: float,
        color_index: int,
    ) -> None:
        """Adiciona um adepto à lista estática usada pelo desenho em lote."""
        if self._crowd_specs is not None:
            self._crowd_specs.append((world_x, world_y, seat_z, color_index))


    @staticmethod
    def _append_mesh_quad(
        vertices: list[float],
        indices: list[int],
        points: tuple[
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
        ],
    ) -> None:
        base = len(vertices) // 4
        for x, y in points:
            vertices.extend((x, y, 0.0, 0.0))
        indices.extend((base, base + 1, base + 2, base, base + 2, base + 3))


    def _cache_stand_quad(
        self,
        color: tuple[float, float, float, float],
        points: tuple[
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
            tuple[float, float],
        ],
    ) -> None:
        """Acrescenta uma face ao lote estático da secção atual."""
        if self._stand_mesh_builders is None:
            return
        key = (self._stand_cache_section, color)
        vertices, indices = self._stand_mesh_builders.setdefault(key, ([], []))
        self._append_mesh_quad(vertices, indices, points)


    def _cache_stand_segment(
        self,
        color: tuple[float, float, float, float],
        start: tuple[float, float],
        end: tuple[float, float],
        width: float,
    ) -> None:
        """Converte uma aresta fina num quadrilátero do mesmo lote gráfico."""
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        length = math.hypot(delta_x, delta_y)
        if length < 1e-6:
            return
        half = max(0.38, width * 0.50)
        normal_x = -delta_y / length * half
        normal_y = delta_x / length * half
        self._cache_stand_quad(
            color,
            (
                (start[0] - normal_x, start[1] - normal_y),
                (start[0] + normal_x, start[1] + normal_y),
                (end[0] + normal_x, end[1] + normal_y),
                (end[0] - normal_x, end[1] - normal_y),
            ),
        )


    def _cache_stand_world_polyline(
        self,
        color: tuple[float, float, float, float],
        points: Iterable[tuple[float, float, float]],
        width: float,
    ) -> None:
        projected = [self.project(*point) for point in points]
        for start, end in zip(projected, projected[1:]):
            self._cache_stand_segment(color, start, end, width)


    def _rebuild_crowd_mesh(
        self,
        spectators: list[tuple],
    ) -> None:
        """Agrupa os adeptos em poucos lotes gráficos por fase de salto."""
        shirts = (
            (0.78, 0.16, 0.12, 0.96),
            (0.12, 0.34, 0.62, 0.96),
            (0.88, 0.66, 0.12, 0.96),
            (0.76, 0.78, 0.74, 0.94),
            (0.16, 0.48, 0.27, 0.95),
            (0.42, 0.20, 0.48, 0.95),
        )
        skins = (
            (0.94, 0.72, 0.52, 0.96),
            (0.72, 0.46, 0.29, 0.96),
            (0.45, 0.27, 0.18, 0.96),
        )
        jump_groups = 4
        shirt_vertices = [[[] for _ in shirts] for _ in range(jump_groups)]
        shirt_indices = [[[] for _ in shirts] for _ in range(jump_groups)]
        skin_vertices = [[[] for _ in skins] for _ in range(jump_groups)]
        skin_indices = [[[] for _ in skins] for _ in range(jump_groups)]


        visible = 0
        for spectator in spectators:
            if len(spectator) == 5:
                screen_x, screen_y, person_height, color_index, _ = spectator
                body_bottom = (screen_x, screen_y)
                body_top = (screen_x, screen_y + person_height * 0.56)
                head = (screen_x, screen_y + person_height * 0.78)
                half_width = clamp(person_height * 0.17, 1.05, 2.15)
                radius = clamp(person_height * 0.135, 1.05, 2.25)
            else:
                world_x, world_y, seat_z, color_index = spectator
                body_bottom = self.project(world_x, world_y, seat_z + 0.05)
                body_top = self.project(world_x, world_y, seat_z + 0.29)
                head = self.project(world_x, world_y, seat_z + 0.38)
                scale = self.pixels_per_meter(world_x, world_y, seat_z + 0.2)
                half_width = clamp(scale * 0.041, 0.82, 1.95)
                radius = clamp(scale * 0.062, 1.38, 3.05)
            if not (
                self.x - 8.0 <= head[0] <= self.right + 8.0
                and self.y - 8.0 <= head[1] <= self.top + 8.0
            ):
                continue


            visible += 1
            delta_x = body_top[0] - body_bottom[0]
            delta_y = body_top[1] - body_bottom[1]
            body_length = max(1e-6, math.hypot(delta_x, delta_y))
            normal_x = -delta_y / body_length * half_width
            normal_y = delta_x / body_length * half_width
            jump_group = color_index % jump_groups
            shirt_index = color_index % len(shirts)
            self._append_mesh_quad(
                shirt_vertices[jump_group][shirt_index],
                shirt_indices[jump_group][shirt_index],
                (
                    (body_bottom[0] - normal_x, body_bottom[1] - normal_y),
                    (body_bottom[0] + normal_x, body_bottom[1] + normal_y),
                    (body_top[0] + normal_x, body_top[1] + normal_y),
                    (body_top[0] - normal_x, body_top[1] - normal_y),
                ),
            )
            skin_index = (color_index // 2) % len(skins)
            self._append_mesh_quad(
                skin_vertices[jump_group][skin_index],
                skin_indices[jump_group][skin_index],
                (
                    (head[0] - radius, head[1] - radius),
                    (head[0] + radius, head[1] - radius),
                    (head[0] + radius, head[1] + radius),
                    (head[0] - radius, head[1] + radius),
                ),
            )


        self.crowd_total = len(spectators)
        self.crowd_visible = visible
        self._crowd_mesh_cache = []
        for jump_group in range(jump_groups):
            for color, vertices, indices in zip(
                shirts,
                shirt_vertices[jump_group],
                shirt_indices[jump_group],
            ):
                if indices:
                    self._crowd_mesh_cache.append(
                        (color, vertices, indices, jump_group)
                    )
            for color, vertices, indices in zip(
                skins,
                skin_vertices[jump_group],
                skin_indices[jump_group],
            ):
                if indices:
                    self._crowd_mesh_cache.append(
                        (color, vertices, indices, jump_group)
                    )


    def _draw_behind_goal_stand(self) -> None:
        """Bancada de fundo contínua, dividida em seis sectores regulares."""
        stand_left = -STAND_CORNER_X
        stand_right = STAND_CORNER_X
        aisle_centers = (-24.0, -12.0, 0.0, 12.0, 24.0)
        aisle_half_width = 0.72


        for row in reversed(range(STAND_ROWS)):
            near_y = STAND_FRONT_Y - row * STAND_ROW_DEPTH
            far_y = near_y - STAND_TREAD_DEPTH
            seat_z = 0.30 + row * STAND_ROW_RISE
            previous_z = max(0.0, seat_z - 0.38)


            near_left = self.project(stand_left, near_y, seat_z)
            near_right = self.project(stand_right, near_y, seat_z)
            far_left = self.project(stand_left, far_y, seat_z)
            far_right = self.project(stand_right, far_y, seat_z)
            lower_left = self.project(stand_left, near_y, previous_z)
            lower_right = self.project(stand_right, near_y, previous_z)


            # Espelho vertical escuro e patamar horizontal claro.
            self._cache_stand_quad(
                STAND_RISER,
                (lower_left, lower_right, near_right, near_left),
            )
            self._cache_stand_quad(
                STAND_TREAD,
                (near_left, near_right, far_right, far_left),
            )
            self._cache_stand_segment(
                STAND_EDGE, near_left, near_right, 0.92
            )


            # As escadas são marcadas pelas arestas e pela ausência de público.
            for aisle_x in aisle_centers:
                stair_left = self.project(
                    aisle_x - aisle_half_width, near_y, seat_z + 0.015
                )
                stair_right = self.project(
                    aisle_x + aisle_half_width, near_y, seat_z + 0.015
                )
                self._cache_stand_segment(
                    STAND_RAIL, stair_left, stair_right, 0.88
                )


            if self._crowd_specs is not None:
                spectator_y = near_y - 0.43
                columns = 184
                for column in range(columns):
                    world_x = -34.5 + column * (69.0 / (columns - 1))
                    if any(
                        abs(world_x - aisle_x) < aisle_half_width + 0.22
                        for aisle_x in aisle_centers
                    ):
                        continue
                    # Pequenas falhas regulares quebram o antigo efeito de
                    # faixas coloridas sem tornar o público demasiado vazio.
                    if (column * 7 + row * 11) % 29 in (0, 1, 2):
                        continue
                    self._draw_spectator(
                        world_x,
                        spectator_y,
                        seat_z,
                        column * 7 + row * 23,
                    )


        rail_z = 0.30 + (STAND_ROWS - 1) * STAND_ROW_RISE + 0.62
        rail_y = (
            STAND_FRONT_Y
            - (STAND_ROWS - 1) * STAND_ROW_DEPTH
            - STAND_TREAD_DEPTH * 0.52
        )
        self._cache_stand_world_polyline(
            STAND_RAIL,
            [(stand_left, rail_y, rail_z), (stand_right, rail_y, rail_z)],
            1.45,
        )


    def _draw_corner_stands(
        self,
        sides: tuple[float, ...] = (-1.0, 1.0),
    ) -> None:
        """Cantos curvos que ligam o fundo às laterais sem sobreposições."""
        arc_segments = 12
        half_pi = math.pi * 0.5


        for side in sides:
            for row in reversed(range(STAND_ROWS)):
                inner_radius = row * STAND_ROW_DEPTH
                outer_radius = inner_radius + STAND_TREAD_DEPTH
                seat_z = 0.30 + row * STAND_ROW_RISE
                previous_z = max(0.0, seat_z - 0.38)


                for segment in range(arc_segments):
                    angle_0 = segment * half_pi / arc_segments
                    angle_1 = (segment + 1) * half_pi / arc_segments


                    def corner_point(
                        radius: float,
                        angle: float,
                        z: float,
                    ) -> tuple[float, float]:
                        return self.project(
                            side * (STAND_CORNER_X + radius * math.cos(angle)),
                            STAND_FRONT_Y - radius * math.sin(angle),
                            z,
                        )


                    inner_0 = corner_point(inner_radius, angle_0, seat_z)
                    inner_1 = corner_point(inner_radius, angle_1, seat_z)
                    outer_0 = corner_point(outer_radius, angle_0, seat_z)
                    outer_1 = corner_point(outer_radius, angle_1, seat_z)
                    low_0 = corner_point(inner_radius, angle_0, previous_z)
                    low_1 = corner_point(inner_radius, angle_1, previous_z)


                    self._cache_stand_quad(
                        STAND_RISER,
                        (low_0, low_1, inner_1, inner_0),
                    )
                    self._cache_stand_quad(
                        STAND_TREAD,
                        (inner_0, inner_1, outer_1, outer_0),
                    )
                    self._cache_stand_segment(
                        STAND_EDGE, inner_0, inner_1, 0.88
                    )


                # Escada central no canto, alinhada em todas as filas.
                aisle_angle = math.pi * 0.25
                aisle_inner = corner_point(
                    inner_radius, aisle_angle, seat_z + 0.015
                )
                aisle_outer = corner_point(
                    outer_radius, aisle_angle, seat_z + 0.015
                )
                self._cache_stand_segment(
                    STAND_RAIL, aisle_inner, aisle_outer, 0.90
                )


                if self._crowd_specs is not None:
                    places = 15 + row * 3
                    spectator_radius = inner_radius + STAND_TREAD_DEPTH * 0.48
                    for place in range(places):
                        angle = (place + 0.5) * half_pi / places
                        if abs(angle - aisle_angle) < 0.075:
                            continue
                        if (place * 5 + row * 13) % 31 in (0, 1):
                            continue
                        world_x = side * (
                            STAND_CORNER_X
                            + spectator_radius * math.cos(angle)
                        )
                        world_y = (
                            STAND_FRONT_Y
                            - spectator_radius * math.sin(angle)
                        )
                        self._draw_spectator(
                            world_x,
                            world_y,
                            seat_z,
                            place * 11 + row * 19 + (3 if side > 0 else 0),
                        )


            rail_radius = (
                (STAND_ROWS - 1) * STAND_ROW_DEPTH
                + STAND_TREAD_DEPTH * 0.52
            )
            rail_z = 0.30 + (STAND_ROWS - 1) * STAND_ROW_RISE + 0.62
            rail_points = []
            for segment in range(19):
                angle = segment * half_pi / 18.0
                rail_points.append(
                    (
                        side * (
                            STAND_CORNER_X
                            + rail_radius * math.cos(angle)
                        ),
                        STAND_FRONT_Y - rail_radius * math.sin(angle),
                        rail_z,
                    )
                )
            self._cache_stand_world_polyline(
                STAND_RAIL, rail_points, 1.42
            )


    def _draw_touchline_stand(self, side: float) -> None:
        """Bancada lateral com os mesmos módulos da bancada de fundo."""
        sections = 6
        y_start = STAND_FRONT_Y
        y_end = 41.5
        section_length = (y_end - y_start) / sections
        aisle_centers = tuple(
            y_start + section * section_length
            for section in range(1, sections)
        )
        aisle_half_width = 0.64


        for row in reversed(range(STAND_ROWS)):
            inner_distance = row * STAND_ROW_DEPTH
            outer_distance = inner_distance + STAND_TREAD_DEPTH
            inner_x = side * (STAND_CORNER_X + inner_distance)
            outer_x = side * (STAND_CORNER_X + outer_distance)
            seat_z = 0.30 + row * STAND_ROW_RISE
            previous_z = max(0.0, seat_z - 0.38)


            low_0 = self.project(inner_x, y_start, previous_z)
            low_1 = self.project(inner_x, y_end, previous_z)
            inner_0 = self.project(inner_x, y_start, seat_z)
            inner_1 = self.project(inner_x, y_end, seat_z)
            outer_0 = self.project(outer_x, y_start, seat_z)
            outer_1 = self.project(outer_x, y_end, seat_z)


            self._cache_stand_quad(
                STAND_RISER,
                (low_0, low_1, inner_1, inner_0),
            )
            self._cache_stand_quad(
                STAND_TREAD,
                (inner_0, inner_1, outer_1, outer_0),
            )


            self._cache_stand_world_polyline(
                STAND_EDGE,
                [(inner_x, y_start, seat_z), (inner_x, y_end, seat_z)],
                0.90,
            )


            # Arestas curtas das escadas; não há placas de outra cor.
            for aisle_y in aisle_centers:
                stair_inner = self.project(
                    inner_x, aisle_y, seat_z + 0.015
                )
                stair_outer = self.project(
                    outer_x, aisle_y, seat_z + 0.015
                )
                self._cache_stand_segment(
                    STAND_RAIL, stair_inner, stair_outer, 0.88
                )


            if self._crowd_specs is not None:
                spectator_x = side * (
                    STAND_CORNER_X
                    + inner_distance
                    + STAND_TREAD_DEPTH * 0.48
                )
                places = 126
                for place in range(places):
                    spectator_y = y_start + 0.8 + place * (
                        (y_end - y_start - 1.6) / (places - 1)
                    )
                    if any(
                        abs(spectator_y - aisle_y) < aisle_half_width + 0.22
                        for aisle_y in aisle_centers
                    ):
                        continue
                    if (place * 9 + row * 7) % 31 in (0, 1, 2):
                        continue
                    self._draw_spectator(
                        spectator_x,
                        spectator_y,
                        seat_z,
                        place * 5 + row * 17 + (2 if side > 0 else 5),
                    )


        rail_x = side * (
            STAND_CORNER_X
            + (STAND_ROWS - 1) * STAND_ROW_DEPTH
            + STAND_TREAD_DEPTH * 0.52
        )
        rail_z = 0.30 + (STAND_ROWS - 1) * STAND_ROW_RISE + 0.62
        self._cache_stand_world_polyline(
            STAND_RAIL,
            [(rail_x, y_start, rail_z), (rail_x, y_end, rail_z)],
            1.42,
        )
        for section in range(sections + 1):
            yy = y_start + section * section_length
            self._cache_stand_world_polyline(
                STAND_RAIL,
                [(rail_x, yy, rail_z - 0.55), (rail_x, yy, rail_z)],
                1.0,
            )


    def _draw_pitch(self) -> None:
        far_y, near_y = -3.0, 32.0
        width = 34.0
        stripes = 12
        for index in range(stripes):
            y0 = far_y + (near_y - far_y) * index / stripes
            y1 = far_y + (near_y - far_y) * (index + 1) / stripes
            p1 = self.project(-width, y0, 0.0)
            p2 = self.project(width, y0, 0.0)
            p3 = self.project(width, y1, 0.0)
            p4 = self.project(-width, y1, 0.0)
            if index % 2:
                Color(0.075, 0.39, 0.18, 1.0)
            else:
                Color(0.06, 0.33, 0.145, 1.0)
            Triangle(points=[*p1, *p2, *p3])
            Triangle(points=[*p1, *p3, *p4])


        # Limites do meio-campo visível.
        Color(0.92, 0.96, 0.88, 0.82)
        self._world_polyline([(-34.0, 0.0, 0.012), (34.0, 0.0, 0.012)], width=1.3)
        self._world_polyline([(-34.0, 0.0, 0.012), (-34.0, 32.0, 0.012)], width=1.1)
        self._world_polyline([(34.0, 0.0, 0.012), (34.0, 32.0, 0.012)], width=1.1)


        # Grande área, pequena área e marca de penálti em medidas reais.
        Color(0.92, 0.96, 0.88, 0.82)
        self._world_polyline(
            [(-20.16, 0.0, 0.01), (-20.16, 16.5, 0.01), (20.16, 16.5, 0.01), (20.16, 0.0, 0.01)],
            width=1.3,
        )
        self._world_polyline(
            [(-9.16, 0.0, 0.012), (-9.16, 5.5, 0.012), (9.16, 5.5, 0.012), (9.16, 0.0, 0.012)],
            width=1.1,
        )


        # Meia-lua da grande área: raio de 9,15 m a partir da marca de
        # penálti, mostrando apenas o arco que fica fora da área.
        penalty_radius = 9.15
        area_depth = 16.5
        penalty_y = 11.0
        start_angle = math.asin((area_depth - penalty_y) / penalty_radius)
        penalty_arc = []
        for index in range(49):
            angle = start_angle + (math.pi - 2.0 * start_angle) * index / 48.0
            penalty_arc.append(
                (
                    penalty_radius * math.cos(angle),
                    penalty_y + penalty_radius * math.sin(angle),
                    0.014,
                )
            )
        self._world_polyline(penalty_arc, width=1.25)


        px, py = self.project(0.0, 11.0, 0.015)
        Color(0.94, 0.97, 0.90, 0.9)
        Ellipse(pos=(px - 3.0, py - 2.0), size=(6.0, 4.0))


    def _world_polyline(self, points: Iterable[tuple[float, float, float]], width: float = 1.0) -> None:
        flat: list[float] = []
        for point in points:
            flat.extend(self.project(*point))
        Line(points=flat, width=width)


    def _net_displacement(self, surface: str, u: float, v: float) -> float:
        total = 0.0
        for ripple in self.ripples:
            if ripple.surface != surface:
                continue
            du = (u - ripple.u) * (5.2 if surface == "back" else 4.3)
            dv = (v - ripple.v) * (4.2 if surface == "back" else 4.6)
            distance = math.sqrt(du * du + dv * dv)
            # A perturbação demora alguns centésimos a chegar a cada nó. Isso
            # cria uma onda que se propaga pela malha, em vez de toda a rede
            # mudar de forma no mesmo frame.
            local_time = ripple.age - distance * 0.038
            if local_time <= 0.0:
                continue
            local = math.exp(-distance * distance * 0.62)
            decay = math.exp(-local_time * 2.75)
            spring = math.sin(local_time * 14.2 - distance * 0.72)
            # O primeiro movimento é para trás; o pequeno retorno negativo
            # dá peso elástico à rede sem a fazer atravessar os postes.
            response = 0.78 * spring + 0.22 * math.sin(local_time * 8.0)
            total += ripple.amplitude * local * decay * response
        return total


    def _net_point(self, surface: str, u: float, v: float) -> tuple[float, float]:
        hw = self.goal_half_width
        # No véu principal, v percorre primeiro o pequeno teto horizontal e só
        # depois a diagonal até ao relvado. Nas laterais, u segue esse mesmo
        # perfil e v é a fração da altura disponível. As superfícies partilham
        # as deformações nas costuras, pelo que nunca se abrem com o impacto.
        if surface == "back":
            base_y, base_z = self._veil_profile(v)
            back = self._net_displacement("back", u, v)
            physical_v = base_z / GOAL_HEIGHT
            left = self._net_displacement("left", v, physical_v) * math.pow(
                1.0 - u, 3.0
            )
            right = self._net_displacement("right", v, physical_v) * math.pow(
                u, 3.0
            )
            return self.project(
                -hw + GOAL_WIDTH * u - left + right,
                base_y - back * 0.92,
                base_z + back * 0.28,
            )


        if surface == "left":
            base_y, top_z = self._veil_profile(u)
            physical_v = (top_z / GOAL_HEIGHT) * v
            side = self._net_displacement("left", u, physical_v)
            edge_blend = u + (1.0 - u) * math.pow(v, 3.0)
            back = self._net_displacement("back", 0.0, u) * edge_blend
            return self.project(
                -hw - side,
                base_y - back * 0.92,
                top_z * v + back * 0.28,
            )


        if surface == "right":
            base_y, top_z = self._veil_profile(u)
            physical_v = (top_z / GOAL_HEIGHT) * v
            side = self._net_displacement("right", u, physical_v)
            edge_blend = u + (1.0 - u) * math.pow(v, 3.0)
            back = self._net_displacement("back", 1.0, u) * edge_blend
            return self.project(
                hw + side,
                base_y - back * 0.92,
                top_z * v + back * 0.28,
            )


        raise ValueError(f"Unknown net surface: {surface}")


    def _draw_goal_net(self) -> None:
        # Véu contínuo: recua horizontalmente nos pequenos ferros dos cantos e
        # só depois cai na diagonal até ao relvado, sem fundo vertical.
        # Fio claro e fino. A opacidade anterior acumulava-se nas dezenas de
        # linhas e fazia a rede parecer uma superfície azul preenchida.
        Color(0.96, 0.97, 0.93, 0.84)
        # Células de cerca de 24 cm: mais visíveis no telemóvel e mais leves
        # de animar do que a antiga malha excessivamente fina.
        self._draw_net_surface("back", 30, 15)


        # As laterais repetem o perfil completo, em vez de serem triângulos.
        Color(0.94, 0.95, 0.91, 0.86)
        self._draw_side_net("left")
        self._draw_side_net("right")


    def _draw_net_surface(self, surface: str, u_steps: int, v_steps: int) -> None:
        for iu in range(u_steps + 1):
            u = iu / u_steps
            points: list[float] = []
            for iv in range(v_steps + 1):
                v = iv / v_steps
                points.extend(self._net_point(surface, u, v))
            Line(points=points, width=0.82)
        for iv in range(v_steps + 1):
            v = iv / v_steps
            points = []
            for iu in range(u_steps + 1):
                u = iu / u_steps
                points.extend(self._net_point(surface, u, v))
            Line(points=points, width=0.82)


    def _draw_side_net(self, surface: str) -> None:
        """Malha lateral ortogonal: fios verticais e horizontais no mundo."""
        mesh_size = 0.24


        # Fios verticais, distribuídos uniformemente em profundidade.
        depth_steps = math.ceil(GOAL_DEPTH / mesh_size)
        for depth_index in range(depth_steps + 1):
            depth = GOAL_DEPTH * depth_index / depth_steps
            y = -depth
            top_z = self._veil_height_at_y(y)
            if top_z < 0.01:
                continue
            u = self._veil_amount_at_y(y)
            vertical_steps = max(1, math.ceil(top_z / mesh_size))
            points: list[float] = []
            for height_index in range(vertical_steps + 1):
                z = top_z * height_index / vertical_steps
                points.extend(self._net_point(surface, u, z / top_z))
            Line(points=points, width=0.82)


        # Fios horizontais: cada um termina quando encontra a queda do véu.
        # Ao contrário da parametrização anterior, não acompanham a diagonal.
        height_steps = math.ceil(GOAL_HEIGHT / mesh_size)
        for height_index in range(height_steps + 1):
            z = GOAL_HEIGHT * height_index / height_steps
            if z < 1e-8:
                # A última fiada acompanha também a folga pousada no relvado.
                max_depth = GOAL_DEPTH
            else:
                max_depth = self._veil_depth_at_height(z)
            horizontal_steps = max(1, math.ceil(max_depth / mesh_size))
            points = []
            for depth_index in range(horizontal_steps + 1):
                depth = max_depth * depth_index / horizontal_steps
                y = -depth
                top_z = self._veil_height_at_y(y)
                u = self._veil_amount_at_y(y)
                v = z / top_z if top_z > 1e-8 else 0.0
                points.extend(self._net_point(surface, u, clamp(v, 0.0, 1.0)))
            Line(points=points, width=0.82)


    def _draw_goal_frame(self) -> None:
        hw = self.goal_half_width
        left_bottom = self.project(-hw, 0.0, 0.0)
        left_top = self.project(-hw, 0.0, GOAL_HEIGHT)
        right_bottom = self.project(hw, 0.0, 0.0)
        right_top = self.project(hw, 0.0, GOAL_HEIGHT)
        left_support = self.project(-hw, -VEIL_TOP_DEPTH, GOAL_HEIGHT)
        right_support = self.project(hw, -VEIL_TOP_DEPTH, GOAL_HEIGHT)


        Color(0.04, 0.08, 0.09, 0.38)
        Line(points=[left_bottom[0] + 3, left_bottom[1] - 3, left_top[0] + 3, left_top[1] - 3], width=5.6)
        Line(points=[right_bottom[0] + 3, right_bottom[1] - 3, right_top[0] + 3, right_top[1] - 3], width=5.6)
        Line(points=[left_top[0] + 3, left_top[1] - 3, right_top[0] + 3, right_top[1] - 3], width=5.6)
        Line(
            points=[left_top[0] + 2, left_top[1] - 2, left_support[0] + 2, left_support[1] - 2],
            width=4.2,
        )
        Line(
            points=[right_top[0] + 2, right_top[1] - 2, right_support[0] + 2, right_support[1] - 2],
            width=4.2,
        )


        Color(0.96, 0.98, 1.0, 1.0)
        Line(points=[*left_bottom, *left_top], width=4.0)
        Line(points=[*right_bottom, *right_top], width=4.0)
        Line(points=[*left_top, *right_top], width=4.0)


        # Pequenos ferros superiores que afastam a rede antes da queda do véu.
        Color(0.88, 0.93, 0.95, 1.0)
        Line(points=[*left_top, *left_support], width=2.8)
        Line(points=[*right_top, *right_support], width=2.8)


    def _draw_field_players(self) -> None:
        """Desenha defesas e atacantes, do mais distante para o mais próximo."""
        player_kit, opponent_kit = self._match_outfield_kits()
        for player in sorted(self.field_players, key=lambda item: item.y):
            x, y = self._field_player_position(player)
            target_x = self.ball.x if self.ball.active else self.shot_origin_x
            target_y = self.ball.y if self.ball.active else self.shot_origin_y
            direction_x = target_x - x
            direction_y = target_y - y
            direction_size = max(0.001, math.hypot(direction_x, direction_y))
            forward_x = direction_x / direction_size
            forward_y = direction_y / direction_size
            side_x, side_y = -forward_y, forward_x
            sway = math.sin(self.elapsed * 2.0 + player.phase) * 0.025


            def world(side: float, forward: float, z: float) -> tuple[float, float, float]:
                return (
                    x + side_x * side * FIELD_PLAYER_SCALE
                    + forward_x * forward * FIELD_PLAYER_SCALE,
                    y + side_y * side * FIELD_PLAYER_SCALE
                    + forward_y * forward * FIELD_PLAYER_SCALE,
                    z * FIELD_PLAYER_SCALE,
                )


            hip_l = world(-0.16, 0.0, 0.82)
            hip_r = world(0.16, 0.0, 0.82)
            shoulder_l = world(-0.25, 0.04 + sway, 1.42)
            shoulder_r = world(0.25, 0.04 + sway, 1.42)
            head_world = world(0.0, 0.05 + sway, 1.72)
            knee_l = world(-0.16, 0.06 + sway, 0.43)
            knee_r = world(0.16, -0.06 - sway, 0.43)
            foot_l = world(-0.19, 0.12 + sway, 0.03)
            foot_r = world(0.19, -0.11 - sway, 0.03)
            hand_l = world(-0.44, 0.03, 1.10)
            hand_r = world(0.44, 0.03, 1.10)


            projected = {
                "hip_l": self.project(*hip_l),
                "hip_r": self.project(*hip_r),
                "shoulder_l": self.project(*shoulder_l),
                "shoulder_r": self.project(*shoulder_r),
                "head": self.project(*head_world),
                "knee_l": self.project(*knee_l),
                "knee_r": self.project(*knee_r),
                "foot_l": self.project(*foot_l),
                "foot_r": self.project(*foot_r),
                "hand_l": self.project(*hand_l),
                "hand_r": self.project(*hand_r),
            }


            shadow_l = self.project(*world(-0.28, -0.12, 0.012))
            shadow_r = self.project(*world(0.28, 0.18, 0.012))
            Color(0.01, 0.03, 0.02, 0.32)
            Line(points=[*shadow_l, *shadow_r], width=4.8)


            if player.team == "defender":
                shirt, shorts, socks, trim = opponent_kit
            else:
                shirt, shorts, socks, trim = player_kit


            Color(*shorts)
            Line(
                points=[*projected["hip_l"], *projected["knee_l"]],
                width=4.4,
            )
            Line(
                points=[*projected["hip_r"], *projected["knee_r"]],
                width=4.4,
            )
            Color(*socks)
            Line(
                points=[*projected["knee_l"], *projected["foot_l"]],
                width=3.0,
            )
            Line(
                points=[*projected["knee_r"], *projected["foot_r"]],
                width=3.0,
            )


            Color(*shirt)
            Triangle(
                points=[
                    *projected["hip_l"],
                    *projected["hip_r"],
                    *projected["shoulder_l"],
                ]
            )
            Triangle(
                points=[
                    *projected["hip_r"],
                    *projected["shoulder_l"],
                    *projected["shoulder_r"],
                ]
            )
            shoulder_middle = (
                (projected["shoulder_l"][0] + projected["shoulder_r"][0]) / 2,
                (projected["shoulder_l"][1] + projected["shoulder_r"][1]) / 2,
            )
            hip_middle = (
                (projected["hip_l"][0] + projected["hip_r"][0]) / 2,
                (projected["hip_l"][1] + projected["hip_r"][1]) / 2,
            )
            Color(*trim)
            Line(points=[*shoulder_middle, *hip_middle], width=1.5)
            Color(*shirt)
            Line(
                points=[*projected["shoulder_l"], *projected["hand_l"]],
                width=3.8,
            )
            Line(
                points=[*projected["shoulder_r"], *projected["hand_r"]],
                width=3.8,
            )


            head_radius = max(
                3.5,
                self.pixels_per_meter(*head_world) * 0.10,
            )
            Color(0.88, 0.61, 0.41, 1.0)
            Ellipse(
                pos=(
                    projected["head"][0] - head_radius,
                    projected["head"][1] - head_radius,
                ),
                size=(head_radius * 2.0, head_radius * 2.0),
            )


    def _draw_player(self) -> None:
        """Desenha o avançado junto à origem variável do remate."""
        # Eixo frontal aponta do local do remate para o ponto escolhido.
        direction_x = self.aim_x - self.shot_origin_x
        direction_y = -self.shot_origin_y
        direction_size = max(0.001, math.hypot(direction_x, direction_y))
        forward_x = direction_x / direction_size
        forward_y = direction_y / direction_size
        side_x, side_y = -forward_y, forward_x


        # O jogador começa atrás da bola e termina o gesto depois
        # do contacto. O apoio mantém-se plantado enquanto a perna remata.
        is_header = self.shot_type == "header"
        distance_from_ball = 0.12 if is_header else 0.52
        player_x = self.shot_origin_x - forward_x * distance_from_ball * PLAYER_SCALE
        player_y = self.shot_origin_y - forward_y * distance_from_ball * PLAYER_SCALE
        kick = clamp(self.player_kick_progress, 0.0, 1.0)
        kick_curve = math.sin(kick * math.pi * 0.5)
        lift = math.sin(kick * math.pi)


        def world(side: float, forward: float, z: float) -> tuple[float, float, float]:
            side *= PLAYER_SCALE
            forward *= PLAYER_SCALE
            z *= PLAYER_SCALE
            return (
                player_x + side_x * side + forward_x * forward,
                player_y + side_y * side + forward_y * forward,
                z,
            )


        if is_header:
            # Flexão, salto curto e avanço da cabeça em direção à bola.
            crouch = 0.10 * math.sin(kick * math.pi)
            jump = 0.14 * math.sin(kick * math.pi)
            lean = -0.03 + 0.36 * kick_curve
            hip_l = world(-0.16, 0.0, 0.84 - crouch + jump)
            hip_r = world(0.16, 0.0, 0.84 - crouch + jump)
            shoulder_l = world(-0.25, lean * 0.72, 1.43 + jump)
            shoulder_r = world(0.25, lean * 0.72, 1.43 + jump)
            head_world = world(0.0, lean, 1.72 + jump)
            support_knee = world(-0.17, 0.03, 0.43 - crouch * 0.55 + jump)
            support_foot = world(-0.20, 0.10, 0.04 + jump)
            kicking_knee = world(0.17, -0.02, 0.43 - crouch * 0.55 + jump)
            kicking_foot = world(0.20, 0.08, 0.04 + jump)
            hand_l = world(-0.58, -0.06, 1.15 + jump)
            hand_r = world(0.58, -0.02, 1.17 + jump)
        else:
            lean = 0.08 + 0.13 * kick_curve
            hip_l = world(-0.16, 0.0, 0.86)
            hip_r = world(0.16, 0.0, 0.86)
            shoulder_l = world(-0.25, lean, 1.45)
            shoulder_r = world(0.25, lean, 1.45)
            head_world = world(0.0, lean + 0.02, 1.72)
            support_knee = world(-0.16, 0.10, 0.45)
            support_foot = world(-0.18, 0.23, 0.04)
            kicking_knee = world(
                0.17,
                -0.18 + 0.58 * kick_curve,
                0.45 + 0.18 * lift,
            )
            kicking_foot = world(
                0.18,
                -0.30 + 1.08 * kick_curve,
                0.05 + 0.30 * lift,
            )
            hand_l = world(-0.52, -0.05 - 0.12 * kick_curve, 1.15)
            hand_r = world(0.48, 0.08 + 0.12 * kick_curve, 1.22)


        points = {
            "hip_l": self.project(*hip_l),
            "hip_r": self.project(*hip_r),
            "shoulder_l": self.project(*shoulder_l),
            "shoulder_r": self.project(*shoulder_r),
            "head": self.project(*head_world),
            "support_knee": self.project(*support_knee),
            "support_foot": self.project(*support_foot),
            "kicking_knee": self.project(*kicking_knee),
            "kicking_foot": self.project(*kicking_foot),
            "hand_l": self.project(*hand_l),
            "hand_r": self.project(*hand_r),
        }


        shadow_l = self.project(*world(-0.32, -0.12, 0.012))
        shadow_r = self.project(*world(0.38, 0.48, 0.012))
        Color(0.015, 0.035, 0.025, 0.35)
        Line(points=[*shadow_l, *shadow_r], width=6.0)


        player_kit, _opponent_kit = self._match_outfield_kits()
        shirt, shorts, socks, trim = player_kit
        # Calções, pernas e chuteiras.
        Color(*shorts)
        Line(
            points=[*points["hip_l"], *points["support_knee"], *points["support_foot"]],
            width=5.3,
        )
        Line(
            points=[*points["hip_r"], *points["kicking_knee"], *points["kicking_foot"]],
            width=5.3,
        )
        Color(*socks)
        Line(points=[*points["support_knee"], *points["support_foot"]], width=3.5)
        Line(points=[*points["kicking_knee"], *points["kicking_foot"]], width=3.5)


        # Camisola nas cores reais do clube e braços abertos para equilibrar.
        Color(*shirt)
        Triangle(points=[*points["hip_l"], *points["hip_r"], *points["shoulder_l"]])
        Triangle(points=[*points["hip_r"], *points["shoulder_l"], *points["shoulder_r"]])
        shoulder_middle = (
            (points["shoulder_l"][0] + points["shoulder_r"][0]) / 2,
            (points["shoulder_l"][1] + points["shoulder_r"][1]) / 2,
        )
        hip_middle = (
            (points["hip_l"][0] + points["hip_r"][0]) / 2,
            (points["hip_l"][1] + points["hip_r"][1]) / 2,
        )
        Color(*trim)
        Line(points=[*shoulder_middle, *hip_middle], width=1.8)
        Color(*shirt)
        Line(points=[*points["shoulder_l"], *points["hand_l"]], width=4.6)
        Line(points=[*points["shoulder_r"], *points["hand_r"]], width=4.6)


        head_radius = max(
            4.3,
            self.pixels_per_meter(*head_world) * 0.11,
        )
        Color(0.91, 0.64, 0.43, 1.0)
        Ellipse(
            pos=(points["head"][0] - head_radius, points["head"][1] - head_radius),
            size=(head_radius * 2.0, head_radius * 2.0),
        )


    def _draw_goalkeeper(self) -> None:
        flat_pose = self._goalkeeper_pose()
        world_pose = self._goalkeeper_world_pose(flat_pose)
        goalkeeper_shirt, goalkeeper_shorts = self._goalkeeper_kit()
        pose = {
            key: self.project(*point)
            for key, point in world_pose.items()
        }


        # A sombra alarga-se no sentido do mergulho.
        ground_pose = [
            self.project(point[0], point[1], 0.012)
            for point in world_pose.values()
        ]
        shadow_l = min(ground_pose, key=lambda point: point[0])
        shadow_r = max(ground_pose, key=lambda point: point[0])
        Color(0.015, 0.035, 0.025, 0.42)
        Line(points=[*shadow_l, *shadow_r], width=6.0)


        # Tronco acompanha a rotação do corpo.
        Color(*goalkeeper_shirt)
        Triangle(points=[*pose["hip_l"], *pose["hip_r"], *pose["shoulder_l"]])
        Triangle(points=[*pose["hip_r"], *pose["shoulder_l"], *pose["shoulder_r"]])
        Line(points=[*pose["shoulder_l"], *pose["hand_l"]], width=4.7)
        Line(points=[*pose["shoulder_r"], *pose["hand_r"]], width=4.7)


        Color(*goalkeeper_shorts)
        Line(points=[*pose["foot_l"], *pose["hip_l"]], width=5.0)
        Line(points=[*pose["foot_r"], *pose["hip_r"]], width=5.0)


        # Luvas avançam primeiro e são também parte da zona de defesa.
        Color(0.94, 0.96, 0.88, 1.0)
        for hand in (pose["hand_l"], pose["hand_r"]):
            Ellipse(pos=(hand[0] - 3.5, hand[1] - 3.5), size=(7.0, 7.0))


        head = pose["head"]
        head_radius = max(
            4.8,
            self.pixels_per_meter(*world_pose["head"]) * 0.12,
        )
        Color(0.93, 0.68, 0.48, 1.0)
        Ellipse(
            pos=(head[0] - head_radius, head[1] - head_radius),
            size=(2.0 * head_radius, 2.0 * head_radius),
        )
        # Pequeno marcador facial orientado para a bola, para a rotação ser
        # legível mesmo com a cabeça desenhada como um círculo pequeno.
        target_x = self.ball.x if self.ball.active else self.shot_origin_x
        target_y = self.ball.y if self.ball.active else self.shot_origin_y
        face_x = target_x - world_pose["head"][0]
        face_y = target_y - world_pose["head"][1]
        face_size = max(1e-6, math.hypot(face_x, face_y))
        face_tip = self.project(
            world_pose["head"][0] + face_x / face_size * 0.13,
            world_pose["head"][1] + face_y / face_size * 0.13,
            world_pose["head"][2],
        )
        Color(0.20, 0.12, 0.09, 0.92)
        Ellipse(
            pos=(face_tip[0] - 1.6, face_tip[1] - 1.6),
            size=(3.2, 3.2),
        )


    def _draw_ball(self) -> None:
        ball = self.ball
        bx, by = self.project(ball.x, ball.y, ball.z)
        ground_x, ground_y = self.project(ball.x, ball.y, 0.01)
        scale = self.pixels_per_meter(ball.x, ball.y, ball.z)
        radius = max(6.0, ball.radius * scale)


        Color(0.01, 0.025, 0.018, 0.40)
        Ellipse(pos=(ground_x - radius * 1.15, ground_y - radius * 0.35), size=(radius * 2.3, radius * 0.70))
        Color(0.97, 0.98, 0.94, 1.0)
        Ellipse(pos=(bx - radius, by - radius), size=(radius * 2, radius * 2))
        Color(0.08, 0.10, 0.11, 1.0)
        Ellipse(pos=(bx - radius * 0.33, by - radius * 0.25), size=(radius * 0.66, radius * 0.58))


    def _draw_aim_marker(self) -> None:
        if self.view != "shot" or self.state != self.STATE_AIMING:
            return
        center = self.project(self.aim_x, -0.04, self.aim_z)
        Color(1.0, 1.0, 1.0, 0.88)
        Line(circle=(center[0], center[1], 11.0), width=1.4)
        Line(points=[center[0] - 16, center[1], center[0] + 16, center[1]], width=1.0)
        Line(points=[center[0], center[1] - 16, center[0], center[1] + 16], width=1.0)


        # Barra de força.
        bar_x = self.right - 57
        bar_y = self.y + 35
        bar_h = 125
        Color(0.02, 0.05, 0.06, 0.78)
        Rectangle(pos=(bar_x - 8, bar_y - 8), size=(28, bar_h + 16))
        Color(0.18, 0.24, 0.23, 1.0)
        Rectangle(pos=(bar_x, bar_y), size=(12, bar_h))
        Color(1.0 - self.power * 0.65, 0.38 + self.power * 0.55, 0.16, 1.0)
        Rectangle(pos=(bar_x, bar_y), size=(12, bar_h * self.power))


    def _draw_hud(self) -> None:
        if self.view != "shot":
            return
        if self.shot_context == "match" and self.match_home and self.match_away:
            self._draw_match_overlay()
            stats = ""
        elif self.shot_context == "training":
            stats = (
                f"TRAINING     SHOT {4 - self.training_shots_left}/3"
                f"     GOALS {self.training_goals}     STAMINA {self.career.stamina:.1f}/20"
            )
        else:
            accuracy = (self.goals / self.attempts * 100.0) if self.attempts else 0.0
            stats = (
                f"SHOTS  {self.attempts:02d}     GOALS  {self.goals:02d}     "
                f"SAVES  {self.saves:02d}     ACCURACY  {accuracy:4.1f}%"
            )
        if stats:
            Color(0.015, 0.035, 0.05, 0.82)
            Rectangle(pos=(self.x + 18, self.top - 74), size=(self.width - 36, 55))
            self._draw_text(
                stats,
                self.x + 36,
                self.top - 47,
                font_size=max(14, int(self.height * 0.025)),
                color=(0.91, 0.96, 0.98, 1.0),
                max_width=self.width - 72,
            )


        if self.shot_context == "match" and self.state == self.STATE_AIMING:
            timer_x, timer_y, timer_width, timer_height = self._shot_timer_bounds()
            ratio = clamp(
                self.shot_time_left / max(0.01, self.shot_time_limit), 0.0, 1.0
            )
            urgent = self.shot_time_left <= 1.5
            Color(0.01, 0.025, 0.03, 0.94)
            Rectangle(pos=(timer_x, timer_y), size=(timer_width, timer_height))
            timer_color = (
                (1.0, 0.16, 0.10, 1.0)
                if urgent
                else (1.0 - ratio * 0.58, 0.30 + ratio * 0.62, 0.14, 1.0)
            )
            Color(*timer_color)
            Rectangle(
                pos=(timer_x + dp(2), timer_y + dp(2)),
                size=((timer_width - dp(4)) * ratio, dp(3)),
            )
            Color(0.92, 0.98, 0.95, 0.92)
            Line(rectangle=(timer_x, timer_y, timer_width, timer_height), width=1.2)
            self._draw_text(
                f"TIME TO SHOOT   {self.shot_time_left:0.1f} s",
                timer_x + timer_width / 2,
                timer_y + timer_height * 0.57,
                dp(11),
                (1.0, 1.0, 1.0, 1.0),
                "center",
                max_width=timer_width - 18,
            )


        if self.state == self.STATE_AIMING:
            action = (
                "PENALTY"
                if self.shot_type == "penalty"
                else "FREE KICK" if self.shot_type == "free_kick"
                else "HEADER" if self.shot_type == "header" else "KICK"
            )
            hint = (
                f"TYPE: {action}   |   SPACE: SHOOT   |   "
                "ARROWS/WASD: AIM   |   C: AUTO   |   R: RESET"
            )
            self._draw_text(
                hint,
                self.center_x,
                self.y + 18,
                font_size=max(11, int(self.height * 0.018)),
                color=(0.83, 0.90, 0.90, 0.88),
                anchor="center",
            )


        if self.result_text:
            pulse = 1.0 + 0.035 * math.sin(self.state_age * 11.0)
            self._draw_text(
                self.result_text,
                self.center_x,
                self.y + self.height * 0.48,
                font_size=int(max(34, self.height * 0.075) * pulse),
                color=self.result_color,
                anchor="center",
            )
            self._draw_text(
                "TAP TO CONTINUE",
                self.center_x,
                self.y + self.height * 0.405,
                font_size=max(12, int(self.height * 0.020)),
                color=(0.90, 0.94, 0.94, 0.88),
                anchor="center",
            )


    def _draw_text(
        self,
        text: str,
        x: float,
        y: float,
        font_size: int,
        color: tuple[float, float, float, float],
        anchor: str = "left",
        max_width: Optional[float] = None,
    ) -> None:
        chosen_size = max(8, int(font_size))
        while True:
            cache_key = (text, chosen_size, tuple(color))
            texture = self._text_texture_cache.get(cache_key)
            if texture is None:
                label = CoreLabel(text=text, font_size=chosen_size, color=color)
                label.refresh()
                texture = label.texture
                if len(self._text_texture_cache) >= 160:
                    self._text_texture_cache.clear()
                self._text_texture_cache[cache_key] = texture
            if max_width is None or texture.width <= max_width or chosen_size <= 8:
                break
            chosen_size -= 1
        if max_width is not None and texture.width > max_width:
            # Even the minimum font can overflow with edited or long club names.
            label = CoreLabel(text=text, font_size=chosen_size, color=color,
                              text_size=(max(1, max_width), None), shorten=True,
                              shorten_from="right", max_lines=1)
            label.refresh()
            texture = label.texture
        if anchor == "center":
            position = (x - texture.width / 2.0, y - texture.height / 2.0)
        elif anchor == "right":
            position = (x - texture.width, y - texture.height / 2.0)
        else:
            position = (x, y - texture.height / 2.0)
        Color(1.0, 1.0, 1.0, 1.0)
        Rectangle(texture=texture, pos=position, size=texture.size)




class StrikerApp(App):
    title = "Scorer"


    def on_pause(self):
        if self.root is not None and self.root._career_started:
            self.root.career.save()
        return True

    def on_stop(self):
        if self.root is not None and self.root._career_started:
            self.root.career.save()

    def build(self):
        force_android_landscape()
        return StrikerGame()




if __name__ == "__main__":
    StrikerApp().run()
"""Original Striker simulation and career, importable without Kivy."""
from __future__ import annotations


import json
import copy
import hashlib
import math
import os
import random
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Protocol


import tempfile
import sys

GAME_VERSION = 47
GRAVITY = 9.81
GOAL_WIDTH = 7.32
GOAL_HEIGHT = 2.44
GOAL_DEPTH = 2.65
VEIL_TOP_DEPTH = 0.55
VEIL_GROUND_SLACK = 0.50
VEIL_TOUCH_DEPTH = GOAL_DEPTH - VEIL_GROUND_SLACK
VEIL_SAG = 0.28
VEIL_SLOPE_LENGTH = math.hypot(
    VEIL_TOUCH_DEPTH - VEIL_TOP_DEPTH, GOAL_HEIGHT
)
VEIL_PATH_LENGTH = VEIL_TOP_DEPTH + VEIL_SLOPE_LENGTH + VEIL_GROUND_SLACK
NET_RIPPLE_DURATION = 1.55
PHYSICS_STEP = 1.0 / 120.0
POST_RADIUS = 0.060
BALL_RADIUS = 0.115
START_Y = 10.0
GOALKEEPER_Y = 0.85
GOALKEEPER_SCALE = 0.80
PLAYER_SCALE = 0.76
FIELD_PLAYER_SCALE = 0.72
HEADER_BALL_HEIGHT = 1.31
STAND_CONCRETE = (0.20, 0.22, 0.21, 1.0)
STAND_RISER = (0.145, 0.165, 0.155, 1.0)
STAND_TREAD = (0.245, 0.265, 0.250, 1.0)
STAND_EDGE = (0.34, 0.37, 0.35, 0.86)
STAND_RAIL = (0.66, 0.69, 0.65, 0.92)
STAND_ROOF = (0.075, 0.095, 0.095, 1.0)
STAND_ROWS = 13
STAND_CORNER_X = 36.20
STAND_FRONT_Y = -3.95
STAND_ROW_DEPTH = 0.92
STAND_TREAD_DEPTH = 0.84
STAND_ROW_RISE = 0.42


SHOT_ORIGINS = (
    (0.0, 7.0),
    (-6.0, 8.0),
    (6.0, 8.0),
    (-15.0, 7.0),
    (15.0, 7.0),
    (-18.0, 5.0),
    (18.0, 5.0),
    (0.0, 11.0),
    (-5.5, 12.5),
    (5.5, 12.5),
    (-10.0, 15.0),
    (10.0, 15.0),
    (-3.5, 18.0),
    (3.5, 18.0),
    (-6.0, 4.6),
    (0.0, 4.9),
    (6.0, 4.6),
)


HEADER_ORIGINS = (
    (-6.2, 4.2),
    (-3.1, 4.8),
    (0.0, 4.6),
    (3.1, 4.8),
    (6.2, 4.2),
)


PENALTY_ORIGIN = (0.0, 11.0)
# FA Cup 2026/27: clubes de League One/League Two entram na 1.ª ronda
# proper; Premier League e Championship entram na 3.ª ronda proper. As semanas
# são calculadas a partir do calendário interno, que começa em 12 Jul 2026.
CUP_WEEKS = (17, 21, 26, 31, 34, 38, 41, 45)
CUP_ROUNDS = (
    'ROUND 1',
    'ROUND 2',
    'ROUND 3',
    'ROUND 4',
    'ROUND 5',
    'QUARTER-FINAL',
    'SEMI-FINAL',
    "FINAL",
)


FREE_KICK_ORIGINS = (
    (-10.5, 20.0), (-6.0, 19.0), (-2.5, 18.5), (0.0, 19.5),
    (2.5, 18.5), (6.0, 19.0), (10.5, 20.0), (-8.0, 23.0),
    (8.0, 23.0), (-4.0, 25.0), (4.0, 25.0),
)


# Nomes reais usados pelo sorteio da FA Cup para evitar os clubes-placeholder
# gerados pelo simulador mundial. Nas rondas 1-2 só entram equipas elegíveis
# das divisões inferiores; a partir da 3.ª entram também PL/Championship.
FA_CUP_EARLY_REAL_CLUBS = (
    "Ashford Rovers", "Bexley Athletic", "Cedarbridge FC", "Dunwich Town",
    "Eastmere United", "Foxley Rovers", "Greyford City", "Highmoor Athletic",
    "Ironvale FC", "Kingsport Town", "Larkspur United", "Moorfield Rovers",
    "Northgate City", "Oakminster FC", "Pinehurst Athletic", "Queensbridge Town",
    "Redhaven Rovers", "Stonebridge United", "Thornfield FC", "Upton Vale",
    "Westmere City", "Yarrow Athletic", "Brookchester FC", "Ravenford Town",
)
FA_CUP_BIG_REAL_CLUBS = (
    "North London FC", "Manchester Sky", "Mersey Reds", "West London Blues",
    "Manchester Reds", "North London Whites", "Birmingham Lions", "Bristol Harbour",
    "Leicester Foxes FC", "South Coast FC", "Sheffield Steel", "Tyne United",
)


# Câmara de bancada central: 12 m para lá da linha lateral, no alinhamento
# do meio-campo e cerca de 9,5 m acima do relvado.
CAMERA_POSITION = (-46.0, 52.5, 9.5)
CAMERA_TARGET = (0.0, 5.0, 1.0)
# Campo de visão suficientemente largo para incluir remates junto às duas
# linhas de fundo sem abandonar a bancada central.
CAMERA_VERTICAL_FOV = 17.0




def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))




def length3(x: float, y: float, z: float) -> float:
    return math.sqrt(x * x + y * y + z * z)




def dot3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]




def subtract3(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]




def cross3(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )




def normalize3(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    size = length3(*vector)
    if size < 1e-9:
        return 0.0, 0.0, 0.0
    return vector[0] / size, vector[1] / size, vector[2] / size




CAMERA_FORWARD = normalize3(subtract3(CAMERA_TARGET, CAMERA_POSITION))
CAMERA_RIGHT = normalize3(cross3(CAMERA_FORWARD, (0.0, 0.0, 1.0)))
CAMERA_UP = normalize3(cross3(CAMERA_RIGHT, CAMERA_FORWARD))




@dataclass
class Ball:
    x: float = 0.0
    y: float = START_Y
    z: float = BALL_RADIUS
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    radius: float = BALL_RADIUS
    active: bool = False
    crossed_goal: bool = False
    goalkeeper_touched: bool = False
    post_cooldown: float = 0.0
    player_cooldown: float = 0.0
    net_cooldown: float = 0.0


    def reset(
        self,
        x: float = 0.0,
        y: float = START_Y,
        z: Optional[float] = None,
    ) -> None:
        self.x = x
        self.y = y
        self.z = self.radius if z is None else z
        self.vx = self.vy = self.vz = 0.0
        self.active = False
        self.crossed_goal = False
        self.goalkeeper_touched = False
        self.post_cooldown = 0.0
        self.player_cooldown = 0.0
        self.net_cooldown = 0.0


    @property
    def speed(self) -> float:
        return length3(self.vx, self.vy, self.vz)




@dataclass
class NetRipple:
    surface: str
    u: float
    v: float
    amplitude: float
    age: float = 0.0




@dataclass
class FieldPlayer:
    x: float
    y: float
    team: str
    phase: float




# ---------------------------------------------------------------------------
# Modo carreira
# ---------------------------------------------------------------------------


FREE_LEAGUE_KEY = "England|4"


def sanitize_local_display_name(value: object, *, limit: int = 48) -> str:
    """Keep local editor names short, printable and inert."""
    raw = str(value or "").strip()
    cleaned = "".join(
        ch for ch in raw
        if (ch.isalnum() or ch in " -.'&") and ch not in "\r\n\t"
    )
    cleaned = " ".join(cleaned.split())[:limit].strip(" .'-&")
    if len(cleaned) < 2:
        raise ValueError("name must contain at least two safe characters")
    return cleaned


def capitalise_player_initials(name: str) -> str:
    """Uppercase word initials without changing internal spelling (e.g. McDonald)."""
    return " ".join(word[:1].upper() + word[1:] for word in name.split(" "))


class EntitlementProvider(Protocol):
    """Production entitlement source contract; billing implementation arrives later."""

    def has_world_access(self) -> bool:
        ...

    def restore_world_access(self) -> bool:
        """Re-query durable ownership and return the resulting WORLD state."""
        ...


class FreeEntitlementProvider:
    """Fail-safe provider used until verified WORLD ownership exists."""

    __slots__ = ()

    def has_world_access(self) -> bool:
        return False

    def restore_world_access(self) -> bool:
        return False


class EntitlementManager:
    """Single fail-closed gateway between gameplay and ownership providers.

    Test/fake providers deliberately live outside this release source file so they
    cannot be enabled by a save edit, local flag, environment variable or hidden UI.
    """

    __slots__ = ("_provider",)

    def __init__(self, provider: Optional[EntitlementProvider] = None) -> None:
        self._provider = provider or FreeEntitlementProvider()

    @property
    def world_unlocked(self) -> bool:
        try:
            return self._provider.has_world_access() is True
        except Exception:
            return False

    def restore_world_access(self) -> bool:
        try:
            restore = getattr(self._provider, "restore_world_access", None)
            if not callable(restore):
                return False
            restored = restore() is True
            return restored and self.world_unlocked
        except Exception:
            return False


LEAGUE_TWO_2026 = (
    "Ashford Rovers", "Bexley Athletic", "Cedarbridge FC", "Dunwich Town",
    "Eastmere United", "Foxley Rovers", "Greyford City", "Highmoor Athletic",
    "Ironvale FC", "Kingsport Town", "Larkspur United", "Moorfield Rovers",
    "Northgate City", "Oakminster FC", "Pinehurst Athletic", "Queensbridge Town",
    "Redhaven Rovers", "Stonebridge United", "Thornfield FC", "Upton Vale",
    "Westmere City", "Yarrow Athletic", "Brookchester FC", "Ravenford Town",
)


# Profundidade das pirâmides nacionais europeias. Apenas entram escalões
# nacionais; campeonatos distritais/regionais ficam deliberadamente de fora.
EUROPE_PYRAMID_DEPTH = {
    "Albania": 2, "Andorra": 2, "Armenia": 2, "Austria": 2,
    "Azerbaijan": 2, "Belarus": 2, "Belgium": 3,
    "Bosnia and Herzegovina": 2, "Bulgaria": 2, "Croatia": 2,
    "Cyprus": 2, "Czechia": 3, "Denmark": 3, "England": 5,
    "Estonia": 2, "Faroe Islands": 2, "Finland": 3, "France": 3,
    "Georgia": 2, "Germany": 3, "Gibraltar": 2, "Greece": 2,
    "Hungary": 2, "Iceland": 3, "Israel": 2, "Italy": 3,
    "Kazakhstan": 2, "Kosovo": 2, "Latvia": 2, "Liechtenstein": 1,
    "Lithuania": 2, "Luxembourg": 2, "Malta": 2, "Moldova": 2,
    "Montenegro": 2, "Netherlands": 2, "North Macedonia": 2,
    "Northern Ireland": 2, "Norway": 3, "Poland": 3, "Portugal": 4,
    "Republic of Ireland": 2, "Romania": 3, "Russia": 3,
    "San Marino": 1, "Scotland": 4, "Serbia": 2, "Slovakia": 2,
    "Slovenia": 2, "Spain": 3, "Sweden": 3, "Switzerland": 2,
    "Turkey": 3, "Ukraine": 2, "Wales": 2,
}


EUROPE_COUNTRIES = tuple(EUROPE_PYRAMID_DEPTH)
SOUTH_AMERICA_COUNTRIES = tuple(
    "Argentina|Bolivia|Brazil|Chile|Colombia|Ecuador|Paraguay|Peru|Uruguay|Venezuela".split("|")
)
NORTH_AMERICA_COUNTRIES = tuple(
    "Anguilla|Antigua and Barbuda|Aruba|Bahamas|Barbados|Belize|Bermuda|British Virgin Islands|Canada|Cayman Islands|Costa Rica|Cuba|Curacao|Dominica|Dominican Republic|El Salvador|Grenada|Guatemala|Guyana|Haiti|Honduras|Jamaica|Mexico|Montserrat|Nicaragua|Panama|Puerto Rico|Saint Kitts and Nevis|Saint Lucia|Saint Vincent and the Grenadines|Suriname|Trinidad and Tobago|Turks and Caicos Islands|United States|US Virgin Islands".split("|")
)
ASIA_COUNTRIES = tuple(
    "Afghanistan|Australia|Bahrain|Bangladesh|Bhutan|Brunei|Cambodia|China|Chinese Taipei|Guam|Hong Kong|India|Indonesia|Iran|Iraq|Japan|Jordan|Kuwait|Kyrgyzstan|Laos|Lebanon|Macau|Malaysia|Maldives|Mongolia|Myanmar|Nepal|North Korea|Northern Mariana Islands|Oman|Pakistan|Palestine|Philippines|Qatar|Saudi Arabia|Singapore|South Korea|Sri Lanka|Syria|Tajikistan|Thailand|Timor-Leste|Turkmenistan|United Arab Emirates|Uzbekistan|Vietnam".split("|")
)
AFRICA_COUNTRIES = tuple(
    "Algeria|Angola|Benin|Botswana|Burkina Faso|Burundi|Cameroon|Cape Verde|Central African Republic|Chad|Comoros|Congo|DR Congo|Djibouti|Egypt|Equatorial Guinea|Eritrea|Eswatini|Ethiopia|Gabon|Gambia|Ghana|Guinea|Guinea-Bissau|Ivory Coast|Kenya|Lesotho|Liberia|Libya|Madagascar|Malawi|Mali|Mauritania|Mauritius|Morocco|Mozambique|Namibia|Niger|Nigeria|Rwanda|Sao Tome and Principe|Senegal|Seychelles|Sierra Leone|Somalia|South Africa|South Sudan|Sudan|Tanzania|Togo|Tunisia|Uganda|Zambia|Zimbabwe".split("|")
)
OCEANIA_COUNTRIES = tuple(
    "American Samoa|Cook Islands|Fiji|New Caledonia|New Zealand|Papua New Guinea|Samoa|Solomon Islands|Tahiti|Tonga|Vanuatu".split("|")
)
WORLD_COUNTRIES = (
    EUROPE_COUNTRIES + SOUTH_AMERICA_COUNTRIES + NORTH_AMERICA_COUNTRIES
    + ASIA_COUNTRIES + AFRICA_COUNTRIES + OCEANIA_COUNTRIES
)


DIVISION_NAMES = {
    "England": ("England Division 1", "England Division 2", "England Division 3", "England Division 4", "England Division 5"),
    "Portugal": ("Portugal Division 1", "Portugal Division 2", "Portugal Division 3", "Portugal Division 4"),
    "Spain": ("Spain Division 1", "Spain Division 2", "Spain Division 3"),
    "Germany": ("Germany Division 1", "Germany Division 2", "Germany Division 3"),
    "Italy": ("Italy Division 1", "Italy Division 2", "Italy Division 3"),
    "France": ("France Division 1", "France Division 2", "France Division 3"),
    "Netherlands": ("Netherlands Division 1", "Netherlands Division 2"),
    "Scotland": ("Scotland Division 1", "Scotland Division 2", "Scotland Division 3", "Scotland Division 4"),
    "Belgium": ("Belgium Division 1", "Belgium Division 2", "Belgium Division 3"),
    "Turkey": ("Turkey Division 1", "Turkey Division 2", "Turkey Division 3"),
}


NATIONAL_CUP_NAMES = {
    "England": "England National Cup",
    "Portugal": "Portugal National Cup",
    "Spain": "Spain National Cup",
    "Germany": "Germany National Cup",
    "Italy": "Italy National Cup",
    "France": "France National Cup",
    "Netherlands": "Netherlands National Cup",
    "Scotland": "Scotland National Cup",
    "Belgium": "Belgium National Cup",
    "Turkey": "Turkey National Cup",
}


FAMOUS_CLUBS = {
    "England": ("North London FC", "Manchester Sky", "Mersey Reds", "West London Blues", "Manchester Reds", "North London Whites"),
    "Portugal": ("Lisbon Eagles", "Lisbon Lions", "Porto Dragons", "Braga Warriors", "Guimaraes Castle", "Minho FC"),
    "Spain": ("Madrid Whites", "Catalonia Stars", "Madrid Stripes", "Basque Lions", "Yellow Coast FC", "San Sebastian Blue"),
    "Germany": ("Munich Reds", "Dortmund Gold", "Rhine Works", "Leipzig Bulls FC", "Frankfurt Eagles", "Swabia FC"),
    "Italy": ("Milan Blue", "Milan Red", "Turin Stripes", "Naples Blue", "Rome Wolves", "Bergamo Blue"),
    "France": ("Paris Blue", "Marseille Coast", "Monaco Red", "Lyon FC", "Lille Red", "Lens Gold"),
    "Netherlands": ("Amsterdam FC", "Eindhoven FC", "Rotterdam FC", "Alkmaar FC", "Twente FC", "Utrecht FC"),
    "Scotland": ("Glasgow Green", "Glasgow Blue", "Aberdeen Red", "Edinburgh Maroon", "Edinburgh Green", "Dundee Orange"),
    "Brazil": ("Rio Red", "Sao Paulo Green", "Sao Paulo Black", "Sao Paulo Tricolor", "Rio Tricolor", "Porto Alegre Blue"),
    "Argentina": ("Buenos Aires Red", "Buenos Aires Blue", "Avellaneda Sky", "Avellaneda Red", "Boedo FC", "Liniers FC"),
    "United States": ("Miami Pink", "Los Angeles Gold", "Seattle Green", "Atlanta Red", "New York Sky", "Columbus Gold"),
    "Saudi Arabia": ("Riyadh Blue", "Riyadh Gold", "Jeddah Tigers", "Jeddah Green", "Dammam FC", "Riyadh White"),
}


# Generic kit palette only; no official club colours/logos are shipped.
CLUB_KIT_HEX: dict[str, tuple[str, str, str, str]] = {}




def division_name(country: str, tier: int) -> str:
    if country == "England" and tier == 4:
        return "Scorer League"
    names = DIVISION_NAMES.get(country, ())
    if 0 < tier <= len(names):
        return names[tier - 1]
    return f"{country} Division {tier}"




def national_cup_name(country: str) -> str:
    return NATIONAL_CUP_NAMES.get(country, f"{country} National Cup")




def hex_rgba(value: str) -> tuple[float, float, float, float]:
    clean = value.lstrip("#")
    return (
        int(clean[0:2], 16) / 255.0,
        int(clean[2:4], 16) / 255.0,
        int(clean[4:6], 16) / 255.0,
        1.0,
    )




def club_kit(
    club_name: str,
) -> tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]:
    saved = CLUB_KIT_HEX.get(club_name)
    if saved:
        return tuple(hex_rgba(value) for value in saved)  # type: ignore[return-value]
    palettes = (
        ("#176FC1", "#FFFFFF", "#176FC1", "#FFFFFF"),
        ("#D71920", "#FFFFFF", "#D71920", "#FFFFFF"),
        ("#188D4B", "#111111", "#188D4B", "#FFFFFF"),
        ("#F4B41A", "#111111", "#F4B41A", "#111111"),
        ("#7A263A", "#FFFFFF", "#7A263A", "#FFFFFF"),
        ("#FFFFFF", "#111111", "#FFFFFF", "#176FC1"),
    )
    digest = hashlib.sha256(club_name.encode("utf-8")).digest()
    chosen = palettes[digest[0] % len(palettes)]
    return tuple(hex_rgba(value) for value in chosen)  # type: ignore[return-value]




def poisson_goal(rng: random.Random, mean: float) -> int:
    """Poisson pequeno sem dependências externas, limitado a 8 golos."""
    limit = math.exp(-max(0.05, mean))
    product = 1.0
    value = 0
    while product > limit and value < 9:
        value += 1
        product *= rng.random()
    return value - 1




# League Two 2022/23–2024/25 pooled goals: 4316 / 1656 fixtures.
# Aggregated reference and reproducible sources: docs/REALISM_0.6.17.md.
MATCH_HOME_GOALS = 1.43
MATCH_AWAY_GOALS = 1.18
CLEAR_CHANCE_CONVERSION = 0.51
HARD_CHANCE_CONVERSION = 0.20


def realistic_goal_means(home_rating: float, away_rating: float) -> tuple[float, float]:
    """Share an empirical goal budget by quality without capping actual scores."""
    advantage = math.log(MATCH_HOME_GOALS / MATCH_AWAY_GOALS) + (home_rating - away_rating) / 18.0
    home_share = 1.0 / (1.0 + math.exp(-clamp(advantage, -4.0, 4.0)))
    total = MATCH_HOME_GOALS + MATCH_AWAY_GOALS
    return total * home_share, total * (1.0 - home_share)


def expected_highlight_goals(chances: int, clear_probability: float) -> float:
    if chances <= 0:
        return 0.0
    return (chances * HARD_CHANCE_CONVERSION
            + clamp(clear_probability, 0.0, 1.0) * (CLEAR_CHANCE_CONVERSION - HARD_CHANCE_CONVERSION))


@dataclass
class CareerClub:
    name: str
    country: str
    league: str
    tier: int
    rating: float
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0


    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


    def add_result(self, scored: int, conceded: int) -> None:
        self.played += 1
        self.goals_for += scored
        self.goals_against += conceded
        if scored > conceded:
            self.won += 1
            self.points += 3
        elif scored == conceded:
            self.drawn += 1
            self.points += 1
        else:
            self.lost += 1




@dataclass(frozen=True)
class OpponentChanceProfile:
    pressure: float
    max_chances: int
    clear_chance_probability: float


@dataclass
class WorldLeague:
    country: str
    name: str
    tier: int
    clubs: list[CareerClub]
    round_index: int = 0
    scorer_goals: dict[str, int] = field(default_factory=dict)
    schedule_version: int = 2


    @property
    def key(self) -> str:
        return f"{self.country}|{self.tier}"


    @property
    def total_rounds(self) -> int:
        count = len(self.clubs)
        if count < 2:
            return 0
        return (count if self.schedule_version == 2 and count % 2 else count - 1) * 2


    def table(self) -> list[CareerClub]:
        return sorted(
            self.clubs,
            key=lambda club: (
                club.points, club.goal_difference, club.goals_for, club.rating
            ),
            reverse=True,
        )


    def pairings(self, round_number: Optional[int] = None) -> list[tuple[CareerClub, CareerClub]]:
        count = len(self.clubs)
        requested = self.round_index if round_number is None else round_number
        if count < 2 or requested < 0 or requested >= self.total_rounds:
            return []
        indexes = list(range(count))
        if count % 2:
            # A fixed bye leaves odd-sized leagues alternating between played
            # fixtures too. Preserve the old rotating bye in legacy seasons.
            indexes = [-1] + indexes if self.schedule_version == 2 else indexes + [-1]
            count += 1
        phase, rotation = divmod(requested, count - 1)
        if self.schedule_version == 2 and phase:
            # Reverse and offset return rounds by two. This also limits breaks
            # counted across the leg boundary, without an immediate rematch
            # in leagues with at least four clubs.
            rotation = (count - 4 - rotation) % (count - 1)
        rotating = indexes[1:]
        rotating = rotating[-rotation:] + rotating[:-rotation] if rotation else rotating
        ordered = [indexes[0]] + rotating
        matches = []
        for index in range(count // 2):
            left, right = ordered[index], ordered[count - 1 - index]
            if left < 0 or right < 0:
                continue
            flip = ((rotation % 2 if index == 0 else index % 2)
                    if self.schedule_version == 2 else (rotation + index) % 2)
            if flip:
                left, right = right, left
            if phase:
                left, right = right, left
            matches.append((self.clubs[left], self.clubs[right]))
        return matches


    def simulate_fixture(
        self,
        home: CareerClub,
        away: CareerClub,
        rng: random.Random,
        forced_score: Optional[tuple[int, int]] = None,
        *, player_club: str = "", player_goals: int = 0,
    ) -> tuple[int, int]:
        if forced_score is None:
            home_mean, away_mean = realistic_goal_means(home.rating, away.rating)
            home_goals = poisson_goal(rng, home_mean)
            away_goals = poisson_goal(rng, away_mean)
        else:
            home_goals, away_goals = forced_score
        home.add_result(home_goals, away_goals)
        away.add_result(away_goals, home_goals)
        self._add_scorers(home, max(0, home_goals - (player_goals if home.name == player_club else 0)), rng)
        self._add_scorers(away, max(0, away_goals - (player_goals if away.name == player_club else 0)), rng)
        return home_goals, away_goals


    @staticmethod
    def squad_names(club_name: str) -> tuple[str, ...]:
        # Local stable RNG: roster generation never changes match randomness.
        seed = int.from_bytes(hashlib.sha256(club_name.encode('utf-8')).digest()[:8], 'big')
        rng = random.Random(seed)
        first = ("Alden", "Bren", "Callen", "Darin", "Ellis", "Finn", "Galen", "Hugo",
                 "Ilan", "Joren", "Kellan", "Lenn", "Milo", "Nolan", "Orin", "Perrin",
                 "Quinn", "Ronan", "Soren", "Tobin", "Vian", "Wren", "Yann", "Zev")
        last = ("Ashwick", "Bexley", "Corven", "Dunmere", "Eastwell", "Fenwick", "Glenford",
                "Harrowby", "Iverton", "Jarrow", "Kestrel", "Loxley", "Merrick", "Norwyn",
                "Oakden", "Penrose", "Quenby", "Ravel", "Stannard", "Thorne", "Veylan",
                "Westmere", "Yardley", "Zelland")
        return tuple(f"{given} {family}" for given, family in
                     zip(rng.sample(first, 12), rng.sample(last, 12)))

    def migrate_scorer_names(self, protected_name: str = '') -> None:
        legacy = ("Silva", "Smith", "Garcia", "Martin", "Costa", "Muller",
                  "Rossi", "Santos", "Brown", "Novak", "Kaya", "Andersson")
        for club in self.clubs:
            for old, new in zip(legacy, self.squad_names(club.name)):
                source, target = f"{old} ({club.name})", f"{new} ({club.name})"
                if source in self.scorer_goals and source != protected_name:
                    goals = self.scorer_goals.pop(source)
                    self.scorer_goals[target] = self.scorer_goals.get(target, 0) + goals

    def _add_scorers(self, club: CareerClub, goals: int, rng: random.Random) -> None:
        names = self.squad_names(club.name)
        for _ in range(goals):
            scorer = f"{rng.choices(names, weights=(32,18,12,8,7,6,5,4,3,2,2,1), k=1)[0]} ({club.name})"
            self.scorer_goals[scorer] = self.scorer_goals.get(scorer, 0) + 1




class CareerMode:
    """Carreira persistente e simulação leve do futebol mundial."""


    SAVE_VERSION = 2
    LEGACY_SAVE_VERSION = 1


    def __init__(self, entitlement_provider: Optional[EntitlementProvider] = None, *, autoload: bool = True) -> None:
        self.entitlements = EntitlementManager(entitlement_provider)
        self._locked_world_career: Optional[dict[str, object]] = None
        self.player_name = "Alex Silva"
        self.nationality = "Portugal"
        self.season = 2026
        self.week = 0
        self.stamina = 10.0
        self.morale = 10.0
        self.club_name = ""
        self.league_key = FREE_LEAGUE_KEY
        self.matches = 0
        self.goals = 0
        self.missed_chances = 0
        self.form_goals: list[int] = []
        self.international_caps = 0
        self.international_goals = 0
        self.called_up = False
        self.last_result = ""
        self.message = 'Choose the first contract of your career.'
        self.last_training_week = -1
        self.training_session_week = -1
        self.training_shots_taken = 0
        self.training_session_goals = 0
        self.cup_active = True
        self.cup_round_index = 0
        self.fixture_history: list[dict[str, object]] = []
        self.cup_history: list[str] = []
        self.national_cup_winners: dict[str, str] = {}
        self.last_offer_week = -99
        self.world_seed = random.randrange(1_000_000, 99_999_999)
        self.rng = random.Random(self.world_seed)
        self.leagues: dict[str, WorldLeague] = {}
        self.international_status: dict[str, str] = {}
        self.offers: list[str] = []
        self.agent_offers: list[tuple[str, str]] = []
        self._build_world()
        self._new_starting_offers()
        self._migrate_legacy_save()
        if autoload:
            self.load()


    @property
    def save_path(self) -> Path:
        override = os.environ.get("STRIKER_SAVE_DIR")
        if override:
            base = Path(override)
        elif sys.platform == "android" or "ANDROID_ARGUMENT" in os.environ:
            from kivy.app import App
            app = App.get_running_app()
            if app is None:
                raise RuntimeError("Android career requires a running Kivy App")
            base = Path(app.user_data_dir)
        else:
            base = Path(__file__).resolve().parent
        return base / "striker_career.json"

    def _migrate_legacy_save(self) -> None:
        """Copy compatible legacy JSON once; never delete or overwrite a save."""
        target = self.save_path
        legacy = Path(__file__).resolve().parent / "striker_career.json"
        if target == legacy or target.exists() or not legacy.is_file():
            return
        try:
            content = legacy.read_text(encoding="utf-8")
            data = json.loads(content)
            if not isinstance(data, dict):
                return
            version = data.get("save_version", self.LEGACY_SAVE_VERSION)
            if version not in (self.LEGACY_SAVE_VERSION, self.SAVE_VERSION):
                return
            if version == self.SAVE_VERSION and not isinstance(data.get("career"), dict):
                return
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8") as destination:
                destination.write(content)
        except (OSError, ValueError):
            return


    @property
    def world_unlocked(self) -> bool:
        """Fail closed: provider errors or missing ownership always mean FREE."""
        return self.entitlements.world_unlocked


    def restore_world_access(self) -> bool:
        """Re-query ownership without mutating or deleting career save data."""
        return self.entitlements.restore_world_access()


    @property
    def product_mode(self) -> str:
        return "WORLD" if self.world_unlocked else "FREE"


    def is_league_playable(self, league_key: str) -> bool:
        return self.world_unlocked or league_key == FREE_LEAGUE_KEY


    @property
    def current_league(self) -> WorldLeague:
        return self.leagues[self.league_key]


    @property
    def club(self) -> Optional[CareerClub]:
        for club in self.current_league.clubs:
            if club.name == self.club_name:
                return club
        return None


    @property
    def current_date(self) -> date:
        return date(self.season, 7, 12) + timedelta(weeks=self.week)


    @staticmethod
    def format_date(value: date) -> str:
        months = (
            "JAN", 'FEB', "MAR", 'APR', 'MAY', "JUN",
            "JUL", 'AUG', 'SEP', 'OCT', "NOV", 'DEC',
        )
        return f"{value.day:02d} {months[value.month - 1]} {value.year}"


    @property
    def transfer_window_open(self) -> bool:
        return self.current_date.month in (1, 2, 7, 8)


    @property
    def trained_this_week(self) -> bool:
        return self.last_training_week == self.week


    @property
    def cup_name(self) -> str:
        return national_cup_name(self.current_league.country)

    def set_player_name(self, requested_name: object) -> bool:
        """Rename the player and their scorer entry without changing career progress."""
        name = sanitize_local_display_name(capitalise_player_initials(
            sanitize_local_display_name(requested_name, limit=32)), limit=32)
        old = self.player_name
        scorers = self.current_league.scorer_goals
        if name != old and name in scorers:
            raise ValueError('A scorer already has that name. Choose another name.')
        previous = dict(scorers)
        self.player_name = name
        if old in scorers:
            scorers[name] = scorers.pop(old)
        if not self.save():
            self.player_name = old
            scorers.clear()
            scorers.update(previous)
            return False
        self.message = f"Player: {name}."
        return True

    def rename_current_club(self, requested_name: object) -> str:
        """Rename only the user's current club locally; never fetch external assets."""
        new_name = sanitize_local_display_name(requested_name)
        club = self.club
        if club is None:
            raise ValueError("no active club")
        old_name = club.name
        club.name = new_name
        if self.club_name == old_name:
            self.club_name = new_name
        self.message = f"Local club name changed to {new_name}."
        self.save()
        return new_name

    def rename_current_competition(self, requested_name: object) -> str:
        """Rename the current league locally and persist it in the career save."""
        new_name = sanitize_local_display_name(requested_name, limit=56)
        self.current_league.name = new_name
        self.message = f"Local competition name changed to {new_name}."
        self.save()
        return new_name


    @property
    def cup_round_label(self) -> str:
        index = min(self.cup_round_index, len(CUP_ROUNDS) - 1)
        return CUP_ROUNDS[index]


    def difficulty_profile(self, international: bool = False) -> tuple[float, float]:
        """Tempo de remate e velocidade da mira para o nível competitivo."""
        if international:
            base_time, aim_speed = 3.75, 3.18
        else:
            tier = self.club.tier if self.club else 4
            profiles = {
                1: (4.35, 2.82),
                2: (4.95, 2.48),
                3: (5.55, 2.16),
                4: (6.15, 1.86),
                5: (6.65, 1.72),
            }
            base_time, aim_speed = profiles.get(tier, (6.65, 1.72))
        if not self.trained_this_week:
            base_time -= 1.20
        return max(2.70, base_time), aim_speed


    def _cup_fixture_for_week(
        self, requested_week: Optional[int] = None
    ) -> Optional[tuple[CareerClub, CareerClub]]:
        player = self.club
        if player is None:
            return None
        week_number = self.week if requested_week is None else requested_week
        cup_rng = random.Random(
            self.world_seed + self.season * 1009 + week_number * 7919
        )


        # Em Inglaterra, a carreira começa na League Two e segue a lógica da
        # FA Cup: L1/L2 na 1.ª ronda proper e PL/Championship a partir da 3.ª.
        # Os adversários são sempre nomes reais, nunca os placeholders do mundo.
        if self.current_league.country == "England":
            round_index = self.cup_round_index
            names = list(FA_CUP_EARLY_REAL_CLUBS)
            if round_index >= 2:
                names.extend(FA_CUP_BIG_REAL_CLUBS)
            names = [name for name in names if name != self.club_name]
            if not names:
                return None
            opponent_name = cup_rng.choice(names)
            existing = next(
                (club for league in self.leagues.values()
                 if league.country == "England"
                 for club in league.clubs if club.name == opponent_name),
                None,
            )
            if existing is None:
                rating = 82.0 if opponent_name in FA_CUP_BIG_REAL_CLUBS else 66.0
                tier = 1 if opponent_name in FA_CUP_BIG_REAL_CLUBS else 3
                existing = CareerClub(
                    opponent_name, "England", division_name("England", tier), tier,
                    rating + cup_rng.uniform(-5.0, 5.0),
                )
            opponent = existing
        else:
            # Nos restantes países, usa apenas clubes que tenham nome próprio.
            # Isto elimina entradas como "Portugal 1-04 FC" das taças.
            prefix = f"{self.current_league.country} "
            candidates = [
                club
                for league in self.leagues.values()
                if league.country == self.current_league.country
                for club in league.clubs
                if club.name != self.club_name
                and not (club.name.startswith(prefix) and club.name.endswith(" FC"))
            ]
            if not candidates:
                return None
            opponent = cup_rng.choice(candidates)


        return (player, opponent) if cup_rng.random() < 0.5 else (opponent, player)


    def next_match(self) -> Optional[tuple[str, CareerClub, CareerClub]]:
        if (
            self.cup_active
            and self.cup_round_index < len(CUP_WEEKS)
            and self.week == CUP_WEEKS[self.cup_round_index]
        ):
            cup_fixture = self._cup_fixture_for_week()
            if cup_fixture:
                return "cup", cup_fixture[0], cup_fixture[1]
        fixture = self.next_fixture()
        if fixture:
            return "league", fixture[0], fixture[1]
        return None


    def calendar_entries(self) -> list[dict[str, object]]:
        """Resultados recentes e próximos jogos com datas de calendário."""
        entries = list(self.fixture_history[-4:])
        future_week = self.week
        future_round = self.current_league.round_index
        future_cup_round = self.cup_round_index
        upcoming = 0
        while upcoming < 8 and future_week < self.week + 60:
            match_date = date(self.season, 7, 12) + timedelta(weeks=future_week)
            if (
                self.cup_active
                and future_cup_round < len(CUP_WEEKS)
                and future_week == CUP_WEEKS[future_cup_round]
            ):
                fixture = self._cup_fixture_for_week(future_week)
                if fixture:
                    entries.append({
                        "date": match_date.isoformat(),
                        "competition": self.cup_name,
                        "home": fixture[0].name,
                        "away": fixture[1].name,
                        "status": CUP_ROUNDS[future_cup_round],
                        "played": False,
                    })
                    upcoming += 1
                future_cup_round += 1
            elif future_round < self.current_league.total_rounds:
                fixture = next(
                    (
                        pair for pair in self.current_league.pairings(future_round)
                        if self.club_name in (pair[0].name, pair[1].name)
                    ),
                    None,
                )
                if fixture:
                    entries.append({
                        "date": match_date.isoformat(),
                        "competition": self.current_league.name,
                        "home": fixture[0].name,
                        "away": fixture[1].name,
                        "status": f"Matchweek {future_round + 1}",
                        "played": False,
                    })
                    upcoming += 1
                future_round += 1
            future_week += 1
        return entries


    def _build_world(self) -> None:
        for country in WORLD_COUNTRIES:
            depth = EUROPE_PYRAMID_DEPTH.get(country, 1)
            for tier in range(1, depth + 1):
                name = division_name(country, tier)
                if country == "England" and tier == 4:
                    names = list(LEAGUE_TWO_2026)
                else:
                    count = 18 if country in EUROPE_PYRAMID_DEPTH else 12
                    if country == "England" and tier in (2, 3):
                        count = 24
                    elif country == "England" and tier == 1:
                        count = 20
                    famous = list(FAMOUS_CLUBS.get(country, ())) if tier == 1 else []
                    names = famous + [
                        f"{country} {tier}-{number:02d} FC"
                        for number in range(1, count - len(famous) + 1)
                    ]
                base = 88.0 - (tier - 1) * 8.0
                if country not in ("England", "Spain", "Germany", "Italy", "France", "Portugal"):
                    base -= 4.0
                clubs = [
                    CareerClub(
                        club_name,
                        country,
                        name,
                        tier,
                        clamp(base + self.rng.uniform(-7.0, 7.0), 35.0, 96.0),
                    )
                    for club_name in names
                ]
                league = WorldLeague(country, name, tier, clubs)
                self.leagues[league.key] = league


        self.international_status = {
            "UEFA Champions League": "League phase - 36 clubs",
            "UEFA Europa League": "League phase - 36 clubs",
            "UEFA Conference League": "League phase - 36 clubs",
            "UEFA Nations League": "League phase - 54 nations",
            "European Championship": "Qualifying",
            "FIFA World Cup": "Qualifying - 6 confederations",
        }


    def _new_starting_offers(self) -> None:
        amount = self.rng.randint(1, 5)
        self.offers = self.rng.sample(list(LEAGUE_TWO_2026), amount)


    def accept_starting_offer(self, club_name: str) -> None:
        if club_name not in self.offers:
            return
        self.club_name = club_name
        self.message = f"Contract signed with {club_name}."
        self.save()


    def next_fixture(self) -> Optional[tuple[CareerClub, CareerClub]]:
        league = self.current_league
        if league.round_index >= league.total_rounds:
            return None
        for home, away in league.pairings():
            if home.name == self.club_name or away.name == self.club_name:
                return home, away
        return None


    def opponent_chance_profile(self, opponent: Optional[CareerClub] = None) -> OpponentChanceProfile:
        """Combine opponent quality with its own league position, once at kick-off."""
        if opponent is None:
            return OpponentChanceProfile(0.0, 3, 0.60)
        quality = clamp((opponent.rating - 45.0) / 45.0, 0.0, 1.0)
        rank_strength, rank_weight, played = 0.0, 0.0, 0
        for league in self.leagues.values():
            if league.country != opponent.country or league.tier != opponent.tier:
                continue
            table = league.table()
            match = next(((index, club) for index, club in enumerate(table)
                          if club.name == opponent.name), None)
            if match is not None:
                index, listed_club = match
                played = listed_club.played
                rank_strength = 1.0 - index / max(1, len(table) - 1)
                # Early tables carry little evidence; an unplayed table has none.
                rank_weight = 0.45 * min(max(0, played) / 5.0, 1.0)
                break
        pressure = quality * (1.0 - rank_weight) + rank_strength * rank_weight
        # An elite squad or an established top-15% side is a very strong opponent.
        if quality >= 0.88 or (played >= 5 and rank_strength >= 0.85):
            pressure = max(0.80, pressure)
        if pressure >= 0.72:
            return OpponentChanceProfile(pressure, 1, 0.0)
        if pressure >= 0.50:
            return OpponentChanceProfile(pressure, 2, 0.15)
        return OpponentChanceProfile(pressure, 3, 0.60 * (1.0 - pressure / 0.72))

    def chance_count(self, opponent: Optional[CareerClub] = None) -> int:
        factor = clamp((self.stamina + self.morale) / 40.0, 0.05, 1.0)
        profile = self.opponent_chance_profile(opponent)
        # A completed mandatory session must lead to at least one playable
        # highlight. Training goals help earn extra chances, never bypassing
        # the opponent's cap or its ban on clear chances.
        trained = self.trained_this_week
        training_goals = self.training_session_goals if trained and self.training_session_week == self.week else 0
        training_bonus = clamp(training_goals, 0, 3) * 0.15
        centre = 0.4 + factor * 2.5 + training_bonus - profile.pressure * 1.5
        return int(clamp(round(self.rng.gauss(centre, 0.70)), 1 if trained else 0, profile.max_chances))


    def fixture_goal_means(
        self, home: CareerClub, away: CareerClub
    ) -> tuple[float, float]:
        """Golos esperados segundo qualidade, classificação e forma atual."""
        league = self.current_league
        table = league.table()
        positions = {club.name: index for index, club in enumerate(table)}
        team_count = max(2, len(table))


        def competitive_strength(club: CareerClub) -> float:
            position = positions.get(club.name, team_count - 1)
            table_score = 1.0 - position / (team_count - 1)
            rating_score = clamp((club.rating - 40.0) / 55.0, 0.0, 1.0)
            if club.played:
                points_score = clamp(club.points / (club.played * 3.0), 0.0, 1.0)
                goal_form = clamp(
                    0.5 + club.goal_difference / max(4.0, club.played * 3.0),
                    0.0,
                    1.0,
                )
            else:
                points_score = table_score
                goal_form = 0.5
            return (
                table_score * 0.46
                + rating_score * 0.26
                + points_score * 0.18
                + goal_form * 0.10
            )


        difference = competitive_strength(home) - competitive_strength(away)
        advantage = math.log(MATCH_HOME_GOALS / MATCH_AWAY_GOALS) + difference * 1.55
        share = 1.0 / (1.0 + math.exp(-advantage))
        total = MATCH_HOME_GOALS + MATCH_AWAY_GOALS
        return total * share, total * (1.0 - share)


    def finish_match(
        self,
        home: CareerClub,
        away: CareerClub,
        player_goals: int,
        player_misses: int,
        is_international: bool = False,
        forced_score: Optional[tuple[int, int]] = None,
        competition: str = "league",
    ) -> tuple[int, int]:
        match_date = self.current_date
        if is_international:
            if forced_score is None:
                home_mean, away_mean = realistic_goal_means(home.rating, away.rating)
                portugal_goals = poisson_goal(self.rng, max(0.05, home_mean - 0.35)) + player_goals
                opponent_goals = poisson_goal(self.rng, away_mean)
            else:
                portugal_goals, opponent_goals = forced_score
            self.international_caps += 1
            self.international_goals += player_goals
            self.last_result = f"Portugal {portugal_goals}-{opponent_goals} {away.name}"
            self._update_attributes(player_goals, player_misses)
            self.fixture_history.append({
                "date": match_date.isoformat(),
                "competition": "Portugal",
                "home": home.name,
                "away": away.name,
                "status": self.last_result,
                "played": True,
            })
            self.fixture_history = self.fixture_history[-20:]
            self.save()
            return portugal_goals, opponent_goals


        league = self.current_league
        previous_league_goals = league.scorer_goals.get(self.player_name, 0)
        if forced_score is not None:
            score = forced_score
        else:
            player_home = home.name == self.club_name
            home_mean, away_mean = self.fixture_goal_means(home, away)
            player_mean = home_mean if player_home else away_mean
            opponent_mean = away_mean if player_home else home_mean
            player_base = poisson_goal(self.rng, max(0.05, player_mean - 0.35))
            opponent_base = poisson_goal(self.rng, opponent_mean)
            if player_home:
                score = (player_base + player_goals, opponent_base)
            else:
                score = (opponent_base, player_base + player_goals)


        decision = ""
        if competition == "cup":
            home_goals, away_goals = score
            player_home = home.name == self.club_name
            if home_goals == away_goals:
                shootout_chance = clamp(
                    0.50
                    + (self.morale - 10.0) * 0.015
                    + (self.stamina - 10.0) * 0.010,
                    0.34,
                    0.68,
                )
                player_won = self.rng.random() < shootout_chance
                if player_home == player_won:
                    penalties = (self.rng.randint(4, 6), self.rng.randint(2, 3))
                else:
                    penalties = (self.rng.randint(2, 3), self.rng.randint(4, 6))
                decision = f" (pen. {penalties[0]}-{penalties[1]})"
            else:
                player_won = (
                    home_goals > away_goals if player_home else away_goals > home_goals
                )
            self.cup_active = player_won
            round_name = self.cup_round_label
            self.cup_history.append(
                f"{round_name}: {home.name} {score[0]}-{score[1]} {away.name}{decision}"
            )
            self.cup_history = self.cup_history[-8:]
            self.cup_round_index += 1
        else:
            for fixture_home, fixture_away in league.pairings():
                if {fixture_home.name, fixture_away.name} == {home.name, away.name}:
                    league.simulate_fixture(fixture_home, fixture_away, self.rng, score,
                                            player_club=self.club_name, player_goals=player_goals)
                else:
                    league.simulate_fixture(fixture_home, fixture_away, self.rng)
            league.round_index += 1


        self.week += 1
        self.matches += 1
        self.goals += player_goals
        self.missed_chances += player_misses
        self.form_goals.append(player_goals)
        self.form_goals = self.form_goals[-8:]
        if competition != "cup":
            league.scorer_goals[self.player_name] = previous_league_goals + player_goals
        self._update_attributes(player_goals, player_misses)


        home_goals, away_goals = score
        self.last_result = (
            f"{home.name} {home_goals}-{away_goals} {away.name}{decision}"
        )
        self.message = self.last_result
        self.fixture_history.append({
            "date": match_date.isoformat(),
            "competition": self.cup_name if competition == "cup" else league.name,
            "home": home.name,
            "away": away.name,
            "status": f"{home_goals}-{away_goals}{decision}",
            "played": True,
        })
        self.fixture_history = self.fixture_history[-20:]
        if competition == "league":
            self._simulate_world_round()
        self._check_national_team()
        self._maybe_generate_transfer_offers()
        if competition == "league" and league.round_index >= league.total_rounds:
            self._finish_season()
        self.save()
        return score


    def _update_attributes(self, goals: int, misses: int) -> None:
        self.morale = clamp(self.morale + goals * 1.20 - misses * 0.25, 0.0, 20.0)
        self.stamina = clamp(
            self.stamina - 0.65 - misses * 0.08 + goals * 0.22,
            0.0,
            20.0,
        )


    @property
    def training_used_this_week(self) -> bool:
        return self.trained_this_week or self.training_session_week == self.week

    def begin_training(self) -> bool:
        """Reserve the career week's sole session before opening its first shot."""
        if not self.club_name:
            self.message = 'Choose a club before training.'
            return False
        if self.trained_this_week:
            self.message = 'This week’s training session has been used. Come back next week.'
            return False
        if self.training_session_week == self.week:
            self.message = 'Resume your weekly training session.'
            return True
        previous = (self.training_session_week, self.training_shots_taken, self.training_session_goals)
        self.training_session_week = self.week
        self.training_shots_taken = self.training_session_goals = 0
        self.message = 'Weekly training started.'
        if self.save() is False:
            self.training_session_week, self.training_shots_taken, self.training_session_goals = previous
            return False
        return True

    def record_training_shot(self, scored: bool) -> bool:
        if self.training_session_week != self.week or self.trained_this_week or self.training_shots_taken >= 3:
            return False
        previous = (self.training_shots_taken, self.training_session_goals)
        self.training_shots_taken += 1
        self.training_session_goals += int(bool(scored))
        if self.save() is False:
            self.training_shots_taken, self.training_session_goals = previous
            return False
        return True

    def complete_training(self, goals: int) -> float:
        if self.trained_this_week:
            self.message = 'This week’s training is already complete.'
            return 0.0
        goals = max(0, min(3, int(goals)))
        previous = (self.stamina, self.morale, self.last_training_week, self.training_session_week)
        self.stamina = clamp(self.stamina + 1.25 + goals * 0.25, 0.0, 20.0)
        self.morale = clamp(self.morale + max(0, goals - 1) * 0.20, 0.0, 20.0)
        self.last_training_week = self.week
        self.training_session_week = self.week
        self.message = f"Training complete: {goals}/3 goals. Energy increased."
        if self.save() is False:
            self.stamina, self.morale, self.last_training_week, self.training_session_week = previous
            return 0.0
        return self.stamina - previous[0]


    def _simulate_world_round(self) -> None:
        for key, league in self.leagues.items():
            if key == self.league_key or league.round_index >= league.total_rounds:
                continue
            for home, away in league.pairings():
                league.simulate_fixture(home, away, self.rng)
            league.round_index += 1


        # As competições internacionais avançam em semanas próprias sem
        # obrigar o Android a guardar milhares de objetos de eliminatórias.
        if self.week and self.week % 4 == 0:
            stage = 1 + self.week // 4
            if stage <= 8:
                self.international_status["UEFA Champions League"] = f"League phase - round {stage}/8"
                self.international_status["UEFA Europa League"] = f"League phase - round {stage}/8"
                self.international_status["UEFA Conference League"] = f"League phase - round {min(stage, 6)}/6"
            elif self.week < 44:
                knockout = "Round of 16" if self.week < 36 else "Semi-finals"
                self.international_status["UEFA Champions League"] = knockout
                self.international_status["UEFA Europa League"] = knockout
                self.international_status["UEFA Conference League"] = knockout
            else:
                european_tables = [
                    league.table() for league in self.leagues.values()
                    if league.country in EUROPE_PYRAMID_DEPTH and league.tier == 1
                ]
                winners = [table[0].name for table in european_tables if table]
                runners = [table[min(1, len(table) - 1)].name for table in european_tables if table]
                thirds = [table[min(2, len(table) - 1)].name for table in european_tables if table]
                if winners:
                    self.international_status["UEFA Champions League"] = f"Winner: {self.rng.choice(winners)}"
                    self.international_status["UEFA Europa League"] = f"Winner: {self.rng.choice(runners)}"
                    self.international_status["UEFA Conference League"] = f"Winner: {self.rng.choice(thirds)}"
        if self.week in (7, 11, 15, 19):
            self.international_status["UEFA Nations League"] = f"League phase - round {min(6, 2 + self.week // 4)}/6"


    def _check_national_team(self) -> None:
        club = self.club
        recent = sum(self.form_goals[-5:])
        self.called_up = bool(
            club and club.tier == 1 and self.matches >= 5
            and recent >= 4 and self.morale >= 13.0 and self.week % 4 == 0
        )
        if self.called_up:
            self.message = 'You have been called up to the national team!'


    def generate_agent_offers(
        self, guaranteed: bool = False
    ) -> list[tuple[str, str]]:
        if not self.transfer_window_open:
            self.agent_offers.clear()
            self.message = (
                "A janela de transferencias esta fechada. "
                "Abre em julho-agosto e janeiro-fevereiro."
            )
            return []
        performance = self.goals / max(1, self.matches)
        current_tier = self.club.tier if self.club else 4
        rise = 0
        if performance >= 0.45 and self.morale >= 11.0:
            rise = 1
        if performance >= 0.85 and self.morale >= 14.0:
            rise = 2
        best_tier = max(1, current_tier - rise)
        maximum = min(5, 1 + int(performance * 4.0) + int(self.morale >= 14.0))
        amount = self.rng.randint(1 if guaranteed else 0, max(1, maximum))
        candidates: list[tuple[str, str]] = []
        leagues = [
            league for league in self.leagues.values()
            if league.country in EUROPE_PYRAMID_DEPTH
            and best_tier <= league.tier <= min(5, current_tier + 1)
        ]
        # Clubes do mesmo país surgem com maior frequência, mas boas épocas
        # podem abrir portas noutros campeonatos europeus.
        domestic = [league for league in leagues if league.country == self.current_league.country]
        leagues.extend(domestic * 2)
        if not self.world_unlocked:
            # FREE has exactly one playable division.
            leagues = [self.leagues[FREE_LEAGUE_KEY]]
        self.rng.shuffle(leagues)
        seen: set[tuple[str, str]] = set()
        current_rating = self.club.rating if self.club else 60.0
        rating_ceiling = current_rating + 5.0 + performance * 12.0
        for league in leagues:
            clubs = [
                club for club in league.clubs
                if club.name != self.club_name and club.rating <= rating_ceiling
            ]
            if clubs:
                club = self.rng.choice(clubs)
                offer = (club.name, league.key)
                if offer not in seen:
                    candidates.append(offer)
                    seen.add(offer)
            if len(candidates) >= amount:
                break
        self.agent_offers = candidates
        self.last_offer_week = self.week
        self.message = (
            f"Your agent found {len(candidates)} offer(s)."
            if candidates else 'No offers yet. Score goals and try again.'
        )
        self.save()
        return candidates


    def _maybe_generate_transfer_offers(self) -> None:
        if not self.transfer_window_open:
            self.agent_offers.clear()
            return
        if self.agent_offers:
            return
        performance = self.goals / max(1, self.matches)
        probability = clamp(
            0.10 + performance * 0.30 + max(0.0, self.morale - 10.0) * 0.018,
            0.08,
            0.68,
        )
        if self.rng.random() < probability:
            self.generate_agent_offers(guaranteed=True)
            if self.agent_offers:
                self.message = (
                    f"Your agent received {len(self.agent_offers)} new offer(s)!"
                )


    def accept_transfer(self, club_name: str, league_key: str) -> None:
        if not self.transfer_window_open:
            self.message = 'Transfers can only be completed during an open window.'
            return
        if not self.is_league_playable(league_key):
            self.message = 'That league requires Scorer World.'
            return
        if (club_name, league_key) not in self.agent_offers:
            return
        self.club_name = club_name
        self.league_key = league_key
        self.agent_offers.clear()
        self.cup_active = False
        self.message = f"Transfer completed to {club_name}."
        self.save()


    def _finish_season(self) -> None:
        league = self.current_league
        table = league.table()
        position = next(
            (index + 1 for index, club in enumerate(table) if club.name == self.club_name),
            len(table),
        )
        promoted = position <= 3 or (4 <= position <= 7 and self.rng.random() < 0.35)
        relegated = position > len(table) - 2
        old_club = self.club
        target_tier = league.tier - 1 if promoted else league.tier + 1 if relegated else league.tier
        target_key = f"{league.country}|{target_tier}"
        if not self.world_unlocked:
            # FREE never crosses the single playable division boundary.
            promoted = relegated = False
            target_tier = league.tier
            target_key = FREE_LEAGUE_KEY
        if old_club and target_key in self.leagues and target_key != self.league_key:
            target = self.leagues[target_key]
            displaced = min(target.clubs, key=lambda club: club.rating)
            target.clubs.remove(displaced)
            target.clubs.append(
                CareerClub(old_club.name, league.country, target.name, target_tier, old_club.rating + (2 if promoted else -2))
            )
            self.league_key = target_key
        self.season += 1
        self.week = 0
        self.last_training_week = -1
        self.training_session_week = -1
        self.training_shots_taken = 0
        self.training_session_goals = 0
        self.cup_active = True
        self.cup_round_index = 0
        self.cup_history.clear()
        self.agent_offers.clear()
        self.last_offer_week = -99
        self.morale = clamp(self.morale + (2 if promoted else -1 if relegated else 0), 0, 20)
        self.stamina = clamp(self.stamina + 3.0, 0, 20)
        self.message = f"Season finished in position {position}. New season {self.season}/{str(self.season + 1)[-2:]}."
        if self.season % 4 == 0:
            self.international_status["European Championship"] = f"Winner: {self.rng.choice(EUROPE_COUNTRIES)}"
        else:
            self.international_status["European Championship"] = "Qualifying"
        if self.season % 4 == 2:
            self.international_status["FIFA World Cup"] = f"Winner: {self.rng.choice(WORLD_COUNTRIES)}"
        else:
            self.international_status["FIFA World Cup"] = "Qualifying - 6 confederations"
        self.national_cup_winners = {}
        for country in WORLD_COUNTRIES:
            candidates = [
                club
                for world_league in self.leagues.values()
                if world_league.country == country
                for club in world_league.clubs
            ]
            if candidates:
                weights = [max(1.0, club.rating - 30.0) ** 2 for club in candidates]
                self.national_cup_winners[country] = self.rng.choices(
                    candidates, weights=weights, k=1
                )[0].name
        for world_league in self.leagues.values():
            world_league.schedule_version = 2
            world_league.round_index = 0
            world_league.scorer_goals.clear()
            for club in world_league.clubs:
                club.played = club.won = club.drawn = club.lost = 0
                club.goals_for = club.goals_against = club.points = 0
        self.goals = 0
        self.matches = 0
        self.missed_chances = 0
        self.form_goals.clear()


    def save(self) -> bool:
        if not self.club_name:
            return True
        league = self.current_league
        data = {
            "save_version": self.SAVE_VERSION,
            "player_name": self.player_name,
            "nationality": self.nationality,
            "season": self.season,
            "week": self.week,
            "stamina": self.stamina,
            "morale": self.morale,
            "club_name": self.club_name,
            "league_key": self.league_key,
            "matches": self.matches,
            "goals": self.goals,
            "missed_chances": self.missed_chances,
            "form_goals": self.form_goals,
            "international_caps": self.international_caps,
            "international_goals": self.international_goals,
            "called_up": self.called_up,
            "world_seed": self.world_seed,
            "last_result": self.last_result,
            "message": self.message,
            "last_training_week": self.last_training_week,
            "training_session_week": self.training_session_week,
            "training_shots_taken": self.training_shots_taken,
            "training_session_goals": self.training_session_goals,
            "cup_active": self.cup_active,
            "cup_round_index": self.cup_round_index,
            "cup_history": self.cup_history,
            "national_cup_winners": self.national_cup_winners,
            "fixture_history": self.fixture_history,
            "agent_offers": self.agent_offers,
            "last_offer_week": self.last_offer_week,
            "league_round": league.round_index,
            "schedule_version": league.schedule_version,
            "league_name": league.name,
            "clubs": [asdict(club) for club in league.clubs],
            "scorers": league.scorer_goals,
            "international_status": self.international_status,
        }
        try:
            envelope = {
                "save_version": self.SAVE_VERSION,
                "career": data,
                "locked_world_career": self._locked_world_career,
            }
            target = self.save_path
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=target.parent,
                    prefix=".striker-", suffix=".tmp", delete=False,
                ) as output:
                    temporary = Path(output.name)
                    json.dump(envelope, output, ensure_ascii=False)
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temporary, target)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
        except OSError:
            self.message = 'Unable to save your career. Please try again.'
            return False
        return True


    def backup_before_new_game(self) -> bool:
        """Preserve the current save atomically before the user starts a new career."""
        temporary = None
        try:
            source = self.save_path
            if not source.exists():
                return True
            content = source.read_bytes()
            with tempfile.NamedTemporaryFile(dir=source.parent, prefix=".striker-backup-",
                                             suffix=".tmp", delete=False) as output:
                temporary = Path(output.name)
                output.write(content)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, source.with_name("striker_career.previous.json"))
            return True
        except OSError:
            self.message = 'Unable to back up your previous career. New game cancelled.'
            return False
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass  # Cleanup failure must not allow a new career to replace the save.

    def load(self) -> bool:
        # Work on isolated state: a damaged save must not partially replace a career.
        candidate = object.__new__(type(self))
        candidate.__dict__ = {key: (value if key == "entitlements" else copy.deepcopy(value))
                              for key, value in self.__dict__.items()}
        if candidate._load_saved_state():
            self.__dict__.update(candidate.__dict__)
            return bool(self.club_name)
        return False

    def _load_saved_state(self) -> bool:
        try:
            if not self.save_path.exists():
                return
            data = json.loads(self.save_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return
            raw = data
            version = int(raw.get("save_version", self.LEGACY_SAVE_VERSION))
            if version == self.LEGACY_SAVE_VERSION:
                active = dict(raw)
                active["save_version"] = self.SAVE_VERSION
                locked = None
            elif version == self.SAVE_VERSION:
                candidate = raw.get("career")
                locked_candidate = raw.get("locked_world_career")
                active = dict(candidate) if isinstance(candidate, dict) else None
                locked = dict(locked_candidate) if isinstance(locked_candidate, dict) else None
            else:
                return


            self._locked_world_career = locked
            if self.world_unlocked and self._locked_world_career is not None:
                active = self._locked_world_career
                self._locked_world_career = None
            if active is None:
                return
            key_for_access = str(active.get("league_key", FREE_LEAGUE_KEY))
            if not self.is_league_playable(key_for_access):
                self._locked_world_career = active
                self.message = (
                    'WORLD career preserved. Restore World access to continue it.'
                )
                return True
            data = active
            for name in ("national_cup_winners", "scorers", "international_status"):
                if not isinstance(data.get(name, {}), dict):
                    raise ValueError("Invalid saved mapping")
            for name in ("form_goals", "cup_history", "fixture_history", "agent_offers", "clubs"):
                if not isinstance(data.get(name, []), list):
                    raise ValueError("Invalid saved list")
            for name in ("player_name", "club_name", "nationality", "message", "last_result"):
                if name in data and not isinstance(data[name], str):
                    raise ValueError("Invalid saved text")
            for name in ("morale", "stamina"):
                value = float(data.get(name, 10))
                if not math.isfinite(value) or not 0 <= value <= 20:
                    raise ValueError("Invalid saved player state")
            if data.get("save_version") != self.SAVE_VERSION:
                return
            key = data.get("league_key", "England|4")
            if key not in self.leagues:
                return
            self.world_seed = int(data.get("world_seed", self.world_seed))
            self.rng = random.Random(self.world_seed + int(data.get("week", 0)))
            self.player_name = data.get("player_name", self.player_name)
            self.nationality = data.get("nationality", self.nationality)
            self.season = int(data.get("season", 2026))
            self.week = int(data.get("week", 0))
            self.stamina = float(data.get("stamina", 10.0))
            self.morale = float(data.get("morale", 10.0))
            self.club_name = data.get("club_name", "")
            self.league_key = key
            self.matches = int(data.get("matches", 0))
            self.goals = int(data.get("goals", 0))
            self.missed_chances = int(data.get("missed_chances", 0))
            self.form_goals = [int(value) for value in data.get("form_goals", [])][-8:]
            self.international_caps = int(data.get("international_caps", 0))
            self.international_goals = int(data.get("international_goals", 0))
            self.called_up = bool(data.get("called_up", False))
            self.last_result = data.get("last_result", "")
            self.message = 'Career loaded.'
            self.last_training_week = int(data.get("last_training_week", -1))
            self.training_session_week = int(data.get("training_session_week", self.last_training_week))
            self.training_shots_taken = int(data.get("training_shots_taken", 0))
            self.training_session_goals = int(data.get("training_session_goals", 0))
            if not 0 <= self.training_session_goals <= self.training_shots_taken <= 3:
                raise ValueError("Invalid saved training state")
            migrated_cup_round = sum(
                1 for cup_week in CUP_WEEKS if cup_week < self.week
            )
            self.cup_active = bool(data.get("cup_active", True))
            self.cup_round_index = int(
                data.get("cup_round_index", migrated_cup_round)
            )
            self.cup_history = [
                str(value) for value in data.get("cup_history", [])
            ][-8:]
            self.national_cup_winners = {
                str(country): str(winner)
                for country, winner in data.get("national_cup_winners", {}).items()
            }
            self.fixture_history = [
                dict(value) for value in data.get("fixture_history", [])
                if isinstance(value, dict)
            ][-20:]
            for entry in self.fixture_history:
                if key == FREE_LEAGUE_KEY and entry.get("competition") == "Liga Scorer":
                    entry["competition"] = "Scorer League"
                status = entry.get("status")
                if isinstance(status, str) and status.startswith("Jornada "):
                    entry["status"] = "Matchweek " + status[len("Jornada "):]
            self.agent_offers = [
                (str(value[0]), str(value[1]))
                for value in data.get("agent_offers", [])
                if isinstance(value, (list, tuple)) and len(value) == 2
                and str(value[1]) in self.leagues
                and self.is_league_playable(str(value[1]))
            ][:5]
            self.last_offer_week = int(data.get("last_offer_week", -99))
            schedule_version = int(data.get("schedule_version", 1))
            if schedule_version not in (1, 2):
                raise ValueError("Unsupported saved schedule")
            for world_league in self.leagues.values():
                world_league.schedule_version = schedule_version
            league = self.current_league
            saved_league_name = data.get("league_name")
            if key == FREE_LEAGUE_KEY and saved_league_name in (
                "England Division 4", "Divisão Striker", "Divisão Scorer", "Liga Scorer"
            ):
                saved_league_name = "Scorer League"
            if saved_league_name:
                try:
                    league.name = sanitize_local_display_name(saved_league_name, limit=56)
                except ValueError:
                    pass
            saved_clubs = data.get("clubs", [])
            if saved_clubs:
                league.clubs = [CareerClub(**club) for club in saved_clubs]
            if key == FREE_LEAGUE_KEY:
                for club in league.clubs:
                    club.league = league.name
            league.round_index = int(data.get("league_round", 0))
            if schedule_version == 1:
                # Upgrade only if every completed fixture retains its opponent
                # and venue. Never silently rewrite past home/away results.
                played = range(min(max(0, league.round_index), league.total_rounds))
                old_fixtures = [[(h.name, a.name) for h, a in league.pairings(r)] for r in played]
                league.schedule_version = 2
                compatible = all(old == [(h.name, a.name) for h, a in league.pairings(r)]
                                 for r, old in enumerate(old_fixtures))
                for world_league in self.leagues.values():
                    world_league.schedule_version = 2 if compatible else 1
            league.scorer_goals = {
                str(name): int(goals) for name, goals in data.get("scorers", {}).items()
            }
            league.migrate_scorer_names(protected_name=self.player_name)
            # Migrate the active player's spelling and scorer key together.
            # Do not overwrite another scorer if an older save has a collision.
            formatted_name = capitalise_player_initials(self.player_name)
            if formatted_name != self.player_name and formatted_name not in league.scorer_goals:
                if self.player_name in league.scorer_goals:
                    league.scorer_goals[formatted_name] = league.scorer_goals.pop(self.player_name)
                self.player_name = formatted_name
            self.international_status.update(data.get("international_status", {}))
            # Mantém todos os outros campeonatos na mesma semana da carreira
            # depois de fechar e voltar a abrir o jogo.
            for other_key, other_league in self.leagues.items():
                if other_key == self.league_key:
                    continue
                target_round = min(league.round_index, other_league.total_rounds)
                while other_league.round_index < target_round:
                    for home, away in other_league.pairings():
                        other_league.simulate_fixture(home, away, self.rng)
                    other_league.round_index += 1
            return True
        except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError):
            # Keep both the original file and all pre-load state intact.
            return False





"""Responsive, touch-friendly career menus for the original Kivy game."""
from career import EUROPE_PYRAMID_DEPTH, WORLD_COUNTRIES
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView

INK = (0.91, 0.96, 0.95, 1)
MUTED = (0.58, 0.72, 0.72, 1)
GREEN = (0.30, 0.91, 0.65, 1)
MENU_VIEWS = frozenset(('offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent', 'world', 'splash', 'start'))


class FlowLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', INK)
        kwargs.setdefault('font_size', sp(15))
        super().__init__(size_hint_y=None, halign='left', valign='middle', **kwargs)
        self.bind(width=self._wrap, texture_size=self._height)
        self._wrap()

    def _wrap(self, *_):
        self.text_size = (max(dp(1), self.width), None)

    def _height(self, *_):
        self.height = max(dp(24), self.texture_size[1] + dp(4))


class TouchButton(Button):
    def __init__(self, text, callback, accent=False, **kwargs):
        super().__init__(text=text, size_hint_y=None, height=dp(52),
                         font_size=sp(14), bold=True, color=INK,
                         background_normal='', background_down='',
                         background_color=(0.08, 0.42, 0.30, 1) if accent else (0.08, 0.19, 0.22, 1),
                         halign='center', valign='middle', **kwargs)
        self.bind(width=self._fit, texture_size=self._fit)
        self.bind(on_release=lambda *_: callback())
        self._fit()

    def _fit(self, *_):
        self.text_size = (max(dp(1), self.width - dp(24)), None)
        self.height = max(dp(52), self.texture_size[1] + dp(24))


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None,
                         padding=dp(18), spacing=dp(12), **kwargs)
        self.bind(minimum_height=self.setter('height'))
        with self.canvas.before:
            Color(0.035, 0.10, 0.12, 1)
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._rect, size=self._rect)

    def _rect(self, *_):
        self._background.pos, self._background.size = self.pos, self.size

    def label(self, text, heading=False, muted=False):
        label = FlowLabel(text=str(text), font_size=sp(18 if heading else 15),
                          bold=heading, color=GREEN if heading else MUTED if muted else INK)
        self.add_widget(label)
        return label


class CareerMenu(BoxLayout):
    def __init__(self, game, **kwargs):
        super().__init__(orientation='vertical', padding=dp(16), spacing=dp(12), **kwargs)
        self.game = game
        self._signature = None
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._stadium = Rectangle(texture=CoreImage('assets/menu_stadium.png').texture,
                                      pos=self.pos, size=self.size)
            self._shade = Color(0.012, 0.035, 0.05, 0.62)
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self._rect, size=self._rect)
        self.sync()

    def _rect(self, *_):
        self._background.pos, self._background.size = self.pos, self.size
        self._stadium.pos, self._stadium.size = self.pos, self.size

    def sync(self):
        self.pos, self.size = self.game.pos, self.game.size
        c = self.game.career
        signature = (self.game.view, c.player_name, c.club_name, c.season, c.week,
                     c.matches, c.goals, c.stamina, c.morale, c.message,
                     c.current_league.name, tuple(c.agent_offers),
                     self.game.training_completed, self.game.training_goals, c.world_unlocked)
        if signature != self._signature:
            self._signature = signature
            self._build()

    def action(self, name, value=None):
        self.game._activate_ui(name, value)
        self.game.draw()

    def _button(self, label, action, value=None, accent=False):
        return TouchButton(label, lambda: self.action(action, value), accent)

    def _build(self):
        self.clear_widgets()
        self._shade.a = 1 if self.game.view == 'splash' else 0.62
        if self.game.view in ('splash', 'start'):
            self.padding = self.spacing = 0
            self.scroll = None
            self.body = SplashScreen(self) if self.game.view == 'splash' else EntryScreen(self)
            self.add_widget(self.body)
            return
        self.padding = dp(12) if self.game.view == 'hub' else dp(16)
        self.spacing = dp(8) if self.game.view == 'hub' else dp(12)
        header = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(8))
        brand = BoxLayout(orientation='vertical')
        if self.game.view == 'hub':
            header.height = dp(52)
            header.add_widget(Image(source='assets/icon.png', size_hint_x=None, width=dp(48)))
            brand.add_widget(BoundedLabel(text='SCORER', font_size=sp(22), bold=True))
            brand.add_widget(BoundedLabel(text='by clemir', font_size=sp(11), color=MUTED))
        else:
            brand.add_widget(FlowLabel(text='SCORER', font_size=sp(22), bold=True))
            brand.add_widget(FlowLabel(text='CARREIRA DE AVANÇADO', font_size=sp(10), color=MUTED))
            brand.bind(minimum_height=lambda widget, value: setattr(header, 'height', max(dp(60), value)))
        header.add_widget(brand)
        if self.game.view not in ('hub', 'offers'):
            back = self._button('VOLTAR', 'hub')
            back.size_hint_x, back.width = None, dp(88)
            header.add_widget(back)
        if self.game.view in ('hub', 'offers'):
            exit_button = TouchButton('SAIR', self.game._request_exit)
            exit_button.size_hint_x, exit_button.width = None, dp(76)
            header.add_widget(exit_button)
        self.add_widget(header)
        if self.game.view == 'hub':
            self.scroll = None
            self.body = MainDashboard(self)
            self.add_widget(self.body)
            return
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(4), scroll_type=['bars', 'content'])
        self.body = GridLayout(cols=1, spacing=dp(16), padding=[0, 0, dp(4), dp(12)], size_hint_y=None)
        self.body.bind(minimum_height=self.body.setter('height'))
        self.scroll.add_widget(self.body)
        self.add_widget(self.scroll)
        getattr(self, '_' + self.game.view)()

    def card(self, title=None):
        card = Card()
        if title:
            card.label(title, heading=True)
        self.body.add_widget(card)
        return card

    def _offers(self):
        card = self.card('O teu primeiro contrato')
        card.label('Uma divisão. A tua carreira começa aqui.', muted=True)
        for club in self.game.career.offers:
            card.add_widget(self._button(club, 'accept_offer', club, accent=True))

    def _training(self):
        g, c = self.game, self.game.career
        card = self.card('Treino de finalização')
        card.label('Três remates à baliza. Melhora a energia e a confiança antes do próximo jogo.')
        if g.training_completed:
            card.label(f'Treino concluído · {g.training_goals}/3 golos', heading=True)
            card.label(f'Energia: {g.training_stamina_before:.1f} → {c.stamina:.1f}')
        card.label(f'Energia atual: {c.stamina:.1f}/20', muted=True)
        card.add_widget(self._button('NOVO TREINO' if g.training_completed else 'INICIAR TREINO', 'training_start', accent=True))

    def _table(self, headings, rows, widths):
        # Both axes scroll at small widths; numeric columns never overlap names.
        self.scroll.do_scroll_x = True
        self.body.size_hint_x = None
        minimum_width = sum(dp(value) for value in widths) + dp(40 + 4 * (len(widths) - 1))
        self.scroll.bind(width=lambda widget, value: setattr(self.body, 'width', max(value, minimum_width)))
        self.body.width = max(self.scroll.width, minimum_width)
        card = self.card()
        for index, values in enumerate([headings] + list(rows)):
            row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(4))
            for text, width in zip(values, widths):
                cell = Label(text=str(text), size_hint_x=None, width=dp(width), font_size=sp(14),
                             color=GREEN if index == 0 else INK, bold=index == 0,
                             halign='left', valign='middle', shorten=True, shorten_from='right', max_lines=1)
                cell.bind(size=lambda widget, value: setattr(widget, 'text_size', value))
                cell.text_size = cell.size
                row.add_widget(cell)
            card.add_widget(row)

    def _standings(self):
        self.card('Classificação').label(self.game.career.current_league.name, muted=True)
        rows = [(i + 1, club.name, club.played, club.won, club.drawn, club.lost,
                 club.goals_for, club.goals_against, club.goal_difference, club.points)
                for i, club in enumerate(self.game.career.current_league.table())]
        self._table(('POS', 'CLUBE', 'J', 'V', 'E', 'D', 'GM', 'GS', 'DG', 'PTS'), rows,
                    (36, 220, 36, 36, 36, 36, 40, 40, 40, 44))

    def _scorers(self):
        c = self.game.career
        ranking = dict(c.current_league.scorer_goals)
        ranking[c.player_name] = c.goals
        self.card('Marcadores')
        self._table(('POS', 'JOGADOR', 'GOLOS'),
                    [(i + 1, name, goals) for i, (name, goals) in enumerate(sorted(ranking.items(), key=lambda item: (-item[1], item[0]))[:30])],
                    (40, 320, 64))

    def _calendar(self):
        self.card('Calendário')
        for entry in self.game.career.calendar_entries():
            card = self.card(str(entry.get('date', '')))
            card.label(f"{entry.get('home', '')} vs {entry.get('away', '')}")
            card.label(f"{entry.get('competition', '')} · {entry.get('status', '')}", muted=True)

    def _agent(self):
        c = self.game.career
        card = self.card('O teu agente')
        card.label(c.message)
        card.label('Janela aberta' if c.transfer_window_open else 'Janela fechada · julho/agosto e janeiro/fevereiro', muted=True)
        for club, key in c.agent_offers:
            card.add_widget(self._button(f'{club}\n{c.leagues[key].name}', 'transfer', (club, key)))
        card.add_widget(self._button('PROCURAR PROPOSTAS', 'agent_refresh'))

    def _world(self):
        if not self.game.career.world_unlocked:
            self.card('Edição gratuita').label('Uma divisão disponível nesta edição.')
            return
        self.card('Mundo do futebol')
        competitions = self.card('Competições')
        for title, status in self.game.career.international_status.items():
            competitions.label(f'{title} · {status}')
        for country in sorted(WORLD_COUNTRIES):
            depth = EUROPE_PYRAMID_DEPTH.get(country, 1)
            self.card(country).label(f'{depth} divisões')


class MatchNotice(BoxLayout):
    """Scroll long match messages while keeping the action reachable on phones."""
    def __init__(self, game, **kwargs):
        super().__init__(orientation='vertical', padding=dp(14), spacing=dp(10),
                         size_hint=(None, None), **kwargs)
        self.game = game
        self.signature = None
        with self.canvas.before:
            Color(0.015, 0.055, 0.065, 0.97)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._rect, size=self._rect)
        self.scroll = ScrollView(do_scroll_x=False)
        self.body = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.body.bind(minimum_height=self.body.setter('height'))
        self.scroll.add_widget(self.body)
        self.add_widget(self.scroll)
        self.button = MenuTile('CONTINUAR', self.proceed, accent=True)
        self.button.size_hint_x = None
        self.button.width = dp(176)
        self.button.pos_hint = {'right': 1}
        self.add_widget(self.button)
        self.body.bind(minimum_height=self._fit_panel)
        self.button.bind(height=self._fit_panel)

    def _fit_panel(self, *_):
        available = max(dp(96), self.game.height - dp(128))
        natural = self.body.minimum_height + self.button.height + dp(38)
        self.height = min(natural, available)
        self.center = self.game.center

    def _rect(self, *_):
        self.background.pos, self.background.size = self.pos, self.size

    def sync(self):
        game = self.game
        self.width = min(game.width * 0.76, dp(460))
        self._fit_panel()
        signature = (game.match_finished, game.match_summary, game.career.morale, game.career.stamina)
        if signature == self.signature:
            return
        self.signature = signature
        self.body.clear_widgets()
        title = game.match_summary if game.match_finished else 'OPORTUNIDADE'
        self.body.add_widget(FlowLabel(text=title, font_size=sp(17), bold=True, color=GREEN))
        detail = (f'Moral {game.career.morale:.1f}/20  ·  Energia {game.career.stamina:.1f}/20'
                  if game.match_finished else 'Prepara o teu remate e marca a diferença.')
        self.body.add_widget(FlowLabel(text=detail, font_size=sp(13)))
        self.button.text = 'CONTINUAR' if game.match_finished else 'JOGAR OPORTUNIDADE'

    def proceed(self):
        if self.game.match_finished:
            self.game._activate_ui('match_continue')
        else:
            self.game._begin_pending_chance()
        self.game.draw()


class BoundedLabel(Label):
    """A concise dashboard field, constrained to its allocated area."""
    def __init__(self, **kwargs):
        kwargs.setdefault('color', INK)
        kwargs.setdefault('font_size', sp(13))
        kwargs.setdefault('max_lines', 2)
        self._preferred_font = kwargs['font_size']
        kwargs.setdefault('halign', 'left')
        super().__init__(valign='middle', shorten=True,
                         shorten_from='right', **kwargs)
        self.bind(size=self._bounds)
        self._bounds()

    def _bounds(self, *_):
        self.font_size = min(self._preferred_font, max(dp(10), self.height * 0.82))
        self.text_size = (max(1, self.width), max(1, self.height))


class MenuTile(TouchButton):
    """Fixed touch area: labels cannot expand the main menu beyond the screen."""
    def __init__(self, text, callback, accent=False):
        super().__init__(text, callback, accent=accent)
        self.font_size = sp(13)
        self.shorten = True
        self.shorten_from = 'right'
        self.max_lines = 2
        self.height = dp(52)
        self._fit()

    def _fit(self, *_):
        self.text_size = (max(1, self.width - dp(16)), max(1, self.height - dp(12)))


class EdgePanel(BoxLayout):
    """Quiet stadium overlay with one accent edge, rather than large solid tiles."""
    def __init__(self, **kwargs):
        kwargs.setdefault('padding', dp(10))
        kwargs.setdefault('spacing', dp(4))
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.02, 0.06, 0.09, 0.90)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
            Color(*GREEN)
            self.edge = Line(points=[self.x, self.top, self.right, self.top], width=1)
        self.bind(pos=self._rect, size=self._rect)

    def _rect(self, *_):
        self.background.pos, self.background.size = self.pos, self.size
        self.edge.points = [self.x, self.top, self.right, self.top]


class SplashScreen(FloatLayout):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_widget(Image(source='assets/splash.png', fit_mode='contain'))
        self.add_widget(BoundedLabel(text='TAP TO START', font_size=sp(13), bold=True,
                                    halign='center', size_hint=(1, None), height=dp(32),
                                    pos_hint={'x': 0, 'y': 0}))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not getattr(touch, 'is_mouse_scrolling', False):
            self.menu.action('splash_continue')
            return True
        return super().on_touch_down(touch)


class EntryScreen(FloatLayout):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.panel = EdgePanel(orientation='vertical', size_hint=(None, None))
        self.panel.add_widget(BoundedLabel(text='SCORER by clemir', font_size=sp(20), bold=True,
                                          size_hint_y=None, height=dp(28)))
        self.info = BoundedLabel(text='A tua carreira. Uma divisão. Todos os golos contam.',
                                 color=MUTED, font_size=sp(12))
        if menu.game.career.message.startswith('Não foi possível'):
            self.info.text = menu.game.career.message
        self.panel.add_widget(self.info)
        self.panel.add_widget(MenuTile('NOVO JOGO', lambda: menu.action('new_game'), accent=True))
        load = MenuTile('CARREGAR JOGO', lambda: menu.action('load_game'))
        load.disabled = not menu.game.career.save_path.is_file()
        self.panel.add_widget(load)
        self.panel.add_widget(MenuTile('SAIR', menu.game._request_exit))
        self.add_widget(self.panel)
        self.bind(pos=self._fit, size=self._fit)
        self._fit()

    def _fit(self, *_):
        self.panel.size = (min(self.width - dp(24), dp(340)), min(self.height - dp(16), dp(280)))
        self.panel.center = self.center
        if self.panel.height < dp(250) and self.info.parent is self.panel:
            self.panel.remove_widget(self.info)
        elif self.panel.height >= dp(250) and self.info.parent is None:
            self.panel.add_widget(self.info, index=3)


class MainDashboard(BoxLayout):
    """Match first; secondary destinations form one compact navigation strip."""
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(6))
        self.menu = menu
        c = menu.game.career
        self.identity = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(12))
        self.identity.add_widget(BoundedLabel(text=c.player_name, font_size=sp(18), bold=True, color=GREEN))
        self.identity.add_widget(BoundedLabel(text=c.club_name, font_size=sp(14)))
        self.identity.add_widget(BoundedLabel(text=f'Energia {c.stamina:.1f}/20 · Moral {c.morale:.1f}/20',
                                             color=MUTED, font_size=sp(11)))
        self.add_widget(self.identity)
        self.hero = BoxLayout(spacing=dp(12))
        self.match = EdgePanel(orientation='vertical', size_hint_x=0.66)
        self.match.add_widget(BoundedLabel(text='PRÓXIMO JOGO', color=GREEN, font_size=sp(10),
                                          bold=True, size_hint_y=None, height=dp(16)))
        fixture = c.next_match()
        teams = BoxLayout(spacing=dp(8))
        home = fixture[1].name if fixture else 'Época concluída'
        away = fixture[2].name if fixture else ''
        teams.add_widget(BoundedLabel(text=home, font_size=sp(18), bold=True, halign='center'))
        teams.add_widget(BoundedLabel(text='VS' if fixture else '', font_size=sp(11), color=MUTED,
                                     halign='center', size_hint_x=0.18))
        teams.add_widget(BoundedLabel(text=away, font_size=sp(18), bold=True, halign='center'))
        self.match.add_widget(teams)
        footer = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        footer.add_widget(BoundedLabel(text=c.format_date(c.current_date), font_size=sp(11), color=MUTED))
        self.play = MenuTile('JOGAR', lambda: menu.action('play'), accent=True)
        self.play.size_hint_x, self.play.width = None, dp(136)
        footer.add_widget(self.play)
        self.match.add_widget(footer)
        self.hero.add_widget(self.match)
        self.season = EdgePanel(orientation='vertical', size_hint_x=0.34)
        self.season.add_widget(BoundedLabel(text='A TUA ÉPOCA', color=GREEN, font_size=sp(10),
                                           bold=True, size_hint_y=None, height=dp(16)))
        numbers = BoxLayout(spacing=dp(8))
        for number, title in ((c.matches, 'JOGOS'), (c.goals, 'GOLOS')):
            column = BoxLayout(orientation='vertical')
            column.add_widget(BoundedLabel(text=str(number), font_size=sp(30), bold=True, halign='center'))
            column.add_widget(BoundedLabel(text=title, font_size=sp(10), color=MUTED, halign='center',
                                           size_hint_y=None, height=dp(20)))
            numbers.add_widget(column)
        self.season.add_widget(numbers)
        self.season.add_widget(BoundedLabel(text=c.current_league.name + (' · 1 DIVISÃO' if not c.world_unlocked else ''),
                                           color=MUTED, font_size=sp(11), size_hint_y=None, height=dp(26)))
        self.hero.add_widget(self.season)
        self.add_widget(self.hero)
        self.actions = GridLayout(cols=5, spacing=dp(6), size_hint_y=None, height=dp(52))
        for title, action in [('TREINO', 'training'), ('CLASSIFICAÇÃO', 'standings'),
                              ('MARCADORES', 'scorers'), ('CALENDÁRIO', 'calendar'), ('AGENTE', 'agent')]:
            button = MenuTile(title, lambda name=action: menu.action(name))
            self.actions.add_widget(button)
        self.add_widget(self.actions)
        self.status = BoundedLabel(text=c.message, color=MUTED, font_size=sp(11),
                                   size_hint_y=None, height=dp(24))
        self.add_widget(self.status)
        self.bind(size=self._arrange)
        self._arrange()

    def _arrange(self, *_):
        tiny = self.height < dp(215)
        portrait = self.width < dp(480) and self.height > dp(400)
        self.identity.height = dp(24 if tiny else 36)
        if tiny:
            if self.hero.parent is self:
                self.remove_widget(self.hero)
                self.play.parent.remove_widget(self.play)
                self.play.size_hint_x = 1
                self.actions.add_widget(self.play, index=len(self.actions.children))
            self.actions.cols = 3
        else:
            if self.hero.parent is None:
                self.actions.remove_widget(self.play)
                self.play.size_hint_x, self.play.width = None, dp(136)
                self.match.children[0].add_widget(self.play)
                self.add_widget(self.hero, index=2)
            self.actions.cols = 2 if portrait else 5
        rows = (len(self.actions.children) + self.actions.cols - 1) // self.actions.cols
        self.actions.height = rows * dp(52) + (rows - 1) * dp(6)
        self.hero.orientation = 'vertical' if portrait else 'horizontal'
        self.match.size_hint = (1, 0.60) if portrait else (0.66, 1)
        self.season.size_hint = (1, 0.40) if portrait else (0.34, 1)

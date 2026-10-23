"""Responsive, touch-friendly career menus for the original Kivy game."""
from career import EUROPE_PYRAMID_DEPTH, WORLD_COUNTRIES
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView

INK = (0.91, 0.96, 0.95, 1)
MUTED = (0.58, 0.72, 0.72, 1)
GREEN = (0.30, 0.91, 0.65, 1)
MENU_VIEWS = frozenset(('offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent', 'world'))


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
            Color(0.012, 0.035, 0.05, 1)
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self._rect, size=self._rect)
        self.sync()

    def _rect(self, *_):
        self._background.pos, self._background.size = self.pos, self.size

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
        header = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(8))
        brand = BoxLayout(orientation='vertical')
        brand.add_widget(FlowLabel(text='STRIKER', font_size=sp(22), bold=True))
        brand.add_widget(FlowLabel(text='CARREIRA DE AVANÇADO', font_size=sp(10), color=MUTED))
        brand.bind(minimum_height=lambda widget, value: setattr(header, "height", max(dp(60), value)))
        header.add_widget(brand)
        if self.game.view not in ('hub', 'offers'):
            back = self._button('VOLTAR', 'hub')
            back.size_hint_x, back.width = None, dp(88)
            header.add_widget(back)
        exit_button = TouchButton('SAIR', self.game._request_exit)
        exit_button.size_hint_x, exit_button.width = None, dp(76)
        header.add_widget(exit_button)
        self.add_widget(header)
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

    def _hub(self):
        c = self.game.career
        grid = GridLayout(cols=1, spacing=dp(16), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.body.add_widget(grid)
        summary = Card()
        grid.add_widget(summary)
        summary.label(c.player_name, heading=True)
        summary.label(c.club_name)
        summary.label(f'{c.current_league.name} · {c.season}/{str(c.season + 1)[-2:]}', muted=True)
        summary.label(c.format_date(c.current_date), muted=True)
        for title, value in (('ENERGIA', c.stamina), ('MORAL', c.morale)):
            summary.label(f'{title}  {value:.1f}/20', muted=True)
            summary.add_widget(ProgressBar(max=20, value=value, size_hint_y=None, height=dp(10)))
        summary.label(f'{c.matches} jogos   ·   {c.goals} golos')
        fixture = c.next_match()
        summary.label('PRÓXIMO JOGO', heading=True)
        summary.label(f'{fixture[1].name} vs {fixture[2].name}' if fixture else 'Época concluída')
        actions = Card()
        grid.add_widget(actions)
        actions.label('A tua carreira', heading=True)
        for title, action in [('JOGAR', 'play'), ('TREINO · 3 REMATES', 'training'),
                              ('CLASSIFICAÇÃO', 'standings'), ('MARCADORES', 'scorers'),
                              ('CALENDÁRIO', 'calendar'), ('AGENTE', 'agent')]:
            actions.add_widget(self._button(title, action, accent=action == 'play'))
        if c.world_unlocked:
            actions.add_widget(self._button('MUNDO DO FUTEBOL', 'world'))
            actions.add_widget(self._button('EDITOR LOCAL', 'editor'))
        def arrange(widget, width):
            wide = width >= dp(760)
            order = (summary, actions) if wide else (actions, summary)
            if getattr(widget, '_card_order', None) != order:
                widget._card_order = order
                widget.clear_widgets()
                widget.cols = 2 if wide else 1
                for card in order:
                    widget.add_widget(card)
        grid.bind(width=arrange)
        arrange(grid, grid.width)
        status = self.card()
        status.label(c.message)
        status.label('EDIÇÃO GRATUITA · UMA DIVISÃO', muted=True)

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

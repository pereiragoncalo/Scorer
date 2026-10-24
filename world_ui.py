"""World catalogue, compact actions and local display-name forms for Kivy."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from menu_ui import MenuTile, BoundedLabel, Card, CompactTable

HELP_PAGES = (
    ('YOUR CAREER', 'Choose New Game or Load Game. Pick a player name and a first contract. Free starts in Scorer League with no country selection. World has a separate career, with local-country contracts and England Division 4 as an option.'),
    ('TRAIN, THEN PLAY', 'Complete the three-shot weekly training to unlock Play. A session can be resumed and cannot be repeated that week. Energy and morale influence your opportunities. Progress saves automatically.'),
    ('TAKE YOUR CHANCE', 'Tap inside the goal to aim and shoot, or use the shoot control with the moving aim. Watch power and the time-to-shoot countdown. Opponent strength changes chance quantity and difficulty. Continue at half-time and full-time.'),
    ('ADS, WORLD & NAMES', 'Free uses ads when available, without blocking offline play. Optional training ads can earn +1 morale once per career week. World unlocks ad-free play with worldwide fictional leagues and a local names editor. Upgrade explains availability; it never charges automatically.'),
)


class CompactHub(BoxLayout):
    """Small windows keep every action visible instead of squeezing the header."""
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(4))
        c = menu.game.career
        self.add_widget(Image(source='assets/menu_logo.png', size_hint_y=None, height=dp(32)))
        actions = GridLayout(cols=4, spacing=dp(4))
        entries = [('TRAINING', 'training'), ('PLAY', 'play'), ('STANDINGS', 'standings'),
                   ('TOP SCORERS', 'scorers'), ('FIXTURES', 'calendar'), ('AGENT', 'agent'),
                   ('PLAYER', 'profile'), ('PRIVACY', 'privacy'), ('HELP', 'help'),
                   ('MODES' if menu.game._world_available else 'UPGRADE', 'upgrade'), ('EXIT', 'exit')]
        for title, action in entries:
            button = MenuTile(title, lambda a=action: menu.action(a), accent=action == 'play')
            button.font_size = sp(12)
            if action == 'play': button.disabled = not c.trained_this_week
            actions.add_widget(button)
        self.add_widget(actions)


class WorldBrowser(BoxLayout):
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(6))
        self.menu = menu
        c = menu.game.career
        self.search = TextInput(text='', hint_text='Search country / football region', multiline=False,
                                size_hint_y=None, height=dp(48), font_size=sp(14),
                                background_normal='', background_active='', background_color=(.06,.14,.17,1),
                                foreground_color=(.94,.98,.97,1), hint_text_color=(.65,.76,.78,1),
                                cursor_color=(.3,1,.7,1), padding=[dp(10),dp(12)])
        self.add_widget(self.search)
        self.grid = GridLayout(cols=3, spacing=dp(6))
        self.add_widget(self.grid)
        controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        controls.add_widget(MenuTile('PREVIOUS', lambda: self.move(-1)))
        self.counter = BoundedLabel(halign='center', size_hint_x=.3)
        controls.add_widget(self.counter)
        controls.add_widget(MenuTile('NEXT', lambda: self.move(1)))
        self.add_widget(controls)
        self.countries = sorted({v.country for v in c.leagues.values()})
        self.page = self.countries.index(c.current_league.country) // 6
        self.search.bind(text=self.filter)
        self.render()

    def filter(self, *_):
        self.page = 0
        self.render()

    def move(self, direction):
        self.page += direction
        self.render()

    def render(self):
        selected = [c for c in self.countries if self.search.text.casefold() in c.casefold()]
        pages = max(1, (len(selected)+5)//6)
        self.page = max(0, min(pages-1, self.page))
        self.counter.text = f'{self.page+1}/{pages}'
        self.grid.clear_widgets()
        for country in selected[self.page*6:self.page*6+6]:
            depth = sum(v.country == country for v in self.menu.game.career.leagues.values())
            self.grid.add_widget(MenuTile(f'{country}\n{depth} divisions', lambda c=country: self.menu.action('world_country', c)))


class NamesEditor(Card):
    def __init__(self, menu):
        super().__init__()
        self.padding, self.spacing = dp(8), dp(4)
        self.menu = menu
        c, game = menu.game.career, menu.game
        league = c.leagues[game.editor_key]
        game.editor_club_index %= len(league.clubs)
        club = league.clubs[game.editor_club_index]
        self.club = club
        controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        controls.add_widget(MenuTile('PREVIOUS CLUB', lambda: menu.action('editor_club', -1)))
        controls.add_widget(MenuTile('NEXT CLUB', lambda: menu.action('editor_club', 1)))
        self.add_widget(controls)
        inputs = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(8))
        for title, text, attr in [('CLUB NAME', c.display_club(club), 'club_name'),
                                 ('LEAGUE NAME', c.display_aliases['leagues'].get(league.key, league.name), 'league_name')]:
            column = BoxLayout(orientation='vertical', spacing=dp(4))
            column.add_widget(BoundedLabel(text=title, font_size=sp(12), size_hint_y=None, height=dp(20)))
            field = TextInput(text=text, multiline=False, size_hint_y=None, height=dp(52),
                              font_size=sp(16), background_normal='', background_active='',
                              background_color=(.06,.14,.17,1), foreground_color=(.94,.98,.97,1),
                              cursor_color=(.3,1,.7,1), padding=[dp(10),dp(14)])
            setattr(self, attr, field)
            column.add_widget(field)
            inputs.add_widget(column)
        self.add_widget(inputs)
        files = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        files.add_widget(MenuTile('SAVE NAMES', self.save_names, accent=True))
        files.add_widget(MenuTile('EXPORT TEMPLATE', lambda: menu.action('names_export')))
        files.add_widget(MenuTile('IMPORT JSON', lambda: menu.action('names_import')))
        files.add_widget(MenuTile('JSON FORMAT', lambda: menu.action('names_format')))
        self.add_widget(files)
        note = self.label('Export this league’s clubs and players; import JSON to preview. Names stay on this device.', muted=True)
        note.font_size = sp(12)
        if c.message.startswith(('Local names', 'Name pack', 'Could not', 'Names must', 'Unknown name')):
            self.label(c.message, muted=True)

    def save_names(self):
        pack = {'version':1, 'clubs':{self.club.uid:self.club_name.text},
                'leagues':{self.menu.game.editor_key:self.league_name.text}}
        try:
            self.menu.game.career.apply_names(pack)
            self.menu.game.career.message = 'Local names saved. Career progress is unchanged.'
        except ValueError as error:
            self.menu.game.career.message = str(error)
        self.menu.game.draw()

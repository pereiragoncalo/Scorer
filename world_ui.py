"""World catalogue, compact actions and local display-name forms for Kivy."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from ui_localization import LocalizedInput as TextInput, localized_call
from localization import current
from kivy.metrics import dp, sp
from menu_ui import MenuTile, BoundedLabel, Card, CompactTable, MenuLogo, ClubButton

HELP_PAGES = (
    ('YOUR CAREER', 'Choose New Game or Load Game. Pick a player name and a first contract. Free starts in Scorer League with no country selection. SCORER World is a separate application and career, with local-country contracts and England Division 2 as an option.'),
    ('TRAIN, THEN PLAY', 'Complete three training shots before every match to unlock Play. Resume an unfinished session. Energy and morale influence your opportunities. Progress saves automatically.'),
    ('TAKE YOUR CHANCE', 'Time your tap to shoot at the moving marker. Watch power and the time-to-shoot countdown. Opponent strength changes chance quantity and difficulty. Continue at half-time and full-time.'),
    ('WORLD & NAMES','Use the names editor to rename clubs, leagues and players or import a JSON names file.'),
)


WORLD_HELP_PAGES = (
 ('YOUR CAREER','Choose New Game or Load Game. Name your player and select a first contract. World suggests your phone’s country, with England Division 2 as another option.'),
 ('TRAIN, THEN PLAY','Complete three training shots before every match to unlock Play. Resume an unfinished session. Energy and morale influence your opportunities. Progress saves automatically.'),
 ('TAKE YOUR CHANCE','Time your tap to shoot at the moving marker. Watch power and the shot timer. Opponent strength changes the number and difficulty of chances. Continue at half-time and full-time.'),
 ('WORLD & NAMES','Open World, then Editor to rename clubs, leagues and players or import a JSON names file. Display names do not change team strength or results.'),
)


from player_development import FOCI,NAMES,HINTS
PROGRESSION_HELP_PAGES=(
 ('OBJECTIVES',('Top-three league finish','Confirmed at season end.','Tracking began in {season}. Earlier seasons are not reconstructed.')),
 ('TRAINING FOCUS',('Three shots earn 12 XP, plus 4 XP per goal on focus. Each level needs 60 + 20 times the current level XP.',
                    'The chosen focus stays fixed until the next weekly team talk.')),
 *tuple((NAMES[focus],(HINTS[focus],)) for focus in FOCI),
 ('COACH TRUST',('Substitute below 45; starter from 45; key player from 80.',
                 'Substitutes enter after 60 minutes. Starters below 60 trust play 75 minutes, or the full match on key occasions. Higher trust brings 90 minutes.',
                 'Role changes the chance frequency slightly. Training and morale minimums always apply.')),
 ('HOW TRUST CHANGES',('Training +2. Goals +6 each, up to +12. A key-game goal adds +2. No goal: -3, or -4 after three misses. No chances: -1.',
                       'Training and goals rebuild trust. A new club starts at 50. International games do not change club trust.')),
)
def _training_help(pages):
    title,text=pages[1]
    return pages[:1]+((title,(text,'Complete this session to unlock the match. Training goals help your chances in the next match.')),)+pages[2:]
HELP_PAGES=_training_help(HELP_PAGES)+PROGRESSION_HELP_PAGES
WORLD_HELP_PAGES=_training_help(WORLD_HELP_PAGES)+PROGRESSION_HELP_PAGES


class CompactHub(BoxLayout):
    """Small windows keep every action visible instead of squeezing the header."""
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(4))
        c = menu.game.career
        from injuries import active,label
        injured=active(c)
        identity=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        identity.add_widget(MenuLogo(size_hint_x=.45))
        self.club_button=ClubButton(menu);self.club_button.size_hint_y=1;identity.add_widget(self.club_button);self.add_widget(identity)
        actions = GridLayout(cols=4, spacing=dp(4))
        entries = [('TRAINING', 'training'), ('PLAY', 'play'), ('STANDINGS', 'standings'),
                   ('TOP SCORERS', 'scorers'), ('LEADERBOARD', 'leaderboard'), ('FIXTURES', 'calendar'), ('AGENT', 'agent'),
                   (c.player_name, 'profile'), ('HELP', 'help'), ('LIFESTYLE','lifestyle'), ('COACH TRUST','coach_trust')]
        if c.world_unlocked:entries.extend([('WORLD LEAGUES','upgrade')])
        entries.extend([('FEEDBACK','feedback'),('EXIT', 'exit')])
        for title, action in entries:
            button = MenuTile(title, lambda a=action: menu.action(a), accent=action == 'play',localize=action!='profile')
            button.font_size = sp(12)
            if action=='profile':button.max_lines=2;button.shorten=True
            if action == 'play':
                button.disabled=(not c.trained_this_week and not injured) or c.coach_meeting_required or c.life['retired']
                if injured:button.text='SIMULATE MATCH'
            if action == 'training': button.disabled = c.coach_meeting_required or injured or c.life['retired']
            if action == 'agent':button.disabled=not c.transfer_window_open
            actions.add_widget(button)
        if injured:self.add_widget(BoundedLabel(text=label(c,menu.game.i18n.tr),localize=False,font_size=sp(10),color=(1,.7,.3,1),size_hint_y=None,height=dp(28)))
        self.add_widget(actions)
        self.bind(size=lambda *_:setattr(actions,'cols',5 if self.height<dp(290) else 4))


class WorldBrowser(BoxLayout):
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(6))
        self.menu = menu
        self.game = menu.game
        c = menu.game.career
        self.search = TextInput(text='', hint_text='Search country / football region', multiline=False,
                                size_hint_y=None, height=dp(48), font_size=sp(14),
                                background_normal='', background_active='', background_color=(.06,.14,.17,1),
                                foreground_color=(.94,.98,.97,1), hint_text_color=(.65,.76,.78,1),
                                cursor_color=(.3,1,.7,1), padding=[dp(10),dp(12)])
        search_row=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        search_row.add_widget(self.search)
        editor=MenuTile('EDITOR',lambda:menu.action('editor'));editor.size_hint_x=None;editor.width=dp(112)
        search_row.add_widget(editor);self.add_widget(search_row)
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

    @localized_call
    def render(self):
        selected = [c for c in self.countries if (self.search.text.casefold() in c.casefold() or self.search.text.casefold() in self.menu.game.i18n.country(c).casefold())]
        pages = max(1, (len(selected)+5)//6)
        self.page = max(0, min(pages-1, self.page))
        self.counter.text = f'{self.page+1}/{pages}'
        self.grid.clear_widgets()
        for country in selected[self.page*6:self.page*6+6]:
            depth = len(self.menu.game.career.domestic_leagues(country))
            self.grid.add_widget(MenuTile(self.menu.game.i18n.country(country)+'\n'+self.menu.game.i18n.tr('{count} divisions',count=depth), lambda c=country: self.menu.action('world_country', c),localize=False))


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
        self.add_widget(MenuTile('IMPORT NAMES FILE',lambda:menu.action('names_import'),accent=True))
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

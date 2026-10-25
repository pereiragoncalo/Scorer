"""Responsive, touch-friendly career menus for the original Kivy game."""
from career import EUROPE_PYRAMID_DEPTH, WORLD_COUNTRIES
from domestic_rules import uses_simplified_model, standing_zone
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp, sp, Metrics
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import math
import edition
import release_settings
from localization import current, using, LANGUAGES
from ui_localization import LocalizedText, localized_call, LocalizedInput as TextInput, LocalizedPopup

INK = (0.91, 0.96, 0.95, 1)
MUTED = (0.58, 0.72, 0.72, 1)
GREEN = (0.30, 0.91, 0.65, 1)
MENU_VIEWS = frozenset(('offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent', 'world', 'splash', 'start', 'profile', 'privacy', 'help', 'upgrade', 'editor', 'world_country', 'world_league', 'language'))
MENU_ERROR_PREFIXES = ('Unable ', 'Could not ', 'Enter a name', 'A scorer already', 'Choose a valid', 'Player creation is only')



class FlowLabel(LocalizedText, Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', INK)
        kwargs.setdefault('font_size', sp(15))
        kwargs.setdefault('halign', 'left')
        super().__init__(size_hint_y=None, valign='middle', **kwargs)
        self.bind(width=self._wrap, texture_size=self._height)
        self._wrap()

    def _wrap(self, *_):
        self.text_size = (max(dp(1), self.width), None)

    def _height(self, *_):
        self.height = max(dp(24), self.texture_size[1] + dp(4))


class TouchButton(LocalizedText, Button):
    def __init__(self, text, callback, accent=False, **kwargs):
        self._accent = accent
        super().__init__(text=text, size_hint_y=None, height=dp(52),
                         font_size=sp(14), bold=True, color=INK, disabled_color=(0.60, 0.63, 0.64, 1),
                         background_normal='', background_down='', background_disabled_normal='',
                         background_color=(0, 0, 0, 0),
                         halign='center', valign='middle', **kwargs)
        with self.canvas.before:
            self._base_color = Color(0.02, 0.07, 0.09, 1)
            self._base = RoundedRectangle(radius=[dp(9)])
            self._face_color = Color(0.10, 0.25, 0.29, 1)
            self._face = RoundedRectangle(radius=[dp(9)])
            self._gloss_color = Color(0.65, 0.85, 0.85, 0.12)
            self._gloss = RoundedRectangle(radius=[dp(8)])
            self._light_color = Color(0.4, 0.62, 0.65, 0.7)
            self._rim = Line(rounded_rectangle=(0, 0, 1, 1, dp(9)), width=1)
        self.bind(width=self._fit, texture_size=self._fit)
        self.bind(pos=self._relief, size=self._relief, state=self._relief, disabled=self._relief)
        self.bind(on_release=lambda *_: callback())
        self._fit()
        self._relief()

    def _relief(self, *_):
        pressed = self.state == 'down'
        inset = dp(1 if pressed else 4)
        self._base.pos, self._base.size = self.pos, self.size
        self._face.pos = (self.x, self.y + inset / 2)
        self._face.size = (self.width, max(1, self.height - inset))
        self._gloss.pos = (self.x + dp(2), self._face.pos[1] + self._face.size[1] * 0.56)
        self._gloss.size = (max(1, self.width - dp(4)), self._face.size[1] * 0.40)
        self._gloss_color.a = 0.025 if pressed or self.disabled else 0.12
        self._rim.rounded_rectangle = (self.x + dp(1), self._face.pos[1] + dp(1),
                                      max(1, self.width - dp(2)), max(1, self.height - inset - dp(2)), dp(9))
        face = (0.10, 0.48, 0.34, 1) if self._accent else (0.10, 0.24, 0.29, 1)
        if self.disabled:
            face = (0.22, 0.24, 0.25, 1)
        factor = 1 if self.disabled else 0.82 if pressed else 1
        self._face_color.rgba = tuple(v * factor for v in face[:3]) + (1,)
        self._light_color.a = 0.25 if pressed or self.disabled else 0.7

    def _fit(self, *_):
        self.text_size = (max(dp(1), self.width - dp(24)), None)
        self.height = max(dp(52), self.texture_size[1] + dp(24))


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None,
                         padding=dp(12), spacing=dp(6), **kwargs)
        self.bind(minimum_height=self.setter('height'))
        with self.canvas.before:
            Color(0.035, 0.10, 0.12, 1)
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._rect, size=self._rect)

    def _rect(self, *_):
        self._background.pos, self._background.size = self.pos, self.size

    def label(self, text, heading=False, muted=False, localize=True):
        label = FlowLabel(text=text, localize=localize, font_size=sp(18 if heading else 15),
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
        signature = (self.game.i18n.language, self.game.i18n.revision, self.game.view, self.game._world_available, self.game._career_mode, c.player_name, c.club_name, c.season, c.week,
                     c.matches, c.goals, c.stamina, c.morale, c.message,
                     c.current_league.name, tuple(c.agent_offers),
                     self.game.training_completed, self.game.training_goals, c.world_unlocked, c.training_used_this_week, c.trained_this_week, c.training_shots_taken, c.training_session_goals,
                     self.game.help_page, self.game.editor_club_index, self.game.editor_key, self.game.world_country, self.game.world_league_key, c.alias_revision, self.game.reward_ad_status, Metrics.density, Metrics.fontscale)
        if signature != self._signature:
            self._signature = signature
            self._build()

    def action(self, name, value=None):
        self.game._activate_ui(name, value)
        self.game.draw()

    def _button(self, label, action, value=None, accent=False):
        return TouchButton(label, lambda: self.action(action, value), accent, localize=action not in ('accept_offer','transfer','start_country','world_league'))

    @localized_call
    def _build(self):
        c = self.game.career
        if self.game.view != 'start':
            self.game.ads.entry_visible(False)
        self.clear_widgets()
        self._shade.a = 1 if self.game.view == 'splash' else 0.62
        if self.game.view == 'language' and not edition.is_world():
            self.game.view='start'
        if self.game.view == 'language':
            self.padding=dp(8);self.spacing=dp(6);self.scroll=None
            self.body=LanguageScreen(self);self.add_widget(self.body);return
        if self.game.view in ('splash', 'start', 'profile'):
            self.padding = self.spacing = 0
            self.scroll = None
            self.body = (SplashScreen(self) if self.game.view == 'splash' else
                         PlayerScreen(self) if self.game.view == 'profile' else EntryScreen(self))
            self.add_widget(self.body)
            return
        if self.game.view == 'hub' and (self.game.width < dp(540) or self.game.height < dp(300)):
            from world_ui import CompactHub
            self.padding, self.spacing = dp(8), dp(4)
            self.scroll = None
            self.body = CompactHub(self)
            self.add_widget(self.body)
            return
        paged = self.game.view in ('standings', 'scorers', 'calendar', 'world_league')
        self.padding = dp(8) if paged else dp(12) if self.game.view == 'hub' else dp(16)
        self.spacing = dp(6) if paged else dp(8) if self.game.view == 'hub' else dp(12)
        header = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(8))
        brand = BoxLayout(orientation='vertical')
        if self.game.view == 'hub':
            header.height = dp(52)
            brand = AnchorLayout(anchor_x='left', anchor_y='center')
            logo = MenuLogo(size_hint=(None, 1), width=dp(250 if edition.is_world() else 190))
            brand.bind(width=lambda widget, width: setattr(logo, 'width', min(dp(250 if edition.is_world() else 190), width)))
            brand.add_widget(logo)
        elif self.game.view in ('world', 'editor', 'world_country'):
            header.height = dp(52)
            title = 'WORLD LEAGUES' if self.game.view == 'world' else 'NAMES EDITOR' if self.game.view == 'editor' else self.game.i18n.country(self.game.world_country).upper()
            brand.add_widget(BoundedLabel(text=self.game.i18n.tr(title) if self.game.view!='world_country' else title, localize=self.game.view!='world_country', font_size=sp(20), bold=True))
            detail = f'{len({v.country for v in c.leagues.values()})} regions · {len(c.domestic_leagues())} divisions' if self.game.view == 'world' else self.game.i18n.league(c,c.leagues[self.game.editor_key]) if self.game.view == 'editor' else 'Choose a division'
            brand.add_widget(BoundedLabel(text=detail, font_size=sp(11), color=MUTED))
        elif paged:
            header.height = dp(52)
            titles = {'standings': 'STANDINGS', 'scorers': 'TOP SCORERS', 'calendar': 'FIXTURES', 'world_league': 'WORLD LEAGUE'}
            brand.add_widget(BoundedLabel(text=titles[self.game.view], font_size=sp(20), bold=True))
            brand.add_widget(BoundedLabel(localize=False,text=self.game.i18n.league(c,c.leagues[self.game.world_league_key] if self.game.view == 'world_league' else c.current_league), font_size=sp(11), color=MUTED))
        else:
            header.height = dp(52)
            brand.add_widget(BrandMark())
        header.add_widget(brand)
        if self.game.view == 'hub':
            profile = MenuTile('PLAYER', lambda: self.action('profile'))
            profile.size_hint_x, profile.width = None, dp(88)
            header.add_widget(profile)
        if self.game.view == 'hub':
            header_actions = [('HELP', 'help')]
            if edition.is_world():header_actions.append(('WORLD', 'upgrade'))
            for title, action in header_actions:
                button = MenuTile(title, lambda a=action: self.action(a))
                button.size_hint_x, button.width = None, dp(76)
                header.add_widget(button)
            privacy = MenuTile('PRIVACY', lambda: self.action('privacy'))
            privacy.size_hint_x, privacy.width = None, dp(76)
            header.add_widget(privacy)
        if self.game.view not in ('hub', 'offers'):
            back = self._button('BACK', 'privacy_back' if self.game.view == 'privacy' else 'upgrade_back' if self.game.view == 'upgrade' else 'help_back' if self.game.view == 'help' else 'world' if self.game.view == 'world_country' else 'hub')
            back.size_hint_x, back.width = None, dp(88)
            header.add_widget(back)
        if self.game.view in ('hub', 'offers'):
            exit_button = TouchButton('EXIT', self.game._request_exit)
            exit_button.size_hint_x, exit_button.width = None, dp(76)
            header.add_widget(exit_button)
        self.add_widget(header)
        if self.game.view == 'hub':
            self.scroll = None
            self.body = MainDashboard(self)
            self.add_widget(self.body)
            return
        if self.game.view == 'world' and c.world_unlocked:
            from world_ui import WorldBrowser
            self.scroll = None
            self.body = WorldBrowser(self)
            self.add_widget(self.body)
            return
        if self.game.view == 'world_league' and c.world_unlocked:
            edit = MenuTile('EDIT NAMES', lambda: self.action('edit_browsed'))
            edit.size_hint_x, edit.width = None, dp(104)
            header.add_widget(edit)
            league = c.leagues[self.game.world_league_key]
            self.scroll = None
            self.body = CompactTable(self.game.i18n.league(c,league) + self._standing_legend(league), ('POS','CLUB','P','PTS'), [(self._standing_position(league,i+1),c.display_club(club),club.played,club.points) for i,club in enumerate(league.table())],title_localize=False)
            self.add_widget(self.body)
            return
        if self.game.view in ('standings', 'scorers', 'calendar'):
            self.scroll = None
            self.body = self._compact_list()
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
            country=title in WORLD_COUNTRIES
            card.label(self.game.i18n.country(title) if country else title, heading=True, localize=not country)
        self.body.add_widget(card)
        return card

    def _offers(self):
        c = self.game.career
        card = self.card('Your first contract' + (' · ' + c.current_league.country if c.world_unlocked else ' · Scorer League'))
        if c.world_unlocked:
            card.label(self.game.i18n.tr('Nationality: {country}',country=self.game.i18n.country(c.nationality)),muted=True)
        grid = GridLayout(cols=3 if self.width >= dp(540) else 2, spacing=dp(6), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        card.add_widget(grid)
        for club in self.game.career.offers:
            grid.add_widget(self._button(c.display_text(club), 'accept_offer', club, accent=True))

    def _training(self):
        g, c = self.game, self.game.career
        used = c.trained_this_week
        resumable = c.training_session_week == c.week and not used
        card = self.card('Finishing practice')
        card.spacing = dp(4)
        if g.training_completed and c.trained_this_week:
            card.label(f'Training complete · {g.training_goals}/3 goals', heading=True)
        elif resumable:
            card.label(f'Resume training · {c.training_shots_taken}/3 shots completed.')
            card.label(c.message, muted=True)
        elif not used:
            card.label('Complete three shots to unlock this week’s match.')
        else:
            card.label('This week’s training session has been used.', muted=True)
        card.label(f'Energy: {c.stamina:.1f}/20  ·  Morale: {c.morale:.1f}/20', muted=True)
        button = self._button('WEEKLY TRAINING USED' if used else 'RESUME TRAINING' if resumable else 'START TRAINING', 'training_start', accent=True)
        button.disabled = used
        actions = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        actions.add_widget(button)
        card.add_widget(actions)
        if self.game._world_available or c.world_unlocked:
            return
        boost = self._button('WATCH AD: +1 MORALE', 'morale_ad')
        boost.disabled = not c.morale_ad_available
        actions.add_widget(boost)
        if c.morale_ad_week == c.week:
            card.label('This week’s morale ad reward has been claimed.', muted=True)
        elif c.morale >= 20:
            card.label('Morale is already at its maximum.', muted=True)
        elif g.reward_ad_status:
            card.label(g.reward_ad_status, muted=True)
        if c.message.startswith(('Reward ad', 'Ad reward', 'Unable to save the morale')):
            card.label(c.message, muted=True)

    def _standing_position(self, league, position):
        if self.game.career.world_unlocked and uses_simplified_model(league.country, EUROPE_PYRAMID_DEPTH):
            zone = standing_zone(league.tier, position, len(league.clubs))
            return f'{position} P' if zone == 'Promotion' else f'{position} R' if zone == 'Relegation' else position
        return position

    def _standing_legend(self, league):
        if self.game.career.world_unlocked and uses_simplified_model(league.country, EUROPE_PYRAMID_DEPTH) and league.tier in (1, 2):
            return self.game.i18n.tr(' · R: bottom 3 go down' if league.tier == 1 else ' · P: top 3 go up')
        return ''

    def _compact_list(self):
        c = self.game.career
        if self.game.view == 'standings':
            rows = [(self._standing_position(c.current_league, i + 1), c.display_club(club), club.played, club.won, club.drawn, club.lost,
                     club.goals_for, club.goals_against, club.goal_difference, club.points)
                    for i, club in enumerate(c.current_league.table())]
            return CompactTable(self.game.i18n.tr('STANDINGS') + ' · ' + self.game.i18n.league(c,c.current_league) + self._standing_legend(c.current_league),
                                ('POS', 'CLUB', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'),
                                rows, focus=c.display_text(c.club_name), summary=(0, 1, 2, 8, 9), detail=(0, 1, 3, 4, 5, 6, 7),title_localize=False)
        if self.game.view == 'scorers':
            ranking = dict(c.current_league.scorer_goals)
            ranking.setdefault(c.player_name, 0)
            rows = [(i + 1, c.display_scorer(name), goals) for i, (name, goals) in enumerate(sorted(ranking.items(), key=lambda x: (-x[1], x[0])))]
            return CompactTable('TOP SCORERS', ('POS', 'PLAYER', 'GOALS'), rows, focus=c.player_name)
        rows = [(str(e.get('date', ''))[8:10] + '/' + str(e.get('date', ''))[5:7], c.display_text(f"{e.get('home', '')} vs {e.get('away', '')}", e.get("country")),
                 self.game.i18n.competition(c,e.get('competition', ''),e.get('country')), self.game.i18n.tr(e.get('status', ''))) for e in c.calendar_entries()]
        return CompactTable(f'FIXTURES · {c.season}/{str(c.season + 1)[-2:]}', ('DATE', 'MATCH', 'COMPETITION', 'STATUS'), rows,
                            summary=(0, 1, 2, 3))

    def _privacy(self):
        card = self.card('PRIVACY' if edition.is_world() else 'Privacy & advertising')
        if self.game._world_available or self.game.career.world_unlocked:
            card.label('SCORER World is a separate ad-free application and can be played offline. Careers and imported names stay on this device; there is no SCORER account or in-app purchase verification service.')
            self._privacy_contact(card)
            return
        card.label('This version uses Google advertising.' if release_settings.is_production() else 'This test version uses Google TEST ads only. They do not generate revenue.')
        self._privacy_contact(card)
        card.label('A banner may appear on the opening menu after the splash. Full-screen ads may appear '
                   'between matches, never during a shot. Training offers an optional ad for +1 morale. '
                   'No connection or no available ad? You can keep playing.')
        card.label('All ad requests are configured for children and users under the age of consent, '
                   'with a general-audience content rating and no personalised advertising.')
        card.label('Google advertising services may process your IP address, device/app information, '
                   'diagnostics and ad interactions. Advertising ID permission is not requested. '
                   'Your player name and career saves are not sent by SCORER to Google.')
        card.label('Google privacy policy: https://policies.google.com/privacy', muted=True)
        if self.game.ads.privacy_required:
            card.add_widget(MenuTile('AD PRIVACY OPTIONS', lambda: self.game.ads.privacy_options()))

    def _privacy_contact(self, card):
        card.label('Careers and name edits are stored privately on this device. Uninstalling or clearing app data removes them; a new game keeps a private backup. There is no SCORER account or career upload.', muted=True)
        card.label('Free and World are separate applications with independent private saves. This app has no in-app purchase or purchase-verification service. World store purchases, when offered, are handled by the store.', muted=True)
        if edition.is_world():
            card.label('Names and colours use reference data. Data and font licences are included.', muted=True)
            card.label('GeoNames / CC BY 4.0 · OpenFootball / CC0 · Annexare / MIT · Barlow, Noto CJK / OFL 1.1 · CLDR / Unicode',muted=True,localize=False)
        else:
            card.label('City data: GeoNames via github.com/datasets/world-cities (CC BY 4.0); adapted names. Licence: creativecommons.org/licenses/by/4.0/. Club/city references: OpenFootball (CC0); country metadata: Annexare (MIT). Licences included.', muted=True)
        if release_settings.DEVELOPER_NAME:
            card.label('Developer: ' + release_settings.DEVELOPER_NAME, muted=True)
        if release_settings.SUPPORT_EMAIL:
            card.label('Support: ' + release_settings.SUPPORT_EMAIL, muted=True)
        if release_settings.PRIVACY_URL:
            card.add_widget(self._button('FULL PRIVACY POLICY', 'open_privacy_policy'))

    def _help(self):
        from world_ui import HELP_PAGES, WORLD_HELP_PAGES
        pages=WORLD_HELP_PAGES if edition.is_world() else HELP_PAGES
        title, text = pages[self.game.help_page]
        card = self.card(title)
        card.label(text)
        if edition.is_world():card.add_widget(self._button('LANGUAGE', 'language'))
        controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        controls.add_widget(self._button('PREVIOUS', 'help_page', -1))
        controls.add_widget(BoundedLabel(text=f'{self.game.help_page+1}/{len(HELP_PAGES)}', halign='center', size_hint_x=.3))
        controls.add_widget(self._button('NEXT', 'help_page', 1))
        card.add_widget(controls)

    def _upgrade(self):
        card = self.card('DISCOVER SCORER WORLD')
        card.label('SCORER World is a separate application, with its own installation and career. Opening this page does not charge you.')
        card.label('World includes worldwide leagues, promotions and transfers, local-country starting contracts and England Division 4.')
        card.label('Play without ads and use the local editor to change club, league and player display names or import your own JSON names file.')
        card.label('Your Free career stays in SCORER Free. World starts a separate career; no automatic transfer or conversion.')
        from world_promotion import listing_url
        url = listing_url(release_settings)
        button = self._button('VIEW WORLD ON GOOGLE PLAY' if url else 'WORLD STORE PAGE COMING SOON', 'open_world_listing', accent=True)
        button.disabled = not bool(url)
        card.add_widget(button)
        card.label('World is in development. Country-specific competition formats are still being verified. No in-app purchase is offered.', muted=True)

    def _language(self):
        card=self.card('LANGUAGE')
        card.label('Language follows your phone unless you choose another language.', muted=True)
        grid=GridLayout(cols=3,size_hint_y=None,spacing=dp(6))
        grid.bind(minimum_height=grid.setter('height'))
        for code,name in LANGUAGES.items():
            button=TouchButton(name,lambda value=code:self.action('choose_language',value),
                               accent=self.game.i18n.choice==code,localize=False)
            grid.add_widget(button)
        card.add_widget(grid)
        card.add_widget(self._button('AUTOMATIC','choose_language','auto',accent=self.game.i18n.choice=='auto'))
        card.add_widget(self._button('BACK','language_back'))

    def _world_country(self):
        c = self.game.career
        card = self.card(self.game.world_country)
        grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(6))
        grid.bind(minimum_height=grid.setter('height'))
        for league in c.domestic_leagues(self.game.world_country):
            key = league.key
            if league.country == self.game.world_country:
                grid.add_widget(self._button(self.game.i18n.league(c,league), 'world_league', key))
        card.add_widget(grid)
        card.label('Simplified format: 2 divisions; 3 promoted and 3 relegated. No playoffs.' if uses_simplified_model(self.game.world_country, EUROPE_PYRAMID_DEPTH) else 'Country regulations under review; regional/amateur competitions are not fully modelled.', muted=True)

    def _editor(self):
        if not self.game.career.world_unlocked:
            self.card('World required').label('The local names editor belongs to World.')
            return
        from world_ui import NamesEditor
        self.body.add_widget(NamesEditor(self))

    def _agent(self):
        c = self.game.career
        card = self.card('Your agent')
        card.label(c.display_text(c.message))
        card.label('Transfer window open' if c.transfer_window_open else 'Window closed · Jul/Aug and Jan/Feb', muted=True)
        for club, key in c.agent_offers:
            card.add_widget(self._button(c.display_text(f'{club}\n{c.leagues[key].name}', c.leagues[key].country), 'transfer', (club, key)))
        card.add_widget(self._button('FIND OFFERS', 'agent_refresh'))

    def _world(self):
        if not self.game.career.world_unlocked:
            self.card('Free edition').label('One division available in this edition.')
            return
        self.card('World football')
        competitions = self.card('Competitions')
        for title, status in self.game.career.international_status.items():
            competitions.label(f'{title} · {status}')
        for country in sorted(WORLD_COUNTRIES):
            depth = EUROPE_PYRAMID_DEPTH.get(country, 1)
            self.card(country).label(f'{depth} divisions')


class MatchNotice(BoxLayout):
    """Scroll long match messages while keeping the action reachable on phones."""
    @localized_call
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
        self.button = MenuTile('CONTINUE', self.proceed, accent=True)
        self.button.size_hint_x = None
        self.button.width = dp(176)
        self.button.pos_hint = {'center_x': 0.5}
        self.add_widget(self.button)
        self.body.bind(minimum_height=self._fit_panel)
        self.button.bind(height=self._fit_panel)

    def _fit_panel(self, *_):
        available = max(dp(96), self.game.height - dp(112))
        natural = self.body.minimum_height + self.button.height + dp(38)
        self.height = min(natural, available)
        self.center = (self.game.center_x, self.game.center_y - dp(44))

    def _rect(self, *_):
        self.background.pos, self.background.size = self.pos, self.size

    @localized_call
    def sync(self):
        game = self.game
        self.width = min(game.width * 0.76, dp(460))
        self._fit_panel()
        signature = (game.match_finished, game.match_halftime, game.match_summary, game.career.morale, game.career.stamina)
        if signature == self.signature:
            return
        self.signature = signature
        self.body.clear_widgets()
        title = game.match_summary if game.match_finished else 'HALF-TIME' if game.match_halftime else 'CHANCE'
        self.body.add_widget(FlowLabel(text=title, font_size=sp(17), bold=True, color=GREEN, halign='center'))
        detail = (f'Morale {game.career.morale:.1f}/20  ·  Energy {game.career.stamina:.1f}/20'
                  if game.match_finished else 'Ready for the second half?' if game.match_halftime else 'Line up your shot and make the difference.')
        self.body.add_widget(FlowLabel(text=detail, font_size=sp(13), halign='center'))
        self.button.text = 'CONTINUE' if game.match_finished else 'SECOND HALF' if game.match_halftime else 'PLAY CHANCE'

    def proceed(self):
        if self.game.match_finished:
            self.game._activate_ui('match_continue')
        elif self.game.match_halftime:
            self.game._resume_second_half()
        else:
            self.game._begin_pending_chance()
        self.game.draw()


class BoundedLabel(LocalizedText, Label):
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
    def __init__(self, text, callback, accent=False, **kwargs):
        super().__init__(text, callback, accent=accent, **kwargs)
        self.font_size = sp(13)
        self.shorten = True
        self.shorten_from = 'right'
        self.max_lines = 2
        self.height = dp(52)
        self._fit()

    def _fit(self, *_):
        self.text_size = (max(1, self.width - dp(16)), max(1, self.height - dp(12)))


class MenuLogo(FloatLayout):
    """Left-aligned original artwork with a native World product lockup."""
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.image=Image(source='assets/menu_logo.png',size_hint=(None,None))
        self.add_widget(self.image)
        self.world=BoundedLabel(text='WORLD',localize=False,font_name='assets/fonts/BarlowCondensed-ExtraBoldItalic.ttf',
                                color=(1,.91,.67,1),font_size=sp(19),size_hint=(None,None)) if edition.is_world() else None
        if self.world:self.add_widget(self.world)
        self.bind(pos=self._fit,size=self._fit);self._fit()

    def _fit(self,*_):
        extra=min(dp(60),self.width*.30) if self.world else 0
        width=max(1,min(self.width-extra,self.height*2048/768))
        height=width*768/2048
        self.image.size=(width,height);self.image.pos=(self.x,self.top-height)
        if self.world:
            self.world.size=(max(1,self.width-width-dp(3)),max(1,height*.48))
            self.world.pos=(self.image.right+dp(3),self.image.y+height*.25)


class CareerStartDialog(ModalView):
    """Content-sized confirmation; no fixed-height empty message area."""
    def __init__(self,game):
        super().__init__(size_hint=(None,None),auto_dismiss=False,background='',
                         background_color=(0,0,0,0),overlay_color=(0,0,0,.68))
        self.game=game
        self.panel=EdgePanel(orientation='vertical',padding=dp(16),spacing=dp(10),background_alpha=1)
        self.panel.background.radius=[dp(12)]
        self.heading=FlowLabel(text='Start a new career?',font_size=sp(18),bold=True,color=GREEN)
        self.panel.add_widget(self.heading)
        self.message=FlowLabel(text='You already have a career. Start again? Your previous career will be backed up locally before it is replaced.',font_size=sp(14))
        self.panel.add_widget(self.message)
        self.buttons=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(10))
        self.buttons.add_widget(MenuTile('CANCEL',self.dismiss))
        self.buttons.add_widget(MenuTile('NEW GAME',game._start_new_career,accent=True))
        self.panel.add_widget(self.buttons);self.add_widget(self.panel)
        self.panel.bind(minimum_height=self._fit)
        self.bind(on_open=self._opened,on_dismiss=self._closed)
        self._fit()

    def _fit(self,*_):
        self.width=min(Window.width-dp(24),dp(520))
        self.height=min(Window.height-dp(24),max(dp(150),self.panel.minimum_height))

    def _opened(self,*_):Window.bind(size=self._fit);self._fit()
    def _closed(self,*_):Window.unbind(size=self._fit)


class EdgePanel(BoxLayout):
    """Quiet stadium overlay with one accent edge, rather than large solid tiles."""
    def __init__(self, **kwargs):
        background_alpha=kwargs.pop('background_alpha',.90)
        kwargs.setdefault('padding', dp(10))
        kwargs.setdefault('spacing', dp(4))
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.02, 0.06, 0.09, background_alpha)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
            Color(*GREEN)
            self.edge = Line(points=[self.x, self.top, self.right, self.top], width=1)
        self.bind(pos=self._rect, size=self._rect)

    def _rect(self, *_):
        self.background.pos, self.background.size = self.pos, self.size
        self.edge.points = [self.x, self.top, self.right, self.top]


class LanguageScreen(BoxLayout):
    """Nine native language names; small screens page rather than scroll."""
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(4))
        self.menu=menu;self.game=menu.game;self.page=getattr(self.game,'_language_page',0)
        error=self.game._language_error
        self.title=BoundedLabel(text=error or 'LANGUAGE',bold=True,font_size=sp(12 if error else 18),size_hint_y=None,height=dp(34 if error else 28))
        self.add_widget(self.title)
        self.info=BoundedLabel(text='Language follows your phone unless you choose another language.',color=MUTED,size_hint_y=None,height=dp(38),font_size=sp(12))
        self.add_widget(self.info)
        self.grid=GridLayout(cols=3,spacing=dp(6))
        self.add_widget(self.grid)
        self.paging=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        self.paging.add_widget(MenuTile('PREVIOUS',lambda:self.move(-1)))
        self.counter=BoundedLabel(halign='center',size_hint_x=.3)
        self.paging.add_widget(self.counter)
        self.paging.add_widget(MenuTile('NEXT',lambda:self.move(1)))
        self.add_widget(self.paging)
        actions=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        actions.add_widget(MenuTile('AUTOMATIC',lambda:menu.action('choose_language','auto'),accent=self.game.i18n.choice=='auto'))
        actions.add_widget(MenuTile('BACK',lambda:menu.action('language_back')))
        self.add_widget(actions)
        self.bind(size=self._render)
        self._render()

    def move(self,step):
        self.page+=step;self._render()

    @localized_call
    def _render(self,*_):
        from localization import CJK_FONTS, ROOT
        small=self.height<dp(290)
        if small and self.info.parent is self:self.remove_widget(self.info)
        elif not small and self.info.parent is None:self.add_widget(self.info,index=len(self.children)-1)
        if not small and self.paging.parent is self:self.remove_widget(self.paging)
        elif small and self.paging.parent is None:self.add_widget(self.paging,index=1)
        count=3 if small else 9
        self.page=max(0,min((9-1)//count,self.page));self.game._language_page=self.page;self.counter.text=f'{self.page+1}/{(9-1)//count+1}'
        self.grid.clear_widgets()
        for code,name in list(LANGUAGES.items())[self.page*count:(self.page+1)*count]:
            font=str(ROOT/'assets/fonts'/CJK_FONTS[code]) if code in CJK_FONTS else str(ROOT/'assets/fonts/Barlow-Regular.ttf')
            self.grid.add_widget(MenuTile(name,lambda value=code:self.menu.action('choose_language',value),
                                         accent=self.game.i18n.choice==code,localize=False,font_name=font))


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
        self.brand = MenuLogo(size_hint=(None,None))
        self.add_widget(self.brand)
        message = menu.game.career.message
        self.info = BoundedLabel(text=message if message.startswith(MENU_ERROR_PREFIXES) else '',
                                 color=(1,.65,.45,1),font_size=sp(14),size_hint_y=None,height=dp(40))
        if self.info.text:self.panel.add_widget(self.info)
        new_row = self.new_row = BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(8))
        new_row.add_widget(MenuTile('NEW GAME', lambda: menu.action('new_game'), accent=True))
        if edition.is_world():
            new_row.add_widget(MenuTile('LANGUAGE', lambda: menu.action('language')))
        self.panel.add_widget(new_row)
        load = self.load_button = MenuTile('LOAD GAME', lambda: menu.action('load_game'))
        load.disabled = not menu.game.career.save_path.is_file()
        self.panel.add_widget(load)
        actions = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        self.entry_actions=actions
        actions.add_widget(MenuTile('HELP', lambda: menu.action('help')))
        actions.add_widget(MenuTile('PRIVACY', lambda: menu.action('privacy')))
        actions.add_widget(MenuTile('EXIT', menu.game._request_exit))
        self.panel.add_widget(actions)
        self.panel.canvas.before.remove(self.panel.edge)
        self.add_widget(self.panel)
        self.bind(pos=self._fit, size=self._fit)
        self._fit()

    def _fit(self, *_):
        banner_fits = not self.menu.game._world_available and not self.menu.game.career.world_unlocked and not self.menu.game._new_game_popup and not self.menu.game._exit_popup and self.height >= dp(340) and self.width >= dp(340)
        self.menu.game.ads.entry_visible(banner_fits)
        self.banner_space = dp(64) if banner_fits else 0
        available = self.height - self.banner_space
        has_error = self.info.parent is self.panel
        compact = available < dp(280)
        margin=dp(8 if compact else 12)
        logo_height=0 if has_error and compact else dp(28 if compact else 52)
        self.brand.size=(min(self.width-margin*2,dp(250 if edition.is_world() else 190)),logo_height)
        self.brand.opacity=1 if logo_height else 0
        self.brand.pos=(self.x+margin,self.top-margin-logo_height)
        header=logo_height+margin if logo_height else 0
        self.panel.padding=dp(8 if compact else 10)
        self.new_row.height=self.load_button.height=self.entry_actions.height=dp(48 if compact else 52)
        for button in (*self.new_row.children,*self.entry_actions.children):button.height=dp(48 if compact else 52)
        self.info.height=dp(32 if compact else 40)
        desired=dp(168 if compact else 184)+(self.info.height+dp(4) if has_error else 0)
        self.panel.size=(min(self.width-dp(24),dp(340)),min(available-header-dp(16),desired))
        self.panel.center=(self.center_x,self.y+self.banner_space+(available-header)/2)


class MainDashboard(BoxLayout):
    """Match first; secondary destinations form one compact navigation strip."""
    def __init__(self, menu):
        super().__init__(orientation='vertical', spacing=dp(6))
        self.menu = menu
        c = menu.game.career
        self.identity = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(12), padding=[dp(10), 0])
        self.identity.add_widget(BoundedLabel(text=c.player_name, localize=False, font_size=sp(18), bold=True, color=GREEN))
        self.identity.add_widget(BoundedLabel(text=c.display_text(c.club_name), localize=False, font_size=sp(14), halign='center'))
        self.identity.add_widget(BoundedLabel(text=f'Energy {c.stamina:.1f}/20 · Morale {c.morale:.1f}/20',
                                             color=MUTED, font_size=sp(11), halign='right'))
        self.add_widget(self.identity)
        self.hero = BoxLayout(spacing=dp(12))
        self.match = EdgePanel(orientation='vertical', size_hint_x=0.66)
        self.match.add_widget(BoundedLabel(text='NEXT MATCH · ' + menu.game.i18n.date(c.current_date), color=GREEN, font_size=sp(10),
                                          bold=True, size_hint_y=None, height=dp(16)))
        fixture = c.next_match()
        teams = BoxLayout(spacing=dp(8))
        home = c.display_club(fixture[1]) if fixture else 'Season complete'
        away = c.display_club(fixture[2]) if fixture else ''
        teams.add_widget(BoundedLabel(text=home if fixture else menu.game.i18n.tr(home), localize=False, font_size=sp(18), bold=True, halign='center'))
        teams.add_widget(BoundedLabel(text='VS' if fixture else '', font_size=sp(11), color=MUTED,
                                     halign='center', size_hint_x=0.18))
        teams.add_widget(BoundedLabel(text=away, localize=False, font_size=sp(18), bold=True, halign='center'))
        self.match.add_widget(teams)
        footer = self.footer = FloatLayout(size_hint_y=None, height=dp(52))
        self.training = MenuTile('TRAINING', lambda: menu.action('training'), accent=not c.trained_this_week)
        self.play = MenuTile('PLAY', lambda: menu.action('play'), accent=True)
        self.play.disabled = not c.trained_this_week
        footer.add_widget(self.training)
        footer.add_widget(self.play)
        self.match.add_widget(footer)
        self.hero.add_widget(self.match)
        self.season = EdgePanel(orientation='vertical', size_hint_x=0.34)
        self.season.add_widget(BoundedLabel(text='YOUR SEASON', color=GREEN, font_size=sp(10),
                                           bold=True, size_hint_y=None, height=dp(16)))
        numbers = BoxLayout(spacing=dp(8))
        for number, title in ((c.matches, 'MATCHES'), (c.goals, 'GOALS')):
            anchor = AnchorLayout()
            column = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(68), spacing=dp(4))
            column.add_widget(BoundedLabel(text=str(number), font_size=sp(30), bold=True, halign='center',
                                           size_hint_y=None, height=dp(44)))
            column.add_widget(BoundedLabel(text=title, font_size=sp(10), color=MUTED, halign='center',
                                           size_hint_y=None, height=dp(20)))
            anchor.add_widget(column)
            numbers.add_widget(anchor)
        self.season.add_widget(numbers)
        self.season.add_widget(BoundedLabel(localize=False,text=menu.game.i18n.league(c,c.current_league),
                                           color=MUTED, font_size=sp(11), size_hint_y=None, height=dp(26)))
        self.hero.add_widget(self.season)
        self.add_widget(self.hero)
        self.actions = GridLayout(cols=4, spacing=dp(6), size_hint_y=None, height=dp(52))
        for title, action in [('STANDINGS', 'standings'),
                              ('TOP SCORERS', 'scorers'), ('FIXTURES', 'calendar'), ('AGENT', 'agent')]:
            button = MenuTile(title, lambda name=action: menu.action(name))
            self.actions.add_widget(button)
            if action == 'scorers':
                self.markers = button
        self.markers.bind(pos=self._align_play, size=self._align_play)
        self.footer.bind(pos=self._align_play, size=self._align_play)
        self.add_widget(self.actions)
        self.status = BoundedLabel(text=c.display_text(c.message) if c.message.startswith(MENU_ERROR_PREFIXES) else '',
                                   color=(1,.65,.45,1),font_size=sp(14),size_hint_y=None,height=dp(36))
        if self.status.text:self.add_widget(self.status)
        self.bind(size=self._arrange)
        self._arrange()

    def _arrange(self, *_):
        tiny = self.height < dp(215)
        portrait = self.width < dp(480) and self.height > dp(400)
        self.identity.height = dp(24 if tiny else 36)
        if tiny:
            if self.hero.parent is self:
                self.remove_widget(self.hero)
                for button in (self.play, self.training):
                    button.parent.remove_widget(button)
                    button.size_hint = (1, None)
                    self.actions.add_widget(button, index=len(self.actions.children))
            self.actions.cols = 3
        else:
            if self.hero.parent is None:
                for button in (self.training, self.play):
                    self.actions.remove_widget(button)
                    self.footer.add_widget(button)
                self.add_widget(self.hero, index=self.children.index(self.identity))
            self.actions.cols = 2 if portrait else 4
        rows = (len(self.actions.children) + self.actions.cols - 1) // self.actions.cols
        self.actions.height = rows * dp(52) + (rows - 1) * dp(6)
        self.hero.orientation = 'vertical' if portrait else 'horizontal'
        self.match.size_hint = (1, 0.60) if portrait else (0.66, 1)
        self.season.size_hint = (1, 0.40) if portrait else (0.34, 1)
        self._align_play()

    def _align_play(self, *_):
        if self.play.parent is not self.footer:
            return
        for button, side in ((self.training, 'x'), (self.play, 'right')):
            button.size_hint = (0.49, None)
            button.pos_hint = {side: 0 if side == 'x' else 1, 'y': 0}


class PlayerScreen(FloatLayout):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.game = menu.game
        self.panel = EdgePanel(orientation='vertical', size_hint=(None, None), padding=dp(14), spacing=dp(8))
        self.panel.canvas.before.remove(self.panel.edge)
        self.panel.background.radius = [dp(12)]
        self.title_label=BoundedLabel(text='YOUR PLAYER', bold=True, font_size=sp(18),size_hint_y=None,height=dp(28))
        self.panel.add_widget(self.title_label)
        existing = menu.game._profile_return == 'hub'
        self.world_creation = edition.is_world() and not existing
        if self.world_creation and self.game._player_draft is None:
            self.game._player_draft = {'name':'','nationality':self.game.career.nationality,
                                       'country':self.game.career.current_league.country}
        self.draft = self.game._player_draft if self.world_creation else None
        self.name = TextInput(text=menu.game.career.player_name if existing else self.draft['name'] if self.draft else '',
                              hint_text='Player name', multiline=False, write_tab=False,
                              font_size=sp(17), padding=[dp(12), dp(12)],
                              size_hint_y=None, height=dp(52), background_normal='', background_active='',
                              background_color=(0, 0, 0, 0), foreground_color=INK, hint_text_color=MUTED, cursor_color=GREEN)
        with self.name.canvas.before:
            Color(0.08, 0.17, 0.20, 1)
            self._name_background = RoundedRectangle(radius=[dp(8)])
            self._name_border_color = Color(0.25, 0.42, 0.44, 0.7)
            self._name_border = Line(rounded_rectangle=(0, 0, 1, 1, dp(8)), width=1)
            Color(1, 1, 1, 1)
        self.name.bind(pos=self._field_rect, size=self._field_rect, focus=self._field_rect, line_height=self._field_rect)
        self._field_rect()
        self.panel.add_widget(self.name)
        if self.world_creation:
            self.name.bind(text=lambda _,text:self.draft.update(name=text))
            choices = self.choices = BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(8))
            self.country_buttons={}
            for field in ('nationality','country'):
                button=MenuTile('',lambda key=field:self.choose_country(key),localize=False)
                self.country_buttons[field]=button;choices.add_widget(button)
            self.panel.add_widget(choices);self._country_labels()
        message = menu.game.career.message
        error = message if message.startswith(MENU_ERROR_PREFIXES) else ''
        self.helper = BoundedLabel(text=error,color=(1,.65,.45,1),font_size=sp(14),size_hint_y=None,height=dp(40))
        if error and not self.world_creation:self.panel.add_widget(self.helper)
        if self.world_creation and error:
            self.title_label.text=error;self.title_label.font_size=sp(11)
        actions = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        actions.add_widget(MenuTile('CANCEL', lambda: menu.action('cancel_profile')))
        self.actions=actions
        actions.add_widget(MenuTile('SAVE' if existing else 'CONTINUE',
                                    lambda: self.submit(), accent=True))
        self.panel.add_widget(actions)
        self.add_widget(self.panel)
        self.name.bind(on_text_validate=lambda *_: self.submit())
        self.bind(pos=self._fit, size=self._fit)
        self.panel.bind(minimum_height=self._fit)
        self._fit()

    def _field_rect(self, *_):
        self._name_background.pos, self._name_background.size = self.name.pos, self.name.size
        self._name_border.rounded_rectangle = (self.name.x, self.name.y, self.name.width, self.name.height, dp(8))
        self._name_border_color.rgba = GREEN if self.name.focus else (0.25, 0.42, 0.44, 0.7)
        vertical = max(dp(8), (self.name.height - self.name.line_height) / 2)
        self.name.padding = (dp(12), vertical, dp(12), vertical)

    def submit(self):
        self.name.focus = False
        self.menu.action('save_profile', dict(self.draft, name=self.name.text) if self.world_creation else self.name.text)

    @localized_call
    def _country_labels(self):
        for field,button in self.country_buttons.items():
            button.text=self.game.i18n.tr('Nationality: {country}' if field=='nationality' else 'Starting country: {country}',
                                         country=self.game.i18n.country(self.draft[field]))

    @localized_call
    def choose_country(self,field):
        if not self.world_creation:return
        self.name.focus=False
        popup=PlayerCountryPicker(self,field)
        self.game._country_popup=popup
        popup.bind(on_dismiss=lambda *_:setattr(self.game,'_country_popup',None))
        popup.open()

    def _fit(self, *_):
        compact = self.height < dp(310) if self.world_creation else self.height < dp(250)
        if self.world_creation:
            self.title_label.height=dp(24 if compact else 28)
            self.name.height=self.choices.height=self.actions.height=dp(48 if compact else 52)
            self.helper.height=0 if compact else dp(36)
            self.helper.opacity=0 if compact else 1
        self.panel.padding = dp(8 if compact and self.world_creation else 10 if compact else 14)
        self.panel.spacing = dp(4 if compact and self.world_creation else 6 if compact else 8)
        self.panel.size = (min(self.width - dp(24), dp(420)), min(self.height - dp(16), self.panel.minimum_height))
        self.panel.center = self.center



class PlayerCountryPicker(LocalizedPopup):
    """Offline country search with bounded pages and canonical callback values."""
    def __init__(self,screen,field):
        self.screen=screen;self.game=screen.game;self.field=field;self.page=0
        body=BoxLayout(orientation='vertical',spacing=dp(4),padding=dp(4))
        self.search=TextInput(hint_text='Search countries',multiline=False,write_tab=False,
                              size_hint_y=None,height=dp(48),font_size=sp(14))
        body.add_widget(self.search)
        self.grid=GridLayout(cols=2,spacing=dp(4));body.add_widget(self.grid)
        nav=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(4))
        self.previous=MenuTile('PREVIOUS',lambda:self.move(-1));nav.add_widget(self.previous)
        self.counter=BoundedLabel(halign='center',size_hint_x=.4);nav.add_widget(self.counter)
        self.next=MenuTile('NEXT',lambda:self.move(1));nav.add_widget(self.next)
        nav.add_widget(MenuTile('CANCEL',lambda:self.dismiss()));body.add_widget(nav)
        super().__init__(title='NATIONALITY' if field=='nationality' else 'STARTING COUNTRY',
                         content=body,size_hint=(.96,.96),auto_dismiss=False)
        self.search.bind(text=self.filter);self.bind(size=self._render)
        self._render()

    def filter(self,*_):
        if len(self.search.text)>64:self.search.text=self.search.text[:64]
        self.page=0;self._render()

    def move(self,step):
        self.page+=step;self._render()

    @localized_call
    def _render(self,*_):
        query=self.search.text.strip().casefold()
        rows=sorted((self.game.i18n.country(c),c) for c in WORLD_COUNTRIES
                    if not query or query in c.casefold() or query in self.game.i18n.country(c).casefold())
        count=2 if self.height<dp(330) else 6
        pages=max(1,math.ceil(len(rows)/count));self.page=max(0,min(self.page,pages-1))
        self.counter.text=f'{self.page+1}/{pages}';self.previous.disabled=self.page==0;self.next.disabled=self.page==pages-1
        self.grid.clear_widgets()
        for label,country in rows[self.page*count:(self.page+1)*count]:
            self.grid.add_widget(MenuTile(label,lambda key=country:self.select(key),localize=False,
                                          accent=self.screen.draft[self.field]==country))
        if not rows:self.grid.add_widget(BoundedLabel(text='No countries found.'))

    def select(self,country):
        if country not in WORLD_COUNTRIES:return
        self.screen.draft[self.field]=country;self.screen._country_labels();self.dismiss()


class CompactTable(EdgePanel):
    """All rows remain accessible through pages; no horizontal or vertical scroll."""
    def __init__(self, title, headings, rows, focus=None, summary=None, detail=None, title_localize=True):
        self._localizer=current()
        super().__init__(orientation='vertical', padding=dp(6), spacing=dp(3))
        self.headings, self.rows, self.focus = tuple(headings), list(rows), focus
        self.summary, self.detail = summary, detail
        self.show_detail = False
        self.page = 0
        self.page_size = 1
        self.title = BoundedLabel(text=title, localize=title_localize, bold=True, color=GREEN, font_size=sp(12),
                                  size_hint_y=None, height=dp(20))
        self.add_widget(self.title)
        self.head = BoxLayout(size_hint_y=None, height=dp(22), spacing=dp(3))
        self.add_widget(self.head)
        self.lines = BoxLayout(orientation='vertical')
        self.add_widget(self.lines)
        self.controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        self.previous = MenuTile('PREVIOUS', lambda: self.move(-1))
        self.next = MenuTile('NEXT', lambda: self.move(1))
        self.controls.add_widget(self.previous)
        self.counter = BoundedLabel(halign='center', font_size=sp(11), size_hint_x=None, width=dp(46))
        self.controls.add_widget(self.counter)
        self.controls.add_widget(self.next)
        if focus:
            self.controls.add_widget(MenuTile('MY POSITION', self.jump_to_focus))
        if detail:
            self.controls.add_widget(MenuTile('STATS', self.toggle_detail))
        self.add_widget(self.controls)
        self.bind(size=self._render)
        self._render()

    def move(self, amount):
        self.page = max(0, min(self.pages - 1, self.page + amount))
        self._render()

    @property
    def pages(self):
        return max(1, math.ceil(len(self.rows) / self.page_size))

    def jump_to_focus(self):
        index = next((i for i, row in enumerate(self.rows) if str(row[1]) == self.focus), 0)
        self.page = index // self.page_size
        self._render()

    def toggle_detail(self):
        if not self.detail:
            return
        self.show_detail = not self.show_detail
        self._render()

    def _cells(self, row, values, indices, heading=False, highlighted=False):
        count = len(indices)
        for index in indices:
            weight = 0.48 if index == 1 else 0.52 / max(1, count - 1)
            label = BoundedLabel(text=str(values[index]), localize=heading, font_size=sp(12),
                                  bold=heading or highlighted, max_lines=1,
                                  color=GREEN if heading or highlighted else INK,
                                  size_hint_x=weight,
                                  halign='left' if index == 1 else 'center')
            row.add_widget(label)

    @localized_call
    def _render(self, *_):
        if not hasattr(self, 'controls'):
            return
        line_height = max(dp(24), sp(12) * 1.35)
        available = max(line_height, self.height - dp(115))
        self.page_size = max(1, int(available // line_height))
        self.page = max(0, min(self.page, self.pages - 1))
        indices = (self.detail if self.show_detail else self.summary) if self.summary else tuple(range(len(self.headings)))
        if self.summary and self.width >= dp(720) and not self.show_detail:
            indices = tuple(range(len(self.headings)))
        self.head.clear_widgets()
        self._cells(self.head, self.headings, indices, heading=True)
        self.lines.clear_widgets()
        start = self.page * self.page_size
        self.visible_rows = self.rows[start:start + self.page_size]
        for offset, values in enumerate(self.visible_rows):
            row = BoxLayout(size_hint_y=None, height=line_height, spacing=dp(3))
            highlighted = self.focus is not None and str(values[1]) == self.focus
            with row.canvas.before:
                Color(0.10, 0.35, 0.28, 0.75 if highlighted else 0.18 if offset % 2 == 0 else 0.02)
                background = Rectangle(pos=row.pos, size=row.size)
            row.bind(pos=lambda w, v, bg=background: setattr(bg, 'pos', v),
                     size=lambda w, v, bg=background: setattr(bg, 'size', v))
            self._cells(row, values, indices, highlighted=highlighted)
            self.lines.add_widget(row)
        self.counter.text = f'{self.page + 1}/{self.pages}'
        self.previous.disabled = self.page == 0
        self.next.disabled = self.page == self.pages - 1


class BrandMark(BoxLayout):
    """Licensed sports display face with a subordinate author credit."""
    def __init__(self, centered=False, word='SCORER', with_icon=False, **kwargs):
        super().__init__(orientation='vertical', spacing=0, **kwargs)
        alignment = 'center' if centered else 'left'
        self.wordmark = BoundedLabel(text=word, localize=False, font_name='assets/fonts/BarlowCondensed-ExtraBoldItalic.ttf',
                                     font_size=sp(32), halign=alignment, size_hint_y=0.70)
        self.credit = BoundedLabel(text='by clemir', localize=False, font_name='assets/fonts/Barlow-Regular.ttf',
                                   font_size=sp(11), halign=alignment, color=MUTED, size_hint_y=0.30)
        if with_icon:
            # Give the S and remaining letters the same line, independent of
            # the credit below. The icon's inset and font cap height then align.
            row = BoxLayout(size_hint_y=0.70, spacing=dp(2))
            self.icon = Image(source='assets/icon.png', size_hint_x=None)
            self.wordmark.size_hint_y = 1
            row.add_widget(self.icon)
            row.add_widget(self.wordmark)
            credit_row = BoxLayout(size_hint_y=0.30)
            self.credit.size_hint_y = 1
            credit_row.add_widget(self.credit)
            def align_icon(*_):
                self.icon.width = row.height
                credit_row.padding = (row.height + dp(2), 0, 0, 0)
            row.bind(height=align_icon)
            align_icon()
            self.add_widget(row)
            self.add_widget(credit_row)
        else:
            self.add_widget(self.wordmark)
            self.add_widget(self.credit)

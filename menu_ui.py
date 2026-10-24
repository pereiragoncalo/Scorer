"""Responsive, touch-friendly career menus for the original Kivy game."""
from career import EUROPE_PYRAMID_DEPTH, WORLD_COUNTRIES
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp, sp, Metrics
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import math
import edition
import release_settings

INK = (0.91, 0.96, 0.95, 1)
MUTED = (0.58, 0.72, 0.72, 1)
GREEN = (0.30, 0.91, 0.65, 1)
MENU_VIEWS = frozenset(('offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent', 'world', 'splash', 'start', 'profile', 'privacy', 'help', 'upgrade', 'editor', 'world_country', 'world_league'))


class FlowLabel(Label):
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


class TouchButton(Button):
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
        signature = ((self.game.billing.status, self.game.billing.price, self.game.billing.can_purchase) if self.game.view == 'upgrade' else None, self.game.view, self.game._world_available, self.game._career_mode, c.player_name, c.club_name, c.season, c.week,
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
        return TouchButton(label, lambda: self.action(action, value), accent)

    def _build(self):
        c = self.game.career
        if self.game.view != 'start':
            self.game.ads.entry_visible(False)
        self.clear_widgets()
        self._shade.a = 1 if self.game.view == 'splash' else 0.62
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
            logo = Image(source='assets/menu_logo.png', size_hint=(None, 1), width=dp(190))
            brand.bind(width=lambda widget, width: setattr(logo, 'width', min(dp(190), width)))
            brand.add_widget(logo)
        elif self.game.view in ('world', 'editor', 'world_country'):
            header.height = dp(52)
            title = 'WORLD LEAGUES' if self.game.view == 'world' else 'NAMES EDITOR' if self.game.view == 'editor' else self.game.world_country.upper()
            brand.add_widget(BoundedLabel(text=title, font_size=sp(20), bold=True))
            detail = f'{len({v.country for v in c.leagues.values()})} regions · {len(c.leagues)} fictional divisions' if self.game.view == 'world' else c.display_league(c.leagues[self.game.editor_key]) if self.game.view == 'editor' else 'Choose a division'
            brand.add_widget(BoundedLabel(text=detail, font_size=sp(11), color=MUTED))
        elif paged:
            header.height = dp(52)
            titles = {'standings': 'STANDINGS', 'scorers': 'TOP SCORERS', 'calendar': 'FIXTURES', 'world_league': 'WORLD LEAGUE'}
            brand.add_widget(BoundedLabel(text=titles[self.game.view], font_size=sp(20), bold=True))
            brand.add_widget(BoundedLabel(text=c.display_league(c.leagues[self.game.world_league_key] if self.game.view == 'world_league' else c.current_league), font_size=sp(11), color=MUTED))
        else:
            header.height = dp(52)
            brand.add_widget(BrandMark())
        header.add_widget(brand)
        if self.game.view == 'hub':
            profile = MenuTile('PLAYER', lambda: self.action('profile'))
            profile.size_hint_x, profile.width = None, dp(88)
            header.add_widget(profile)
        if self.game.view == 'hub':
            for title, action in [('HELP', 'help'), ('MODES' if self.game._world_available else 'UPGRADE', 'upgrade')]:
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
            self.body = CompactTable(c.display_league(league), ('POS','CLUB','P','PTS'), [(i+1,c.display_club(club),club.played,club.points) for i,club in enumerate(league.table())])
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
            card.label(title, heading=True)
        self.body.add_widget(card)
        return card

    def _offers(self):
        c = self.game.career
        card = self.card('Your first contract' + (' · ' + c.current_league.country if c.world_unlocked else ' · Scorer League'))
        if c.world_unlocked:
            card.label('Suggested from phone: ' + c.suggested_country + '. Choose a starting division.', muted=True)
            choices = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
            choices.add_widget(self._button(c.suggested_country.upper(), 'start_country', c.suggested_country))
            choices.add_widget(self._button('ENGLAND DIVISION 4', 'start_country', 'England'))
            card.add_widget(choices)
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
        note = card.label('Optional ad: +1 morale after completion. Once per week, max 20.', muted=True)
        note.font_size = sp(12)
        if c.morale_ad_week == c.week:
            card.label('This week’s morale ad reward has been claimed.', muted=True)
        elif c.morale >= 20:
            card.label('Morale is already at its maximum.', muted=True)
        elif g.reward_ad_status:
            card.label(g.reward_ad_status, muted=True)
        if c.message.startswith(('Reward ad', 'Ad reward', 'Unable to save the morale')):
            card.label(c.message, muted=True)

    def _compact_list(self):
        c = self.game.career
        if self.game.view == 'standings':
            rows = [(i + 1, c.display_club(club), club.played, club.won, club.drawn, club.lost,
                     club.goals_for, club.goals_against, club.goal_difference, club.points)
                    for i, club in enumerate(c.current_league.table())]
            return CompactTable('STANDINGS · ' + c.display_league(c.current_league),
                                ('POS', 'CLUB', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS'),
                                rows, focus=c.display_text(c.club_name), summary=(0, 1, 2, 8, 9), detail=(0, 1, 3, 4, 5, 6, 7))
        if self.game.view == 'scorers':
            ranking = dict(c.current_league.scorer_goals)
            ranking.setdefault(c.player_name, 0)
            rows = [(i + 1, c.display_scorer(name), goals) for i, (name, goals) in enumerate(sorted(ranking.items(), key=lambda x: (-x[1], x[0])))]
            return CompactTable('TOP SCORERS', ('POS', 'PLAYER', 'GOALS'), rows, focus=c.player_name)
        rows = [(str(e.get('date', ''))[8:10] + '/' + str(e.get('date', ''))[5:7], c.display_text(f"{e.get('home', '')} vs {e.get('away', '')}", e.get("country")),
                 c.display_text(e.get('competition', ''), e.get('country')), e.get('status', '')) for e in c.calendar_entries()]
        return CompactTable(f'FIXTURES · {c.season}/{str(c.season + 1)[-2:]}', ('DATE', 'MATCH', 'COMPETITION', 'STATUS'), rows,
                            summary=(0, 1, 2, 3))

    def _privacy(self):
        card = self.card('Privacy & advertising')
        if self.game._world_available or self.game.career.world_unlocked:
            card.label('World is ad-free. A verified purchase supports up to seven days of offline access before an online ownership check. Careers and imported names stay on this device; there is no SCORER account.')
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
        card.label(self.game.ads.status, muted=True)
        card.label(self.game.ads.break_status, muted=True)
        card.label(self.game.ads.reward_status, muted=True)
        if self.game.ads.privacy_required:
            card.add_widget(MenuTile('AD PRIVACY OPTIONS', lambda: self.game.ads.privacy_options()))

    def _privacy_contact(self, card):
        card.label('Careers and name edits are stored privately on this device. Uninstalling or clearing app data removes them; a new game keeps a private backup. There is no SCORER account or career upload.', muted=True)
        card.label('When purchases are enabled, Google Play and the developer verification service check your World purchase. The service receives the purchase token and a random installation ID, never your player name or career. No card details are handled by SCORER.', muted=True)
        card.label('City data: GeoNames via github.com/datasets/world-cities (CC BY 4.0); adapted names. Licence: creativecommons.org/licenses/by/4.0/. Club/city references: OpenFootball (CC0); country metadata: Annexare (MIT). Licences included.', muted=True)
        if release_settings.DEVELOPER_NAME:
            card.label('Developer: ' + release_settings.DEVELOPER_NAME, muted=True)
        if release_settings.SUPPORT_EMAIL:
            card.label('Support: ' + release_settings.SUPPORT_EMAIL, muted=True)
        if release_settings.PRIVACY_URL:
            card.add_widget(self._button('FULL PRIVACY POLICY', 'open_privacy_policy'))

    def _help(self):
        from world_ui import HELP_PAGES
        title, text = HELP_PAGES[self.game.help_page]
        card = self.card(title)
        card.label(text)
        controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        controls.add_widget(self._button('PREVIOUS', 'help_page', -1))
        controls.add_widget(BoundedLabel(text=f'{self.game.help_page+1}/{len(HELP_PAGES)}', halign='center', size_hint_x=.3))
        controls.add_widget(self._button('NEXT', 'help_page', 1))
        card.add_widget(controls)

    def _upgrade(self):
        card = self.card('SCORER WORLD — upgrade information')
        if self.game._world_available:
            card.label('World is unlocked. Free and World use separate careers and saved progress.')
            modes = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
            modes.add_widget(self._button('FREE CAREER', 'select_mode', 'free'))
            modes.add_widget(self._button('WORLD CAREER', 'select_mode', 'world', accent=True))
            card.add_widget(modes)
            if self.game.career.world_unlocked:
                card.add_widget(self._button('WORLD LEAGUES', 'world'))
            card.add_widget(self._button('RESTORE PURCHASE', 'restore_world'))
            return
        card.label('World is a one-time upgrade inside SCORER. It unlocks worldwide fictional leagues and the local name editor, and removes ads. Opening this page does not charge you.')
        card.label('World includes worldwide fictional domestic leagues, promotions and transfers, local starting contracts and England Division 4.')
        card.label('The editor changes display names and imports your own club, league and squad names from local JSON. Existing statistics stay intact.')
        card.label('Free and World have separate careers in this app. Your Free career stays in Free; World starts with its own player and contracts. No second installation or subscription is required.')
        card.label('Purchases use Google Play. Pending, cancelled or unverified payments never unlock World. Restore uses the purchasing Google account.', muted=True)
        buy = self._button('UPGRADE TO WORLD' + (' · ' + self.game.billing.price if self.game.billing.price else ''), 'buy_world', accent=True)
        buy.disabled = self.game._world_available or not self.game.billing.can_purchase
        card.add_widget(buy)
        card.add_widget(self._button('RESTORE PURCHASE', 'restore_world'))
        card.label(self.game.billing.status, muted=True)
        card.label('Only Google Play displays the final price and payment confirmation.' + ('' if release_settings.is_production() else ' No payment is activated in this test build.'), muted=True)
        if self.game.career.message.startswith('World is owned'):
            card.label(self.game.career.message)

    def _world_country(self):
        c = self.game.career
        card = self.card(self.game.world_country)
        grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(6))
        grid.bind(minimum_height=grid.setter('height'))
        for key, league in c.leagues.items():
            if league.country == self.game.world_country:
                grid.add_widget(self._button(c.display_league(league), 'world_league', key))
        card.add_widget(grid)
        card.label('Fictional domestic pyramids; regional/amateur competitions are not modelled.', muted=True)

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
        self.brand = Image(source='assets/menu_logo.png', size_hint_y=None, height=dp(52))
        self.panel.add_widget(self.brand)
        self.info = BoundedLabel(text=('World unlocked. Ad-free. Local name editor.' if not edition.WORLD_PREVIEW else 'World preview. Ad-free. No payments.') if menu.game.career.world_unlocked else ('Free career. One division. Ads removed.' if menu.game._world_available else 'One division. Contains ads. See Privacy.' if release_settings.is_production() else 'One division. Google test ads. See Privacy.'),
                                 color=MUTED, font_size=sp(12), halign='center')
        if menu.game.career.message.startswith('Unable to continue'):
            self.info.text = menu.game.career.message
        self.panel.add_widget(self.info)
        new_row = BoxLayout(spacing=dp(8))
        new_row.add_widget(MenuTile('NEW GAME', lambda: menu.action('new_game'), accent=True))
        if menu.game._world_available:
            new_row.add_widget(MenuTile('WORLD' if menu.game._career_mode == 'free' else 'FREE', lambda: menu.action('select_mode', 'world' if menu.game._career_mode == 'free' else 'free')))
        self.panel.add_widget(new_row)
        load = MenuTile('LOAD GAME', lambda: menu.action('load_game'))
        load.disabled = not menu.game.career.save_path.is_file()
        self.panel.add_widget(load)
        actions = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        actions.add_widget(MenuTile('HELP', lambda: menu.action('help')))
        actions.add_widget(MenuTile('PRIVACY', lambda: menu.action('privacy')))
        actions.add_widget(MenuTile('EXIT', menu.game._request_exit))
        self.panel.add_widget(actions)
        self.panel.canvas.before.remove(self.panel.edge)
        self.add_widget(self.panel)
        self.bind(pos=self._fit, size=self._fit)
        self._fit()

    def _fit(self, *_):
        banner_fits = not self.menu.game._world_available and not self.menu.game.career.world_unlocked and self.height >= dp(340) and self.width >= dp(340)
        self.menu.game.ads.entry_visible(banner_fits)
        self.banner_space = dp(64) if banner_fits else 0
        available = self.height - self.banner_space
        self.panel.size = (min(self.width - dp(24), dp(340)), min(available - dp(16), dp(280)))
        self.panel.center = (self.center_x, self.y + self.banner_space + available / 2)
        self.brand.height = dp(28) if self.panel.height < dp(244) else dp(52)
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
        self.identity = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(12), padding=[dp(10), 0])
        self.identity.add_widget(BoundedLabel(text=c.player_name, font_size=sp(18), bold=True, color=GREEN))
        self.identity.add_widget(BoundedLabel(text=c.display_text(c.club_name), font_size=sp(14), halign='center'))
        self.identity.add_widget(BoundedLabel(text=f'Energy {c.stamina:.1f}/20 · Morale {c.morale:.1f}/20',
                                             color=MUTED, font_size=sp(11), halign='right'))
        self.add_widget(self.identity)
        self.hero = BoxLayout(spacing=dp(12))
        self.match = EdgePanel(orientation='vertical', size_hint_x=0.66)
        self.match.add_widget(BoundedLabel(text='NEXT MATCH · ' + c.format_date(c.current_date), color=GREEN, font_size=sp(10),
                                          bold=True, size_hint_y=None, height=dp(16)))
        fixture = c.next_match()
        teams = BoxLayout(spacing=dp(8))
        home = c.display_club(fixture[1]) if fixture else 'Season complete'
        away = c.display_club(fixture[2]) if fixture else ''
        teams.add_widget(BoundedLabel(text=home, font_size=sp(18), bold=True, halign='center'))
        teams.add_widget(BoundedLabel(text='VS' if fixture else '', font_size=sp(11), color=MUTED,
                                     halign='center', size_hint_x=0.18))
        teams.add_widget(BoundedLabel(text=away, font_size=sp(18), bold=True, halign='center'))
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
        self.season.add_widget(BoundedLabel(text=c.display_league(c.current_league) + (' · 1 DIVISION' if not c.world_unlocked else ''),
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
        self.status = BoundedLabel(text=c.display_text(c.message) if c.trained_this_week else 'Complete weekly training to unlock Play.', color=MUTED, font_size=sp(11),
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
                self.add_widget(self.hero, index=2)
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
        self.panel = EdgePanel(orientation='vertical', size_hint=(None, None), padding=dp(14), spacing=dp(8))
        self.panel.canvas.before.remove(self.panel.edge)
        self.panel.background.radius = [dp(12)]
        self.panel.add_widget(BoundedLabel(text='YOUR PLAYER', bold=True, font_size=sp(18),
                                          size_hint_y=None, height=dp(28)))
        existing = menu.game._profile_return == 'hub'
        self.name = TextInput(text=menu.game.career.player_name if existing else '',
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
        message = menu.game.career.message
        self.panel.add_widget(BoundedLabel(text=message if ('name' in message.lower() or 'scorer' in message.lower() or 'save' in message.lower())
                                          else 'Choose your name. Your progress is kept.',
                                          color=MUTED, font_size=sp(12), size_hint_y=None, height=max(dp(36), sp(12)*2.5)))
        actions = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        actions.add_widget(MenuTile('CANCEL', lambda: menu.action('cancel_profile')))
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
        self.menu.action('save_profile', self.name.text)

    def _fit(self, *_):
        compact = self.height < dp(250)
        self.panel.padding = dp(10 if compact else 14)
        self.panel.spacing = dp(6 if compact else 8)
        self.panel.size = (min(self.width - dp(24), dp(420)), min(self.height - dp(16), self.panel.minimum_height))
        self.panel.center = self.center


class CompactTable(EdgePanel):
    """All rows remain accessible through pages; no horizontal or vertical scroll."""
    def __init__(self, title, headings, rows, focus=None, summary=None, detail=None):
        super().__init__(orientation='vertical', padding=dp(6), spacing=dp(3))
        self.headings, self.rows, self.focus = tuple(headings), list(rows), focus
        self.summary, self.detail = summary, detail
        self.show_detail = False
        self.page = 0
        self.page_size = 1
        self.title = BoundedLabel(text=title, bold=True, color=GREEN, font_size=sp(12),
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
            label = BoundedLabel(text=str(values[index]), font_size=sp(12),
                                  bold=heading or highlighted, max_lines=1,
                                  color=GREEN if heading or highlighted else INK,
                                  size_hint_x=weight,
                                  halign='left' if index == 1 else 'center')
            row.add_widget(label)

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
        self.wordmark = BoundedLabel(text=word, font_name='assets/fonts/BarlowCondensed-ExtraBoldItalic.ttf',
                                     font_size=sp(32), halign=alignment, size_hint_y=0.70)
        self.credit = BoundedLabel(text='by clemir', font_name='assets/fonts/Barlow-Regular.ttf',
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

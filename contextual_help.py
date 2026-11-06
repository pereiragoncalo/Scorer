"""Screen-specific gameplay guidance; no global manual in normal navigation."""
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp,sp
from menu_ui import EdgePanel,MenuTile,FlowLabel

# Reuse translated gameplay paragraphs, but expose only relevant topics per screen.
def topics(game):
    from world_ui import HELP_PAGES,WORLD_HELP_PAGES,PROGRESSION_HELP_PAGES
    from player_development import FOCI,NAMES,HINTS
    import edition
    base=WORLD_HELP_PAGES if edition.is_world() else HELP_PAGES
    view=game.view
    training=(base[1],*PROGRESSION_HELP_PAGES[1:6])
    special={
        'start':(base[0],), 'offers':(('Your first contract',START),),
        'hub':(('HELP',HUB),), 'profile':(PROGRESSION_HELP_PAGES[0],),
        'training':training,'development':PROGRESSION_HELP_PAGES[-2:],
        'shot':(base[2],)+(training if game.shot_context=='training' else ()),
        'match':(base[2],), 'standings':(('STANDINGS',TABLE),),
        'competition':(('COMPETITIONS',TABLE),),'competitions':(('COMPETITIONS',TABLE),),
        'world_league':(('STANDINGS',TABLE),),'scorers':(('TOP SCORERS',SCORERS),),
        'calendar':(('FIXTURES',CALENDAR),),'agent':(('AGENT',AGENT),),
        'world':(base[3],),'world_country':(base[3],),'editor':(base[3],),
        'coach':(('COACH MEETING',COACH),),'newspaper':(('MATCH REPORT',PAPER),),
        'club':(('CLUB',CLUB),),'language':(('LANGUAGE',LANGUAGE),),
        'leaderboard':(('LEADERBOARD',RECORDS),),'record_safety':(('LEADERBOARD',RECORDS),),
        'family':(('ADULT CONTROLS',CONTROLS),),'privacy':(('SETTINGS',SETTINGS),),
        'data_notice':(('BEFORE YOU PLAY',NOTICE),),'upgrade':(base[3],),
    }
    return special.get(view,(base[0],))

START='Choose a contract to begin your career. Your nationality determines which national team can call you up.'
HUB='Choose an action to open its screen. Use the Help button there for guidance about that part of the game.'
TABLE='Select a competition to see its standings or fixtures. Switch groups when available. Knockout rounds show results, two-leg ties and penalties. Use the page controls to see every row.'
SCORERS='This table ranks league scorers by goals. My Position finds your player. Cup and international goals are counted separately.'
CALENDAR='Check dates, opponents, competitions and results. Complete training before each playable fixture, including matches in the same week.'
AGENT='Choose an offer during the transfer window. A free agent can sign outside the window. Changing clubs keeps your career progress.'
COACH='Meet the coach after a scoring drought or a key match. Read the feedback and finish the meeting to continue.'
PAPER='Read the previous match report, including goals and the result. Continue to a requested coach meeting or back to your career.'
CLUB='View the club foundation, honours, stadium and capacity. Club colours follow the selected team.'
LANGUAGE='English is the default. Choose a language or select Automatic to follow your phone.'
RECORDS='Load the public records table. Publishing your own record is optional. Select a position to report or block an entry.'
CONTROLS='An adult can manage access to public features. These controls do not prevent playing your local career.'
SETTINGS='Export your career before changing devices or uninstalling. Import restores a compatible career after confirmation.'
NOTICE='Choose I AGREE to continue or I DO NOT AGREE to close the game.'

class ContextHelp(ModalView):
    def __init__(self,game):
        super().__init__(size_hint=(.94,.92),auto_dismiss=False)
        self.game=game;self.origin=game.view;loc=game.i18n
        panel=EdgePanel(orientation='vertical',padding=dp(12));scroll=ScrollView(do_scroll_x=False)
        self.body=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(10));self.body.bind(minimum_height=self.body.setter('height'))
        for title,text in topics(game):
            self.body.add_widget(FlowLabel(text=loc.tr(title),font_size=sp(18),bold=True))
            for paragraph in text if isinstance(text,tuple) else (text,):
                rendered=loc.tr(paragraph,season=game.career.development['tracked_since']) if paragraph.startswith('Tracking began in ') else loc.tr(paragraph)
                self.body.add_widget(FlowLabel(text=rendered,localize=False,halign='justify'))
        scroll.add_widget(self.body);panel.add_widget(scroll)
        actions=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        if self.origin in ('hub','start'):
            def navigate(action):self.dismiss();game._activate_ui(action);game.draw()
            actions.add_widget(MenuTile('SETTINGS',lambda:navigate('privacy')))
            import edition
            if edition.is_world():actions.add_widget(MenuTile('LANGUAGE',lambda:navigate('language')))
        actions.add_widget(MenuTile('CLOSE',self.dismiss));panel.add_widget(actions);self.add_widget(panel)
        self.bind(on_dismiss=lambda *_:setattr(game,'_context_help',None))

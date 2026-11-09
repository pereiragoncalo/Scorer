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
        'hub':(('HELP',HUB+' Injuries have a 1–3% risk per played match, depending on fitness, and last 1–3 missed fixtures. Use Simulate Match while recovering; no appearance or training is counted.'),), 'profile':(PROGRESSION_HELP_PAGES[0],),
        'training':(base[1],),'development':PROGRESSION_HELP_PAGES[-2:],
        'shot':(base[2],),
        'match':(base[2],), 'standings':(('STANDINGS',TABLE),),
        'competition':(('COMPETITIONS',TABLE),),'competitions':(('COMPETITIONS',TABLE),),
        'world_league':(('STANDINGS',TABLE),),'scorers':(('TOP SCORERS',SCORERS),),
        'calendar':(('FIXTURES',CALENDAR),),'agent':(('AGENT',AGENT),),
        'world':(base[3],),'world_country':(base[3],),'editor':(base[3],),
        'lifestyle':(('LIFESTYLE','Your weekly contract salary is paid once per career week. Buy homes, cars, clothes and gifts for your girlfriend using local career money. Purchases do not improve your finishing. From age 38, choose whether to retire each season; continuing makes finishing progressively harder.'),),
        'shopping':(('SHOPPING','Use career money to buy homes, cars, clothes and gifts. Owned items appear in My Assets.'),),
        'possessions':(('MY ASSETS','Your portrait shows your best owned home, outfit and car. Open Collection to browse every purchase.'),),
        'collection':(('COLLECTION','Browse only the purchases already acquired in this career. The displayed value is the purchase price.'),),
        'private_coach':(('INDIVIDUAL MEETING','An individual meeting can follow five or more games without scoring or a transfer proposal. Your weekly training focus is chosen in the team talk.'),),
        'title_coach':(("CHAMPIONS' TEAM TALK",'This title belongs to everyone. Enjoy the moment with the supporters.'),),
        'coach':(('WEEKLY TEAM TALK',COACH),)+training[1:],'newspaper':(('MATCH REPORT',PAPER),),
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
AGENT='Choose an offer during the transfer window. A free agent can sign outside the window. Changing clubs keeps your career progress. Offers must be from an equal or higher league status band. Your agent prioritises your country until you stand out. A strong season can bring an eligible offer from your favourite club.'
COACH='Attend one team talk each week. Read the team and individual feedback, choose one of two training focuses, then finish the talk. The choice applies to the week; extra matches do not require another talk.'
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

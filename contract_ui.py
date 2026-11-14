"""Club meetings: requests, agent advice, explicit club reply and signature."""
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from contract_negotiation import current,package,advice,remaining,ensure,expiry_date
from datetime import date
from career_life import ITEMS


def years_text(c,loc,offer=None,compact=False):
    if offer is not None:
        return loc.tr('Contract: {years} years · until {date}',years=offer['years'],date=loc.date(expiry_date(c.current_date,offer['years'])))
    record=ensure(c)
    if compact:return loc.tr('Contract: {years} years',years=remaining(c)) if record else ''
    return loc.tr('{years} years remaining · until {date}',years=remaining(c),date=loc.date(date.fromisoformat(record['end_date']))) if record else ''


def benefits(card,offer):
    names={i[0]:i[2]for i in ITEMS};loc=card._i18n if hasattr(card,'_i18n')else None
    from localization import current as localizer
    loc=loc or localizer()
    if offer['home']:card.label(loc.tr('Housing included: {item}',item=loc.tr(names[offer['home']])),muted=True,localize=False)
    if offer['car']:card.label(loc.tr('Car included: {item}',item=loc.tr(names[offer['car']])),muted=True,localize=False)
    if offer['squad']:card.label('Squad investment included',muted=True)
    if not any(offer[k]for k in ('home','car','squad')):card.label('No additional benefits.',muted=True)


def build(menu):
    game=menu.game;c=game.career;loc=game.i18n;uid=getattr(game,'_contract_uid','');row=current(c,uid)
    if row is None:
        menu.card('CONTRACT MEETING').label('This offer is no longer available.')
        menu.body.add_widget(menu._button('Hear other clubs','contract_back'));return
    title=menu.card('CONTRACT MEETING');title.label(c.display_text(row['club']),heading=True,localize=False)
    title.label('Negotiate your contract before signing.',muted=True)
    if c.message.startswith(('Unable ','Could not ')):title.label(c.message)
    requested=package(row);card=menu.card('Requested terms')
    grid=GridLayout(cols=2,spacing=dp(6),size_hint_y=None);grid.bind(minimum_height=grid.setter('height'));card.add_widget(grid)
    labels={
      'years':loc.tr('Years: {years}',years=requested['years']),
      'premium':loc.tr('Salary: €{salary}/month (+{premium}%)',salary=requested['salary'],premium=row['request']['premium']),
      'home':loc.tr('Housing: {value}',value=loc.tr(next(i[2]for i in ITEMS if i[0]==requested['home']))if requested['home']else loc.tr('No')),
      'car':loc.tr('Car: {value}',value=loc.tr(next(i[2]for i in ITEMS if i[0]==requested['car']))if requested['car']else loc.tr('No')),
      'squad':loc.tr('Squad investment: {value}',value=loc.tr('Yes'if row['request']['squad']else 'No')),
    }
    for key,label in labels.items():
        button=menu._button(label,'contract_change',key);button.disabled=row['round']>=3;grid.add_widget(button)
    agent=menu.card('Your agent');agent.label(advice(c,uid))
    if row['round']<3:agent.add_widget(menu._button('Send demands','contract_propose',accent=True))
    else:agent.label('Three rounds used. This is the final offer.',muted=True)
    club=menu.card("The club's offer")
    if row['status']=='accepted':club.label('Club accepted your demands.')
    elif row['status']=='counter':club.label('Club declined the full package and made a counter-offer.')
    elif row['status']=='offer':club.label("This is the club's original offer.")
    club.label(years_text(c,loc,row['offer']),localize=False)
    club.label(loc.tr('€{salary}/month',salary=row['offer']['salary']),localize=False)
    benefits(club,row['offer'])
    if row['status']=='draft':club.label('Send the new demands before signing.',muted=True)
    sign=menu._button('Sign club offer','contract_sign',accent=True);sign.disabled=row['status']=='draft';club.add_widget(sign)
    club.add_widget(menu._button('Hear other clubs','contract_back'))

"""Persistent, once-only collective trophy presentation. No winner prediction."""
import copy,hashlib,math
FIELDS=('season','competition','title','team_uid','team','country')
def fresh():return dict(version=1,queue=[],seen=[])
def identity(row):return hashlib.sha256(':'.join(str(row[k]) for k in ('season','competition','team_uid')).encode()).hexdigest()[:24]
def collective(row):return not row['competition'].startswith(('scorer:','playoff:','reserve:'))
def team_record(club):return {k:getattr(club,k) for k in ('uid','name','country','tier','rating')}
def match_scene(c,home,away):
    from attendance import team_turnout
    def fraction(club):return team_turnout(c,club)
    return dict(home=team_record(home),away=team_record(away),turnout=dict(home=fraction(home),away=fraction(away)))
def enqueue(c,row):
    if not collective(row):return
    state=getattr(c,'title_events',None)
    if state is None:c.title_events=state=fresh()
    key=identity(row)
    if key in state['seen']:return
    scene=getattr(c,'_title_match_scene',None)
    if not scene or row['team_uid'] not in (scene['home']['uid'],scene['away']['uid']):
        club=next((t for l in c.leagues.values() for t in l.clubs if t.uid==row['team_uid']),None)
        if club is None:
            from career import CareerClub
            club=CareerClub(row['team'],row['country'],'National Team',1,80,uid=row['team_uid'])
        scene=match_scene(c,club,club)
    from coach import appearance_for
    event={k:row[k] for k in FIELDS};event.update(id=key,stage='celebration',scene=copy.deepcopy(scene),portrait=appearance_for(row['team_uid'],c.coach_appearance)['portrait'])
    state['queue']=(state['queue']+[event])[-16:];state['seen']=(state['seen']+[key])[-256:]
def pending(c):
    queue=getattr(c,'title_events',{}).get('queue',[])
    return queue[0] if queue else None
def view(c):
    e=pending(c)
    return ('trophy' if e['stage']=='celebration' else 'title_coach') if e else None
def needs_focus(c):
    e=pending(c)
    return bool(e and c.club and c.coach_meeting_required)
def to_coach(c):
    e=pending(c)
    if not e or e['stage']!='celebration':return False
    # Resolve the next playable week before choosing its weekly focus.
    # Otherwise hub construction can advance the calendar after the title talk.
    c.next_match()
    e['stage']='coach'
    if c.save() is False:e['stage']='celebration';return False
    return True
def finish(c,focus=None):
    e=pending(c)
    if not e or e['stage']!='coach':return False
    required=bool(c.club and c.coach_meeting_required)
    if required and focus not in c.coach_focus_options():return False
    before=copy.deepcopy(c.title_events)
    c.title_events['queue'].pop(0)
    previous_private=c.life.get('private_meeting','');c.life['private_meeting']=''
    stage=c.post_match_stage
    if stage=='coach':c.post_match_stage=''
    ok=c.attend_coach_meeting(focus) if required else c.save()
    if ok is False:c.post_match_stage=stage;c.life['private_meeting']=previous_private
    if ok is False:c.title_events=before;return False
    return True

def clean(raw,honours):
    state=fresh()
    if not isinstance(raw,dict) or raw.get('version')!=1:return state
    records={identity(r):r for r in honours['trophies'] if collective(r)}
    seen=raw.get('seen',[])
    if isinstance(seen,list):state['seen']=list(dict.fromkeys(x for x in seen[-256:] if isinstance(x,str) and x in records))
    rows=raw.get('queue',[])
    if not isinstance(rows,list):return state
    for e in rows[:16]:
        try:
            key=e['id'];row=records[key]
            if key in {x['id'] for x in state['queue']} or any(e[k]!=row[k] for k in FIELDS) or e['stage']not in ('celebration','coach') or type(e['portrait'])is not int or not 0<=e['portrait']<10:continue
            scene=e['scene']
            if set(scene)!={'home','away','turnout'} or set(scene['turnout'])!={'home','away'}:continue
            for side in ('home','away'):
                t=scene[side]
                if set(t)!={'uid','name','country','tier','rating'} or any(not isinstance(t[k],str) or not 1<=len(t[k])<=100 or not t[k].isprintable() for k in ('uid','name','country')):raise ValueError()
                if type(t['tier'])is not int or not 1<=t['tier']<=8 or type(t['rating'])not in (int,float) or not math.isfinite(t['rating']) or not 0<=t['rating']<=100:raise ValueError()
                value=scene['turnout'][side]
                if type(value)not in (int,float) or not math.isfinite(value) or not 0<=value<=1:raise ValueError()
            if e['team_uid'] not in (scene['home']['uid'],scene['away']['uid']):continue
            item={k:copy.deepcopy(e[k]) for k in (*FIELDS,'id','stage','scene','portrait')};state['queue'].append(item)
            if key not in state['seen']:state['seen'].append(key)
        except (KeyError,ValueError,TypeError,AttributeError):continue
    return state

"""Persistent weekly coach conversations; no reward, match RNG or shot changes."""
import copy
import hashlib

STYLES = ('Encouraging', 'Demanding', 'Balanced')
ROUTINE = ('No special feedback today. Prepare well in training and be ready for the next match.',
           'A short check-in today. Work on your finishing and prepare for the next match.')
FEEDBACK = {
    'drought': (
        ('The goals have dried up, but I believe in you. Keep working and the next chance will come.',
         'A difficult run does not define you. Stay confident and keep getting into scoring positions.'),
        ('You have gone several games without scoring. Focus on your movement and make training count.',
         'We need a response to this goalless run. Stay composed and work harder on your finishing.'),
        ('You are in a goalless spell. Let us work on finding space and choosing the right moment to shoot.',
         'The goals are missing. Concentrate on your next action, not on the length of this run.'),
    ),
    'decisive': (
        ('You delivered in a big match. That was an excellent performance. Well done!',
         'You stood up when the pressure was highest. You deserve praise for that performance.'),
        ('A strong performance in an important match. Now keep your focus; the next game starts at zero.',
         'You handled a big occasion well. Keep that standard in training and do not get carried away.'),
        ('You made your chances count in an important match. Keep preparing with the same care.',
         'An impressive performance under pressure. Enjoy it, then turn your attention to the next match.'),
    ),
    'key_match': (
        ('That was an important match. Let us learn from it and prepare the next one with confidence.',),
        ('An important match deserves an honest review. Keep your focus and work on what needs improving.',),
        ('Let us review that key match calmly, then take the lessons into training.',),
    ),
    'form': (
        ('Your recent scoring form has been excellent. Keep believing in your ability.',),
        ('You are scoring regularly. Keep your focus and keep demanding more from yourself.',),
        ('Your recent finishing has been strong. Keep the same preparation and consistency.',),
    ),
}
REQUIRED = 'Your coach has requested a meeting before training or playing.'


def number(value, maximum=1_000_000_000):
    return type(value) is int and 0 <= value <= maximum


def fresh_state(uid='', recent=()):
    goals = [g for g in recent[-8:] if number(g, 100)]
    drought = 0
    for g in reversed(goals):
        if g:break
        drought += 1
    return dict(version=1, club=uid, games=len(goals), drought=drought, recent=goals,
                feedback_game=0, feedback_kind='', latest_decisive=False, pending_key=False, meeting=None)


def clean_state(raw):
    """Optional save extension: discard damaged coach data, never the career."""
    if not isinstance(raw, dict) or raw.get('version') != 1:
        return fresh_state()
    uid=raw.get('club')
    if not isinstance(uid,str) or len(uid)>64 or not uid.isprintable() and uid:
        return fresh_state()
    state=fresh_state(uid)
    if not all(number(raw.get(k)) for k in ('games','drought','feedback_game')):
        return state
    if raw['drought']>raw['games'] or raw['feedback_game']>raw['games']:
        return state
    recent=raw.get('recent')
    if not isinstance(recent,list) or len(recent)>8 or not all(number(g,100) for g in recent):
        return state
    kind=raw.get('feedback_kind','')
    if kind not in ('','drought','decisive','key_match','form') or type(raw.get('latest_decisive')) is not bool:
        return state
    state.update({k:raw[k] for k in ('games','drought','feedback_game','recent','feedback_kind','latest_decisive')})
    state['pending_key']=raw.get('pending_key',state['latest_decisive']) is True
    m=raw.get('meeting')
    if (isinstance(m,dict) and isinstance(m.get('key'),str) and len(m['key'])<=160 and m['key'].isprintable()
            and m.get('kind') in ('routine',*FEEDBACK) and number(m.get('style'),2) and number(m.get('variant'),1)):
        state['meeting']={k:m[k] for k in ('key','kind','style','variant')}
    return copy.deepcopy(state)


def style_for(uid):
    return int(hashlib.sha256(('scorer-coach-v1:'+uid).encode()).hexdigest()[:8],16)%3


def conversation(state, key, uid):
    existing=state.get('meeting')
    if existing and existing['key']==key and not meeting_due(state):
        return dict(existing)
    kind='routine'
    if state['games']>state['feedback_game']:
        if state['pending_key'] or state['latest_decisive']:
            kind='decisive' if state['latest_decisive'] else 'key_match'
        elif state['drought']>=3 and (state['feedback_kind']!='drought' or state['games']-state['feedback_game']>=3):
            kind='drought'
    style=style_for(uid)
    options=ROUTINE if kind=='routine' else FEEDBACK[kind][style]
    index=int(hashlib.sha256((key+':'+kind+':'+str(state['games'])).encode()).hexdigest()[:8],16)%len(options)
    return dict(key=key,kind=kind,style=style,variant=index)


ADVICE = ('In training, alternate low shots and shots across the goalkeeper. Watch the target, stay composed and choose your moment rather than rushing the finish.', 'Take that confidence into training. Practise different finishes so you have more than one answer when the next important chance arrives.', 'Think about the chances you had: when did you rush, and when could you have waited? Use this week’s practice to improve the timing of your next finish.')
FOLLOW_UP = ('I am backing you. We will work through this together; focus on one good decision at a time.', 'I expect concentration in every exercise. Show me a controlled finish and carry that discipline into the next match.', 'Keep your preparation consistent. Judge the next opportunity on its own merits and take the lesson forward.')

def conversation_text(meeting):
    kind = meeting['kind']
    if kind == 'routine':return ROUTINE[meeting['variant']%len(ROUTINE)]
    options = FEEDBACK[kind][meeting['style']]
    advice = ADVICE[0 if kind == 'drought' else 1 if kind in ('decisive','form') else 2]
    return '\n\n'.join((options[meeting['variant']%len(options)], advice, FOLLOW_UP[meeting['style']]))


def meeting_due(state):
    return state['games']>state['feedback_game'] and (state['pending_key'] or state['latest_decisive'] or
        (state['drought']>=3 and (state['feedback_kind']!='drought' or state['games']-state['feedback_game']>=3)))


class CoachCareer:
    def _select_coach_appearance(self):
        if self.club:self.coach_appearance=appearance_for(self.club.uid,self.coach_appearance)

    @property
    def coach_portrait(self):
        uid=self.club.uid if self.club else ''
        return PORTRAITS[appearance_for(uid,self.coach_appearance)['portrait']]

    @property
    def coach_key(self):
        return f'{self.season}:{self.week}:{self.club.uid}' if self.club else ''

    def _current_coach_state(self):
        uid=self.club.uid if self.club else ''
        return self.coach_state if self.coach_state['club']==uid else fresh_state(uid)

    @property
    def coach_meeting_held(self):
        m=self._current_coach_state()['meeting']
        return bool(self.club and not self.free_agent and m and m['key']==self.coach_key)

    @property
    def coach_meeting_required(self):
        return bool(self.club and not self.free_agent and meeting_due(self._current_coach_state()))

    def coach_conversation(self):
        return conversation(self._current_coach_state(),self.coach_key,self.club.uid if self.club else '')

    def attend_coach_meeting(self):
        if not self.club or self.free_agent:
            self.message='Choose a club before meeting your coach.'
            return False
        if not self.coach_meeting_required:return True
        previous=self.coach_state
        state=copy.deepcopy(self._current_coach_state())
        meeting=self.coach_conversation()
        state['meeting']=meeting
        if meeting['kind']!='routine':
            state['feedback_game']=state['games'];state['feedback_kind']=meeting['kind']
            if meeting['kind'] in ('decisive','key_match'):
                state['latest_decisive']=False;state['pending_key']=False
        self.coach_state=state
        if self.save() is False:
            self.coach_state=previous
            self.message='Unable to save the meeting. Please try again.'
            return False
        self.message='Coach meeting complete. You can train now.'
        return True

    def record_coach_performance(self,goals,misses,moments,not_lost,key_match=False):
        from match_moments import clean_moments
        state=copy.deepcopy(self._current_coach_state())
        state['games']+=1
        state['drought']=state['drought']+1 if goals==0 else 0
        state['recent']=(state['recent']+[goals])[-8:]
        events=clean_moments(moments)
        key_match=key_match or any(e['kind'] in ('final','playoff','derby','survival') or
            (e['kind'] in ('equaliser','lead') and e['outcome']=='goal' and not_lost) for e in events)
        state['pending_key']=state['pending_key'] or key_match
        state['latest_decisive']=state['latest_decisive'] or any(
            (goals>=2 and key_match) or (e['kind'] in ('equaliser','lead') and e['outcome']=='goal' and goals>=1 and not_lost)
            for e in events) or (key_match and goals>=2)
        self.coach_state=state


PORTRAITS=tuple(f'assets/coaches/coach_{i:02d}.png' for i in range(1,11))


def clean_appearance(raw):
    if (isinstance(raw,dict) and isinstance(raw.get('club'),str) and len(raw['club'])<=64
            and (not raw['club'] or raw['club'].isprintable()) and number(raw.get('portrait'),9)):
        return {k:raw[k] for k in ('club','portrait')}
    return dict(club='',portrait=0)


def appearance_for(uid,previous):
    """Keep the current coach stable; a different club cannot reuse their face."""
    previous=clean_appearance(previous)
    if uid==previous['club']:return previous
    index=int(hashlib.sha256(('scorer-coach-face-v1:'+uid).encode()).hexdigest()[:8],16)%len(PORTRAITS)
    if previous['club'] and index==previous['portrait']:index=(index+1)%len(PORTRAITS)
    return dict(club=uid,portrait=index)

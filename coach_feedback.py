"""Deterministic varied feedback: no gameplay RNG, specific events take priority."""
HAT_TRICK=(
 'A hat-trick! Outstanding finishing. You deserve the applause, and the whole squad shares this moment.',
 'Three goals. Well done, but keep your feet on the ground. Your next performance matters just as much.',
 'A hat-trick is an excellent achievement. Enjoy it, thank your teammates and keep preparing carefully.')
TEAM={
 'win':('We earned that win together.','Our movement and discipline made the difference.','We took our chances and protected the result.','The result rewards the work of the whole squad.','We showed patience and found a way to win.','That was a good response from the team.'),
 'loss':('We have to respond together after that defeat.','The result hurt, but we must review it honestly.','We gave the opposition too much control.','We need a stronger collective response next time.','We must turn our chances into a better result.','Our next performance starts with our preparation.'),
 'draw':('There were positives in that draw.','We earned a point, but there was more available.','We need more composure when the game is level.','We stayed competitive until the final whistle.','We can build on the work behind that point.','Small improvements could turn that draw into a win.'),
 'new':('A new week starts with a clear plan.','We have to earn our place through our work.','I want a committed effort from the whole squad.','Preparation gives us the best chance of a result.','Our standards start here in the dressing room.','Everyone has a role in what we achieve next.')}
STYLE=(('Trust each other and play with confidence.','Encourage your teammates and keep moving for them.','Bring that belief into the next match.','I want you to enjoy playing together.'),('Stay disciplined and keep your focus.','Do the simple things properly every time.','Keep your feet on the ground and meet our standards.','Concentration has to last until the final whistle.'),('Review the details and prepare consistently.','Balance your attacking movement with the needs of the team.','Take the lessons into our next performance.','Keep communicating and make good decisions together.'))
INDIVIDUAL={
 'drought':('Your movement can create the next chance.','Stay composed when the opportunity arrives.','Keep finding space rather than forcing the finish.','Review your timing and the quality of your first touch.','A scoring drought needs patience and purposeful work.','Make the next decision calmly, one chance at a time.'),
 'positive':('Your finishing helped the team.','You made a valuable contribution in front of goal.','Your movement was rewarded with a goal.','You gave the opposition something to worry about.','Your contribution mattered to the result.','You found the right moment to make an impact.'),
 'routine':('Keep making runs that give your teammates an option.','Your work away from the ball still matters.','I want purposeful movement and calm decisions.','Stay available for the pass and read the space.','Be ready to contribute when your chance arrives.','Make your next action useful to the team.')}
TEAM={key:values[:3] for key,values in TEAM.items()}
STYLE=tuple(values[:3] for values in STYLE)
INDIVIDUAL={key:values[:3] for key,values in INDIVIDUAL.items()}
def feedback(c,team,outcome='new'):
 from coach import style_for
 state=c._current_coach_state();style=style_for(c.club.uid if c.club else '')
 n=c.week*7+state['games']*4+c.season
 if team:return TEAM[outcome][n%3]+'\n'+STYLE[style][(n//3)%3]
 if state['recent'] and state['recent'][-1]>=3:return HAT_TRICK[style]
 meeting=c.coach_conversation()
 if meeting['kind'] in ('decisive','key_match','form'):
  from coach import FEEDBACK
  choices=FEEDBACK[meeting['kind']][style]
  return choices[n%len(choices)]+'\n'+STYLE[style][(n//3+1)%3]
 kind='drought' if state['drought']>=5 else 'positive' if state['recent'] and state['recent'][-1]>0 else 'routine'
 return INDIVIDUAL[kind][n%3]+'\n'+STYLE[style][(n//3+1)%3]

HAT_TRICK_LIVE=('Outstanding finishing!','Keep your feet on the ground.','Well done. Stay focused.')
def translate(loc,text):return ' '.join(loc.tr(part) for part in text.split('\n'))

"""Build and validate the research-only domestic format catalogue; no save writes.

Source identity discovery never implies a reviewed competition format. Runtime
profiles are deliberately separate until the phase engine supports each model.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from career import WORLD_COUNTRIES
DATA=ROOT/'docs/data/domestic-formats'


def validate_definition(definition,sources):
    errors=[];name=definition.get('league','?')
    def fail(message):errors.append(name+': '+message)
    n=definition.get('teams')
    if type(n)is not int or not 2<=n<=128:fail('invalid team count');return errors
    if definition.get('tier') not in (1,2):fail('only tiers1/2 belong in this catalogue')
    if definition.get('runtime_status')!='not_integrated':fail('research data must not claim runtime integration')
    refs=definition.get('source_ids',[])
    if not refs or any(ref not in sources for ref in refs):fail('missing pinned source')
    if not isinstance(definition.get('season'),str) or not re.fullmatch(r'20\d\d(?:–\d\d)?',definition['season']):fail('season must be explicit')
    phases=definition.get('phases',[]);seen=set();games={}
    for phase in phases:
        key=phase.get('id')
        if not isinstance(key,str) or key in seen:fail('phase IDs must be unique');continue
        seen.add(key);kind=phase.get('kind')
        if kind in ('round_robin','split_round_robin','qualified_round_robin'):
            sizes=phase.get('group_sizes',[]);legs=phase.get('legs')
            expected=phase.get('participants') if kind=='qualified_round_robin' else n
            if type(expected)is not int or not 2<=expected<=n or not sizes or any(type(s)is not int or s<2 for s in sizes) or sum(sizes)!=expected:fail(key+' groups do not cover the league');continue
            if kind=='qualified_round_robin' and not phase.get('selection'):fail(key+' qualified groups need an explicit selection')
            legs_list=legs if isinstance(legs,list) else [legs]*len(sizes)
            if len(legs_list)!=len(sizes) or any(type(value)is not int or not 1<=value<=4 for value in legs_list):fail(key+' invalid number of legs');continue
            points=phase.get('points');point_rules=points if isinstance(points,list) else [points]*len(sizes)
            if len(point_rules)!=len(sizes) or any(rule not in ('reset','carry','half_floor','half_ceil','unresolved') for rule in point_rules):fail(key+' unknown point carry rule')
            if kind=='split_round_robin':
                selectors=phase.get('rank_ranges',[])
                actual=[p for a,b in selectors for p in range(a,b+1)] if all(isinstance(x,list) and len(x)==2 and all(type(p)is int for p in x) for x in selectors) else []
                if sorted(actual)!=list(range(1,n+1)) or len(set(actual))!=n or [b-a+1 for a,b in selectors]!=sizes:fail(key+' split must partition ranks exactly once')
            inter=phase.get('intergroup_games',0)
            if type(inter)is not int or inter<0:fail(key+' invalid intergroup games');continue
            calculated=sorted(set((size-1)*count+inter for size,count in zip(sizes,legs_list)))
            if kind!='qualified_round_robin':games[key]=calculated
            if phase.get('games_per_club')!=calculated:fail(key+' stated match count differs from the schedule')
        elif kind=='scheduled_league':
            sizes=phase.get('group_sizes',[]);counts=phase.get('games_per_club',[])
            if not sizes or any(type(v)is not int or v<2 for v in sizes) or sum(sizes)!=n:fail(key+' scheduled groups do not cover the league')
            if len(counts)!=1 or type(counts[0])is not int or counts[0]<1 or n*counts[0]%2:fail(key+' scheduled match count cannot be conserved')
            else:games[key]=counts
            if not phase.get('opponent_rules'):fail(key+' scheduled league needs opponent rules')
        elif kind=='knockout':
            field=phase.get('field');rounds=phase.get('rounds',[])
            if type(field)is not int or not 2<=field<=n:fail(key+' invalid knockout field');continue
            remaining=field
            for tie in rounds:
                byes=tie.get('byes',0);ties=tie.get('ties')
                if type(ties)is not int or type(byes)is not int or ties<1 or byes<0 or ties*2+byes!=remaining:fail(key+' knockout field is not conserved');break
                if (tie.get('legs') not in (1,2) and not (tie.get('format')=='best_of' and tie.get('legs')==3 and tie.get('wins_required')==2)) or tie.get('decision') not in ('extra_time_penalties','penalties','regular_season_rank','extra_time_then_rank','conditional','unresolved'):fail(key+' invalid tie rules')
                if tie.get('format')=='best_of' and (tie.get('legs')!=3 or tie.get('wins_required')!=2):fail(key+' best-of-three needs two match wins and up to three games')
                remaining=ties+byes
            if remaining!=phase.get('qualifiers',1):fail(key+' knockout does not produce its declared qualifiers')
        elif kind=='bracket_graph':
            seeds=phase.get('seeds',[]);available={'seed:'+seed for seed in seeds};match_ids=set()
            if len(seeds)!=len(set(seeds)) or not 2<=len(seeds)<=n:fail(key+' invalid graph seeds')
            for match in phase.get('matches',[]):
                mid=match.get('id');inputs=match.get('inputs',[])
                if not isinstance(mid,str) or mid in match_ids:fail(key+' graph match IDs must be unique');continue
                if len(inputs)!=2 or len(set(inputs))!=2 or any(i not in available for i in inputs):fail(key+' graph has missing, repeated or forward inputs')
                if match.get('legs') not in (1,2) or match.get('decision') not in ('extra_time_penalties','penalties','regular_season_rank','extra_time_then_rank','conditional','unresolved'):fail(key+' invalid graph tie rules')
                match_ids.add(mid);available.update(('winner:'+mid,'loser:'+mid))
            outputs=phase.get('outputs',{})
            if not outputs or any(not refs or any(ref not in available for ref in refs) for refs in outputs.values()):fail(key+' graph outputs must reference resolved matches')
        elif kind=='pending_review':
            if not phase.get('topics') or not phase.get('reason'):fail(key+' pending review needs topics and a reason')
        elif kind=='external_playoff':
            if not phase.get('entrants') or not phase.get('purpose'):fail(key+' external playoff needs entrants and purpose')
        else:fail(key+' unsupported phase kind')
    if not phases:fail('no structural definition')
    if any(p.get('points')=='unresolved' or (isinstance(p.get('points'),list) and 'unresolved' in p['points']) for p in phases) and definition.get('definition_status')!='partially_defined':fail('unresolved point carry requires a partial definition')
    regular=definition.get('regular_games_per_club')
    if regular is not None and any(p.get('kind')=='qualified_round_robin' for p in phases):fail('qualified schedules require path-specific totals, not a universal season total')
    if regular is not None:
        sums={0}
        for values in games.values():sums={a+b for a in sums for b in values}
        if regular!=sorted(sums):fail('season regular-game totals do not match phase totals')
    if definition.get('definition_status') not in ('structure_reviewed','partially_defined'):fail('invalid review status')
    if not isinstance(definition.get('unresolved'),list):fail('unresolved rules must be explicit')
    if definition.get('country') not in WORLD_COUNTRIES:fail('unknown game country')
    return errors


def build():
    index=json.loads((DATA/'source-index.json').read_text());review=json.loads((DATA/'reviewed.json').read_text())
    sources={row['id']:row for row in index['sources']};titles={row['title']:row for row in sources.values()};definitions=review['definitions'];errors=[]
    for definition in definitions:
        errors+=validate_definition(definition,sources)
    if errors:raise ValueError('\n'.join(errors))
    ids=[d['id'] for d in definitions]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate league definition')
    for country,absence in review.get('no_domestic_league',{}).items():
        if country not in WORLD_COUNTRIES or not absence.get('reason') or not absence.get('source_ids') or any(ref not in sources for ref in absence['source_ids']):raise ValueError('Unsourced absence claim')
        if any(d['country']==country for d in definitions):raise ValueError('A country with no domestic league cannot also define leagues')
    for country, tiers in review.get('no_competition_at_tier',{}).items():
        for tier, absence in tiers.items():
            if country not in WORLD_COUNTRIES or tier not in ('1','2') or not absence.get('reason') or not absence.get('source_ids') or any(ref not in sources for ref in absence['source_ids']):raise ValueError('Unsourced tier absence claim')
            if any(d['country']==country and d['tier']==int(tier) for d in definitions):raise ValueError('An absent tier cannot also define leagues')
    result=[]
    for country in WORLD_COUNTRIES:
        rows=[];absence=review.get('no_domestic_league',{}).get(country)
        for tier in (1,2):
            tier_absence=review.get('no_competition_at_tier',{}).get(country,{}).get(str(tier))
            defined=[copy.deepcopy(d) for d in definitions if d['country']==country and d['tier']==tier]
            candidates=[s['id'] for s in sources.values() if s['kind']=='league_article' and not s['excluded_from_current_identities'] and s['tier_candidate']==tier and country in s['countries']]
            if country=='Canada':candidates=[sid for sid in candidates if sources[sid]['title']!='Major League Soccer']
            rows.append(dict(tier=tier,definitions=defined,source_candidates=sorted(candidates),status=('partially_defined' if any(d['definition_status']=='partially_defined' for d in defined) else 'structure_reviewed') if defined else 'not_applicable' if absence or tier_absence else 'needs_review',absence=tier_absence,runtime_status='unchanged'))
        result.append(dict(country=country,domestic_league='absent' if absence else 'present' if any(d['country']==country and d['tier']==1 for d in definitions) else 'under_review',absence=absence,divisions=rows,full_country_model_implemented=False))
    return dict(schema=1,reviewed_on=review['reviewed_on'],purpose='Research definitions for real first/second-tier formats; not runtime fallback rules.',country_count=len(result),division_definitions=len(definitions),countries_with_definitions=len({d['country'] for d in definitions}),structures_reviewed=sum(d['definition_status']=='structure_reviewed' for d in definitions),partially_defined=sum(d['definition_status']=='partially_defined' for d in definitions),countries=result)


def report(catalogue):
    lines=['# Domestic format definitions','',f"Reviewed on {catalogue['reviewed_on']}. {catalogue['division_definitions']} records in {catalogue['countries_with_definitions']} countries: {catalogue['structures_reviewed']} regular structures reviewed and {catalogue['partially_defined']} partial definitions. All {catalogue['country_count']} game countries are indexed.",'','These definitions do not alter the released APK or saved careers. A sourced identity is not a reviewed format; a reviewed structure is not a full implemented country model.','', '| Country | Tier | Competition / season | Teams | Phases | Regular games | Status |','|---|---:|---|---:|---|---|---|']
    pending=[]
    for row in catalogue['countries']:
        if row['domestic_league']=='absent':lines.append('| '+row['country']+' | — | No domestic league; clubs use the Swiss pyramid | — | — | — | Confirmed exception |');continue
        for division in row['divisions']:
            if division['status']=='not_applicable':
                lines.append('| '+row['country']+' | '+str(division['tier'])+' | No separate senior competition at this tier | — | — | — | Sourced exception |');continue
            if not division['definitions']:pending.append(row['country']+' / '+str(division['tier']));continue
            for d in division['definitions']:
                phases=' → '.join(p['kind'] for p in d['phases']);games=', '.join(map(str,d.get('regular_games_per_club',[]))) or 'phase dependent'
                lines.append(f"| {row['country']} | {division['tier']} | {d['league']} / {d['season']} | {d['teams']} | {phases} | {games} | {d['definition_status']} |")
    lines+=['','## Outstanding division reviews','',', '.join(pending), '', 'Exact tie-breakers, club licensing/reserve eligibility and season-specific changes remain recorded in each definition’s unresolved list. No unknown league is assigned a generic 12-team or three-up rule.','']
    return '\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();catalogue=build();content=json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n';markdown=report(catalogue)
    if args.check:
        assert (DATA/'catalogue.json').read_text()==content,'Catalogue is stale'
        assert (ROOT/'docs/regulations/DOMESTIC_FORMAT_DEFINITIONS.md').read_text()==markdown,'Report is stale'
    else:
        (DATA/'catalogue.json').write_text(content);(ROOT/'docs/regulations/DOMESTIC_FORMAT_DEFINITIONS.md').write_text(markdown)
    print(f"Validated {catalogue['division_definitions']} definitions across {catalogue['countries_with_definitions']} countries; {catalogue['country_count']} countries indexed")

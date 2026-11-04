"""Select executable, sourced regular/split structures; never certify access rules."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build():
    review=json.loads((ROOT/'docs/data/domestic-formats/reviewed.json').read_text());out={}
    by={}
    for d in review['definitions']:by.setdefault((d['country'],d['tier']),[]).append(d)
    for country in sorted({c for c,t in by}):
        pair={}
        for tier in (1,2):
            rows=by.get((country,tier),[])
            if len(rows)!=1:break
            d=rows[0];phases=[p for p in d['phases'] if p['kind'] in ('round_robin','split_round_robin')]
            if (d['definition_status']!='structure_reviewed' or not 1<=len(phases)<=2 or phases[0]['kind']!='round_robin' or phases[0]['group_sizes']!=[d['teams']] or d['teams']%2 or not 6<=d['teams']<=24):break
            if any(any(n%2 for n in p['group_sizes']) or p['points'] not in ('reset','carry','half_floor','half_ceil') for p in phases):break
            if len(phases)==2 and phases[1]['kind']!='split_round_robin' and phases[1]['group_sizes']!=[d['teams']]:break
            if any(p['kind'] in ('bracket_graph','qualified_round_robin','scheduled_league') or 'championship' in p['id'] or p['id'] in ('format_review','season_resolution') for p in d['phases']):break
            pair[str(tier)]={'teams':d['teams'],'phases':phases,'definition_id':d['id'],'source_ids':d['source_ids'],'season':d['season'],'full_country_rules':False}
        if len(pair)==2:out[country]=pair
    return {'version':1,'scope':'Regular league capacities and supported splits only; access models remain separately configured. Existing saves keep their original layout.','countries':out}
if __name__=='__main__':
    data=build();(ROOT/'assets/data/domestic_formats.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(len(data['countries']),'countries')

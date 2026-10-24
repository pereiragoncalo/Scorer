"""Compute real-world aggregates from local openfootball and FootballData exports.

No raw names or downloaded match data are embedded in the app. See
REALISM_0.6.17.md for immutable source links and revisions.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re


def analyse(openfootball_dir, shot_dir):
    result = {'results': [], 'shots': []}
    for season in ('2022-23', '2023-24', '2024-25'):
        for division, expected in (('1-premierleague', 380), ('4-league2', 552)):
            path = Path(openfootball_dir) / season / (division + '.txt')
            scores = []
            for line in path.read_text().splitlines():
                if line.startswith(('#', '=')):
                    continue
                match = re.search(r'\s(\d+)-(\d+)(?:\s|$)', line)
                if match:
                    scores.append(tuple(map(int, match.groups())))
            if len(scores) != expected:
                raise ValueError(f'{path}: expected {expected} complete fixtures, found {len(scores)}')
            result['results'].append(dict(season=season, division=division,
                matches=len(scores), home_goals=sum(a for a,b in scores), away_goals=sum(b for a,b in scores),
                draws=sum(a==b for a,b in scores), nil_nil=sum(a==b==0 for a,b in scores),
                five_plus=sum(a+b>=5 for a,b in scores), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    for season in ('2017-2018', '2018-2019'):
        for division, expected in (('Premier', 380), ('League-2', 552)):
            path = Path(shot_dir) / f'{season}-{division}.csv'
            with path.open(encoding='utf-8-sig') as stream:
                rows = [r for r in csv.DictReader(stream) if r.get('FTHG','').isdigit()]
            if len(rows) != expected:
                raise ValueError(f'{path}: incomplete season')
            result['shots'].append(dict(season=season, division=division, matches=len(rows),
                goals=sum(int(r['FTHG'])+int(r['FTAG']) for r in rows),
                shots=sum(int(r['HS'])+int(r['AS']) for r in rows),
                on_target=sum(int(r['HST'])+int(r['AST']) for r in rows),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--openfootball-dir', required=True)
    parser.add_argument('--shot-dir', required=True)
    args = parser.parse_args()
    print(json.dumps(analyse(args.openfootball_dir, args.shot_dir), indent=2, sort_keys=True))

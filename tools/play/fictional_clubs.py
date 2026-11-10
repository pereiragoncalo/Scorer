"""Build a fictional-only shipping catalogue; reference data never ships as identity."""
import json
from pathlib import Path

SOLID_SHIRTS = {'Benfica','Sporting Braga','Braga','Liverpool','Arsenal','Chelsea','Manchester City','Manchester United','Everton','Tottenham Hotspur','Real Madrid','Sevilla','Valencia','Villarreal','Roma','Napoli','Fiorentina','Lazio','Bayern Munich','Bayern München','Borussia Dortmund','Hamburger SV','Paris Saint-Germain','Lyon','Marseille','Bordeaux','Cruzeiro','Santos','Corinthians','Independiente'}


def shipping_data(directory):
    directory = Path(directory)
    def read(name):
        path = directory / (name + '.json')
        return json.loads(path.read_text(encoding='utf8')) if path.exists() else None
    world = read('world_clubs')
    if not world or world.get('version') != 1 or not isinstance(world.get('clubs'), dict):
        raise ValueError('Missing canonical fictional identities')
    names = {}
    for uid, row in world['clubs'].items():
        name = row.get('canonical')
        if not isinstance(name, str) or not 2 <= len(name) <= 56:
            raise ValueError('Missing canonical fictional name: ' + uid)
        names[uid] = name
    result = {'world_clubs': {'version': 1, 'identity': 'fictional', 'clubs': {
        uid: dict(canonical=name, name=name, **({'colours': world['clubs'][uid]['colours']} if 'colours' in world['clubs'][uid] else {}))
        for uid, name in names.items()}}}
    profiles = read('club_profiles')
    if profiles is not None:
        result['club_profiles'] = {'version': 1, 'identity': 'fictional', 'clubs': {}}
        for uid, row in profiles['clubs'].items():
            if uid not in names: continue  # Obsolete reference-only UID, no shipping club.
            # Retain venue geometry and kit pattern, never transfer real history to fiction.
            result['club_profiles']['clubs'][uid] = {
                'club': names[uid], 'capacity': row.get('capacity'),
                'shirt_pattern': row.get('shirt_pattern', 'plain' if row.get('club') in SOLID_SHIRTS else 'striped')}
    status = read('league_status')
    if status is not None:
        status['clubs'] = {uid: row for uid, row in status['clubs'].items() if uid in names}
        for uid, row in status['clubs'].items():
            row['name'] = names[uid]
            for season in row.get('seasons', []):
                season.pop('name', None)
        result['league_status'] = status
    return result


def stage_fictional_clubs(directory):
    for name, data in shipping_data(directory).items():
        (Path(directory)/(name+'.json')).write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf8')


def verify_fictional_data(name, raw, reference_directory):
    expected = shipping_data(reference_directory)[name]
    if json.loads(raw) != expected:
        raise ValueError('Non-fictional or unreviewed club data in ' + name)
    if name == 'world_clubs' and any(row['name'] != row['canonical'] for row in json.loads(raw)['clubs'].values()):
        raise ValueError('Real-name presentation overlay must not ship')
    return len(expected.get('clubs', {}))

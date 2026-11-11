"""Public compatibility policy shared by client and owner-hosted endpoint."""
import json
from pathlib import Path

PACKAGE='com.clemir.scorerworld'
STORE_URL='https://play.google.com/store/apps/details?id='+PACKAGE

def validate(data):
    if not isinstance(data,dict) or set(data)!={'schema','package','minimum_version_code','latest_version_code','latest_version_name'}:
        raise ValueError('Invalid version policy schema')
    if type(data['schema'])is not int or data['schema']!=1 or data['package']!=PACKAGE:raise ValueError('Wrong version policy identity')
    for key in ('minimum_version_code','latest_version_code'):
        if type(data[key])is not int or not 0<=data[key]<=2100000000:raise ValueError('Invalid version code')
    if data['minimum_version_code']>data['latest_version_code']:raise ValueError('Minimum exceeds latest version')
    value=data['latest_version_name']
    if not isinstance(value,str) or not 1<=len(value)<=32 or any(not c.isprintable() or c in '<>[]' for c in value):raise ValueError('Invalid version name')
    return dict(data)

def read(path):
    raw=Path(path).read_bytes()
    if len(raw)>4096:raise ValueError('Version policy too large')
    return validate(json.loads(raw))

def blocked(policy,installed):return policy is not None and installed<policy['minimum_version_code']

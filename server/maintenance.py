"""Aggregate-only backups; never preserve names/tokens/reports for restoration."""
from pathlib import Path
import argparse,os,sqlite3,time
from server.moderation import prune
from server import privacy_cases
PRIVATE_TABLES=('leaderboard','season_records','division_records','moderation','reports','banned_publishers')
def backup(database,target):
    target=Path(target)
    if target.exists():raise ValueError('Use a fresh backup path')
    target.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(target,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    try:
        with sqlite3.connect(database) as src,sqlite3.connect(target) as dst:
            dst.execute('CREATE TABLE totals(day TEXT NOT NULL,event TEXT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(day,event))')
            dst.executemany('INSERT INTO totals VALUES(?,?,?)',src.execute('SELECT day,event,count FROM totals'))

    except Exception:target.unlink(missing_ok=True);raise

def maintain(database):
    database=Path(database)
    with sqlite3.connect(database) as db:privacy_cases.initialize(db);prune(db);privacy_cases.prune(db)
    old=database.parent/'online.backup.sqlite'
    # Older installer backups can contain names: remove once on migration.
    old.unlink(missing_ok=True)
    folder=database.parent/'aggregate-backups';folder.mkdir(exist_ok=True,mode=0o700)
    for path in folder.glob('*.sqlite'):
        if time.time()-path.stat().st_mtime>=7*86400:path.unlink()
    target=folder/(time.strftime('%Y%m%d-%H%M%S')+'.sqlite')
    backup(database,target)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,required=True);a=p.parse_args();maintain(a.db)

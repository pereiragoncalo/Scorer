"""Local family controls; no age, PIN or birth date is transmitted."""
from datetime import date
import hashlib,hmac,json,os,secrets,tempfile,time
from pathlib import Path

NOTICE_VERSION=2
TERMS_VERSION=1
TERMS_TEXT=('Use a nickname, never a real full name, contact details or school. Do not publish abuse, hate, sexual content, threats, impersonation or spam. Names and teams are public only after review. Report or block unsafe entries. Moderators may remove records and suspend publishing. Scores are self-reported. You can stop sharing and remove your records at any time.')
NOTICE_TEXT=('Scorer World sends usage counters to stats.clemir.com: app openings and closes, careers created and loaded, training, matches, goals and save/load failures. No names, career files or device IDs are included. Pending counters expire after 7 days; server daily totals after 90 days. Cloudflare processes connection data, including IP addresses. Public record sharing is separate and optional. I AGREE continues with automatic usage reporting; I DO NOT AGREE closes the game.')

def atomic_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(dir=path.parent,prefix='.scorer-local-')
    try:
        with os.fdopen(fd,'w',encoding='utf8') as f:json.dump(data,f,ensure_ascii=False);f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:Path(name).unlink(missing_ok=True)

class FamilyControls:
    def __init__(self,directory,clock=time.time):
        self.path=Path(directory)/'scorer_safety.json';self.clock=clock
        self.notice=0;self.terms=0;self.social=False;self.salt='';self.pin_hash='';self.failures=0;self.locked_until=0
        try:
            if self.path.stat().st_size>16384:return
            d=json.loads(self.path.read_text());self.notice=int(d.get('notice',0));self.terms=int(d.get('terms',0))
            salt=d.get('salt','');digest=d.get('pin_hash','')
            if len(salt)==32 and len(digest)==64:
                bytes.fromhex(salt);bytes.fromhex(digest);self.salt=salt;self.pin_hash=digest;self.social=d.get('social') is True
            self.failures=max(0,min(100,int(d.get('failures',0))));self.locked_until=float(d.get('locked_until',0))
        except (OSError,ValueError,TypeError,AttributeError):pass
    @property
    def notice_seen(self):return self.notice==NOTICE_VERSION
    @property
    def terms_accepted(self):return self.terms==TERMS_VERSION
    @property
    def configured(self):return bool(self.salt and self.pin_hash)
    def save(self):
        atomic_json(self.path,{k:getattr(self,k) for k in ('notice','terms','social','salt','pin_hash','failures','locked_until')})
    def acknowledge(self):self.notice=NOTICE_VERSION;self.save()
    def accept_terms(self):self.terms=TERMS_VERSION;self.save()
    def configure(self,birth_date,pin,confirmation):
        """Self-declared adult action, not verified identity or legal parental consent."""
        try:
            born=date.fromisoformat(birth_date);today=date.today()
            age=today.year-born.year-((today.month,today.day)<(born.month,born.day))
        except (ValueError,TypeError):return False
        if self.configured or not 18<=age<=120 or not isinstance(pin,str) or not pin.isascii() or not pin.isdigit() or not 6<=len(pin)<=12 or pin!=confirmation:return False
        self.salt=secrets.token_hex(16);self.pin_hash=hashlib.pbkdf2_hmac('sha256',pin.encode(),bytes.fromhex(self.salt),200000).hex();self.social=True;self.save();return True
    def unlock(self,pin):
        if not self.configured or self.clock()<self.locked_until or not isinstance(pin,str) or len(pin)>12:return False
        digest=hashlib.pbkdf2_hmac('sha256',pin.encode(),bytes.fromhex(self.salt),200000).hex()
        ok=hmac.compare_digest(digest,self.pin_hash)
        if ok:self.failures=0;self.locked_until=0
        else:
            self.failures+=1
            if self.failures>=3:self.locked_until=self.clock()+300
        self.save();return ok
    def set_social(self,enabled,pin):
        if not self.unlock(pin):return False
        self.social=bool(enabled);self.save();return True

"""Inspect trusted compiled metadata with the same Python version as the APK/AAB."""
import io,marshal,sys,tarfile,zipfile
artifact,product,channel=sys.argv[1:]
with zipfile.ZipFile(artifact) as z:
    name=next(n for n in z.namelist() if n.endswith('assets/private.tar'))
    with tarfile.open(fileobj=io.BytesIO(z.read(name))) as tar:
        def module(name):
            m=next(m for m in tar if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
            return marshal.loads(tar.extractfile(m).read()[16:])
        e={};exec(module('edition'),e);r={};exec(module('release_settings'),r)
        assert e['WORLD_BUILD'] is (product=='world') and e['WORLD_PREVIEW'] is False
        assert r['CHANNEL']==channel
        assert r['DEVELOPER_NAME']=='Gonçalo Pereira' and r['SUPPORT_EMAIL']=='goncalo@clemir.com'
        assert r['PRIVACY_URL']=='https://stats.clemir.com/privacy'
        assert r['WORLD_LISTING_READY'] is False
        names=tar.getnames()
        for required in ('online_safety','career_transfer','career_documents','privacy_requests','defensive_difficulty'):
            assert any(n.endswith('/'+required+'.pyc') or n==required+'.pyc' for n in names)
        code=module('anonymous_stats');assert 'APP_STATS_MANDATORY' in code.co_names
print('Compiled edition/channel/public metadata/safety/transfer modules verified:',product,channel)

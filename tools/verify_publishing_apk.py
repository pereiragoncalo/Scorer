import io,marshal,sys,tarfile,tempfile,zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
    with tarfile.open(fileobj=io.BytesIO(z.read('assets/private.tar'))) as tar:
        def code(name):
            member=next(m for m in tar if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
            return marshal.loads(tar.extractfile(member).read()[16:])
        stats={};exec(code('anonymous_stats'),stats);safety={};exec(code('online_safety'),safety)
        assert stats['APP_STATS_MANDATORY'] is True
        with tempfile.TemporaryDirectory() as t:
            u=stats['create_statistics'](False,t,endpoint='');assert u.enabled and u.mandatory and not u.delivery_ready
            u.begin_session();assert u.counts=={'sessions':1};assert not u.set_enabled(False);assert not u.flush_async()
            f=safety['FamilyControls'](t);assert not f.social and not f.configured
            assert f.configure('1980-01-01','123456','123456');assert f.social and f.unlock('123456')
            f.acknowledge();assert stats['create_statistics'](False,t,endpoint='').delivery_ready
        game=next(c for c in code('main').co_consts if hasattr(c,'co_name') and c.co_name=='StrikerGame')
        action=next(c for c in game.co_consts if hasattr(c,'co_name') and c.co_name=='_activate_ui')
        assert 'notice_continue' in action.co_consts and 'adult_disable' in action.co_consts and 'career_import' in action.co_consts
        transfer=code('career_transfer');assert 'validated_import' in transfer.co_names
    dex=b''.join(z.read(n) for n in z.namelist() if n.endswith('.dex'))
    assert b'chooseCareerImport' in dex and b'chooseCareerExport' in dex and b'readCareer' in dex
print('Actual APK: mandatory usage gated by notice, no disable, adult controls, career transfer and SAF bridge verified; no network sent')

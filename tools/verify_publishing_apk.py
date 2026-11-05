import io,marshal,sys,tarfile,tempfile,zipfile,types
with zipfile.ZipFile(sys.argv[1]) as z:
    with tarfile.open(fileobj=io.BytesIO(z.read('assets/private.tar'))) as tar:
        def code(name):
            member=next(m for m in tar if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
            return marshal.loads(tar.extractfile(member).read()[16:])
        safety_module=types.ModuleType('online_safety');sys.modules['online_safety']=safety_module
        safety=safety_module.__dict__;exec(code('online_safety'),safety)
        stats={};exec(code('anonymous_stats'),stats)
        assert stats['APP_STATS_MANDATORY'] is True
        with tempfile.TemporaryDirectory() as t:
            u=stats['create_statistics'](False,t,endpoint='');assert u.enabled and u.mandatory and not u.delivery_ready
            u.begin_session();assert u.counts=={'sessions':1};assert not u.set_enabled(False);assert not u.flush_async()
            f=safety['FamilyControls'](t);assert not f.social and not f.configured
            assert f.configure('1980-01-01','123456','123456');assert f.social and f.unlock('123456')
            f.acknowledge();assert not stats['create_statistics'](False,t,endpoint='').delivery_ready
            u.reject_notice();assert not u.delivery_ready and not u.counts and not u.flush_async()
        game=next(c for c in code('main').co_consts if hasattr(c,'co_name') and c.co_name=='StrikerGame')
        action=next(c for c in game.co_consts if hasattr(c,'co_name') and c.co_name=='_activate_ui')
        def flatten(items):
            for item in items:
                if isinstance(item,str):yield item
                elif isinstance(item,tuple):yield from flatten(item)
        constants=set(flatten(action.co_consts))
        assert {'notice_continue','adult_disable','career_import'}<=constants
        notice=next(c for c in code('menu_ui').co_consts if hasattr(c,'co_name') and c.co_name=='LaunchNotice')
        constructor=next(c for c in notice.co_consts if hasattr(c,'co_name') and c.co_name=='__init__')
        assert {'I AGREE','I DO NOT AGREE'}<=set(flatten(constructor.co_consts))
        import json
        pt_member=next(m for m in tar if m.name.endswith('assets/i18n/pt.json'))
        pt=json.loads(tar.extractfile(pt_member).read())
        assert pt['I AGREE']=='CONCORDO' and pt['I DO NOT AGREE']=='NÃO CONCORDO'
        app=next(c for c in code('main').co_consts if hasattr(c,'co_name') and c.co_name=='StrikerApp')
        flush=next(c for c in app.co_consts if hasattr(c,'co_name') and c.co_name=='_flush_usage')
        assert 'pending_withdrawal' in flush.co_names and 'sync' in flush.co_names
        transfer=code('career_transfer');assert 'validated_import' in transfer.co_names
        help_strings=list(flatten(code('world_ui').co_consts))
        assert any('three training shots before every match' in text for text in help_strings)
        assert not any('Usage counts are automatic, as explained in Privacy' in text for text in help_strings)
        assert not any('Free uses ads when available' in text for text in help_strings)
    dex=b''.join(z.read(n) for n in z.namelist() if n.endswith('.dex'))
    assert b'chooseCareerImport' in dex and b'chooseCareerExport' in dex and b'readCareer' in dex
print('Actual APK: mandatory usage gated by notice, no disable, adult controls, career transfer and SAF bridge verified; no network sent')

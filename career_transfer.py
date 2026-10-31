"""Explicit local edition-bound career transfer; never transfers credentials."""
import copy,json
MAX_BYTES=8*1024*1024

def export_career(career):
    if not career.club_name or career.save() is False:raise ValueError('No saved career to export.')
    data=json.loads(career.save_path.read_text(encoding='utf8'))
    # Do not export a historical career of another edition hidden in the envelope.
    data['locked_world_career']=None
    text=json.dumps({'format':'scorer-career','version':1,'edition':career.product_mode,'save':data},ensure_ascii=False)
    if len(text.encode('utf8'))>MAX_BYTES:raise ValueError('Career file is too large.')
    return text

def validated_import(career,text):
    if not isinstance(text,str) or len(text.encode('utf8'))>MAX_BYTES:raise ValueError('Invalid career document.')
    try:
        data=json.loads(text)
        if not isinstance(data,dict) or set(data)!={'format','version','edition','save'} or data['format']!='scorer-career' or type(data['version']) is not int or data['version']!=1 or data['edition']!=career.product_mode:raise ValueError()
        save=data['save']
        if not isinstance(save,dict) or not isinstance(save.get('career'),dict) or save['career'].get('edition')!=career.product_mode or save.get('locked_world_career') is not None:raise ValueError()
        # Bound nesting and containers before the existing semantic load validator.
        stack=[(save,0)];nodes=0
        while stack:
            item,depth=stack.pop();nodes+=1
            if depth>40 or nodes>400000:raise ValueError()
            if isinstance(item,dict):stack.extend((v,depth+1) for v in item.values())
            elif isinstance(item,list):stack.extend((v,depth+1) for v in item)
        candidate=object.__new__(type(career));candidate.__dict__={k:(v if k=='entitlements' else copy.deepcopy(v)) for k,v in career.__dict__.items()}
        if not candidate._load_saved_state(json.dumps(save,ensure_ascii=False)) or not candidate.club_name:raise ValueError()
        return candidate
    except (ValueError,TypeError,KeyError,RecursionError,OverflowError,AttributeError) as e:raise ValueError('Invalid or incompatible career document.') from e

def import_career(career,text):
    candidate=validated_import(career,text)
    if not career.backup_before_new_game():raise OSError('Previous career backup failed.')
    if candidate.save() is False:raise OSError('Could not save imported career.')
    career.__dict__.update(candidate.__dict__)

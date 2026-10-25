import json
import os
from pathlib import Path
import string
import tempfile
import unittest
from unittest.mock import patch
from localization import Localizer, LANGUAGES, catalogue, country_catalogue, language_for_tag, CJK_FONTS
from device_locale import language_from_locale


class LocalizationTests(unittest.TestCase):
    def test_free_always_english_and_never_reads_or_writes_language_preferences(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'scorer_language.json'
            path.write_text('{"version":1,"language":"ja","WORLD_BUILD":true}')
            before=path.read_bytes()
            with patch.object(Path,'read_text',side_effect=AssertionError('Free must not read preferences')):
                loc=Localizer(False,'pt-PT',temp)
                self.assertEqual(loc.language,'en')
                self.assertEqual(loc.tr('PLAY'),'PLAY')
                self.assertFalse(loc.choose('ja'))
            self.assertEqual(path.read_bytes(),before)
            loc.refresh_system('ko-KR');self.assertEqual(loc.language,'en')

    def test_world_automatic_selection_for_all_nine_languages_and_fallback(self):
        for tag,code in [('en-US','en'),('pt-PT','pt'),('pt-BR','pt'),('es-MX','es'),('de-DE','de'),
                         ('it-IT','it'),('ko-KR','ko'),('ja-JP','ja'),('zh-Hans-CN','zh'),('zh-Hant-TW','zh'),('vi-VN','vi'),('fr-FR','en'),(None,'en')]:
            self.assertEqual(language_for_tag(tag),code)
            self.assertEqual(language_from_locale(tag),code)
            self.assertEqual(Localizer(True,tag).language,code)

    def test_preferences_persist_independently_of_career_and_restore_automatic(self):
        with tempfile.TemporaryDirectory() as temp:
            career=Path(temp)/'striker_world_career.json';career.write_text('unchanged career')
            loc=Localizer(True,'pt-PT',temp);self.assertTrue(loc.choose('de'))
            restored=Localizer(True,'ja-JP',temp);self.assertEqual(restored.language,'de')
            restored.refresh_system('ko-KR');self.assertEqual(restored.language,'de')
            self.assertTrue(restored.choose('auto'));self.assertEqual(restored.language,'ko')
            self.assertEqual(career.read_text(),'unchanged career')
            self.assertEqual(sorted(p.name for p in Path(temp).iterdir()),['scorer_language.json','striker_world_career.json'])

    def test_failed_save_keeps_previous_language_and_file(self):
        with tempfile.TemporaryDirectory() as temp:
            loc=Localizer(True,'en',temp);loc.choose('pt');before=(Path(temp)/'scorer_language.json').read_bytes()
            with patch('localization.os.replace',side_effect=OSError('full disk')):
                self.assertFalse(loc.choose('ja'))
            self.assertEqual(loc.language,'pt')
            self.assertEqual((Path(temp)/'scorer_language.json').read_bytes(),before)
            self.assertFalse(list(Path(temp).glob('.scorer-language-*')))

    def test_invalid_or_oversized_preferences_cannot_select_paths_or_change_edition(self):
        for value in ('[]','{broken','{"version":1,"language":"../../keys"}',
                      '{"version":true,"language":"ja"}', 'x'*1025):
            with tempfile.TemporaryDirectory() as temp:
                (Path(temp)/'scorer_language.json').write_text(value)
                loc=Localizer(True,'vi-VN',temp);self.assertEqual(loc.language,'vi')
                self.assertFalse(loc.choose('../../keys'))

    def test_complete_catalogues_preserve_all_placeholders(self):
        english=catalogue('en');self.assertGreaterEqual(len(english),200)
        self.assertEqual(len(LANGUAGES),9)
        fields=lambda text:sorted(f for _,f,_,_ in string.Formatter().parse(text) if f is not None)
        for lang in LANGUAGES:
            data=catalogue(lang);self.assertEqual(set(data),set(english),lang)
            for source,text in data.items():
                self.assertTrue(text.strip(),(lang,source))
                self.assertEqual(fields(text),fields(source),(lang,source))

    def test_dynamic_values_and_custom_names_are_never_retranslated(self):
        for lang in LANGUAGES:
            loc=Localizer(True,lang)
            alias='PLAY 日本語 Nguyễn'
            output=loc.tr('Contract signed with '+alias+'.')
            self.assertIn(alias,output)
            self.assertIn('17',loc.tr('Your agent found 17 offer(s).'))
            self.assertEqual(loc.tr(loc.tr('PLAY')),loc.tr('PLAY'))

    def test_country_labels_keep_all_canonical_keys_and_football_regions(self):
        from career import WORLD_COUNTRIES
        data=country_catalogue()
        for lang in LANGUAGES:self.assertEqual(set(data[lang]),set(WORLD_COUNTRIES))
        self.assertEqual(Localizer(True,'ja').country('Japan'),'日本')
        self.assertEqual(Localizer(True,'zh').country('Chinese Taipei'),'中华台北')
        self.assertEqual(Localizer(False,'ja').country('Japan'),'Japan')

    def test_ui_and_country_characters_are_present_in_bundled_fonts(self):
        from fontTools.ttLib import TTFont
        base=Path(__file__).resolve().parents[1]
        for lang in LANGUAGES:
            file=CJK_FONTS.get(lang,'Barlow-Regular.ttf')
            font=TTFont(base/'assets/fonts'/file)
            try:
                cmap=font.getBestCmap()
                texts=list(catalogue(lang).values())+list(country_catalogue()[lang].values())
                missing={c for text in texts for c in text if not c.isspace() and ord(c) not in cmap}
                self.assertFalse(missing,(lang,missing))
            finally:font.close()

    def test_world_staging_contains_only_public_translation_assets_and_free_strips_them(self):
        from tools.prepare_editions import prepare_edition
        with tempfile.TemporaryDirectory() as temp:
            world=prepare_edition('world',Path(temp)/'world')
            free=prepare_edition('free',Path(temp)/'free')
            for lang in LANGUAGES:self.assertTrue((world/'assets/i18n'/f'{lang}.json').is_file())
            for name in CJK_FONTS.values():self.assertTrue((world/'assets/fonts'/name).is_file())
            self.assertFalse((free/'assets/i18n').exists())
            self.assertFalse(list((free/'assets/fonts').glob('*Noto*')))

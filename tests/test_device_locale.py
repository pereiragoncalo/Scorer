import sys
import types
import unittest
from unittest.mock import Mock, patch

from device_locale import phone_country, phone_locale_tag, language_from_locale


class DeviceLocaleTests(unittest.TestCase):
    def native(self, config, default='en-US'):
        resources = Mock()
        resources.getSystem.return_value.getConfiguration.return_value = config
        java_locale = Mock()
        java_locale.getDefault.return_value.toLanguageTag.return_value = default
        return types.SimpleNamespace(autoclass=Mock(side_effect=lambda name:
            resources if name == 'android.content.res.Resources' else java_locale))

    def test_system_portuguese_wins_over_english_runtime_default(self):
        config = Mock()
        config.getLocales.return_value.size.return_value = 2
        config.getLocales.return_value.get.return_value.toLanguageTag.return_value = 'pt-PT'
        native = self.native(config)
        with patch.dict(sys.modules, jnius=native):
            self.assertEqual(phone_country(True), 'Portugal')
        config.getLocales.return_value.get.assert_called_once_with(0)

    def test_pre_api24_uses_configuration_locale(self):
        config = Mock()
        config.getLocales.side_effect = AttributeError('API 23')
        config.locale.toLanguageTag.return_value = 'pt-BR'
        with patch.dict(sys.modules, jnius=self.native(config)):
            self.assertEqual(phone_country(True), 'Brazil')

    def test_empty_system_locale_list_uses_legacy_configuration_locale(self):
        config = Mock()
        config.getLocales.return_value.size.return_value = 0
        config.locale.toLanguageTag.return_value = 'pt-PT'
        with patch.dict(sys.modules, jnius=self.native(config)):
            self.assertEqual(phone_country(True), 'Portugal')

    def test_java_default_is_last_android_fallback(self):
        config = Mock()
        config.getLocales.side_effect = RuntimeError('Unavailable')
        config.locale = None
        with patch.dict(sys.modules, jnius=self.native(config, 'es-MX')):
            self.assertEqual(phone_country(True), 'Mexico')

    def test_missing_native_bridge_has_safe_fallback(self):
        with patch.dict(sys.modules, jnius=None):
            self.assertEqual(phone_locale_tag(True), '')
            self.assertEqual(phone_country(True), 'England')

    def test_translation_hook_does_not_change_region_selection(self):
        for tag in ('pt-PT', 'pt_PT', 'pt-BR', 'pt'):
            self.assertEqual(language_from_locale(tag), 'pt')
        for tag in ('en-US', 'fr-FR', '', None):
            self.assertEqual(language_from_locale(tag), 'en')

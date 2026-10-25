"""Offline football-region suggestion from locale, never IP/GPS or UI translation."""
REGIONS = dict(item.split('=', 1) for item in (
    'PT=Portugal|BR=Brazil|GB=England|US=United States|ES=Spain|FR=France|DE=Germany|IT=Italy|'
    'NL=Netherlands|BE=Belgium|AT=Austria|CH=Switzerland|IE=Republic of Ireland|'
    'DK=Denmark|SE=Sweden|NO=Norway|FI=Finland|IS=Iceland|PL=Poland|CZ=Czechia|SK=Slovakia|'
    'HU=Hungary|RO=Romania|BG=Bulgaria|GR=Greece|TR=Turkey|RU=Russia|UA=Ukraine|'
    'RS=Serbia|HR=Croatia|SI=Slovenia|BA=Bosnia and Herzegovina|ME=Montenegro|'
    'AL=Albania|MK=North Macedonia|XK=Kosovo|LT=Lithuania|LV=Latvia|EE=Estonia|'
    'MT=Malta|CY=Cyprus|LU=Luxembourg|MD=Moldova|BY=Belarus|GE=Georgia|AM=Armenia|'
    'AZ=Azerbaijan|KZ=Kazakhstan|IL=Israel|AD=Andorra|SM=San Marino|LI=Liechtenstein|'
    'GI=Gibraltar|FO=Faroe Islands|AR=Argentina|UY=Uruguay|CL=Chile|CO=Colombia|'
    'PE=Peru|EC=Ecuador|BO=Bolivia|PY=Paraguay|VE=Venezuela|MX=Mexico|CA=Canada|'
    'CR=Costa Rica|PA=Panama|GT=Guatemala|HN=Honduras|SV=El Salvador|NI=Nicaragua|'
    'CU=Cuba|DO=Dominican Republic|HT=Haiti|JM=Jamaica|PR=Puerto Rico|TT=Trinidad and Tobago|'
    'GY=Guyana|SR=Suriname|BZ=Belize|BS=Bahamas|BB=Barbados|AG=Antigua and Barbuda|'
    'DM=Dominica|GD=Grenada|KN=Saint Kitts and Nevis|LC=Saint Lucia|VC=Saint Vincent and the Grenadines|'
    'AW=Aruba|CW=Curacao|BM=Bermuda|KY=Cayman Islands|VG=British Virgin Islands|'
    'VI=US Virgin Islands|AI=Anguilla|MS=Montserrat|TC=Turks and Caicos Islands|'
    'CN=China|TW=Chinese Taipei|HK=Hong Kong|MO=Macau|JP=Japan|KR=South Korea|'
    'KP=North Korea|IN=India|BD=Bangladesh|PK=Pakistan|LK=Sri Lanka|NP=Nepal|'
    'BT=Bhutan|AF=Afghanistan|IR=Iran|IQ=Iraq|SY=Syria|LB=Lebanon|JO=Jordan|PS=Palestine|'
    'SA=Saudi Arabia|AE=United Arab Emirates|QA=Qatar|BH=Bahrain|KW=Kuwait|OM=Oman|'
    'YE=Yemen|ID=Indonesia|MY=Malaysia|SG=Singapore|BN=Brunei|TH=Thailand|VN=Vietnam|KH=Cambodia|'
    'LA=Laos|MM=Myanmar|PH=Philippines|TL=Timor-Leste|MN=Mongolia|MV=Maldives|'
    'UZ=Uzbekistan|KG=Kyrgyzstan|TJ=Tajikistan|TM=Turkmenistan|GU=Guam|MP=Northern Mariana Islands|'
    'AU=Australia|NZ=New Zealand|FJ=Fiji|PG=Papua New Guinea|SB=Solomon Islands|'
    'VU=Vanuatu|NC=New Caledonia|PF=Tahiti|WS=Samoa|AS=American Samoa|TO=Tonga|CK=Cook Islands|'
    'ZA=South Africa|AO=Angola|MZ=Mozambique|CV=Cape Verde|GW=Guinea-Bissau|'
    'ST=Sao Tome and Principe|EG=Egypt|MA=Morocco|DZ=Algeria|TN=Tunisia|LY=Libya|'
    'SD=Sudan|SS=South Sudan|ET=Ethiopia|ER=Eritrea|DJ=Djibouti|SO=Somalia|'
    'KE=Kenya|UG=Uganda|TZ=Tanzania|RW=Rwanda|BI=Burundi|CD=DR Congo|CG=Congo|'
    'GA=Gabon|GQ=Equatorial Guinea|CM=Cameroon|CF=Central African Republic|TD=Chad|'
    'NG=Nigeria|NE=Niger|GH=Ghana|CI=Ivory Coast|BJ=Benin|TG=Togo|BF=Burkina Faso|'
    'ML=Mali|MR=Mauritania|SN=Senegal|GM=Gambia|GN=Guinea|SL=Sierra Leone|LR=Liberia|'
    'NA=Namibia|BW=Botswana|ZM=Zambia|ZW=Zimbabwe|MW=Malawi|LS=Lesotho|SZ=Eswatini|'
    'MG=Madagascar|MU=Mauritius|SC=Seychelles|KM=Comoros'
).split('|'))
LANGUAGES = dict(item.split('=') for item in (
    'pt=Portugal|en=England|es=Spain|fr=France|de=Germany|it=Italy|nl=Netherlands|'
    'da=Denmark|sv=Sweden|no=Norway|nb=Norway|nn=Norway|fi=Finland|is=Iceland|'
    'pl=Poland|cs=Czechia|sk=Slovakia|hu=Hungary|ro=Romania|bg=Bulgaria|el=Greece|'
    'tr=Turkey|ru=Russia|uk=Ukraine|sr=Serbia|hr=Croatia|sl=Slovenia|sq=Albania|'
    'lt=Lithuania|lv=Latvia|et=Estonia|he=Israel|ar=Saudi Arabia|fa=Iran|'
    'zh=China|ja=Japan|ko=South Korea|hi=India|bn=Bangladesh|ur=Pakistan|'
    'id=Indonesia|ms=Malaysia|th=Thailand|vi=Vietnam|sw=Kenya|af=South Africa'
).split('|'))


def country_from_locale(tag):
    parts = str(tag or '').replace('_', '-').split('-')
    language = parts[0].lower()
    region = ''
    for part in parts[1:]:
        if len(part) == 1:
            break
        if len(part) == 2 and part.isalpha():
            region = part.upper()
            break
    if region == 'GB' and language in ('cy', 'gd'):
        return 'Wales' if language == 'cy' else 'Scotland'
    return REGIONS.get(region, LANGUAGES.get(language, 'England'))


def phone_locale_tag(android=False):
    """Read the system's primary locale, independently of this app's language.

    Locale.getDefault() may reflect an app/runtime override. Prefer Android's
    system configuration and support both LocaleList and pre-API-24 devices.
    """
    try:
        if android:
            from jnius import autoclass
            try:
                configuration = autoclass('android.content.res.Resources').getSystem().getConfiguration()
                try:
                    locales = configuration.getLocales()
                    if locales.size() > 0:
                        return str(locales.get(0).toLanguageTag())
                except Exception:
                    pass
                if configuration.locale is not None:
                    return str(configuration.locale.toLanguageTag())
            except Exception:
                pass
            return str(autoclass('java.util.Locale').getDefault().toLanguageTag())
        import locale
        return locale.getlocale()[0] or ''
    except Exception:
        return ''


def phone_country(android=False):
    return country_from_locale(phone_locale_tag(android))


def language_from_locale(tag):
    """Translation selection hook; it does not translate game text by itself."""
    return 'pt' if str(tag or '').replace('_', '-').split('-')[0].lower() == 'pt' else 'en'

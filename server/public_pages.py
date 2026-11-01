"""Public PT/EN documents; a review draft cannot silently become a final policy."""
import html,json,re
from pathlib import Path
from online_safety import TERMS_TEXT

TERMS_PT='Usa uma alcunha, nunca o nome completo real, contactos ou escola. Não publiques abuso, ódio, conteúdo sexual, ameaças, usurpação de identidade ou spam. Nomes e equipas só ficam públicos após análise. Denuncia ou bloqueia entradas inseguras. Os moderadores podem remover recordes e suspender publicações. Os resultados são auto-reportados. Podes parar a partilha e remover os teus recordes a qualquer momento.'
DETAIL_FIELDS=('legal_basis','provider_practices','children_practices','international_transfers')
SOURCE_LINKS=(
 ('Cloudflare — Privacy policy','https://www.cloudflare.com/privacypolicy/'),
 ('Cloudflare — Data Processing Addendum','https://www.cloudflare.com/cloudflare-customer-dpa/'),
 ('Cloudflare — GDPR','https://www.cloudflare.com/trust-hub/gdpr/'),
 ('Google Play — User Data','https://support.google.com/googleplay/android-developer/answer/10144311?hl=en'),
 ('Google Play — Families','https://support.google.com/googleplay/android-developer/answer/9893335?hl=en'),
)

def load_config(config_path,privacy=True):
    path=Path(config_path)
    if path.stat().st_size>65536:raise ValueError('Public configuration exceeds limit')
    d=json.loads(path.read_text(encoding='utf8'))
    if not isinstance(d,dict):raise ValueError('Public configuration must be an object')
    if not all(isinstance(d.get(k),str) and d[k].strip() for k in ('developer_name','support_email')):raise ValueError('Developer name and support email are required')
    if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',d['support_email']):raise ValueError('Invalid public email')
    status=d.get('publication_status','draft')  # Missing status must never imply that legal review is complete.
    if status not in ('draft','published'):raise ValueError('Unknown policy status')
    if privacy:
        if not all(isinstance(d.get(k),str) and d[k].strip() for k in ('effective_date',*DETAIL_FIELDS)):raise ValueError('Privacy description fields are incomplete')
        for k in DETAIL_FIELDS:
            if k+'_en' in d and (not isinstance(d[k+'_en'],str) or not d[k+'_en'].strip()):raise ValueError('Invalid English description')
    return dict(d,publication_status=status)

def _p(text):return '<p>'+html.escape(text)+'</p>'
def _heading(text):return '<h2>'+html.escape(text)+'</h2>'

def _privacy(d,en=False):
    detail=lambda k:d.get(k+'_en',d[k]) if en else d[k]
    if en:
        parts=[_p('Scorer and Scorer World are separate free apps with independent on-device careers. No adverts, advertising SDKs or in-app purchases.'),
        _heading('Automatic usage counts'),_p('The 0.6.46 app displays a detailed notice before its first usage transmission. It automatically sends nine numeric counters: app openings and normal closes, new and loaded careers, completed training and matches, goals and save/load failures. Recipient: stats.clemir.com; purpose: understand game usage. There is no in-game usage switch. No player name, career, free text, exact event time or device/session identifier is in this payload. These are events, not unique players. Local unsent counts expire after seven days; own server totals are combined by UTC receipt day and kept for 90 days with periodic cleanup. Delays and uncertain acknowledgements can duplicate counts. Older test builds may behave differently: update to the current app.'),
        _heading('Optional public records'),_p('Adult-managed access, community rules and explicit Share precede publication of player name, team, completed season, matches, goals and edition/country/division. Use a nickname, never personal contact or school details. New or changed submissions await moderator review; scores are self-reported. A private random ownership token authorizes uploads/removal; the server stores its hash. Opaque public publisher/record IDs support reports and blocking, but cannot authorize deletion. Records remain until withdrawal or moderation.'),
        _heading('Children and local adult controls'),_p(detail('children_practices')),_p('Adult PINs are stored as salted hashes on the device. Blocked publisher IDs and safety preferences also remain local. An adult can lock public access and queue withdrawal of records. PINs are never published, exported or sent to the server.'),
        _heading('Reports, moderation and removal'),_p('Report/block tools are inside the app. Reports transmit the reporter token, target public publisher ID and a fixed reason; the server keeps the hashed reporter identity, target and reason for up to 30 days with periodic cleanup. Moderators may reject/erase records and suspend publishers. A suspended public ID remains until lifted to prevent re-publication. Stop sharing & remove is available even when public features are locked. Offline removal is retried while the app runs; keep the app until removal completes. If app data or the ownership credential is lost, contact support without sending secret tokens. Uninstalling does not remove public records.'),
        _heading('Local careers, exports and backups'),_p('Careers remain on-device; there is no automatic cloud career upload or email/password account. World uses phone language locally. Android app backup is disabled. User-selected career exports contain player names and game progress; keep them private and choose a trusted document provider, which may itself use cloud storage. Exports exclude adult controls, usage counters and online ownership credentials. Only the same edition can import a career. Uninstall removes private local files, not exported documents. Managed server recovery backups contain aggregate counters only, exclude public records/reports/tokens, and expire after seven days.'),
        _heading('Transport and Cloudflare'),_p('HTTPS validates certificates. The server is operated by the developer and uses Cloudflare Tunnel/CDN. Our collector suppresses IP, user-agent and raw-request logging. This does not mean the network provider processes no personal data.'),_p(detail('provider_practices')),
        _heading('International processing'),_p(detail('international_transfers')),
        _heading('Legal basis and rights'),_p(detail('legal_basis')),_p('Contact the privacy address to request information, access, correction, erasure, objection or other applicable rights. We must assess requests and implement the applicable requirements; listing an email does not waive those rights. Anonymous combined totals cannot be separated back into individual contributions. If you email support, your reply address and message are used to handle the request. Do not send passwords, PINs, full career files or administrator/ownership tokens. No automated email-summary service is active. You may contact the competent data-protection authority where applicable.')]
    else:
        parts=[_p('Scorer e Scorer World são apps gratuitas separadas, com carreiras independentes no dispositivo. Não têm anúncios, SDKs de publicidade ou compras dentro da aplicação.'),
        _heading('Contagens automáticas de utilização'),_p('A app 0.6.46 apresenta um aviso detalhado antes do primeiro envio. Envia automaticamente nove contagens: aberturas e fechos normais, carreiras novas e carregadas, treinos e jogos concluídos, golos e falhas de gravação/carregamento. O destinatário é stats.clemir.com e a finalidade é compreender a utilização do jogo. Não existe interruptor de estatísticas na app. Este payload não inclui nomes, carreiras, texto livre, hora exata de eventos ou identificadores de dispositivo/sessão. São eventos, não jogadores únicos. As contagens por enviar expiram localmente após sete dias; o nosso servidor agrega os totais pelo dia UTC de receção e conserva-os durante 90 dias, com limpeza periódica. Atrasos e confirmações de rede incertas podem duplicar contagens. Versões de teste anteriores podem funcionar de outra forma: atualiza para a app atual.'),
        _heading('Recordes públicos opcionais'),_p('O acesso gerido por adulto, as regras da comunidade e a ação explícita Partilhar precedem a publicação do nome do jogador, equipa, época concluída, jogos, golos e edição/país/divisão. Usa uma alcunha, nunca contactos pessoais ou informações da escola. Novas publicações e alterações aguardam análise de um moderador; os resultados são auto-reportados. Um token privado aleatório autoriza envios e remoções; o servidor guarda o seu hash. Identificadores públicos opacos permitem denunciar e bloquear, mas não autorizam a eliminação de dados. Os recordes ficam guardados até retirada ou moderação.'),
        _heading('Menores e controlos locais de adulto'),_p(detail('children_practices')),_p('Os PINs de adulto ficam no dispositivo como hashes com salt. Os identificadores bloqueados e as preferências de segurança também ficam locais. Um adulto pode bloquear o acesso público e colocar os recordes em fila de remoção. Os PINs nunca são publicados, exportados ou enviados para o servidor.'),
        _heading('Denúncias, moderação e remoção'),_p('Há ferramentas de denúncia e bloqueio na app. As denúncias transmitem o token do autor da denúncia, o identificador público visado e um motivo predefinido; o servidor guarda o hash do autor, o alvo e o motivo até 30 dias, com limpeza periódica. O moderador pode rejeitar/apagar recordes ou suspender publicações. O identificador público suspenso mantém-se até a suspensão ser levantada para evitar nova publicação. Parar partilha e remover está disponível mesmo com o acesso público bloqueado. A remoção offline é repetida enquanto a app estiver em execução; mantém a app até confirmar a conclusão. Se perderes os dados ou a credencial de posse, contacta o apoio sem enviar tokens secretos. Desinstalar não remove os recordes públicos.'),
        _heading('Carreiras, exportações e cópias locais'),_p('As carreiras ficam no dispositivo; não há envio automático da carreira para a nuvem nem conta com email/password. O World usa o idioma do telefone localmente. O backup Android da app está desativado. As exportações escolhidas pelo jogador incluem nomes e progresso; mantém-nas privadas e escolhe um fornecedor de documentos de confiança, que poderá usar armazenamento na nuvem. Não são exportados controlos de adulto, contagens ou credenciais de posse online. Só a mesma edição pode importar a carreira. Desinstalar remove ficheiros privados locais, não documentos exportados. As cópias geridas de recuperação do servidor contêm apenas totais agregados, excluem recordes/denúncias/tokens e expiram após sete dias.'),
        _heading('Transporte e Cloudflare'),_p('O HTTPS valida certificados. O servidor é operado pelo responsável e usa Cloudflare Tunnel/CDN. O nosso coletor suprime registos de IP, user agent e pedidos em bruto. Isso não significa que o fornecedor de rede não trate dados pessoais.'),_p(detail('provider_practices')),
        _heading('Tratamento internacional'),_p(detail('international_transfers')),
        _heading('Fundamento e direitos'),_p(detail('legal_basis')),_p('Podes contactar o endereço de privacidade para pedir informação, acesso, correção, eliminação, oposição ou outros direitos aplicáveis. Os pedidos têm de ser avaliados e os requisitos aplicáveis implementados; indicar um email não afasta esses direitos. Totais anónimos já combinados não permitem separar contribuições individuais. Se enviares um email ao apoio, o endereço de resposta e a mensagem são usados para tratar o pedido. Não envies passwords, PINs, carreiras completas nem tokens de administração/posse. Não existe serviço automático de resumos por email. Podes contactar a autoridade de proteção de dados competente, quando aplicável.')]
    return ''.join(parts)

def page(path,config_path):
    if path not in ('/privacy','/terms','/delete'):return 404,b'Not found.'
    try:d=load_config(config_path,privacy=path=='/privacy')
    except (OSError,ValueError,TypeError):return 503,b'Public policy configuration is pending.'
    e=lambda k:html.escape(d[k]);contact='<a href="mailto:'+e('support_email')+'">'+e('support_email')+'</a>'
    title={'/privacy':'Scorer e Scorer World — Política de privacidade / Privacy policy','/terms':'Scorer — Regras da comunidade / Community rules','/delete':'Scorer — Remover recordes / Remove records'}[path]
    draft=path=='/privacy' and d['publication_status']=='draft'
    banner=''
    if draft:
        banner='<aside role="note" class="draft"><strong>PROPOSTA EM REVISÃO — VERSÃO DE TESTE</strong><p>A base jurídica das estatísticas obrigatórias para menores e as condições efetivas da Cloudflare continuam por validar. Esta proposta não é uma política final para submissão à Google Play.</p><strong>DRAFT UNDER REVIEW — TEST BUILD</strong><p>Mandatory analytics for minors and actual Cloudflare practices remain under review. This is not a final policy for a Google Play submission.</p></aside>'
    identity=_p('Responsável / Responsible developer: '+d['developer_name'])+'<p>Privacidade e apoio / Privacy and support: '+contact+'</p>'
    if path=='/privacy':
        identity+=_p(('Proposta atualizada em / Draft updated: ' if draft else 'Em vigor desde / Effective: ')+d['effective_date'])
        body='<section id="pt" lang="pt-PT">'+_heading('Português')+_privacy(d)+'</section><section id="en" lang="en">'+_heading('English')+_privacy(d,True)+'</section>'
        body+='<h2>Referências oficiais / Official references</h2><ul>'+''.join('<li><a href="'+html.escape(url,quote=True)+'">'+html.escape(name)+'</a></li>' for name,url in SOURCE_LINKS)+'</ul>'
    elif path=='/terms':body='<section id="pt" lang="pt-PT">'+_heading('Português')+_p(TERMS_PT)+'</section><section id="en" lang="en">'+_heading('English')+_p(TERMS_TEXT)+'</section>'
    else:
        pt='Na app, abre Leaderboard e escolhe Parar partilha e remover. Mantém a app instalada até a remoção terminar. Podes remover os teus recordes mesmo quando as funções públicas estão bloqueadas. Se perdeste a app ou não consegues remover um recorde, contacta o endereço acima e indica o nome público, equipa, época e divisão. Não envies passwords, PINs nem tokens de administração ou posse. Avaliamos a posse sem divulgar dados de terceiros. A app não tem conta com email/password. Desinstalar não apaga recordes públicos.'
        en='In the app, open Leaderboard and choose Stop sharing & remove. Keep the app until removal completes. You can remove your records even when public features are locked. If you lost the app or cannot remove a record, contact the address above with the public name, team, season and division. Do not send passwords, PINs or administrator/ownership tokens. We assess ownership without disclosing another person’s data. The app has no email/password account. Uninstalling does not erase public records.'
        body='<section id="pt" lang="pt-PT">'+_heading('Português')+_p(pt)+'</section><section id="en" lang="en">'+_heading('English')+_p(en)+'</section>'
    nav='<nav><a href="#pt">Português</a> · <a href="#en">English</a> · <a href="/privacy">Privacidade / Privacy</a> · <a href="/terms">Regras / Rules</a> · <a href="/delete">Remoção / Removal</a></nav>'
    status='draft' if draft else 'operational' if path!='/privacy' else 'published'
    doc='<!doctype html><html lang="pt-PT" data-publication-status="'+status+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(title)+'</title>'+('<meta name="robots" content="noindex">' if draft else '')+'<style>body{font:18px system-ui;max-width:900px;margin:28px auto;padding:16px;line-height:1.65;color:#132d37}a{color:#005d66}h1{font-size:1.8em}h2{font-size:1.3em}nav{padding:12px 0}.draft{padding:18px;background:#fff3cc;border:2px solid #a66b00;border-radius:8px}section{margin:36px 0}p{overflow-wrap:anywhere}</style><body><h1>'+html.escape(title)+'</h1>'+nav+banner+identity+body+nav+'</body></html>'
    return 200,doc.encode('utf8')

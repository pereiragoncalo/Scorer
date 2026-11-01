## 0.9: point 1 implemented

World tournaments now have persistent fixtures, qualifying/group tables, knockout results, national-team participation, domestic cups, played promotion playoffs, balanced promotion/relegation, qualification snapshots and recoverable season transitions. Explicit game formats and validation are [documented](docs/WORLD_COMPETITIONS_0.9.md). Proceed to real Android acceptance, then remaining server and Play release checks; public version remains1.0.

## Release sequence: 0.9 → 1.0

Owner decision: next test version 0.9; public World release 1.0. Preserve the same package/saves and increasing unused Android version codes. Finish World competition behaviour and multi-season validation, real Android acceptance, actual final-policy/server deployment and production Play signing/forms/testing. See [current checklist](docs/play/ROAD_TO_1.0.md). Earlier release schedules below are historical; version numbering does not imply production approval.

## Difficulty update — 0.6.48

Owner requests >1 goal per match to be difficult. Progressive competitive keeper/marking now implemented; physical high/low save gaps fixed, morale opportunities and training preserved. See [paired measurements](docs/DIFFICULTY_0.6.48.md). World QA update only; production Play gates remain as documented.

## Current decision — 1 November 2026

Launch only Scorer World on Google Play: free, ad-free, no IAP, names editor included. Free remains legacy QA. Public policies and listing are English; game UI retains nine languages. The owner confirms Cloudflare Tunnel/proxy only and legal exceptions for usage collection. Version 0.6.47 implements privacy-request suspension. Earlier contradictory plans below are historical. See [current launch steps](docs/play/WORLD_LAUNCH_0.6.47.md).

## Estado atual — 01/11/2026

O dono confirmou conta Play ativa/verificada. Scorer e Scorer World são apps
independentes, GRATUITAS e sem publicidade/IAP. Público inclui menores.
A preparação0.6.46 acrescenta divulgação automática, controlos adultos,
moderação/denúncia/bloqueio, transferência de carreira e AABs de ensaio.
[Entrega e gates externos](docs/play/RELEASE_0.6.46.md).
O plano abaixo é histórico onde contradiz estas decisões; não reativar anúncios,
compras ou modelos de app única. Publicação depende de configuração/revisão
legal no laptop, assinatura e testes/formulários da Play.

## Latest owner decisions — 25 October 2026

Two separate APKs: Free com.clemir.striker, World com.clemir.scorerworld.
Free has one English-only division, test AdMob and offline World promotion.
World has its own career/editor, nine UI languages, no advertising SDK or in-app
billing. Paid-app listing, release signing and public Play publication remain
pending. Historical single-app billing plans below are superseded.

# Roteiro executável — 24/10 a 06/11/2026

| Dia | Data | Trabalho Codex | Aceitação verificável |
| --- | --- | --- | --- |
| 1 | 24/10 | Auditoria, ambiente, compilação Python e Android configs | Problemas identificados, plano de build reproduzível |
| 2 | 25/10 | Primeiro APK debug no Android | APK instalado, app abre; ou bloqueio documentado |
| 3 | 26/10 | Saves app-private, recuperação e nome genérico | Progressão mantém-se após fechar/reabrir |
| 4 | 27/10 | Controlos por toque, dimensões, landscape | Navegação/partida viável em 2 dimensões de ecrã |
| 5 | 28/10 | Motor de painéis via Canvas nas bordas do campo | Visíveis, sem ocultar jogadores, bola ou baliza |
| 6 | 29/10 | Campanhas locais, rotação e fallback offline | Troca de anúncios sem rede e sem travar o jogo |
| 7 | 30/10 | Performance e robustez das texturas | Perfil FPS/memória comparado com baseline |
| 8 | 31/10 | Regressões carreira e mecânicas existentes | Treino, agente, partida, classificação, saves |
| 9 | 01/11 | Testes Android em mais do que 1 aparelho | Relatório de crashes, rotação, UX e resolução |
| 10 | 02/11 | Capturas reais, ícone, texto e gameplay trailer | Assets comerciais criados a partir do jogo |
| 11 | 03/11 | Build release, assinatura e verificação do pacote | APK assinado e testado, chaves não expostas |
| 12 | 04/11 | Lançamento beta direto e recolha de bugs | Testadores têm APK e canal de feedback |
| 13 | 05/11 | Hotfix final, revisão legal e privacidade | Checklist de release preenchida |
| 14 | 06/11 | Publicação itch.io e campanha orgânica | Página e APK públicos após autorização humana |

## Google Play em paralelo
- Abrir/verificar Play Console; conta pode exigir teste fechado com 12 pessoas por 14 dias seguidos antes de solicitar produção.
- Configurar AAB com target API 36, privacidade, conteúdos, classificação etária, declaração de publicidade e testes.
- Decisão atual 0.6.25: uma só aplicação com compra única Google Play para World/editor e remoção de anúncios. Manter a carreira Free apenas no modo Free e uma carreira World separada na mesma aplicação; Free sem escolha de país. Preparar e testar Billing/verificação/restauro sem ativar pagamentos ou publicação antes de aprovação explícita.
- Play Store depende de revisão externa; não prometer aprovação até 06/11.

## Estratégia de comunidade
- Público: jogadores Android, indies, fãs de jogos de futebol retro e carreira de futebol.
- 3 clips curtos de jogabilidade real: remate/golo, carreira/transferência, campo com painéis de publicidade.
- Publicar em itch.io, vídeo vertical YouTube Shorts e TikTok, e divulgar em comunidades adequadas respeitando as regras de autopromoção.
- Objetivo inicial: 30 testadores de interesse genuíno, 100 downloads orgânicos, 10 relatos úteis; são metas, não garantias.
- Medir downloads e feedback sem adicionar telemetria oculta.

## Âmbito excluído dos 14 dias
Multiplayer, ads AdMob convencionais, gestão online de sponsors, contas online, modos pagos, integrações sociais obrigatórias, reconstrução web ou mudança de engine.

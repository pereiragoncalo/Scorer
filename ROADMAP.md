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
- World passa a aplicação paga separada, conforme docs/PRODUCT_MODEL.md. Não integrar compras/desbloqueio no FREE. Preparar cobertura mundial e editor/importador antes de qualquer cobrança ou publicação aprovada.
- Play Store depende de revisão externa; não prometer aprovação até 06/11.

## Estratégia de comunidade
- Público: jogadores Android, indies, fãs de jogos de futebol retro e carreira de futebol.
- 3 clips curtos de jogabilidade real: remate/golo, carreira/transferência, campo com painéis de publicidade.
- Publicar em itch.io, vídeo vertical YouTube Shorts e TikTok, e divulgar em comunidades adequadas respeitando as regras de autopromoção.
- Objetivo inicial: 30 testadores de interesse genuíno, 100 downloads orgânicos, 10 relatos úteis; são metas, não garantias.
- Medir downloads e feedback sem adicionar telemetria oculta.

## Âmbito excluído dos 14 dias
Multiplayer, ads AdMob convencionais, gestão online de sponsors, contas online, modos pagos, integrações sociais obrigatórias, reconstrução web ou mudança de engine.

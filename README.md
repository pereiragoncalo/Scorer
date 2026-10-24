# STRIKER Android — base para trabalhar com Codex

## Estado em 23/10/2026
Código original Python/Kivy recuperado da Google Drive `Projetos/Striker/Builds/Striker-P0-05-v006.py`, com aproximadamente 6290 linhas. Reúne simulação de futebol, carreira de avançado, treino, agente, classificação e componentes FREE/WORLD. **Não é a versão web.**

- `main.py`: cópia do código-fonte v006, com o nome esperado pelo Buildozer.
- `baseline/`: cópia histórica imutável para comparação.
- `buildozer.spec`: configuração Android original já guardada na Drive; ainda não validada mediante compilação real.
- `docs/AndroidManifest.release.reference.xml`: referência estática; não implica que o Manifest final do Android já a incorpore.
- `AGENTS.md`: regras persistentes para Codex.
- `FIRST_CODEX_TASK.md`: pedido inicial para Codex.
- `ROADMAP.md`: sequência de trabalho até 6 de novembro de 2026.

## Como abrir no Codex
- Extrair este ZIP para uma pasta local.
- Abrir a pasta na aplicação Codex ou, num terminal já com Codex instalado, executar `codex` dentro da pasta.
- Fornecer o texto de `FIRST_CODEX_TASK.md` como primeira tarefa.
- Preferencialmente importar a pasta para um repositório GitHub **privado** e conceder-lhe acesso através do Codex. Não é obrigatório para executar Codex localmente.
- Revisar o diff e os resultados dos testes antes de aceitar cada alteração.

## Verificações simples já disponíveis
```bash
python3 -m py_compile main.py
```
Isto verifica apenas sintaxe. A funcionalidade Android exige um ambiente de build Linux com SDK/NDK e testes num telemóvel real.

## Critérios de lançamento
1. APK Android instalado e executado em dispositivos reais.
2. Jogo funcional, save persistente em armazenamento app-private e regresso à carreira.
3. Painéis visíveis na simulação, carregados de imagens locais e sem FPS degradado.
4. Fim de uma partida, avanço de carreira e exportação/instalação testados.
5. APK assinado disponibilizável; AAB preparado para Play (aprovação não garantida).
6. Direitos dos conteúdos e privacidade verificados antes da publicação pública.

## Fase 1 — candidato de código 0.6.1

A carreira original está em `career.py`, importável sem Kivy; `main.py` mantém a
interface. Testes: `python3 -m unittest discover -s tests -v`.
Ver [build Android e limitações](docs/ANDROID_BUILD.md) e [resultados](docs/BUILD_LOG.md).
Já foi compilado um APK debug arm64 0.6.1, com assinatura e alinhamento ELF/ZIP verificados. O proprietário confirmou que 0.6.1 abre e corre sem crashes no Android; não é uma versão de distribuição. Não foi gerado AAB.

## 0.6.2 — menus responsivos

O proprietário confirmou que 0.6.1 abre e corre sem crashes no telemóvel.
A nova interface 0.6.2 usa texto multilinha, deslocação, alvos de toque de 52 dp e
botão Sair com confirmação/gravação. Mantém a mesma aplicação/carreira.

Testes Kivy reais, além da suite sem interface:
```sh
KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python -m unittest discover -s ui_tests -v
```
A separação FREE/World e funcionalidades ainda por implementar estão descritas
em [modelo de produto](docs/PRODUCT_MODEL.md). Free tem uma divisão; a aplicação
paga separada e o editor de importação mundial ainda não são produtos entregues.

## SCORER 0.6.3 — identidade e correções

Nome público atualizado para **SCORER**, splash em inglês com crédito clemir.
Sair só no menu principal, painel final responsivo e leitura segura de saves
malformados. Mantidos identificador Android e formato de carreira para atualização.
Ver [auditoria, testes e limitações](docs/AUDIT_0.6.3.md). Suite: 21 testes sem
interface e 10 testes Kivy; esta beta ainda exige validação no telemóvel.

## SCORER 0.6.4 — menu de um só ecrã e identidade visual

Menu principal sem scroll: resumo compacto da carreira e seis ações visíveis,
com Sair apenas no cabeçalho. Listas de classificação/calendário continuam
navegáveis por deslocação. Painel final dimensionado pelo conteúdo, botão
Continuar limitado a 176 dp. Splash «SCORER by clemir» e ícone próprio Android.
Ver [verificação da versão](docs/UI_0.6.4.md).

## SCORER 0.6.5 — escolher a carreira ao abrir

O splash permanece até tocar no ecrã, inclusive depois de rodar. Segue-se
Novo jogo / Carregar jogo / Sair. Novo jogo com save existente exige confirmação
e cópia local de segurança; cancelar ou fechar antes da escolha preserva o save.
Nome legado «England Division 4» migra para Liga Scorer sem apagar progresso:
FREE permite uma única divisão. Novo menu com fundo original de estádio,
próximo jogo destacado e navegação inferior, sem scroll.
[Alterações, referência visual, 40 testes e limitações](docs/UI_0.6.5.md).

## SCORER 0.6.6 — personalização e navegação compacta

Novo jogo pede o nome do jogador. Para alterar Alex Silva numa carreira existente,
abrir **Jogador** no menu principal; o progresso mantém-se. Splash com crédito
clemir menor, botões arredondados com relevo e listas de classificação,
marcadores e calendário paginadas, sem scroll horizontal/vertical.
[Alterações, 45 testes e limitações](docs/UI_0.6.6.md).

## SCORER 0.6.7 — alinhamento e tipografia

Marca nativa com Barlow Condensed ExtraBold Italic e crédito Barlow Regular,
fontes incluídas offline com licença. Ajustados eixos de texto nos menus,
indicadores e painel de oportunidade/resultado; texto dos botões centrado na face.
Corrigida a seta em falta no resumo de energia do treino.
[Alterações, fontes, 45 testes e limitações](docs/UI_0.6.7.md).

## SCORER 0.6.8 — treino semanal e menu

Jogar alinhado com Marcadores; ícone S seguido de CORER. Splash com preparação
do remate coerente. Uma sessão de treino por semana da carreira, descontada
ao começar e persistente ao reabrir.
[Alterações, 53 testes e limitações](docs/UI_0.6.8.md).

## SCORER 0.6.9 — alinhamento da marca

S do ícone e CORER na mesma linha, com as bases visuais alinhadas.
Crédito by clemir por baixo. Ajuste apenas visual do cabeçalho principal.

## SCORER 0.6.10 — English edition

All generated game text is in English, including menus, feedback, dates and
confirmations. Existing careers retain progress and custom names. This edition
stays in English on every phone; automatic language selection requires future
translations. [Changes and localisation approach](docs/UI_0.6.10.md).

## SCORER 0.6.11 — scoreboard and half-time

Fixed top-left scoreboard with stacked teams, clock on the right and a local
goal highlight. Shared position during chances; bottom time bar removed.
Half-time pauses after 45 plus added time; SECOND HALF resumes at 45:00.
[Changes and validation](docs/UI_0.6.11.md).

## SCORER 0.6.12 — training before Play

Smaller scoreboard with First half / Second half. Training sits left of Play,
which stays grey until all three weekly shots are completed. Interrupted
training can resume; completed sessions cannot be repeated. Match notice
widgets remain attached during redraws to preserve touches.
[Changes, 62 tests and limitations](docs/UI_0.6.12.md).

## SCORER 0.6.13 — tougher finishing and new logo

At most three personal highlights per match, with at most one clear chance;
all others have harder positions, defensive pressure and sharper goalkeeping.
New icon-based SCORER logo on the main and entry menus, without by clemir.
Existing career totals remain intact.
[Changes, 65 tests and 720 physical shot samples](docs/UI_0.6.13.md).

## SCORER 0.6.14 — timer and player initials

TIME TO SHOOT is attached directly beneath the scoreboard. Player-name
initials are capitalised automatically on profile save and career load,
keeping progress and scorer identity.
[Changes, 67 tests and limitations](docs/UI_0.6.14.md).

## SCORER 0.6.15 — chances depend on the opponent

Opponent quality and league position now determine chance quantity and clear
chance probability. Very strong opponents allow at most one chance, always
hard. Energy/morale still matter and career progress is retained.
[Rules, 70 tests and limitations](docs/UI_0.6.15.md).

## SCORER 0.6.16 — participation after training

Completing weekly training now guarantees at least one match opportunity.
Training goals help earn extras within the opponent's existing limits.
Very strong opponents still allow exactly one hard chance. Existing saves
continue without starting over. [Fix and validation](docs/UI_0.6.16.md).

## SCORER 0.6.17 — researched goal realism

Calibrated scoring against three full League Two seasons and historical shot
data. Match finishing has physical pressure/accuracy; teammate goals reserve
the player's contribution. Fixed duplicate scorer attribution and cup goals
in league rankings. Existing progress and guaranteed trained participation
remain. [Sources, experiments, 79 tests and limitations](docs/REALISM_0.6.17.md).

## SCORER 0.6.18 — balanced league calendar

League fixtures alternate home/away with at most one repeated pair per leg,
no triples, reversed return venues and equal full-season totals. In-progress
legacy calendars are retained when changing them would rewrite played fixtures;
new seasons use the new rule. Cup draws remain independent.
[Rules, save compatibility, 84 tests and limitations](docs/UI_0.6.18.md).

## SCORER 0.6.19 — player name panel

Removed the stray line, rounded the name field, centred text and tightened
the panel spacing/alignment. Name handling and career progress are unchanged.
[Visual fix, 84 tests and limitations](docs/UI_0.6.19.md).

## SCORER 0.6.20 — practice and match balance

Harder practice with match ball physics; slightly more achievable hard match
shots, slower morale loss and stronger goal reward. Club-specific fictional
scorer names preserve saved totals. Standing saves hold the ball during a
forward fall; corner flags and a broadcast-style scoreboard improve presentation.
[87 tests, measured balance and Android verification](docs/UI_0.6.20.md).

## SCORER 0.6.21 — season draw and cup progression

Fixtures shows the complete league calendar without a STATS submenu. New season
league draws are fixed from the start; cup opponents appear one round at a time
through the final. League dates remain fixed after cup elimination.
[Changes, save compatibility and 89 tests](docs/UI_0.6.21.md).

## SCORER 0.6.22 — AdMob test integration

Native Google Mobile Ads + UMP compiled into Android; a test banner after the
splash on the entry menu and test interstitials at completed-match breaks, with
frequency limits and graceful offline fallback.
Privacy screen and child-directed/non-personalised request settings. No revenue
yet: owner account/app IDs, approval and phone validation remain pending.
[Setup and activation](docs/ADMOB_SETUP.md) · [97 tests and build evidence](docs/UI_0.6.22.md).

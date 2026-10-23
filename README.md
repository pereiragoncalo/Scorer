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

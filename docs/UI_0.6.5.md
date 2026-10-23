# SCORER 0.6.5 — arranque, uma divisão e novo menu

## Comportamento
1. O presplash nativo passa para um ecrã Kivy com a mesma imagem. Este segundo
   ecrã não tem temporizador: continua visível, incluindo após rotação, até um
   toque. A indicação «TAP TO START» torna esta ação explícita.
2. Depois do toque surgem **Novo jogo**, **Carregar jogo** e **Sair**. Não há
   carregamento automático da carreira. Carregar fica desativado sem ficheiro.
3. Com um save existente, Novo jogo pede confirmação. Cancelar mantém tudo.
   Confirmar cria primeiro uma cópia atómica em `striker_career.previous.json`,
   no armazenamento privado da aplicação. Se a cópia falhar, não inicia a nova
   carreira. O save principal só é substituído ao aceitar o primeiro contrato.
4. Pausar/fechar antes de carregar ou iniciar uma carreira não grava uma carreira
   vazia sobre a antiga. Ficheiro inválido é preservado e apresenta erro de carga.

## FREE: uma única divisão
A fronteira existente já autorizava apenas uma liga (`England|4` é o identificador
interno herdado do original, não uma contagem de quatro divisões). A captura do
proprietário mostrou um **nome legado**: `league_name` do save reintroduzia
«England Division 4». Agora os nomes automáticos antigos («England Division 4»,
«Divisão Striker», «Divisão Scorer») migram para **Liga Scorer**, mantendo clube,
resultados, semana e progresso. Nomes personalizados não são substituídos.
O menu explicita «1 DIVISÃO». O identificador interno permanece compatível com
os saves anteriores; a arquitetura WORLD continua preparada e inacessível em FREE.

Testes reforçados demonstram: só uma liga autorizada, propostas de transferência
apenas dessa liga, transferência forjada para outra bloqueada e dois fins de época
sem promoção para outra divisão. Não foram ativados pagamentos ou WORLD.

## Referência visual e execução
Pesquisa de menus de futebol em fontes públicas acessíveis. Foi inspecionada a
[imagem de menu FIFA 2000](https://github.com/tihamr/FIFA2000/blob/main/images/bg.png)
do projeto [UI Nostalgia](https://github.com/tihamr/FIFA2000). A consulta da galeria
Steam falhou com HTTP 403; outras pesquisas no GitHub encontraram recriações,
kits e projetos sem capturas aproveitáveis. Não se afirma ter inspecionado galerias
modernas inacessíveis. A referência usada foi hierarquia de navegação e destaque
da ação principal. Nenhum código, imagem, marca ou interface externa foi integrado.

O novo menu é Python/Kivy: fundo original de estádio, identidade em faixa compacta,
próximo jogo em destaque com Jogar, resumo da época e barra inferior para Treino,
Classificação, Marcadores, Calendário e Agente. Sem scroll. A disposição adapta-se
para portrait e janelas muito baixas mantendo os seis destinos e Sair acessíveis.

## Ficheiros e validação
- `main.py`: estados de arranque, escolha explícita, confirmação e ciclo de vida.
- `career.py`: autoload opcional, resultado de load, backup e migração de nomes.
- `menu_ui.py`, `assets/menu_stadium.png`: apresentação original e menus.
- `buildozer.spec`: 0.6.5 e exclusão de todas as cópias de saves do pacote.
- Suites de carreira/Kivy, README, AGENTS e BUILD_LOG.

25 testes sem interface e 15 testes Kivy aprovados: 40 no total. Incluem toque real,
rotações e tempo decorrido sem sair do splash, opções de entrada, cancelamento e
confirmação, falha de backup, save inválido, conservação do save ao pausar, uma
única divisão e regressões anteriores. Capturas reais da janela Kivy do splash,
entrada e menu em 1280×589/densidade 1,64 foram inspecionadas. Não são testes Android.

APK debug arm64 realmente compilado, assinatura v2 e alinhamento ZIP/118 ELF
AArch64 a 16 KB verificados. Recursos novos e ausência de saves no pacote
verificados. Instalar como atualização, sem desinstalar. Mesma identidade Android
`com.clemir.striker` e certificado debug. A validação física de 0.6.5 continua
pendente; não se trata de release de loja ou AAB.

## Próximo teste no telemóvel
Abrir, rodar e esperar sem tocar: o splash deve permanecer. Tocar e escolher
Carregar jogo: confirmar clube/progresso e Liga Scorer. Verificar que o menu não
precisa de scroll. Para experimentar Novo jogo, cancelar primeiro a confirmação;
confirmar apenas se quiser iniciar outra carreira (a anterior fica na cópia local).

# SCORER 0.6.6 — jogador, botões e listas compactas

## Nome do jogador
Alex Silva era o nome fictício predefinido, usado também nos saves existentes.
Não há alteração automática de nomes guardados. Novo jogo passa por um formulário
obrigatório antes do primeiro contrato. O botão **Jogador** no menu principal
permite alterar o nome de uma carreira existente, mantendo clube e progresso.
Nomes aceitam caracteres seguros, mínimo dois, máximo 32. A alteração atualiza
também a entrada do jogador na lista de marcadores, para não deixar um duplicado
com o nome antigo. Colisão com outro marcador é rejeitada; uma falha de gravação
repõe o nome e os marcadores anteriores e conserva o ficheiro original.

## Identidade e botões
Crédito «by clemir» mantém a posição abaixo de SCORER, com cerca de um quarto da
altura anterior. Arte editada através da geração de imagem; mantém o jogador,
estádio e texto inglês. O splash continua até um toque e suporta rotação.
Botões Kivy partilham cantos arredondados, base escura, face elevada, brilho e
rebordo; ao pressionar, a face baixa e escurece. Sem novas dependências. Alvos
de toque mantêm 52 dp de altura, incluindo paginação e confirmação.

## Menos deslocação
- Classificação, marcadores e calendário usam páginas, sem ScrollView horizontal
  ou vertical. Todos os registos continuam disponíveis.
- Linhas de dados têm 24 dp (não são controlos de toque) e fonte de 12 sp; a altura
  cresce com fontes do sistema ampliadas. No tamanho lógico 640×360 aparecem
  sete linhas por página; no telefone 1280×589/densidade 1,64 também sete.
- Anterior/Seguinte, contador de páginas, **Meu lugar** para o clube/jogador e
  **Dados** para estatísticas adicionais. Em ecrãs largos a classificação mostra
  todas as colunas; nos mais estreitos alterna resumo e detalhes sem cortar a
  tabela para fora do ecrã. O clube/jogador aparece destacado.
- Calendário mostra dia/mês, com época indicada no título e competição acessível
  em Dados. Histórico não foi apagado nem reduzido para obter uma lista curta.
- Cards gerais têm menos margens; propostas iniciais passam para duas colunas.
  Listas auxiliares extensas ainda podem deslocar-se em ecrãs baixos para manter
  legibilidade e alvos de toque adequados. Menu principal continua sem scroll.

## Ficheiros e testes
`career.py`, `main.py`, `menu_ui.py`, `assets/splash.png`, `buildozer.spec`, suites
core/Kivy, README, AGENTS e BUILD_LOG. Baseline e identidade Android preservados.

27 testes sem interface + 18 Kivy aprovados (45). Cobrem nome novo/existente,
marcadores sem duplicação, nomes inválidos/colisões/falha de save, navegação por
**todos** os registos das listas, salto para o clube, limites dos widgets e estado
de botão premido, além da regressão de splash, rotação, saves, FREE e menus.
Durante a primeira verificação, foi corrigido acesso incorreto às coordenadas de
RoundedRectangle; a suite final está aprovada. Capturas reais da janela Kivy
inspecionadas: classificação, menu e formulário. Não são capturas Android.

APK debug arm64 compilado realmente, assinatura v2 e alinhamento ZIP/118 ELF
AArch64 de 16 KB verificados. Recursos de ícone/splash conferidos e nenhum save,
backup ou chave de assinatura incluído no pacote. Mesma aplicação e certificado
para atualização sem desinstalar. Sem dispositivo Android ligado ao ambiente:
validar no telemóvel o teclado, a alteração de nome, relevo dos botões e paginação.
Não é um build release/AAB nem uma publicação de loja.

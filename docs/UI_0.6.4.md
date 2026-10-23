# SCORER 0.6.4 — menu compacto, resultado e marca

## Alterações
- Menu principal sem ScrollView. Resumo da carreira e grelha com Jogar, Treino,
  Classificação, Marcadores, Calendário e Agente; Sair no cabeçalho.
- Em landscape o resumo e as ações ficam lado a lado; em portrait empilham-se.
  Em janelas muito baixas as ações usam três colunas e metadados secundários
  cedem espaço à identidade, energia/moral e próximo jogo. Dados completos
  continuam nas páginas correspondentes. Texto longo é abreviado na área
  reservada, em vez de expandir o menu ou atravessar os seus limites.
- Painel final com altura calculada a partir do texto e da ação; sem a altura
  fixa de 260 dp. Largura máxima 460 dp e botão Continuar de 176×52 dp,
  em vez de ocupar toda a caixa. Mantida rolagem de segurança apenas para
  mensagens excepcionalmente extensas dentro deste painel.
- Novo splash em inglês: SCORER / by clemir / YOUR CAREER STARTS HERE.
- Ícone original: monograma S, bola e traço de remate, nas cores da aplicação.
  Configurado como recurso launcher e mostrado no cabeçalho do menu.

## Ficheiros
`menu_ui.py`, `ui_tests/test_menus.py`, `assets/splash.png`, `assets/icon.png`,
`buildozer.spec`, README, AGENTS e documentação desta etapa. Sem alterações
à simulação, esquema de save, applicationId ou baseline.

## Testes
- 21 testes sem interface de carreira/build/segurança e 11 testes Kivy.
- Teste novo confirma ausência de ScrollView no menu, sete botões visíveis,
  alvos de pelo menos 48 dp, ausência de sobreposição e limites do ecrã.
- Tamanhos/densidades: 640×360 a 1, 800×360 a 1, 1280×589 a 1,64
  (aproximação à captura do proprietário), 2400×1080 a 3, portrait 360×800
  e janela compacta 320×240. Mantidos testes de fonte ampliada, navegação,
  confirmação/gravação antes de sair e proteção FREE.
- Teste do resultado verifica altura proporcional ao conteúdo, limite de
  200 dp para a mensagem longa de teste, texto dentro dos limites e retorno
  à carreira. Inspeção de capturas reais da janela Kivy a 1280×589/densidade
  1,64. Estas capturas não representam execução Android.

## Entrega e próximo passo
APK debug Android arm64 0.6.4 compilado e verificado quanto à assinatura,
alinhamento ZIP 16 KB e todos os 118 ELF AArch64. Recursos de ícone/splash
conferidos dentro do APK. Instalar como atualização, sem desinstalar a beta
anterior; mantém certificado e identificador. Verificar no telemóvel o ícone,
splash, ausência de scroll no menu, treino, oportunidades e fim de jogo.
Sem dispositivo ligado a este ambiente; validação física desta versão pendente.
Não é uma publicação Play Store nem uma versão assinada para distribuição final.

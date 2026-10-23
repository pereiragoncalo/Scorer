# SCORER 0.6.8 — alinhamento e treino semanal

## Alterações
- Jogar partilha as margens esquerda/direita e largura de Marcadores no menu
  horizontal. Mantida adaptação a ecrãs estreitos e retrato.
- O ícone com S é seguido por CORER, formando SCORER; crédito by clemir menor.
- Splash revisto: pé esquerdo apoiado, perna direita recuada e bola no relvado,
  antes do remate. Mantidos título em inglês e espera pelo toque.
- Uma sessão de três remates por semana da carreira. A sessão é descontada
  ao começar e guardada antes do primeiro remate: abandonar ou reabrir não
  permite repetir. Botão bloqueado e informação sobre a próxima semana.
- Bónus de energia/moral aplicado uma única vez. Falhas de gravação revertem
  a reserva ou a recompensa. Sem reiniciar a contagem de remates de uma sessão
  ativa. Nova semana/época permite novo treino.
- Campo opcional training_session_week nos saves, mantendo a versão 2 e
  compatibilidade com saves anteriores, incluindo treinos já concluídos.

## Ficheiros modificados
career.py, main.py, menu_ui.py, assets/splash.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, AGENTS.md, README.md e documentação.
Baseline e ícone preservados. Sem alteração da simulação dos jogos.

## Testes e problemas corrigidos
31 testes core/build/segurança e 22 testes Kivy passaram (53), mais py_compile
 e git diff --check. Cobertura de persistência, repetição, abandono, época,
falhas de gravação, saves antigos, igualdade das margens dos botões em quatro
combinações de resolução/densidade e visibilidade do resumo de treino.

As primeiras verificações expuseram posição negativa de Jogar em retrato,
widgets com dimensões antigas após mudança de densidade e resumo de treino
alto demais. Corrigidos com ancoragem relativa, reconstrução ao mudar
 densidade/escala e texto compacto. Capturas reais da janela Kivy de menu e
 treino inspecionadas; não são capturas Android.

## Entrega e próxima tarefa
APK beta debug arm64 0.6.8; os resultados da compilação e verificações do pacote
ficam no BUILD_LOG. Atualizar sem desinstalar para preservar a carreira.
Próximo: validar no telemóvel alinhamento, splash e bloqueio de treino após
reabrir e desbloqueio após avançar uma semana. Teste físico desta versão
pendente; esta etapa não produz AAB ou assinatura release para loja.

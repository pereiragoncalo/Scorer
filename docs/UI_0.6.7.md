# SCORER 0.6.7 — alinhamento e tipografia da marca

## Alterações
- Marca nativa partilhada: SCORER em **Barlow Condensed ExtraBold Italic** e
  crédito menor em **Barlow Regular**. Consistente no menu de entrada, cabeçalho
  principal e restantes menus com marca. A entrada apresenta o conjunto centrado,
  com a frase introdutória alinhada pelo mesmo eixo. Removida a linha que
  atravessava a zona do título. A imagem do splash mantém a arte aprovada em 0.6.6.
- Face elevada dos botões centrada no texto; rebordo acompanha a face. Mantidos
  relevo, feedback premido, cantos arredondados e alvos de 52 dp.
- Identidade do jogador alinhada com a margem interior dos painéis; clube
  centrado e indicadores alinhados à direita. Números/legendas de jogos e golos
  ficam agrupados e partilham os mesmos eixos.
- Oportunidade e resultado: título, descrição e botão centrados no painel.
- Energia no resumo do treino usa «10.0 para 11.8», evitando o símbolo de seta
  que não era representado corretamente no telefone do proprietário.

## Fontes e funcionamento offline
Fontes originais, sem modificações, obtidas do repositório oficial Google Fonts:
[Barlow Condensed](https://github.com/google/fonts/tree/main/ofl/barlowcondensed)
e [Barlow](https://github.com/google/fonts/tree/main/ofl/barlow).
Copyright 2017 The Barlow Project Authors. SIL Open Font License 1.1 incluída
com cada fonte em `assets/fonts/OFL-*.license` e dentro do APK. Os ficheiros têm
extensão `.license` para inclusão explícita sem empacotar ficheiros de texto
arbitrários. Não há download de fontes durante o jogo ou permissões novas.

## Ficheiros
`menu_ui.py`, `ui_tests/test_menus.py`, `assets/fonts/`, `buildozer.spec`,
README, AGENTS e BUILD_LOG. Motor, carreira, saves, splash e ícone não alterados.

## Validação
27 testes de carreira/build/segurança + 18 Kivy aprovados (45). A regressão do
botão verifica também que o centro da face coincide com o centro do texto/widget.
Mantidas verificações de limites, seis combinações de ecrã/densidade, fontes
ampliadas, paginação, nomes, saves e splash persistente.
Capturas reais da janela Kivy da entrada, menu, treino concluído e oportunidade
em 1280×589/densidade 1,64 foram inspecionadas; não são capturas Android.

APK debug arm64 realmente compilado. Assinatura v2 e alinhamento ZIP/118 ELF
AArch64 a 16 KB verificados. Fontes e licenças conferidas dentro do pacote;
mesmo identificador e certificado para atualizar sem desinstalar.
Próximo: verificar os quatro ecrãs no telemóvel, incluindo os textos com as fontes
novas e estado dos botões. Validação física desta versão pendente; sem release
assinada para loja ou AAB nesta etapa.

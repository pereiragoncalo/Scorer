# Ativar receita publicitária no SCORER

## Estado real — 0.6.22

Existe uma integração Android nativa Google Mobile Ads 25.5.0 + UMP 4.0.0,
ligada ao jogo Python/Kivy: banner no menu após o splash e intersticiais entre partidas. O APK compilou com os SDKs, bridge Java, identificadores
oficiais de teste e permissões verificadas. A apresentação de um anúncio no
telemóvel ainda NÃO foi validada. A conta AdMob do proprietário ainda não existe.
Esta beta não gera receitas. Não substitui criar/aprovar a conta ou a aplicação.

A pedido do proprietário, publicidade de rede substitui nesta etapa a antiga
restrição de apenas patrocínios diretos. Não há publicidade deformada em texturas,
compras nem desbloqueio World. Os painéis offline continuam a ser uma possibilidade
separada de patrocínio; não foram implementados nesta revisão.

## O que o proprietário tem de fazer

1. Abrir https://admob.google.com/home/ e criar a conta com a própria conta Google.
   A escolha do país, dados fiscais, aceitação do contrato, verificação de identidade
   e configuração de pagamentos têm de corresponder ao titular real. Não enviar
   palavras-passe, documentos, dados bancários ou acesso à conta nesta conversa.
2. Adicionar a app Android SCORER, package `com.clemir.striker`. Declarar honestamente
   se ainda não está numa loja. Criar um bloco **Banner** para o menu inicial e um bloco **Interstitial** para o intervalo
   entre partidas (não rewarded, não app-open). O SDK não dá direito a anunciar
   receitas antes de a Google aprovar conta/app e disponibilizar anúncios.
3. Enviar apenas os três identificadores públicos: App ID `ca-app-pub-…~…`,
   Banner ID e Interstitial ID (ambos `ca-app-pub-…/…`). Não são palavras-passe. Os IDs de teste desta beta
   pertencem à Google e nunca pagam ao proprietário.
4. Configurar o público real (inclui menores), classificação de anúncios,
   privacidade/mensagens e requisitos de consentimento na consola. A configuração
   do APK trata conservadoramente TODOS os pedidos como infantis/abaixo da idade
   de consentimento, sem personalização e com classificação G; isso não dispensa
   as declarações corretas nem a avaliação das políticas Families na publicação.
5. Preparar a listagem numa loja suportada, a página pública de privacidade com
   identificação/contacto do responsável e, quando solicitado, website do produtor
   e app-ads.txt com o publisher ID fornecido pela consola. APK GitHub/itch.io por
   si só não garante elegibilidade nem anúncios sem limitações. Seguir o estado
   real de análise/verificação da consola; não declarar uma loja inexistente.
6. Depois dos testes reais e das configurações da conta, preparar build de produção
   com os IDs do proprietário, verificar o manifesto e testar exclusivamente com
   dispositivos de teste registados. Ativar anúncios pagos só após essa revisão.
   Nunca clicar nos próprios anúncios nem pedir cliques a testadores.

Não se pode garantir receita, preenchimento, eCPM ou data de aprovação. AdMob paga
segundo a sua elegibilidade, tráfego válido, condições e limiares de pagamento.
Nenhum contrato de patrocínio é necessário para usar a rede, mas a conta é.

## Comportamento implementado

- Banner 320x50 dp apenas no menu NEW GAME/LOAD GAME, depois do toque no splash.
  Reserva inferior de 64 dp com afastamento dos botões; oculto se não houver
  largura/altura seguras (mínimo 340x340 dp), removido ao sair do menu inicial.
  Carregamento assíncrono, sem bloquear o menu nem apresentar fullscreen no arranque.
- Intersticiais depois de um jogo terminado, ao tocar CONTINUE.
- Pelo menos três jogos concluídos e 180 segundos desde o arranque/último intervalo.
- Nada no splash, treino, oportunidades, intervalo do jogo ou ao sair. O único
  anúncio de arranque é o banner após o splash, nunca um fullscreen obrigatório.
- Um anúncio carregado só pode ser reservado/apresentado uma vez. Se falhar,
  não aparecer mais tarde no meio da jogabilidade. Fechar/falhar regressa ao menu.
- Sem rede, consentimento permitido ou anúncio disponível: continuar a jogar.
- Pré-carregamento assíncrono; no máximo nova tentativa após 60 s quando falha.
  Anúncios com mais de 55 minutos expiram. Não há loop de pedidos por frame.
- Estado/contadores locais por execução, sem enviar nome, carreira ou match key.
- Google UMP atualiza requisitos antes da inicialização de pedidos; só pede
  anúncios se canRequestAds permitir. Em erro sem permissão, falha fechado.
  Opções de privacidade só aparecem se o SDK indicar que são necessárias.
- Público inclui menores: TFCD=true, TFUA=true, UMP under-age=true, rating G,
  extras npa=1 e sem permissão AD_ID/Privacy Sandbox. Não recolhe datas de nascimento.
  Não alterar para publicidade personalizada silenciosamente.
- PRIVACY acessível antes de carregar a carreira e no menu principal, sem alterar
  saves, explica uso do SDK, dados e estado de teste. A página é informação da
  beta, não uma política pública final com todos os dados do responsável.

## Dados e permissões

SCORER não envia os nomes/carreiros ao SDK. O SDK Google pode tratar IP (incluindo
localização aproximada derivada), informações de app/dispositivo, diagnósticos e
interações com anúncios; não prometer ausência de dados só porque não há AD_ID.
A versão passa a usar a Internet para publicidade; o jogo mantém funcionamento
sem rede. A permissão AD_ID e as três permissões AdServices são removidas do
manifesto fundido. O manifesto inclui INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK,
FOREGROUND_SERVICE e a permissão interna de receiver assinada do AndroidX,
provenientes das dependências. Nenhuma permissão de localização/câmara/microfone.
Atualizar Data Safety/declaração de publicidade com os SDKs efetivamente usados
antes de submissão à loja; não reutilizar a declaração antiga sem rede.

## Como testar esta beta no telefone

1. Instalar por cima, abrir PRIVACY e confirmar a descrição de anúncios de teste.
2. Com rede, tocar no splash e observar o banner no rodapé do menu inicial,
   afastado dos botões. Consultar PRIVACY e observar o estado. Carregar/iniciar
   carreira deve remover o banner imediatamente.
   O UMP pode bloquear pedidos se a configuração da aplicação/consentimento não
   estiver disponível; a app deve continuar a funcionar, sem fingir que há anúncio.
3. Concluir pelo menos três partidas, com três minutos de execução; CONTINUE deve
   apresentar apenas um anúncio com indicação TEST se já houver um pronto.
4. Fechar/voltar e confirmar regresso ao menu, save e som/toques normais. Repetir
   offline: sem espera obrigatória ou bloqueio da carreira. Rodar e pôr em segundo
   plano durante carregamento e apresentação. Não usar IDs pagos nestes testes.
5. Falhas de apresentação/consentimento, retorno da Activity, performance/FPS e
   conteúdo precisam de validação Android real. Testes desktop não substituem isto.

## Fontes e alterações

API/modelo conferidos no repositório oficial Google:
https://github.com/googleads/googleads-mobile-android-examples/tree/eac5db1a64ff2858676c98889c275cef926e3ab6/java/admob/InterstitialExample
(app/build.gradle, MyActivity.java, GoogleMobileAdsConsentManager.java e manifesto).
O acesso direto a developers.google.com devolveu HTTP403 no ambiente; usou-se
este exemplo oficial via GitHub, não um SDK de terceiros. Dependências resolvidas
por Gradle nos repositórios oficiais com verificação TLS.

Código: advertising.py (limites/falhas), android/src/com/clemir/striker/ads/ScorerAds.java
(SDK/consentimento/ciclo de vida), android/manifest-extra.xml, buildozer.spec,
main.py (intervalo após resultado), menu_ui.py (privacidade).

# Auditoria de publicação Google Play — 31/10/2026

**Estado: ainda não pronto para submissão de produção.** A versão 0.6.45 tem
APKs de teste funcionais e verificados, mas faltam requisitos técnicos, de dados,
conteúdo e conta. Este relatório cobre **Scorer** (`com.clemir.striker`) e
**Scorer World** (`com.clemir.scorerworld`) separadamente. O EXE Windows não entra
na publicação Google Play.

Base auditada: commit `b97fcf453c2ed9e376517bffd54a778bc176dbb0`. As alterações
locais de competições/carreira ainda não concluídas não foram tratadas como
funcionalidades da versão entregue. Não houve acesso à Play Console, email
privado da Google, conta Cloudflare, chaves de assinatura ou administração do
laptop. As fontes oficiais abaixo foram consultadas nesta data. As três
validações específicas de configuração/manifesto executadas nesta auditoria
passaram; os 279 testes e verificações dos APKs são evidência prévia da 0.6.45,
não uma nova execução completa nem testes em aparelhos.

## Bloqueios e trabalho necessário

| Prioridade | Tema | Evidência atual | O que falta / aceitação |
| --- | --- | --- | --- |
| P0 | Identidade e privacidade pública | `release_settings.py` e configuração de exemplo têm nome, email e URL vazios; validação de produção devolve os três erros | Definir identidade pública e contacto, finalizar e alojar política HTTPS acessível sem login, região ou PDF; incluir link na app e Play Console. Identificar as duas apps, dados, finalidade, destinatários, segurança, retenção, eliminação e direitos |
| P0 | Estatísticas automáticas | Factory obrigatória, preferência antiga Off sobreposta; `App.on_start` transmite antes de qualquer aceitação. Splash tem só aviso curto; detalhes estão num menu | Documentar a base jurídica adequada, incluindo menores e utilizadores antigos. Verificar requisitos de divulgação destacada/consentimento aplicáveis antes da primeira transmissão. A ausência de nomes no payload não resolve o processamento de IP pelo fornecedor. O aviso atual não demonstra conformidade |
| P0 | Público infantil/misto | O público previsto inclui menores; não há controlos de adulto para publicar nomes | Definir faixas etárias verdadeiras por app; aplicar Families quando incluir crianças. Implementar gestão da funcionalidade social por adultos e ação de adulto antes de partilhar informação pessoal de crianças. Aviso de nickname/SHARE não verifica adulto. Não alterar artificialmente o público para contornar regras |
| P0 | Conteúdo público do leaderboard | Nomes de jogador e equipa são texto livre visível a outros; `safe_text` só limita formato/tamanho. Não há termos aceites, denúncia, bloqueio ou fila de moderação | Termos/regras de conteúdo aceites antes de publicar; denúncia dentro da app para conteúdo/utilizador, bloqueio adequado ao UGC público e identificadores públicos seguros para o suportar; ferramentas de moderação/remoção/bloqueio no servidor, operador e processo de resposta. Não expor token secreto para denunciar. Testar nomes ofensivos, contactos e tentativas de contorno |
| P0 | AABs de produção | Entregues APKs debug; AAB histórico 0.6.25 é de outro modelo comercial. CLI `tools/play/prepare.py` está retirada; `prepare_editions.py` força rehearsal | Completar staging de produção independente para Free e World, com identidade/ícone/idiomas/flags corretos e configurações públicas validadas; gerar AAB release novo de cada uma. Não usar o comando histórico retirado nem renomear APK para AAB |
| P0 | Assinatura e identidade | APKs usam certificado debug de QA. Não há upload key configurada nesta sessão | Configurar Play App Signing e upload key protegida, verificar certificado e versionCode não usado por pacote na Console, assinar e validar os AABs. `jarsigner -verify` sozinho não prova que a chave é a correta. Confirmar eventual existência dos pacotes na conta antes da primeira submissão |
| P0/conta | Verificação e acesso à produção | Estado da conta não consultável nesta sessão | Confirmar tipo/data da conta, verificações de identidade/contactos/dispositivo exigidas, declarações regionais/trader e tarefas pendentes na Console. Organização pode exigir D-U-N-S; monetização pode exigir perfil de pagamentos. Não inferir concluído por existir uma conta |
| P0/condicional | Teste fechado | Sem prova de acesso à produção para nenhum dos pacotes | Se for conta pessoal criada após 13/11/2023 abrangida pela regra: pelo menos 12 testadores inscritos continuamente durante 14 dias no teste fechado e posterior pedido de acesso à produção. Confirmar em cada app. Downloads de APK fora da Play e duas sessões do dono não substituem isto |
| P0 | Declarações Play | Inventário em rascunho; nada submetido/verificado na Console | Preencher Data Safety, público-alvo, IARC, publicidade e acesso à app para cada pacote; rever todas as tarefas de App content. Declarar sem anúncios e sem compras na app só nos artefactos finais verificados. Explicar ranking público e contagem automática |
| P1 | Passagem dos APKs QA para a Play | As instalações distribuídas usam chave debug; a assinatura de produção será diferente | Não prometer atualização direta com preservação de carreira entre certificados diferentes. Preparar e testar um percurso explícito de exportação/importação local ou outra migração segura antes de pedir aos testadores que desinstalem. Atualizações entre releases Play devem manter a identidade de assinatura |
| P1 | Traduções das divulgações | As três novas strings de aviso/título/estado automático não constam de nenhum dos oito catálogos não ingleses; fallback é inglês | Traduzir aviso, detalhes de dados, confirmação/remoção/termos e mensagens relevantes para as nove línguas suportadas no World; verificar compreensão, quebra de linhas e botões nas dimensões pequenas. Inglês é correto para a Free |
| P1 | Ficha e imagens de loja | Textos ainda em rascunho. Ícones atuais são RGB 1254×1254, maiores que 1 MB; não são os ficheiros finais de loja | Nome até 30 caracteres, descrição curta até 80 e completa até 4000; categoria/desporto, contactos e localizações coerentes. Exportar ícones 512×512 até 1024 KB no formato exigido; feature graphic 1024×500 sem alpha; pelo menos duas screenshots válidas e reais por ficha, mostrando as diferenças entre apps. Não usar capturas Windows como prova de Android. Vídeo promocional é opcional |
| P1 | Testes Android e Play | Assinatura, API36, ZIP/118 ELF 16KB e testes automatizados existentes; sem relatório de execução do AAB final pela Play nem teste 16KB em execução | Instalar pela faixa de teste os APKs que a Play gera do AAB; pre-launch report, aparelhos/resoluções e versões Android suportadas, incluindo execução 16KB. Testar toque/landscape, arranque, pausa/retoma, saves/atualização, offline/TLS, partida/época/promoção, ranking por divisão, publicação/remoção e SAF no World. Corrigir crashes, ANRs, incompatibilidades e sobreposições encontradas |
| P1 | Eliminação e suporte | Remoção dentro da app por token existe; perde-se a prova de posse ao limpar dados; não há apoio público definido | Verificar publicação/remoção reais com registo de teste acordado, recuperação/offline e pedido de suporte sem pedir segredos. Avaliar se identidade pública persistente configura conta na definição Play; se houver criação de conta, disponibilizar eliminação dentro da app E recurso web. Mesmo sem conta, explicar direitos e tratamento dos registos |
| P1 | Retenção e operação do servidor | Totais são podados só em novos POSTs; backup SQLite do instalador não tem expiração; v2 não tem TTL | Definir política para base ativa, backups, restauros e logs Cloudflare; implementar limpeza regular e não reintroduzir dados eliminados num restauro. Registos v2 ficam até remoção: dizer isso corretamente. Garantir laptop ligado, sem suspensão, serviço/túnel após reboot, atualizações, cópias protegidas, recuperação e contacto de incidentes |
| P1 | Preço e países | World é app separada, sem Billing; preço não ativado | Decidir se World será pago e os países de distribuição antes da oferta gratuita pública. A Google não permite converter a mesma app de gratuita para paga depois de oferecida gratuitamente. Uma app paga separada não exige adicionar compra dentro da Free. Confirmar perfil comercial/impostos quando aplicável |
| P1 | Exatidão e direitos | Licenças de dados/fontes incluídas; modelo de competições World continua provisório | Confirmar proveniência/direitos de toda a arte, ícones, marcas e textos; manter atribuições. Não prometer ligas/regulamentos reais completos, equipas licenciadas, anti-cheat, multiplayer ou funções ainda não entregues. Descrever resultados como auto-reportados |

P0 significa bloquear a preparação/submissão final enquanto não estiver resolvido
ou esclarecido; P1 também precisa de fecho antes do lançamento, mas pode avançar
em paralelo. Itens condicionais não são afirmações de que a conta está irregular.

## Estatísticas automáticas: avaliação precisa

A Google **não estabelece uma proibição geral de todos os contadores automáticos**,
nem a existência de um interruptor é, por si só, prova de conformidade. O pedido
do dono de remover o interruptor mantém-se; esta auditoria não voltou a ativá-lo.

A política User Data exige divulgação destacada e consentimento nos cenários de
dados pessoais/sensíveis fora da expectativa razoável. Também diz expressamente
que apps que usem outra base jurídica, por exemplo interesse legítimo no RGPD,
têm de cumprir os requisitos legais e as divulgações aplicáveis. Não se pode
escolher essa base só escrevendo-a numa política: é preciso avaliar necessidade,
proporcionalidade, direitos/oposição, contexto infantil e práticas do fornecedor.
Se a avaliação exigir consentimento ou possibilidade de oposição, o comportamento
de produção terá de respeitá-lo; um botão SHARE do ranking não cobre estatísticas.

Hoje o envio começa em `on_start`, e o aviso pequeno diz apenas que existem
contagens automáticas e remete para Privacy. Não detalha no fluxo inicial os
campos, finalidade e destinatário, nem espera qualquer escolha. Por isso **não
recomendo submeter a 0.6.45 tal como está** com a suposição de que o aviso resolve
User Data/Families. Falta fechar a avaliação e implementar o fluxo que dela resulte.

O payload dos contadores não tem ID individual, nome ou carreira. Já o ranking
usa um token persistente de autorização e nomes escolhidos que a Google inclui
na categoria de dados pessoais mesmo quando são nicknames. Tratar os fluxos
separadamente, sem declarar que a app não recolhe dados.

## Data Safety: mapa para preencher, não submissão automática

- **App interactions / analytics**: aberturas, fechos normais e atividade do jogo;
  recolha obrigatória na versão atual, não opcional. Avaliar também Diagnostics
  para contagens de falhas de gravação/carregamento; não há stack traces.
- **Name**: nome escolhido publicado opcionalmente; a definição Google inclui
  nickname. Equipa personalizada e resultados: considerar outros conteúdos
  gerados pelo utilizador/atividade conforme formulário atual.
- **Identificadores**: classificar corretamente o token persistente do ranking
  perante as definições de User IDs/Device or other IDs; token aleatório não
  autoriza marcar todos os identificadores como ausentes. Não é token admin.
- **IP/Cloudflare**: confirmar configurações e dados tratados/retidos pelo
  fornecedor. Não declarar localização aproximada só por usar rede: verificar
  se existe inferência geográfica. Também não omitir inferência real se existir.
- **Collected/shared/ephemeral**: transmissão fora do dispositivo entra na análise.
  Processamento efémero deve ser indicado no formulário quando aplicável;
  agregados retidos 90 dias não são simplesmente efémeros. Há exceções à definição
  de sharing para prestadores e ações iniciadas pelo utilizador: verificar as
  condições, sem automaticamente classificar Cloudflare/publicação como venda.
- **Segurança/eliminação**: HTTPS verificado está implementado. Publicação tem
  remoção por token; totais combinados não permitem separar contribuição pessoal.
  Explicar retenção e suporte. Não prometer eliminação de registos públicos só
  por desinstalar. Não existe login email/password nem upload de carreira.
- **Ads = No**, **in-app purchases = No** para os artefactos finais sem esses SDKs.
  A eventual compra da app World na loja é distinta de uma compra dentro da app.

Usar [inventário](DATA_SAFETY.md) e [rascunho da política](PRIVACY_POLICY_DRAFT.md)
como base. Não há declaração final preenchida ou aprovada nesta sessão.

## O que já existe e não precisa de recomeçar

- Código original Python/Kivy; dois pacotes e saves independentes; sem anúncios,
  SDK de publicidade/UMP/Billing ou permissões de localização/câmara/microfone.
- Target **API36**, mínimo26, arm64; a fonte oficial consultada exige API36 para
  apps novas e atualizações desde 31/08/2026.
- APKs 0.6.45 com assinatura debug consistente e alinhamento ZIP/118 ELF 16KB
  verificado. Isto não valida automaticamente um AAB futuro ou execução em 16KB.
- HTTPS com validação de certificado, política de rede sem cleartext e sem backup
  Android; carreiras locais e fila offline de contagens.
- Consentimento e retirada independentes para o ranking; recordes de épocas
  terminadas e divisões, sem converter golos parciais em recordes finais.
- Servidor do dono já está acessível: leitura pública `/health` **200**, v2 Free
  **200/schema2**, `/v1/totals` sem token **404** em 31/10/2026. Nenhum evento ou
  nome de teste foi enviado nesta auditoria, nenhum total foi alterado. A rota
  `/privacy` devolveu404 e nenhuma URL pública de política está configurada;
  isso não prova que não exista outra página do dono noutro endereço.
- Ferramentas de assinatura e inspeção existem. Precisam de integração e
  validação final; ter scripts não equivale a ter uma release de produção.

## Acesso dos revisores e operação de lançamento

O jogo não exige login SCORER. Nas instruções App access explicar criação de
jogador/contrato, treino/partida e localização do leaderboard/Privacy, incluindo
que partilhar nomes é opcional e requer época concluída para haver recorde. O
painel privado `/admin` é uma ferramenta do operador, não um login necessário
para jogar: **não fornecer o token administrativo à Google nem colocá-lo no
pacote**. Manter backend/túnel disponíveis durante revisão e testes.

Para World pago, concluir configuração comercial/países e acesso dos testadores
pela Play; não adicionar o antigo Billing por inferência. Preparar notas de
versão, contactos de suporte, monitorização Android vitals e procedimento de
correção/halt após lançamento. A submissão só deve usar uma revisão escolhida,
com testes repetidos se incluir as alterações de competições ainda locais.

## Sequência recomendada

1. **Em paralelo:** confirmar conta/teste fechado e dados públicos do responsável;
   fechar público-alvo/base de tratamento e requisitos infantis.
2. Implementar termos, denúncia/bloqueio/moderação, controlos adultos e o fluxo de
   divulgação de dados exigido; traduzir as mensagens World. Validar no servidor.
3. Publicar política e suporte; acertar retenção/backups/eliminação e Data Safety.
4. Completar staging de produção para os dois pacotes; escolher preço World,
   preparar artes/textos e gerar AABs com versão e assinatura adequadas.
5. Teste interno pela Play, pre-launch/aparelhos/16KB e correções. Iniciar/manter o
   teste fechado quando aplicável; guardar feedback e evidência de uso real.
6. Fechar formulários por app, pedir acesso à produção se necessário, rever o
   artefacto exato e obter aprovação do dono para submissão/rollout.

Se os 12 testadores exigidos começassem todos em **31/10/2026**, os 14 dias
completariam, no mais cedo, em **14/11/2026 à mesma hora**. A seguir ainda existe
pedido de acesso/revisão; isto não é uma data de aprovação garantida. Se o
requisito já estiver cumprido ou não se aplicar, não há razão para reiniciar o
prazo por esta auditoria. O prazo antigo de 06/11 não pode ser prometido para Play.

## Fontes oficiais consultadas

1. [Target API](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en).
2. [Testes de contas pessoais](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).
3. [User Data, divulgação, privacidade e eliminação](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en).
4. [Families, dados de crianças e funcionalidades sociais](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en).
5. [Conteúdo gerado por utilizadores](https://support.google.com/googleplay/android-developer/answer/9876937?hl=en).
6. [Data Safety e definições](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en).
7. [Ícones, screenshots e imagem de destaque](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en).
8. [Identidade e informações da conta](https://support.google.com/googleplay/android-developer/answer/13628312?hl=en).
9. [Classificação de conteúdo](https://support.google.com/googleplay/android-developer/answer/9859655?hl=en).
10. [App content e instruções de acesso](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en).
11. [Suporte de páginas16KB](https://developer.android.com/guide/practices/page-sizes).
12. [Preço gratuito/pago](https://support.google.com/googleplay/android-developer/answer/6334373?hl=en).

Manifesto de fontes e verificações objetivas em [evidence](evidence/). Este é um
relatório de engenharia e preparação, não aprovação Google nem parecer jurídico.

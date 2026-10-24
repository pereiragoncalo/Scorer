# Current owner correction — 0.6.26

Free has no country choice: new games start in Scorer League. Existing Free careers
retain their current single league. A World purchase unlocks a separate World career
inside the same app, not a conversion of the Free career. Free stays Free even when
World is owned. Slots, players, training, calendars, aliases and backups are separate;
mode changes save first, and a failed save blocks switching. No Free progress is
imported into World. Owners can return to their Free slot; starting/loading a career
is always explicit. World alone suggests the phone's country and England Division4.
Earlier 0.6.25 Free-to-World transfer text is superseded. Billing remains disabled.

# Current decision — 0.6.25: one application with a World purchase

The owner explicitly replaced the earlier separate-app model. Ship only
com.clemir.striker: Free has one chosen division, and a one-time, non-consumable
Google Play product scorer_world_upgrade unlocks World, the local name editor
and ad-free play inside the same installation. Preserve existing Free career,
player identity, fixtures, progress and private saves when upgrading. No subscription
or external payment link. Existing World Preview APKs are historical test tools.

Billing is prepared but disabled. Google Play price/confirmation, purchase query,
pending/cancelled handling, Restore purchase, server verification/acknowledgement
and signed seven-day offline licence are implemented. Service deployment, owner
configuration, real Play tester/device/refund tests and explicit activation approval
remain pending. See [Play preparation](play/README.md). Sections below are history
and do not override this decision.

# Atualização 0.6.24 — World e Upgrade em teste

A pedido do proprietário, Free ganha HELP e UPGRADE informativo. Novas carreiras
sugerem contratos pelo locale do telefone, ou England Division4; Free mantém uma
única divisão por carreira. World é uma aplicação separada/ad-free, com editor
local de clubes/ligas/jogadores e importação JSON passiva com pré-visualização.
A prévia TESTE World tem 212 regiões, 758 divisões ficcionais, sem compras. Não
é uma reprodução de todas as divisões regionais reais. A carreira Free fica
preservada na sua aplicação; não há migração automática nem cobrança nesta fase.
UPGRADE explica e pode abrir a prévia instalada com assinatura correspondente.
Preço, licença/distribuição de produção e publicação paga exigem validação e
aprovação; a versão World Preview está deliberadamente aberta para testes.
Ver docs/WORLD_0.6.24.md. As proibições históricas de botão World/Upgrade abaixo
ficam substituídas por esta decisão; não existe desbloqueio de pagamento em Free.

# Atualização 0.6.22 — publicidade de rede

O proprietário pediu integração para receita sem contratos diretos e confirmou
público geral incluindo menores, sem conta AdMob ainda. AdMob nativo de TESTE
é agora permitido, separado dos painéis. Sem receitas reais nesta beta; conta,
IDs próprios, aprovação, política pública e testes Android pendentes. Limites de
frequência, tratamento infantil/não personalizado e UMP em docs/ADMOB_SETUP.md.
A restrição anterior a apenas painéis/sem AdMob abaixo é histórica e fica
substituída por esta decisão. FREE continua com uma divisão e sem pagamentos.

# Striker — direção confirmada pelo proprietário

## Decisão de produto

- **Striker gratuito:** aplicação básica, uma única divisão jogável, clubes e
  jogadores fictícios. Receita exclusivamente de publicidade nas bordas do campo.
  Sem compras, subscrições ou botão de desbloqueio World nesta aplicação.
- **Striker World:** segunda aplicação, paga, com divisões do mundo inteiro,
  nomes fictícios por defeito e editor com importação local de nomes fornecidos
  pelo utilizador. Identificador Android, distribuição e carreira separados;
  partilha do motor Python/Kivy. Nenhuma compra real é ativada nesta fase.
- Não incluir nomes oficiais, emblemas oficiais ou pacotes de nomes reais no
  produto distribuído. Não descarregar conteúdos da Internet por omissão.
- Publicidade mantém a opção já definida: painéis locais de patrocínio direto,
  sem AdMob, trackers ou interrupções da simulação. Patrocínios reais e publicação
  pública continuam sujeitos à aprovação explícita do proprietário.

## Entrega desta etapa: 0.6.2 FREE

Menus Kivy responsivos com texto multilinha, botões de toque, listas e tabelas
com deslocação, navegação fixa e confirmação para guardar/sair. O jogo original,
a carreira e os saves mantêm-se. O editor e acesso World não aparecem no menu
FREE; a proteção no encaminhamento de ações também impede abrir o editor nessa
edição. O contrato de entitlement existente é preservado para trabalho futuro,
sem um flag local ou alteração do save capaz de transformar FREE em WORLD.

O editor local existente tinha uma referência inválida a current_club; corrigida
para club e testada a gravação/restauro. Essa correção não constitui o editor de
importação mundial, que permanece uma tarefa própria da aplicação paga.

## Trabalho seguinte, sem promessas de funcionalidades inexistentes

1. Confirmar 0.6.2 no telemóvel: menus, deslocação, textos longos, toque, sair e
   recuperar a carreira. O proprietário reportou que 0.6.1 executa sem crashes;
   isso não substitui testes da nova interface.
2. Integrar e testar painéis fictícios offline na aplicação gratuita.
3. Preparar projeto/package separado para World, sem cobrar antes da aprovação.
4. Completar profundidades de divisões fora da Europa. O motor atual contém
   apenas uma divisão em muitos países, pelo que ainda não satisfaz "todas as
   divisões do mundo".
5. Editor World: definir identificadores estáveis de clubes/competições e aliases
   de apresentação; importar JSON UTF-8 local, com tamanho e esquema limitados,
   validação de nomes e pré-visualização. Nunca executar scripts, macros ou URLs.
   Guardar cópia antes de aplicar; rejeitar entradas inválidas sem aplicação
   parcial. Não alterar chaves de carreira/estatísticas com aliases visuais.
6. Testar exportação/restauro das edições separadas; decidir mais tarde a eventual
   transferência de carreira FREE → World sem sobrescrever a carreira existente.

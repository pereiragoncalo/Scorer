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

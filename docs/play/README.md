# Publicação Google Play — Scorer e Scorer World

**Estado atual: 0.6.45 é QA, ainda não é release de produção.**
Ver [auditoria de 31/10/2026](PUBLISHING_AUDIT_2026-10-31.md) para a lista atual
priorizada, evidências, fontes oficiais e dependências da conta.

São duas aplicações independentes: Free `com.clemir.striker`, World
`com.clemir.scorerworld`. Sem anúncios ou compras dentro da aplicação.
World pode vir a ser uma app paga na loja; preço/distribuição dependem do dono.
Ambas usam contadores agregados automáticos e ranking público opcional.
Não reutilizar as declarações do antigo modelo de app única com AdMob/Billing.

## Materiais atuais

- [Auditoria e ordem de execução](PUBLISHING_AUDIT_2026-10-31.md).
- [Inventário Data Safety](DATA_SAFETY.md), ainda sem submissão na Console.
- [Política de privacidade](PRIVACY_POLICY_DRAFT.md), ainda rascunho sem dados públicos.
- [Textos de loja](STORE_LISTING.md), ainda sem pacote final de imagens Android.
- [Artefactos QA 0.6.45](../AUTOMATIC_0.6.45_artifacts.json).

## Ferramentas existentes e limites

`tools/prepare_editions.py` prepara cópias isoladas **QA/rehearsal** para Free e
World. Não é ainda um caminho completo de staging de produção; falta integrar
configuração pública validada e canal production por edição. O CLI antigo
`tools/play/prepare.py` foi retirado: não seguir comandos históricos que o invocam.
A função de validação ainda é usada pelos testes e staging.

`tools/play/sign_aab.sh` assina um AAB existente com upload key protegida; não cria
chave nem publica. `tools/play/verify_bundle.sh` verifica AAB e APK derivado para
`free|world`; a opção production não prova chave, aceitação Play, consentimento,
flags compiladas ou testes reais. Verificar essas condições separadamente.

Antes de usar estas ferramentas numa submissão: resolver os bloqueios da
auditoria, gerar AAB final de cada pacote, confirmar Play App Signing/versões,
instalar através da Play e testar. Nunca colocar chaves, passwords, tokens admin
ou credenciais do servidor na app, configuração pública ou Git.

## Documentação histórica

[READINESS_0.6.25.json](READINESS_0.6.25.json) e relatórios de versões anteriores
registam o que se fez nessa altura. O AAB 0.6.25, instruções de compras/AdMob e
preferências default-off não representam a versão atual e não servem para
submissão dos dois produtos. O relatório 0.6.43 também antecede a confirmação
de servidor v2 online e a recolha automática da 0.6.45.

Esta preparação não faz uploads, pagamentos ou rollout. Submissão e publicação
exigem aprovação do dono sobre a release concreta pronta para revisão.

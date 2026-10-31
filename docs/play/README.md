# Publicação Google Play — Scorer e Scorer World

**Estado atual: 0.6.46 prepara a publicação; os gates externos continuam pendentes.**
Ver [auditoria de 31/10/2026](PUBLISHING_AUDIT_2026-10-31.md) para a lista atual
priorizada, evidências, fontes oficiais e dependências da conta.

São duas aplicações independentes: Free `com.clemir.striker`, World
`com.clemir.scorerworld`. Sem anúncios ou compras dentro da aplicação.
Ambas as apps serão gratuitas, por decisão do dono.
Ambas usam contadores agregados automáticos e ranking público opcional.
Não reutilizar as declarações do antigo modelo de app única com AdMob/Billing.

## Materiais atuais

- [Auditoria e ordem de execução](PUBLISHING_AUDIT_2026-10-31.md).
- [Inventário Data Safety](DATA_SAFETY.md), ainda sem submissão na Console.
- [Política de privacidade](PRIVACY_POLICY_DRAFT.md), ainda rascunho sem dados públicos.
- [Textos de loja](STORE_LISTING.md), ainda sem pacote final de imagens Android.
- [Artefactos QA 0.6.45](../AUTOMATIC_0.6.45_artifacts.json).

## Preparação atual0.6.46

[Trabalho concluído e dependências externas](RELEASE_0.6.46.md),
[atualização do laptop](SERVER_0.6.46.md) e
[base jurídica para revisão](LEGAL_BASIS_REVIEW.md).
Conta ativa/verificada confirmada pelo dono. Responsável Gonçalo Pereira,
goncalo@clemir.com. Ambas as apps gratuitas e destinadas também a menores.

O caminho por edição suporta agora `--channel production --config release.local.json
--publication-config publication.local.json`. Os flags de revisão só podem ser
preenchidos com factos revistos pelo operador. O CLI antigo continua retirado.

```sh
python tools/prepare_editions.py --edition free --channel rehearsal --output /workspace/scorer-free-aab
python tools/prepare_editions.py --edition world --channel rehearsal --output /workspace/scorer-world-aab
```

Compilar release AAB sequencialmente com tools/android/run.sh e tools/build_android.py.
Para produção, completar os ficheiros públicos de exemplo em release/, confirmar
versionCode por pacote, política live e revisões pendentes. Assinar o AAB final
com tools/play/sign_aab.sh e a upload key protegida do dono. Verificar com
tools/play/verify_bundle.sh, passando free|world. O canal production exige
SCORER_UPLOAD_CERT_SHA256 confirmado na Console e rejeita o certificado debug.
Não colocar chaves/passwords/tokens na app, Git ou configuração pública.

Os APKs de inspeção derivados de AAB continuam assinados com a chave debug para
QA: não são a assinatura de produção nem um teste Play real. Os scripts não
fazem uploads/rollout e não substituem revisão legal, aparelhos ou Play Console.

## Documentação histórica

[READINESS_0.6.25.json](READINESS_0.6.25.json) e relatórios de versões anteriores
registam o que se fez nessa altura. O AAB 0.6.25, instruções de compras/AdMob e
preferências default-off não representam a versão atual e não servem para
submissão dos dois produtos. O relatório 0.6.43 também antecede a confirmação
de servidor v2 online e a recolha automática da 0.6.45.

Esta preparação não faz uploads, pagamentos ou rollout. Submissão e publicação
exigem aprovação do dono sobre a release concreta pronta para revisão.

# Primeira tarefa para Codex: validar a versão Android original

Trabalha **nesta app Kivy existente** (`main.py`, base Striker-P0-05-v006). Não uses o Striker web, não mudes de motor, não reescrevas os sistemas de carreira.

Objetivo imediato: produzir um caminho de compilação Android reproduzível e identificar/corrigir os problemas que impedem um APK instalável. Antes de introduzir publicidade, faz o seguinte:

1. Audita a estrutura, as dependências e o ficheiro `buildozer.spec`. Valida a compatibilidade do Kivy/Buildozer/python-for-android com target API 36, arquitetura arm64-v8a e requisitos de 16 KB page size aplicáveis.
2. Executa `python3 -m py_compile main.py` e adiciona um conjunto mínimo de testes sem interface para a carreira/free/entitlements/saves. Evita efeitos colaterais indesejados ao importar o módulo.
3. Corrige a persistência Android: `CareerMode.save_path` grava junto a `__file__`; passa a usar diretório gravável da aplicação no Android, com migração segura e comportamento desktop/teste preservado. Testa gravação e recuperação.
4. Substitui o nome pessoal predefinido no jogo por nome fictício/genérico, sem afetar saves existentes.
5. Prepara um comando/documentação fiável para compilar APK debug localmente, depois AAB release. Não digas que compilou se não houver SDK/NDK.
6. Documenta logs dos comandos executados, resultados, alterações e bloqueios em `docs/BUILD_LOG.md`.

Conclui apenas esta fase antes de integrar painéis. Entrega resumo dos ficheiros alterados, testes e próximos passos. Não publiques, não atives pagamentos ou patrocínios reais.

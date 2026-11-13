# Scorer 1 — redes deformáveis e simulador

Implementação exclusiva do Scorer 1, em Python/Kivy, sem motor físico externo.
A deteção de golo, os remates, as colisões físicas da bola, os resultados e a
carreira mantêm-se. A perspetiva lateral foi extraída sem mudar os cálculos.

## Arquitetura e ficheiros

| Ficheiro | Responsabilidade |
|---|---|
| `net_cloth.py` | Partículas, geometria com folga, costuras soldadas, fixações, molas estruturais/cisalhamento, Verlet, limites, amortecimento e repouso |
| `net_render.py` | Malha quadrada/hexagonal, interpolação da malha física, `Mesh` e índices reutilizados; fios locais à frente da bola |
| `net_presentation.py` | Adaptador entre o jogo e a simulação, sem escrever no objeto `Ball` ou no resultado |
| `goal_projection.py` | Projeção lateral original, partilhada com o simulador |
| `main.py` | Captura da velocidade de impacto, atualização a passo fixo, reinício por remate e desenho |
| `goal_nets.py` | Mantém os estilos atribuídos aos estádios; acrescenta densidade de malha configurável |
| `tools/net_lab/` | Simulador, presets, referência JSON e medição CPU; excluído do pacote de produção |
| `tests/test_net_cloth.py`, `ui_tests/test_net_cloth.py`, `ui_tests/test_net_lab.py` | Física, repetibilidade, regressões de jogo, renderização e controlos reais |
| `tools/play/prepare.py`, `tests/test_sprite_payload.py`, `tools/verify_sprite_apk.py` | Exclusão do laboratório e verificação dos módulos realmente empacotados |

Os três painéis partilham partículas nas costuras. Postes/trave, base e suportes
apropriados a cada geometria mantêm restrições. A geometria de repouso já inclui
folga e sag sob gravidade; o integrador calcula perturbações em torno desse
estado carregado. Molas e restrições distribuem o impulso local e limitam a
extensão. A simulação usa 1/120 s, limita subpassos e adormece após estabilizar.

O Android usa 218 partículas na caixa / 223 no véu; o perfil Windows usa a
resolução fina de 446 / 453. É o mesmo algoritmo em ambas. O laboratório permite
escolher `mobile` ou `full`; não existe uma segunda física de demonstração.
A densidade gráfica também baixa quando a baliza ocupa poucos píxeis.

O impacto é alimentado pelo contacto original, posição e velocidade da bola,
**apenas depois de um golo legal**. Uma curta apresentação cinemática pós-golo
acompanha a malha, mantendo a esfera no lado interior e mostrando parte dos
fios à frente. A posição/velocidade físicas e a decisão do jogo não são alteradas.
A malha continua a recuperar também entre oportunidades, sem ficar congelada.

## Parâmetros

Em `NetConfig`, partilhado integralmente pelo jogo e pelo simulador:

| Parâmetro | Valor inicial | Efeito |
|---|---:|---|
| `net_slack` | 0.20 | Folga/sag da geometria de repouso e reserva antes da tensão |
| `net_stiffness` | 24 | Retorno elástico à geometria carregada |
| `net_damping` | 3.4 | Dissipação progressiva |
| `net_gravity` | 9.81 | Sag do estado de repouso carregado |
| `net_impact_scale` | 0.48 | Transferência do impulso local |
| `net_max_stretch` | 1.90 | Limite numérico de extensão das ligações da malha grosseira |
| `net_wave_propagation` | 48 | Acoplamento/tensão entre vizinhos |
| `net_settle_threshold` | 0.0025 | Limiar de repouso; depois deixa de simular |

Os parâmetros são limitados e validados. O limite das ligações é um parâmetro da
aproximação grosseira, não uma medição de deformação real do fio de nylon.

## Executar o simulador

Na raiz do repositório, com o ambiente Python/Kivy já utilizado pelo Scorer:

```bash
python tools/net_lab/main.py
python tools/net_lab/main.py --structure veil --mesh hexagon
python tools/net_lab/main.py --resolution full
python tools/net_lab/main.py --config tools/net_lab/near-post-reference.json
```

Não abre carreiras nem instancia o jogo. Não aparece nos menus normais.
A coluna de controlos tem scroll: depois dos controlos de força/ângulo/posição
estão os oito parâmetros, comparação A/B e guardar/carregar JSON. Os parâmetros
alterados são aplicados ao disparar novamente. Os perfis A/B e JSON guardam a
configuração selecionada; não modificam definições dos jogadores.

Controlos: **FIRE / REPEAT**, **RESET NET**, **PAUSE / PLAY**, **STEP 1/120**,
velocidade `1.0` / `0.5` / `0.25`, malha técnica e captura de ecrã. Para avançar
manualmente, pausar primeiro. A velocidade de reprodução altera quantos passos
são executados por segundo de reprodução, sem alterar os parâmetros físicos.

Presets:

- Near Post Strong, Near Post Medium, Near Post Weak
- Far Post Strong
- Center Strong
- Top Corner
- Low Shot

O primeiro é a referência principal. `u` e `v` permitem deslocar o impacto no
painel selecionado; força, yaw e pitch controlam velocidade/direção. Os remates
são determinísticos; não utilizam o RNG da carreira.

## Exportar e comparar

```bash
python tools/net_lab/main.py --view-only --capture /tmp/net-normal --frames 360
python tools/net_lab/main.py --view-only --playback .25 --capture /tmp/net-slow --frames 360
python tools/net_lab/benchmark.py --output /tmp/net-benchmark.json
```

As sequências PNG e `metrics.json` ficam na pasta indicada. Para criar vídeo,
**apenas no ambiente de desenvolvimento** com ffmpeg já disponível:

```bash
ffmpeg -framerate 60 -pattern_type glob -i '/tmp/net-normal/frame-*.png' \
  -c:v libx264 -pix_fmt yuv420p /tmp/net-normal.mp4
```

Não há ffmpeg, exportador ou dependências adicionais no APK/AAB.

Evidência em `docs/data/deformable_nets_1030016/`:

- `near-post-normal.mp4`: contacto, bolsa, oscilações e recuperação a 100%.
- `near-post-quarter-speed.mp4`: aproximação e bolsa a 25%.
- `contact.png`, `pocket.png`, `secondary.png`, `recovered.png`.
- `stiffer-pocket.png`: comparação com material mais rígido/amortecido.
- `simulator.png`: interface real do laboratório, com a vista limitada à sua área.
- `benchmark-mobile.json`: medições e resultados de todos os presets.

As sequências de contacto/máxima extensão/recuperação foram inspecionadas; foram
gerados vídeos normais e lentos para avaliação. Isto não substitui avaliação no
telemóvel nem certifica que o efeito seja indistinguível de uma rede real.

## Validações executadas e limites

```bash
python -m unittest tests.test_net_cloth tests.test_career \
  tests.test_finishing_balance tests.test_sprite_payload -q
PYTHONPATH=ui_tests:. python -m unittest ui_tests.test_net_cloth \
  ui_tests.test_net_lab ui_tests.test_training_nets ui_tests.test_goal_geometry \
  ui_tests.test_mesh_limits ui_tests.test_finishing_balance \
  ui_tests.test_retro_sprites ui_tests.test_opportunity_sequences -q
```

Foram executados 58 testes da lógica/empacotamento e 30 nativos Kivy. Incluem os
sete presets nas duas geometrias, forças, fixações, recuperação completa, estados
finitos, impactos repetidos, costuras, JSON, A/B, pausa/passo, 30/60/120 FPS e
100/50/25%, projeção original, caches, redimensionamento, 120 redesenhos sem acumular grupos e limites de índices. Vinte pares de jogadas
(40 trajetórias físicas) com a apresentação ligada/desligada tiveram os mesmos
estados físicos da bola, golos e pontos de passagem pela linha.

No host Linux x86_64, o preset forte móvel atingiu ~1.00 m na caixa e ~1.11 m no
véu, adormecendo cerca de 4.2 s após o disparo. A mediana CPU foi ~1.16–1.30 ms por
passo de 1/120 s; inclui a leitura de métricas do laboratório. Não é uma medição
de FPS Android nem do custo total do jogo/GPU.

AAB 1030016 compilado e auditado separadamente; o laboratório não foi incluído.
Os 248 frames/35 folhas originais dos sprites mantiveram-se intactos. As dimensões
Windows foram testadas no Kivy do Linux; não foi executado um binário Windows
nativo nem feito um teste físico de Android. Os 60 FPS em hardware modesto
continuam por validar num aparelho real.

O modelo é uma aproximação visual de baixa resolução: não simula cada fio,
autocolisões ou fricção detalhada entre fio e bola. A trajetória física original
mantém-se como fonte de verdade; a interação visual pós-golo não constitui um
segundo motor de resultados. Os parâmetros podem continuar a ser afinados com
o laboratório, sem alterar carreiras ou regras.

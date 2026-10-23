# SCORER 0.6.3 — auditoria e correções

## Âmbito
Original Python/Kivy: menus, painel de jogo, gravação/recuperação, identidade da aplicação e pacote Android. Não é uma auditoria externa de segurança nem garante ausência de todos os bugs.

## Problemas corrigidos
- **Texto e botão sobrepostos no resultado:** o painel Canvas tinha coordenadas fixas. Substituído por widgets Kivy com texto multilinha, área deslocável e ação de pelo menos 52 dp. A oportunidade usa o mesmo componente. O cenário mantém o motor original.
- **Sair na localização errada:** removido do jogo e dos submenus; disponível apenas no menu principal/primeiro contrato. Mantida confirmação e gravação antes de fechar; falha de gravação impede o fecho.
- **HUD demasiado pequeno:** marcador e rodapé usam dimensões em dp e largura disponível. Nomes longos ficam limitados à área reservada, mesmo quando ultrapassam a largura no tamanho mínimo de fonte.
- **Save malformado:** dados incompletos podiam alterar parcialmente a carreira; mapas inválidos causavam AttributeError e valores NaN eram aceites. Leitura isolada, validação dos tipos principais e dos limites de energia/moral; erros preservam o estado anterior e o ficheiro original.
- **Identidade:** título visível SCORER e splash original em inglês, jogador a rematar, crédito discreto «clemir». Presplash Android usa FIT_CENTER para conservar a imagem inteira. Divisão gratuita predefinida passa a «Divisão Scorer»; nomes personalizados guardados mantêm-se.

## Compatibilidade
Mantidos applicationId `com.clemir.striker`, nome do save e esquema 2: instalar como atualização da beta anterior. Não desinstalar para atualizar. FREE continua com uma divisão, sem pagamentos, telemetria ou permissões Android solicitadas. Não foram adicionadas dependências.

## Verificação
- 21 testes de carreira/build/segurança e 10 testes Kivy reais: aprovados.
- Menus em seis tamanhos, fontes ampliadas, painel final em 640×360, 960×540 e 1280×589, nomes extensos, continuidade para carreira, localização de Sair e saves danificados.
- Captura real da janela Kivy do painel final inspecionada; não é uma captura Android.
- APK debug compilado realmente; assinatura, alinhamento ZIP 16 KB e 118 binários ELF AArch64 verificados.

## Limitações e próxima tarefa
A versão 0.6.3 precisa de instalação e teste no telemóvel do proprietário: splash, menu, treino, oportunidade, fim de partida e fecho/reabertura da carreira. Não há telemóvel ligado ao ambiente. Esta beta não é APK release/AAB nem foi submetida à Play Store. Assinatura de distribuição e allowBackup da versão release continuam pendentes. Auditoria de desempenho, todos os estados de remate e a matriz de aparelhos continuam no roteiro.

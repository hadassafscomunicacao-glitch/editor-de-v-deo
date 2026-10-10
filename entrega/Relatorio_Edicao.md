# Relatório de edição — "O elevador do conflito"

Gerado em 10/10/2026. Todos os tempos abaixo se referem ao **vídeo final** (mm:ss), salvo indicação.

## 1. Material de origem

- Arquivo `IMG_0623.MOV` (exportado do CapCut): 20:45,2 · 1080×1920 vertical (9:16) · 30 fps · HEVC 8 bits BT.709 · áudio AAC estéreo (dual-mono) 44,1 kHz.
- Plano fixo com as duas apresentadoras lado a lado: **Indira Matos** à esquerda (blazer azul) e **Hellen de Paula** à direita (blusa bege, óculos). Há uma inserção de 2 s de uma segunda câmera em 01:02–01:04 do bruto.
- Imagem: cortina cinza-média (≈ 30% de luminância) com pouca separação do primeiro plano, leve dominante quente, rostos com pouco contraste.
- Áudio: fala limpa (ruído de fundo abaixo de -70 dBFS), abafada acima de 3 kHz, -17,3 LUFS, alguns picos em 0 dBFS; a Hellen estava 2,6 LU mais baixa que a Indira.
- 20 cortes manuais já existentes foram detectados por diferença de quadros (sobretudo na primeira metade), e as emendas foram revisadas.

## 2. Transcrição e revisão da fala

- Transcrição local com marcação de tempo por sílaba: NVIDIA Parakeet TDT v3, com Silero VAD para segmentação e Whisper large-v3 para checagem cruzada dos trechos duvidosos.
- Identificação de quem fala: impressões vocais (WeSpeaker) agrupadas em dois locutores e confirmadas pelo movimento da boca de cada uma no vídeo.
- Revisão por 5 "editores de diálogo" (um por trecho de ~4 min). Em seguida, 5 revisores adversariais reouviram cada corte proposto com uma sonda de áudio (re-transcrição e energia a cada 10–20 ms) e tentaram refutá-lo. Só entrou o que passou nessa checagem.
- A fala real difere bastante do roteiro: as apresentadoras improvisaram, mudaram a ordem e incluíram dados, um teste com 4 perguntas e a oferta "Experiência Cultura em Ação". **A edição segue o que foi dito, não o roteiro.**
- A transcrição revisada está em `Projeto_Editavel/dados/transcricao_final.md`.

## 3. Cortes de fala

Duração: 20:45,2 (bruto) → **20:36,3** (final). Foram removidos 8,9 s em 15 intervenções, todas com emenda ajustada ao quadro de vídeo e ao ponto mais silencioso do áudio (deslocamento máximo de 20 ms, com crossfade de 12 ms).

| Final | Bruto | Tipo | O que saiu | Como ficou |
|---|---|---|---|---|
| 00:34,0 | 00:34,0 | resíduo de emenda anterior | murmúrio de ~50 ms deixado por um corte já existente | "…nem sabia que estava insatisfeito. Primeiro, eu quero te tranquilizar, tá?" |
| 02:53,1 | 02:53,2 | hesitação | "hum" (pausa preenchida de 0,2 s) | "…onde existe problema de gente: pessoas do mesmo setor que não se entendem" |
| 02:56,7 | 02:57,0 | palavra interrompida | "estabelec…" antes de "bem estabelecida" | "uma regra que não foi bem estabelecida" |
| 03:29,1 | 03:29,9 | reinício de frase | "vai para o R…" | "Do líder, sobe para o RH" |
| 04:58,2 | 04:59,8 | correção imediata | "problema, esse" | "Quando esse conflito sobe esse elevador…" |
| 10:15,0 | 10:17,4 | pausa encurtada | pausa de 0,82 s → ~0,4 s | "…sustentada aqui. Através da normativa" |
| 10:38,7 | 10:41,6 | correção imediata | "isso," | "E quando essa situação na sua empresa não muda…" |
| 11:14,2 | 11:17,5 | resíduo de emenda anterior | fragmento "Tu" de ~80 ms antes de um corte já existente | "…sobre o diagnóstico. Tudo começa…" |
| 12:32,8 | 12:36,3 | reinício de frase | "porque a gente tem um caminho" | "com o diagnóstico na mão, a gente tem aí um caminho para um tratamento mais adequado" |
| 13:11,9 | 13:16,5 | repetição | "da" em "parte da das" | "…muito pulada por grande parte das empresas" |
| 14:02,3 | 14:07,1 | reinício de frase | "Por isso que ele" | "…para o colaborador, né? Nas nossas implementações…" |
| 16:20,8 | 16:26,4 | reinício de frase | "As pessoas." | "E o que acontece, gente? O mercado hoje…" |
| 17:48,6 | 17:54,8 | reinício de frase | "Se o seu primeiro não," | "Esse primeiro não em alguma dessas perguntas é o seu ponto de partida" |
| 18:30,1 | 18:38,1 | pausa encurtada | pausa de 1,26 s → ~0,65 s (transição de bloco preservada) | "…realizá-la. Se durante essa aula…" |
| 18:49,2 | 18:57,8 | pausa encurtada | hesitação silenciosa de 0,36 s no meio da frase | "…um passo a mais, né? Sem adquirir o programa." |

**Propostas analisadas e mantidas no vídeo**, para preservar a integridade e a naturalidade da fala (tempos do bruto):

- **00:19,8 e 00:43,9**: pausas dramáticas antes de "gente". Preservadas: são a virada do bloco de abertura.
- **00:52,5**: "ge-re-renciar" (suposta sílaba repetida). A análise fina mostrou uma única sílaba: não havia gagueira.
- **02:52,3**: "ge…" antes de "gente". É o "de" pronunciado devagar ("dji"); cortar deixaria "problema d'gente".
- **04:34,6**: pausa após "O que seria essa percepção da injustiça?". Preservada: pausa retórica antes da resposta.
- **06:52,4**: pausa entre "menos de mil" e "5 mil". Preservada: prepara o impacto do número.
- **07:23,5**: "que foi aquele caso do TST, né?". Não há ponto de corte limpo; a fala é natural.
- **13:12,9**: pausa após "terceira etapa". Preservada: transição de bloco.
- **14:09,0**: "implemententações" (suposta sílaba repetida). A análise fina mostrou a palavra pronunciada uma única vez.
- **17:26 a 17:47**: pausas entre as perguntas do teste. Preservadas: tempo para o espectador responder.
- **20:30,9**: ritmo lento de "E tudo começa sabendo ouvir". Preservado: frase de encerramento dita devagar de propósito.

**Observação de conteúdo (decisão de vocês):** aos 11:11 do bruto (11:08,1 do final), a Hellen diz *"Porque três semanas depois vai perder o efeito."* A versão 2 do roteiro diz que **"três semanas" sai de toda a aula**. A fala foi mantida, porque a edição segue o que foi gravado, mas ficou sem destaque gráfico. Se quiserem, a frase sai com um corte limpo, e o trecho continua coerente: "A gente não pode contratar um treinamento sem antes escutar e sem antes escrever. A gente vai começar falando sobre o diagnóstico."

**Emenda anterior irrecuperável:** em 14:42 do bruto, o corte manual já existente encurta o final de "implementação" (~50 ms). Não há material gravado para reconstituir a sílaba. Ela continua compreensível.

## 4. Motion graphics e representações visuais

Linguagem gráfica única: azul-marinho, petróleo e dourado (a mesma paleta das artes do método no roteiro), tipografia **Inter Tight** (texto) e **Fraunces itálico** (destaques). As animações entram com fade, deslocamento curto e desfoque suave (easing cúbico/quártico), sem elasticidade nem explosões. O texto fica na área da cortina, acima das cabeças, e as legendas ficam embaixo, sobre a mesa, sem sobreposição. Cada palavra de lettering aparece no momento exato em que é falada.

| Início | Fim | Intervenção |
|---|---|---|
| 00:00,3 | 00:05,6 | Título de abertura "O elevador do conflito" sobre a cortina |
| 00:13,4 | 00:23,3 | Lista que se risca: estratégia ✕ cliente ✕ dinheiro ✕ → "era sobre gente" em destaque |
| 00:39,2 | 00:46,6 | Lettering "E esse desafio é gente." |
| 00:50,2 | 00:58,6 | Palavras sincronizadas: pessoas, comportamentos, emoções e conflitos |
| 01:15,7 | 01:26,5 | Pergunta errada riscada × pergunta certa |
| 01:29,9 | 01:36,1 | "Quando chega até o RH, o conflito já explodiu." |
| 01:47,9 | 02:14,9 | Roteiro da aula (3 pontos + teste) |
| 02:19,9 | 02:26,7 | Crachá Hellen de Paula |
| 02:25,7 | 02:33,1 | Crachá Indira Matos |
| 02:41,0 | 02:51,1 | Grande ideia: "Eles vão subir de andar." |
| 02:53,0 | 03:08,5 | Onde o problema começa (exemplos do andar de baixo) |
| 03:10,2 | 03:18,2 | "Uma simples conversa de 10 minutos…" |
| 03:18,7 | 04:08,5 | SIMULAÇÃO DO ELEVADOR (tela dividida): cabine sobe Colaborador → Líder → RH → Dono → Advogado, portas abrem a cada andar, indicador de andar, conflito cresce e esquenta; selo "passivo trabalhista" *(tela dividida)* |
| 04:08,9 | 04:13,7 | "Ninguém, em nenhum momento, foi incompetente." |
| 04:20,1 | 04:32,1 | Elevador: "✕ sem freio" em cada andar + acelerador "percepção de injustiça" (cabine vibra) *(tela dividida)* |
| 04:46,0 | 04:52,4 | Percepção de injustiça: "quando a regra depende de alguém" |
| 04:52,2 | 05:11,7 | Elevador: o conflito muda de forma a cada andar (fofoca → perda de produtividade → atestado → demissão inesperada) *(tela dividida)* |
| 05:15,3 | 05:21,3 | "Ela está pedindo demissão do líder." |
| 05:41,3 | 05:56,8 | Cadeia: sem regra clara → decisão subjetiva → percepção de injustiça → processo |
| 05:57,9 | 06:09,4 | Dado: +2,3 milhões de novas ações (2025) |
| 06:37,3 | 06:46,7 | Dado: assédio moral +22% em um ano / 142 mil processos |
| 06:46,8 | 06:53,6 | Dado: burnout < 1 mil → 5 mil |
| 06:54,3 | 07:03,3 | Dado: +546 mil afastamentos por saúde mental |
| 07:06,8 | 07:16,7 | "Por trás de cada um deles, existe uma conversa que não aconteceu." |
| 07:22,5 | 07:36,9 | Caso TST: R$ 238 mil |
| 07:37,7 | 07:55,3 | Contador 15 reclamações → "15 vezes o conflito subiu" |
| 08:03,6 | 08:31,5 | Curva da consciência: pico após o workshop e queda nos meses seguintes |
| 09:17,2 | 09:45,1 | Comparação: modelos prontos/ChatGPT × profissional com diagnóstico |
| 09:47,1 | 10:03,2 | Documentos normativos empilhados caem na gaveta |
| 10:17,7 | 10:30,3 | Ciclo Regra (Indira) ⇄ Comportamento (Hellen) |
| 10:31,0 | 10:35,9 | "O documento muda a regra, mas não muda o comportamento." |
| 10:40,7 | 10:46,5 | Nome do inimigo: "Gestão no improviso." |
| 10:46,6 | 11:11,7 | As 4 etapas em sequência + "o mercado começa por aqui" (liderança) |
| 11:12,2 | 11:16,9 | Cartão Etapa 1 · Diagnóstico |
| 11:23,0 | 11:28,7 | Citação: "Já sei quem é o culpado." |
| 11:31,0 | 11:36,9 | Indicador de elevador: "ele só sabe aquilo que sobe até ele" |
| 11:37,0 | 11:47,6 | Por isso o diagnóstico vem de fora |
| 11:48,6 | 12:04,8 | Pesquisa de clima × diagnóstico organizacional |
| 12:08,8 | 12:22,5 | Analogia do médico: exames = diagnóstico |
| 12:25,9 | 12:29,8 | Cartão Etapa 2 · Estrutura |
| 12:29,8 | 12:40,3 | "Vai virar uma estrutura escrita." |
| 12:60,0 | 13:06,5 | "Protege por ser aplicável." |
| 13:06,5 | 13:10,1 | Cartão Etapa 3 · Implementação |
| 13:40,2 | 13:54,7 | Orientação jurídica: advertência sem ciência → punição anulada |
| 14:04,6 | 14:15,4 | Implementação: linguagem acessível, regras conhecidas, comprovação de ciência |
| 14:36,3 | 14:40,3 | Cartão Etapa 4 · Liderança |
| 14:50,1 | 15:12,0 | Cadeia: promovido pela técnica → não conduz conversas difíceis → adia → sobe de andar |
| 15:14,5 | 15:31,6 | Dois perfis de líder: aprende a lidar × aprende a esperar |
| 15:44,4 | 16:11,0 | Ferramenta do líder com IA (interface) |
| 16:16,7 | 16:51,2 | MANDALA (tela dividida): o mercado pinta de fora para dentro ✕; pintura de dentro para fora; dependências entre etapas *(tela dividida)* |
| 16:54,2 | 17:05,1 | Abertura do teste |
| 17:11,2 | 17:20,9 | Pergunta 1 · Diagnóstico |
| 17:21,0 | 17:30,5 | Pergunta 2 · Estrutura |
| 17:30,6 | 17:41,4 | Pergunta 3 · Implementação |
| 17:41,4 | 17:48,5 | Pergunta 4 · Liderança |
| 17:48,5 | 17:54,0 | "Esse primeiro não é o seu ponto de partida." |
| 18:04,7 | 18:30,1 | Passo a passo da semana: Dono / RH / Líder |
| 18:52,2 | 19:00,9 | Experiência Cultura em Ação |
| 19:10,8 | 19:44,0 | Como funciona: escuta → panorama executivo → reunião de direcionamento |
| 19:52,4 | 20:00,9 | 3 vagas · 100% custeado |
| 20:03,2 | 20:14,3 | Botão "Clique no link aqui embaixo" com seta |
| 20:15,0 | 20:24,6 | "Uma empresa organizada não acontece por acaso. Construída." |
| 20:26,2 | 20:36,3 | Cartão final: Experiência Cultura em Ação · inscreva-se |

**O elevador.** A metáfora central foi construída como um corte transversal de prédio em 2,5D, ocupando a parte de cima da tela enquanto as duas continuam visíveis embaixo (tela dividida com a imagem original, sem perda de resolução). A cabine só se move quando a fala menciona cada andar. As portas abrem a cada parada, o indicador mostra T→4 e um "ding" marca cada chegada. O "conflito" (esfera dentro da cabine) cresce e passa de dourado a vermelho a cada andar, traduzindo a ideia de que o problema fica maior e mais caro ao subir. O elevador reaparece em "em nenhum andar existe um freio" (marcas ✕ SEM FREIO e cabine vibrando quando a fala cita o acelerador, a percepção de injustiça) e na segunda subida, em que o conflito muda de forma a cada andar. Há ainda chamadas do mesmo motivo visual em "15 vezes o conflito subiu" e "ele só sabe aquilo que sobe até ele".

## 5. Enquadramento

77 planos. Nas emendas e nas mudanças naturais de frase, a imagem alterna entre plano aberto e plano médio (punch-in de 13%, deslocado para quem fala), com aproximações lentas de até 4,5% nos trechos longos. O zoom máximo é de 18%, para preservar a nitidez de um material 1080 px. Durante os textos o zoom fica limitado a 8%, para os rostos não subirem para baixo do lettering, e durante os crachás o plano fica aberto. Os cortes coincidem com mudanças de enquadramento, o que disfarça os saltos de imagem.

## 6. Color grading

1. **Correção técnica:** balanço de branco neutralizando a dominante quente medida na cortina (R 0,962 · B 1,055), com um toque de calor preservado na pele.
2. **Separação primeiro plano / fundo:** máscara das pessoas (segmentação MediaPipe a cada 2 quadros, mediana temporal contra cintilação e encolhimento de 1–2 px com borda suave contra halos). O fundo recebe -34% de exposição, -18% de saturação e um leve tom frio nas sombras, e as pessoas mantêm a exposição.
3. **Presença:** contraste local de raio largo (desfoque gaussiano σ = 16) aplicado só nas pessoas, com leve vibração seletiva que protege a pele já saturada.
4. **Look:** curva de filme suave (pretos profundos sem esmagar, realce com roll-off) e vinheta discreta.
Tudo foi aplicado com LUTs 3D (65³) por região, sem filtros prontos e sem suavização de pele.

## 7. Áudio

Filtro passa-altas em 75 Hz → redução de ruído leve (FFT, 4 dB) → equalização: -2 dB em 250 Hz (ressonância de caixa), -1 dB em 800 Hz, +2,5 dB em 3,2 kHz (presença), +1,5 dB em prateleira a partir de 8 kHz → de-esser suave → compressão 2:1 → limitador. Em seguida, equilíbrio entre as vozes (+2,3 dB nos trechos da Hellen, por palavra) e normalização EBU R128 em duas passadas.
Efeitos sonoros pontuais, sintetizados para este projeto: "ding" de elevador nas chegadas, motor discreto na subida, whoosh na abertura das telas divididas, impacto grave em 4 frases-chave e ticks nos dados. **Não foi usada trilha musical**, porque não havia um arquivo licenciado disponível. O vídeo está pronto para receber uma trilha, que deve ficar cerca de 20 dB abaixo da voz.

## 8. Legendas

Geradas a partir do texto revisado e sincronizadas com as palavras que realmente ficaram depois dos cortes. Palavras removidas nunca aparecem. Usam no máximo 2 linhas e ~30 caracteres por linha, quebram nas pausas e na pontuação e não terminam em artigo ou preposição. Fonte Inter Tight SemiBold 56 px, branca, com contorno escuro suave, posicionada sobre a mesa (margem inferior de 290 px). `Legendas.srt` traz o mesmo texto para uso em plataformas.

## 9. Controle de qualidade

- Todas as animações foram revistas quadro a quadro em folhas de contato sobre a imagem tratada.

## 10. Limitações e pontos para validação

- **Números ditos no vídeo:** 2,3 milhões de ações, +22% de assédio moral, 142 mil processos, burnout de menos de mil para 5 mil, 546 mil afastamentos e R$ 238 mil. Eles aparecem nos cartões exatamente como falados. O roteiro pede validação de qualquer número antes de publicar. Os revisores encontraram fontes públicas para os 22%, os 142 mil e o caso de R$ 238 mil (TST); os demais precisam de confirmação de vocês.
- **Valor do caso no TST:** na segunda menção, a transcrição automática ouviu "288 mil", mas o Whisper, a sonda de áudio e a fonte pública indicam R$ 238 mil. O cartão mostra R$ 238 mil, e a legenda também.
- O vídeo menciona um teste e uma oferta (Experiência Cultura em Ação, 3 vagas) que não estão no roteiro. Foram mantidos porque estão na gravação.
- Não houve trilha musical, por falta de arquivo licenciado.
- O material de origem tem 1080 px de largura, por isso os reenquadramentos foram limitados a 18% de zoom. Acima disso a nitidez cairia.
- O recorte das pessoas para o fundo usa segmentação automática. Em gestos muito rápidos, a borda pode ficar até 1 quadro atrás, o que foi mitigado com escurecimento moderado e borda suave.

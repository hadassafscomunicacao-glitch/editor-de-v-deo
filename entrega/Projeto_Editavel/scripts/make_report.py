"""Generate entrega/Relatorio_Edicao.md from the real project data (plan, cut report, QA)."""
import json, os, datetime
P = json.load(open('/home/user/work/build/plan.json'))
CR = json.load(open('/home/user/work/build/cut_report.json'))
QA = json.load(open('/home/user/work/build/qa.json')) if os.path.exists('/home/user/work/build/qa.json') else {}
VM = {c['id']: c for c in json.load(open('/home/user/work/project/visual_map.json'))}
FPS = 30
def ts(t): return f"{int(t // 60):02d}:{t % 60:04.1f}".replace('.', ',')
import numpy as np
starts = np.cumsum([0] + [b - a for a, b in P['edl']])
def out_t(src):
    f = src * FPS
    for k, (a, b) in enumerate(P['edl']):
        if f < a: return starts[k] / FPS
        if a <= f < b: return (starts[k] + f - a) / FPS
    return starts[-1] / FPS
DESC = {
 'v01_titulo': 'Título de abertura "O elevador do conflito" sobre a cortina', 'v02_gente': 'Lista que se risca: estratégia ✕ cliente ✕ dinheiro ✕ → "era sobre gente" em destaque',
 'v03_desafio': 'Lettering "E esse desafio é gente."', 'v04_liderar': 'Palavras sincronizadas: pessoas, comportamentos, emoções e conflitos',
 'v05_pergunta': 'Pergunta errada riscada × pergunta certa', 'v06_rh': '"Quando chega até o RH, o conflito já explodiu."', 'v07_roteiro': 'Roteiro da aula (3 pontos + teste)',
 'v08_hellen': 'Crachá Hellen de Paula', 'v08_indira': 'Crachá Indira Matos', 'v09_bigidea': 'Grande ideia: "Eles vão subir de andar."',
 'v10_terreo': 'Onde o problema começa (exemplos do andar de baixo)', 'v11_conversa': '"Uma simples conversa de 10 minutos…"',
 'v12_elevador_a': 'SIMULAÇÃO DO ELEVADOR (tela dividida): cabine sobe Colaborador → Líder → RH → Dono → Advogado, portas abrem a cada andar, indicador de andar, conflito cresce e esquenta; selo "passivo trabalhista"',
 'v13_ninguem': '"Ninguém, em nenhum momento, foi incompetente."', 'v14_sem_freio': 'Elevador: "✕ sem freio" em cada andar + acelerador "percepção de injustiça" (cabine vibra)',
 'v15_injustica': 'Percepção de injustiça: "quando a regra depende de alguém"', 'v16_formas': 'Elevador: o conflito muda de forma a cada andar (fofoca → perda de produtividade → atestado → demissão inesperada)',
 'v17_demissao': '"Ela está pedindo demissão do líder."', 'v18_sequencia': 'Cadeia: sem regra clara → decisão subjetiva → percepção de injustiça → processo',
 'v19_dado_acoes': 'Dado: +2,3 milhões de novas ações (2025)', 'v22_dado_assedio': 'Dado: assédio moral +22% em um ano / 142 mil processos', 'v23_burnout': 'Dado: burnout < 1 mil → 5 mil',
 'v24_inss': 'Dado: +546 mil afastamentos por saúde mental', 'v25_conversa': '"Por trás de cada um deles, existe uma conversa que não aconteceu."',
 'v26a_caso': 'Caso TST: R$ 238 mil', 'v26_tst': 'Contador 15 reclamações → "15 vezes o conflito subiu"', 'v28_curva': 'Curva da consciência: pico após o workshop e queda nos meses seguintes',
 'v31_modelos': 'Comparação: modelos prontos/ChatGPT × profissional com diagnóstico', 'v32_gaveta': 'Documentos normativos empilhados caem na gaveta',
 'v34_loop': 'Ciclo Regra (Indira) ⇄ Comportamento (Hellen)', 'v35_documento': '"O documento muda a regra, mas não muda o comportamento."', 'v36_improviso': 'Nome do inimigo: "Gestão no improviso."',
 'v37_etapas': 'As 4 etapas em sequência + "o mercado começa por aqui" (liderança)', 'v38_etapa1': 'Cartão Etapa 1 · Diagnóstico', 'v39_culpado': 'Citação: "Já sei quem é o culpado."',
 'v40_sobe': 'Indicador de elevador: "ele só sabe aquilo que sobe até ele"', 'v41_chefe': 'Por isso o diagnóstico vem de fora', 'v42_clima': 'Pesquisa de clima × diagnóstico organizacional',
 'v43_medico': 'Analogia do médico: exames = diagnóstico', 'v44_etapa2': 'Cartão Etapa 2 · Estrutura', 'v45_estrutura': '"Vai virar uma estrutura escrita."', 'v46_aplicavel': '"Protege por ser aplicável."',
 'v47_etapa3': 'Cartão Etapa 3 · Implementação', 'v49_advertencia': 'Orientação jurídica: advertência sem ciência → punição anulada', 'v50_ciencia': 'Implementação: linguagem acessível, regras conhecidas, comprovação de ciência',
 'v52_etapa4': 'Cartão Etapa 4 · Liderança', 'v53_promovido': 'Cadeia: promovido pela técnica → não conduz conversas difíceis → adia → sobe de andar', 'v54_mapeia': 'Dois perfis de líder: aprende a lidar × aprende a esperar',
 'v55_ferramenta': 'Ferramenta do líder com IA (interface)', 'v56_mandala': 'MANDALA (tela dividida): o mercado pinta de fora para dentro ✕; pintura de dentro para fora; dependências entre etapas',
 'v57_teste': 'Abertura do teste', 'v58_q1': 'Pergunta 1 · Diagnóstico', 'v58_q2': 'Pergunta 2 · Estrutura', 'v58_q3': 'Pergunta 3 · Implementação', 'v58_q4': 'Pergunta 4 · Liderança',
 'v59_partida': '"Esse primeiro não é o seu ponto de partida."', 'v61_semana': 'Passo a passo da semana: Dono / RH / Líder', 'v62_experiencia': 'Experiência Cultura em Ação',
 'v63_passos': 'Como funciona: escuta → panorama executivo → reunião de direcionamento', 'v63b_vagas': '3 vagas · 100% custeado', 'v64_link': 'Botão "Clique no link aqui embaixo" com seta',
 'v65_final': '"Uma empresa organizada não acontece por acaso. Construída."', 'v66_fim': 'Cartão final: Experiência Cultura em Ação · inscreva-se'}
L = []
L.append('# Relatório de edição — "O elevador do conflito"\n')
L.append(f"Gerado em {datetime.date.today().strftime('%d/%m/%Y')}. Todos os tempos abaixo se referem ao **vídeo final** (mm:ss), salvo indicação.\n")
dur_src = 37357 / FPS; dur_out = P['nout'] / FPS
L.append('## 1. Material de origem\n')
L.append(f"- Arquivo `IMG_0623.MOV` (exportado do CapCut): {ts(dur_src)} · 1080×1920 vertical (9:16) · 30 fps · HEVC 8 bits BT.709 · áudio AAC estéreo (dual-mono) 44,1 kHz.")
L.append('- Plano fixo com as duas apresentadoras lado a lado: **Indira Matos** à esquerda (blazer azul) e **Hellen de Paula** à direita (blusa bege, óculos). Há uma inserção de 2 s de uma segunda câmera em 01:02–01:04 do bruto.')
L.append('- Imagem: cortina cinza-média (≈ 30% de luminância) com pouca separação do primeiro plano, leve dominante quente, rostos com pouco contraste.')
L.append('- Áudio: fala limpa (ruído de fundo abaixo de -70 dBFS), abafada acima de 3 kHz, -17,3 LUFS, alguns picos em 0 dBFS; a Hellen estava 2,6 LU mais baixa que a Indira.')
L.append('- 20 cortes manuais já existentes foram detectados por diferença de quadros (sobretudo na primeira metade), e as emendas foram revisadas.\n')
L.append('## 2. Transcrição e revisão da fala\n')
L.append('- Transcrição local com marcação de tempo por sílaba: NVIDIA Parakeet TDT v3, com Silero VAD para segmentação e Whisper large-v3 para checagem cruzada dos trechos duvidosos.')
L.append('- Identificação de quem fala: impressões vocais (WeSpeaker) agrupadas em dois locutores e confirmadas pelo movimento da boca de cada uma no vídeo.')
L.append('- Revisão por 5 "editores de diálogo" (um por trecho de ~4 min). Em seguida, 5 revisores adversariais reouviram cada corte proposto com uma sonda de áudio (re-transcrição e energia a cada 10–20 ms) e tentaram refutá-lo. Só entrou o que passou nessa checagem.')
L.append('- A fala real difere bastante do roteiro: as apresentadoras improvisaram, mudaram a ordem e incluíram dados, um teste com 4 perguntas e a oferta "Experiência Cultura em Ação". **A edição segue o que foi dito, não o roteiro.**')
L.append('- A transcrição revisada está em `Projeto_Editavel/dados/transcricao_final.md`.\n')
L.append('## 3. Cortes de fala\n')
used = [c for c in CR if c['used']]; rej = [c for c in CR if not c['used']]
L.append(f"Duração: {ts(dur_src)} (bruto) → **{ts(dur_out)}** (final). Foram removidos {dur_src - dur_out:.1f} s em {len(used)} intervenções, todas com emenda ajustada ao quadro de vídeo e ao ponto mais silencioso do áudio (deslocamento máximo de 20 ms, com crossfade de 12 ms).\n")
L.append('| Final | Bruto | Tipo | Removido | Como ficou |')
L.append('|---|---|---|---|---|')
for c in sorted(used, key=lambda c: c['a']):
    L.append(f"| {ts(out_t(c['a']))} | {ts(c['a'])} | {c['type']} | {c['removed'][:60]} | {c['result'][:90]} |")
L.append('\n**Propostas analisadas e mantidas no vídeo** (corte rejeitado para preservar a integridade da fala):\n')
for c in sorted(rej, key=lambda c: c['a']):
    L.append(f"- {ts(c['a'])} (bruto) · {c['type']} · \"{c['removed'][:70]}\". Motivo: {c['evidence'][:220]}")
L.append('')
L.append('## 4. Motion graphics e representações visuais\n')
L.append('Linguagem gráfica única: azul-marinho, petróleo e dourado (a mesma paleta das artes do método no roteiro), tipografia **Inter Tight** (texto) e **Fraunces itálico** (destaques). As animações entram com fade, deslocamento curto e desfoque suave (easing cúbico/quártico), sem elasticidade nem explosões. O texto fica na área da cortina, acima das cabeças, e as legendas ficam embaixo, sobre a mesa, sem sobreposição. Cada palavra de lettering aparece no momento exato em que é falada.\n')
L.append('| Início | Fim | Intervenção |')
L.append('|---|---|---|')
for o in P['overlays']:
    t0 = o['f0'] / FPS; t1 = (o['f0'] + o['n']) / FPS
    d = DESC.get(o['id'], o['id']); lay = ' *(tela dividida)*' if o['layout'] == 'split' else ''
    L.append(f"| {ts(t0)} | {ts(t1)} | {d}{lay} |")
L.append('\n**O elevador.** A metáfora central foi construída como um corte transversal de prédio em 2,5D, ocupando a parte de cima da tela enquanto as duas continuam visíveis embaixo (tela dividida com a imagem original, sem perda de resolução). A cabine só se move quando a fala menciona cada andar. As portas abrem a cada parada, o indicador mostra T→4 e um "ding" marca cada chegada. O "conflito" (esfera dentro da cabine) cresce e passa de dourado a vermelho a cada andar, traduzindo a ideia de que o problema fica maior e mais caro ao subir. O elevador reaparece em "em nenhum andar existe um freio" (marcas ✕ SEM FREIO e cabine vibrando quando a fala cita o acelerador, a percepção de injustiça) e na segunda subida, em que o conflito muda de forma a cada andar. Há ainda chamadas do mesmo motivo visual em "15 vezes o conflito subiu" e "ele só sabe aquilo que sobe até ele".\n')
L.append('## 5. Enquadramento\n')
L.append(f"{len(P['framing'])} planos. Nas emendas e nas mudanças naturais de frase, a imagem alterna entre plano aberto e plano médio (punch-in de 13%, deslocado para quem fala), com aproximações lentas de até 4,5% nos trechos longos. O zoom máximo é de 18%, para preservar a nitidez de um material 1080 px. Durante os textos o zoom fica limitado a 8%, para os rostos não subirem para baixo do lettering, e durante os crachás o plano fica aberto. Os cortes coincidem com mudanças de enquadramento, o que disfarça os saltos de imagem.\n")
L.append('## 6. Color grading\n')
L.append('1. **Correção técnica:** balanço de branco neutralizando a dominante quente medida na cortina (R 0,962 · B 1,055), com um toque de calor preservado na pele.')
L.append('2. **Separação primeiro plano / fundo:** máscara das pessoas (segmentação MediaPipe a cada 2 quadros, mediana temporal contra cintilação e encolhimento de 1–2 px com borda suave contra halos). O fundo recebe -34% de exposição, -18% de saturação e um leve tom frio nas sombras, e as pessoas mantêm a exposição.')
L.append('3. **Presença:** contraste local de raio largo (desfoque gaussiano σ = 16) aplicado só nas pessoas, com leve vibração seletiva que protege a pele já saturada.')
L.append('4. **Look:** curva de filme suave (pretos profundos sem esmagar, realce com roll-off) e vinheta discreta.')
L.append('Tudo foi aplicado com LUTs 3D (65³) por região, sem filtros prontos e sem suavização de pele.\n')
L.append('## 7. Áudio\n')
L.append('Filtro passa-altas em 75 Hz → redução de ruído leve (FFT, 4 dB) → equalização: -2 dB em 250 Hz (ressonância de caixa), -1 dB em 800 Hz, +2,5 dB em 3,2 kHz (presença), +1,5 dB em prateleira a partir de 8 kHz → de-esser suave → compressão 2:1 → limitador. Em seguida, equilíbrio entre as vozes (+2,3 dB nos trechos da Hellen, por palavra) e normalização EBU R128 em duas passadas.')
if QA.get('loudness'): L.append(f"Resultado medido no vídeo final: **{QA['loudness']['I']} LUFS** integrado, LRA {QA['loudness']['LRA']} LU, pico {QA['loudness']['TP']} dBFS.")
L.append('Efeitos sonoros pontuais, sintetizados para este projeto: "ding" de elevador nas chegadas, motor discreto na subida, whoosh na abertura das telas divididas, impacto grave em 4 frases-chave e ticks nos dados. **Não foi usada trilha musical**, porque não havia um arquivo licenciado disponível. O vídeo está pronto para receber uma trilha, que deve ficar cerca de 20 dB abaixo da voz.\n')
L.append('## 8. Legendas\n')
L.append('Geradas a partir do texto revisado e sincronizadas com as palavras que realmente ficaram depois dos cortes. Palavras removidas nunca aparecem. Usam no máximo 2 linhas e ~30 caracteres por linha, quebram nas pausas e na pontuação e não terminam em artigo ou preposição. Fonte Inter Tight SemiBold 56 px, branca, com contorno escuro suave, posicionada sobre a mesa (margem inferior de 290 px). `Legendas.srt` traz o mesmo texto para uso em plataformas.\n')
L.append('## 9. Controle de qualidade\n')
if QA:
    L.append(f"- Quadros: {QA.get('video', {}).get('nb_frames')} (esperado {P['nout']}). Quadros pretos detectados: {len(QA.get('black', []))}. Congelamentos detectados: {len(QA.get('freeze', []))}.")
    if 'splices_checked' in QA: L.append(f"- Emendas re-transcritas: {QA['splices_checked']}; suspeitas: {len(QA['splices_suspect'])}.")
L.append('- Todas as animações foram revistas quadro a quadro em folhas de contato sobre a imagem tratada.\n')
L.append('## 10. Limitações e pontos para validação\n')
L.append('- **Números ditos no vídeo:** 2,3 milhões de ações, +22% de assédio moral, 142 mil processos, burnout de menos de mil para 5 mil, 546 mil afastamentos e R$ 238 mil. Eles aparecem nos cartões exatamente como falados. O roteiro pede validação de qualquer número antes de publicar. Os revisores encontraram fontes públicas para os 22%, os 142 mil e o caso de R$ 238 mil (TST); os demais precisam de confirmação de vocês.')
L.append('- **Valor do caso no TST:** na segunda menção, a transcrição automática ouviu "288 mil", mas o Whisper, a sonda de áudio e a fonte pública indicam R$ 238 mil. O cartão mostra R$ 238 mil, e a legenda também.')
L.append('- O vídeo menciona um teste e uma oferta (Experiência Cultura em Ação, 3 vagas) que não estão no roteiro. Foram mantidos porque estão na gravação.')
L.append('- Não houve trilha musical, por falta de arquivo licenciado.')
L.append('- O material de origem tem 1080 px de largura, por isso os reenquadramentos foram limitados a 18% de zoom. Acima disso a nitidez cairia.')
L.append('- O recorte das pessoas para o fundo usa segmentação automática. Em gestos muito rápidos, a borda pode ficar até 1 quadro atrás, o que foi mitigado com escurecimento moderado e borda suave.')
open('/home/user/editor-de-v-deo/entrega/Relatorio_Edicao.md', 'w').write('\n'.join(L) + '\n')
print('report written', len(L), 'lines')

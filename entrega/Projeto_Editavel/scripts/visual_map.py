"""Edit map: every motion-graphics intervention, anchored to the words actually spoken (source timeline).
Times are absolute SOURCE seconds wrapped as {'@t': x}; build_plan converts them to scene-relative OUTPUT seconds after the cuts.
On-screen text is faithful to what is said (condensed only where it is a title/label for the idea)."""
import sys, re
sys.path.insert(0, '/home/user/work/project')
from words_util import find, WORDS, _n

def T(x): return {'@t': round(float(x), 3)}
def S(p, near, w=10): return find(p, near, window=w)[0]
def Ee(p, near, w=10): return find(p, near, window=w)[1]

def L(text, near, font='sans', size=None, cls='', pop=(), color=None, gap=None, weight=None, w=10, display=None):
    """Lettering line whose words appear exactly when spoken. `text` must match the spoken words (punctuation free);
    `display` (optional) is the on-screen spelling with accents/punctuation, same number of words."""
    s, e, i, j = find(text, near, window=w)
    shown = (display or text).split()
    assert len(shown) == j - i + 1, (text, display)
    words = [{'text': shown[k], 't': T(WORDS[i + k]['s'] - 0.05), 'cls': cls, **({'pop': True} if shown[k] in pop or k in pop else {})} for k in range(len(shown))]
    ln = {'words': words, 'font': font}
    if size: ln['size'] = size
    if color: ln['color'] = color
    if gap is not None: ln['gap'] = gap
    if weight: ln['weight'] = weight
    return ln

def Lfix(text, t, font='sans', size=None, cls='', step=0.07, color=None, gap=None, weight=None):
    """Lettering line revealed word by word from absolute time t (for titles/labels not spoken verbatim)."""
    ws = text.split()
    ln = {'words': [{'text': x, 't': T(t + k * step), 'cls': cls} for k, x in enumerate(ws)], 'font': font}
    if size: ln['size'] = size
    if color: ln['color'] = color
    if gap is not None: ln['gap'] = gap
    if weight: ln['weight'] = weight
    return ln

CUES = []
def cue(id, scene, start, end, params, layout='top', sfx=None, prio=1):
    CUES.append({'id': id, 'scene': scene, 'start': round(start, 3), 'end': round(end, 3), 'params': params, 'layout': layout, 'sfx': sfx or [], 'prio': prio})

# ---------------- ABERTURA (Indira) ----------------
cue('v01_titulo', 'lettering', 0.25, 5.6, {'kicker': 'Aula', 'kickerT': T(0.35), 'top': 205,
    'lines': [Lfix('O elevador', 0.55, font='serif', size=96, cls='serif', color='#FFFFFF'), Lfix('do conflito', 0.75, font='serif', size=96, cls='serif gold')]})
cue('v02_gente', 'list', S('não era sobre estratégia', 14.0) - 0.5, Ee('sobre gente', 20) + 2.6, {
    'kicker': 'Um problema que não era sobre…', 'kickerT': T(S('não era sobre estratégia', 14.0) - 0.4), 'top': 175, 'size': 54, 'numW': 56,
    'items': [
        {'n': '✕', 'text': 'estratégia', 't': T(S('estratégia', 15)), 'strikeT': T(S('estratégia', 15) + 0.55), 'dimAt': T(S('gente', 20) - .1)},
        {'n': '✕', 'text': 'o cliente', 't': T(S('o cliente', 17)), 'strikeT': T(S('o cliente', 17) + 0.55), 'dimAt': T(S('gente', 20) - .1)},
        {'n': '✕', 'text': 'o dinheiro', 't': T(S('dinheiro', 18.5)), 'strikeT': T(S('dinheiro', 18.5) + 0.55), 'dimAt': T(S('gente', 20) - .1)},
        {'n': '✓', 'text': 'era sobre gente.', 't': T(S('era sobre gente', 19.5)), 'hiT': T(S('gente', 20)), 'numColor': '#9FD3C7', 'size': 66, 'weight': 750},
    ]}, sfx=[('tick', S('gente', 20), -22)])
cue('v03_desafio', 'lettering', S('existe um desafio real', 40) - 0.2, Ee('gente', 44.5) + 1.8, {'top': 220,
    'lines': [L('existe um desafio real e comum a todas as empresas', 40, size=52, weight=650, display='Existe um desafio real e comum a todas as empresas'),
              L('e esse desafio é gente', 43, font='serif', size=96, cls='serif gold', pop=(4,), display='E esse desafio é gente.', gap=14)]})
cue('v04_liderar', 'lettering', S('liderar na prática', 50.5) - 0.2, Ee('emoções e conflitos', 56) + 1.6, {'top': 205,
    'kicker': 'Liderar na prática é gerenciar', 'kickerT': T(S('liderar na prática', 50.5)),
    'lines': [L('pessoas comportamentos', 54, size=70, display='pessoas, comportamentos,'),
              L('emoções e conflitos', 56, size=70, display='emoções e conflitos.', cls='', pop=(2,))]})
cue('v05_pergunta', 'list', S('a pergunta que você deve fazer', 76) - 0.3, Ee('quando ele aparecer', 84) + 1.4, {
    'kicker': 'A pergunta certa', 'kickerT': T(S('a pergunta que você deve fazer', 76)), 'top': 165, 'size': 44, 'numW': 52,
    'items': [{'n': '✕', 'text': 'Como evitar o conflito?', 't': T(S('como evitar o conflito', 78.5)), 'strikeT': T(S('e sim', 79.8)), 'dimAt': T(S('e sim', 79.8) + .2)},
              {'n': '✓', 'numColor': '#9FD3C7', 'text': 'A minha empresa está preparada para gerenciar e conduzir o conflito quando ele aparecer?', 't': T(S('a minha empresa está preparada', 81)), 'size': 48}]})
cue('v06_rh', 'lettering', S('quando chega até o rh', 90) - 0.2, Ee('mais difícil ainda', 94.5) + 0.8, {'top': 230,
    'kicker': 'E se você é do RH', 'kickerT': T(S('e se você é do', 86.5)),
    'lines': [L('quando chega até o rh', 90, size=58, weight=650, display='Quando chega até o RH,'),
              L('o conflito já explodiu', 92.5, font='serif', size=86, cls='serif gold', display='o conflito já explodiu.')]})
cue('v07_roteiro', 'list', S('nos próximos minutos', 107.5) - 0.3, Ee('quatro perguntas', 131.5) + 1.8, {
    'kicker': 'Nos próximos minutos', 'kickerT': T(S('nos próximos minutos', 107.5)), 'top': 160, 'size': 40, 'rowGap': 16,
    'items': [{'text': 'O que acontece quando essa estrutura falha', 't': T(S('o que acontece com a sua empresa', 111.5))},
              {'text': 'Por que as soluções mais comuns não se sustentam sozinhas', 't': T(S('algumas soluções', 116.5))},
              {'text': 'O caminho em quatro etapas', 't': T(S('quatro etapas', 123.5))},
              {'n': '✎', 'text': 'Um teste: quatro perguntas', 't': T(S('realizar um teste', 129.3)), 'color': '#E2C88F'}]})
cue('v08_hellen', 'nameTag', S('eu sou a ellen', 140.2) - 0.1, Ee('lado do comportamento', 145.5) + 0.9, {'side': 'R', 'name': 'Hellen de Paula', 'role': 'Psicóloga organizacional', 'y': 520})
cue('v08_indira', 'nameTag', S('eu sou indira', 146) - 0.1, Ee('prevenção empresarial', 152.3) + 0.4, {'side': 'L', 'name': 'Indira Matos', 'role': 'Advogada e mediadora', 'y': 540})

# ---------------- O ELEVADOR (Hellen -> Indira) ----------------
cue('v09_bigidea', 'lettering', S('e os conflitos', 161.3) - 0.2, Ee('subir de andar', 168.5) + 1.6, {'top': 190,
    'kicker': 'A grande ideia', 'kickerT': T(S('e os conflitos', 161.3)),
    'lines': [L('os conflitos quando não são resolvidos', 162, size=52, weight=650, display='Os conflitos, quando não são resolvidos,'),
              L('não vão deixar de existir', 165, size=52, weight=650, display='não vão deixar de existir.'),
              L('eles vão subir de andar', 167.5, font='serif', size=96, cls='serif gold', pop=(4,), display='Eles vão subir de andar.', gap=16)]}, sfx=[('impact', S('subir de andar', 168.5), -24)])
cue('v10_terreo', 'list', S('pessoas do mesmo setor', 173.5) - 0.4, Ee('andar de baixo', 187) + 1.0, {
    'kicker': 'Onde o problema começa', 'kickerT': T(S('pessoas do mesmo setor', 173.5) - .3), 'top': 165, 'size': 40, 'rowGap': 12, 'numSize': 34, 'numW': 46,
    'items': [{'n': '·', 'text': 'pessoas do mesmo setor que não se entendem', 't': T(S('pessoas do mesmo setor', 173.5))},
              {'n': '·', 'text': 'uma regra que não foi bem estabelecida', 't': T(S('uma regra', 176))},
              {'n': '·', 'text': 'uma promessa do líder que não foi cumprida', 't': T(S('uma promessa', 178.6))},
              {'n': '·', 'text': 'uma escala mal feita', 't': T(S('uma escala', 181.5))},
              {'n': '↳', 'text': 'sempre começa no andar de baixo', 't': T(S('andar de baixo', 186.7)), 'color': '#E2C88F', 'size': 46}]})
cue('v11_conversa', 'lettering', S('uma simples conversa', 191) - 0.2, Ee('nunca acontece', 197) + 0.9, {'top': 215,
    'lines': [L('uma simples conversa de 10 minutos', 191.5, size=58, weight=650, display='Uma simples conversa de 10 minutos'),
              L('poderia resolver tudo', 194, font='serif', size=80, cls='serif gold', display='poderia resolver tudo.'),
              L('mas essa conversa nunca acontece', 196, size=44, weight=600, display='Mas essa conversa nunca acontece.', gap=18, color='#F2B3A3')]})
FLOORS = [
    {'level': 'Térreo', 'name': 'Colaborador', 'desc': 'onde o problema começa', 't': T(S('do colaborador', 204))},
    {'level': '1º andar', 'name': 'Líder', 'desc': 'sem preparo para conversas difíceis', 't': T(S('o líder', 205.5))},
    {'level': '2º andar', 'name': 'RH', 'desc': 'sem norma: atua caso a caso', 't': T(S('o rh', 211))},
    {'level': '3º andar', 'name': 'Dono', 'desc': 'muitas vezes não consegue resolver', 't': T(S('o dono', 233.4))},
    {'level': '4º andar', 'name': 'Advogado', 'desc': 'o único andar com data e valor definido', 't': T(S('advogado', 239.4))},
]
t_split_a0 = S('quando ela não acontece', 200) - 0.9
cue('v12_elevador_a', 'elevator', t_split_a0, Ee('passivo trabalhista', 248) + 1.3, {
    'header': 'O elevador do conflito', 'sub': 'quando a conversa não acontece, ela pega um elevador', 'floors': FLOORS,
    'topNote': {'t': T(S('passivo trabalhista', 247.5) - .1), 'text': 'pode virar passivo trabalhista'}},
    layout='split', sfx=[('whoosh_down', t_split_a0, -20)] + [('ding', f['t']['@t'] - 0.05, -21) for f in FLOORS[1:]] + [('motor', f['t']['@t'] - 1.3, -30) for f in FLOORS[1:]])
cue('v13_ninguem', 'lettering', S('ninguém em nenhum momento', 250.6) - 0.2, Ee('foi incompetente', 252.5) + 1.8, {'top': 240,
    'lines': [L('ninguém em nenhum momento', 251, size=54, weight=650, display='Ninguém, em nenhum momento,'),
              L('foi incompetente', 252.5, font='serif', size=88, cls='serif gold', display='foi incompetente.', gap=10)]})
t_b0 = S('o problema maior', 263) - 0.6
cue('v14_sem_freio', 'elevator', t_b0, Ee('percepção de injustiça', 271.5) + 1.4, {
    'header': 'O elevador do conflito', 'sub': 'em nenhum andar existe um freio',
    'floors': [dict(f, t=T(t_b0 + 0.15 + 0.12 * k)) for k, f in enumerate(FLOORS)], 'startFloor': 4, 'stops': [],
    'freio': T(S('existe um freio', 265.5) - 0.1), 'accel': {'t': T(S('acelera ainda mais', 267.5)), 'text': 'o que acelera ainda mais:', 'text2': 'percepção de injustiça', 't2': T(S('percepção de injustiça', 271))}},
    layout='split', sfx=[('whoosh_down', t_b0, -20)])
cue('v15_injustica', 'lettering', S('a regra depende de alguém', 288) - 0.3, Ee('procurar o líder', 293) + 0.5, {'top': 230,
    'kicker': 'Percepção de injustiça', 'kickerT': T(S('a regra depende de alguém', 288) - .3),
    'lines': [L('quando a regra depende de alguém', 288, font='serif', size=70, cls='serif', color='#FFFFFF', display='Quando a regra depende de alguém…'),
              L('essa pessoa vai deixar de procurar o líder', 291.5, size=42, weight=600, display='a pessoa deixa de procurar o líder.' if False else 'essa pessoa vai deixar de procurar o líder.', gap=18, color='#E2C88F')]})
t_c0 = S('subir o elevador novamente', 294.3) - 0.5
FORMS = [('fofoca', S('fofoca', 305.8)), ('perda de produtividade', S('perca da produtividade', 307.6)), ('atestado', S('atestado', 309.6)), ('demissão inesperada', S('uma demissão', 310.4))]
cue('v16_formas', 'elevator', t_c0, Ee('não era esperada', 312.5) + 1.2, {
    'header': 'O elevador do conflito', 'sub': 'no caminho, ele se transforma em outra coisa',
    'floors': [dict(f, t=T(t_c0 + 0.15 + 0.1 * k)) for k, f in enumerate(FLOORS)], 'rowsDim': True, 'startFloor': 0,
    'stops': [{'t': T(t), 'floor': k} for k, (txt, t) in enumerate(FORMS)],
    'pills': [{'t': T(t), 'text': txt} for k, (txt, t) in enumerate(FORMS)]},
    layout='split', sfx=[('whoosh_down', t_c0, -20)] + [('ding', t - 0.05, -22) for _, t in FORMS[1:]])
cue('v17_demissao', 'lettering', S('pedindo demissão da empresa', 318.2) - 0.4, Ee('demissão do líder', 321) + 1.8, {'top': 230,
    'lines': [L('ela não está pedindo demissão da empresa', 317.2, size=50, weight=650, display='Ela não está pedindo demissão da empresa.'),
              L('ela está pedindo demissão do líder', 320, font='serif', size=78, cls='serif gold', pop=(5,), display='Está pedindo demissão do líder.' if False else 'Ela está pedindo demissão do líder.', gap=16)]},
    sfx=[('impact', S('do líder', 321), -26)])
cue('v18_sequencia', 'chain', S('regra clara', 344.4) - 0.6, Ee('vira processo', 357) + 1.3, {
    'kicker': 'Não é ameaça — é sequência' if False else 'A sequência', 'kickerT': T(S('regra clara', 344.4) - .5), 'top': 150, 'size': 40, 'arrowH': 26,
    'nodes': [{'text': 'Sem regra clara', 't': T(S('não existe regra clara', 344))},
              {'text': 'decisão subjetiva', 't': T(S('decisão subjetiva', 347))},
              {'text': 'percepção de injustiça', 't': T(S('percepção de injustiça', 352))},
              {'text': 'processo', 't': T(S('vira processo', 357)), 'color': '#E2C88F', 'size': 54, 'weight': 750}]})
# ---------------- DADOS (Indira / Hellen) ----------------
cue('v19_dado_acoes', 'dataCard', S('só em 2025', 359.5) - 0.3, Ee('em 2017', 369) + 1.6, {
    'kicker': 'Justiça do Trabalho · 2025', 'value': 2.3, 'decimals': 1, 'unit': 'milhões', 'prefix': '+',
    'tCount': T(S('2,3', 363.6)), 'label': 'de novas ações', 'tLabel': T(S('novas ações', 365.5)),
    'sub': 'o maior volume desde a reforma trabalhista de 2017', 'tSub': T(S('o maior volume', 366.5))}, sfx=[('tick', S('2,3', 363.6), -24)])
cue('v22_dado_assedio', 'dataCard', S('ações de assete moral', 399.5) - 0.4, Ee('só em 2025', 409) + 0.8, {
    'kicker': 'Ações de assédio moral', 'value': 22, 'prefix': '+', 'suffix': '%', 'tCount': T(S('22%', 402.6)),
    'label': 'em um ano', 'tLabel': T(S('em um ano', 404)), 'sub': 'mais de 142 mil novos processos só em 2025', 'tSub': T(S('142', 405.9))}, sfx=[('tick', S('22%', 402.6), -24)])
cue('v23_burnout', 'fromTo', S('as ações por', 409.5) - 0.2, Ee('ano de 2025', 414.8) + 0.9, {
    'kicker': 'Ações por burnout', 'a': {'text': '< 1 mil', 'label': 'antes'}, 'b': {'text': '5 mil', 'label': 'em 2025'}, 'tB': T(S('para 5 mil', 412.9))})
cue('v24_inss', 'dataCard', S('546', 418) - 1.4, Ee('saúde mental', 424) + 1.2, {
    'kicker': 'INSS · 2025', 'value': 546, 'unit': 'mil', 'prefix': '+', 'tCount': T(S('546', 418.2)),
    'label': 'afastamentos por saúde mental', 'tLabel': T(S('saúde mental', 423.5))})
cue('v25_conversa', 'lettering', S('por trás de cada um deles', 429.5) - 0.2, Ee('conversa difícil', 437) + 1.0, {'top': 225,
    'lines': [L('por trás de cada um deles', 429.5, size=50, weight=650, display='Por trás de cada um deles,'),
              L('existe uma conversa que não aconteceu', 431.5, font='serif', size=74, cls='serif gold', display='existe uma conversa que não aconteceu.', gap=14)]})
cue('v26a_caso', 'dataCard', S('aquele caso tst que ele manteve', 446) - 0.4, S('15 reclamações', 461) - 1.4, {
    'kicker': 'Caso julgado no TST', 'value': 238, 'prefix': 'R$ ', 'unit': 'mil', 'size': 132, 'tCount': T(S('238', 449.8)),
    'label': 'condenação mantida contra uma montadora', 'tLabel': T(S('contra uma montadora', 452)),
    'sub': 'um líder que sofria assédio de um subordinado', 'tSub': T(S('sofria assédio', 455))}, sfx=[('tick', S('238', 449.8), -24)])
cue('v26_tst', 'elevMini', S('15 reclamações', 461) - 0.6, Ee('existia um freio', 476) + 0.8, {
    'count': 15, 'tCount': T(S('15 reclamações', 461)), 'countDur': 1.8, 'top': 175, 'size': 46,
    'texts': [{'t': T(S('15 reclamações', 461)), 'text': '15 reclamações em dois anos'},
              {'t': T(S('a empresa não fez nada', 463.3)), 'text': '15 reclamações em dois anos.<br><span style="color:#F2B3A3">A empresa não fez nada.</span>'},
              {'t': T(S('15 vezes o conflito subiu', 471.3)), 'text': '15 vezes o conflito subiu —<br><span style="color:#E2C88F">e em nenhum andar existia um freio.</span>'}]})
# ---------------- O INIMIGO ----------------
cue('v28_curva', 'curve', S('uma palestra', 487) - 0.3, Ee('não muda a regra', 512) + 1.6, {
    'kicker': '1ª coisa: contratar um treinamento', 'label1': 'palestra / workshop', 'label2': 'alguns meses depois',
    'tEvent': T(S('vai gerar uma consciência', 492.5)), 'tDecay': T(S('alguns meses', 499)) , 'label3': 'gera consciência — mas não muda a regra.', 'tLabel3': T(S('não muda a regra', 511))})
cue('v31_modelos', 'contrast', S('a primeira modelos prontos', 560) - 0.4, Ee('realidade da empresa', 586) + 1.0, {
    'top': 175, 'divH': 340,
    'left': {'kicker': '2ª coisa · normativa', 'title': 'Modelos prontos ou ChatGPT', 'size': 48, 't': T(S('modelos prontos', 560.5)),
             'items': [{'text': 'é um risco', 'mark': 'no', 't': T(S('é um risco', 565))},
                       {'text': 'não conversa com a realidade da empresa', 'mark': 'no', 't': T(S('realidade da sua empresa', 568.5))}]},
    'right': {'kicker': 'outro caminho', 'title': 'Um profissional, um advogado', 'size': 48, 't': T(S('contratar um profissional', 574.5)),
              'items': [{'text': 'faz um diagnóstico', 'mark': 'ok', 't': T(S('fazer um diagnóstico', 581))},
                        {'text': 'constrói com a realidade da empresa', 'mark': 'ok', 't': T(S('realidade da empresa', 585.5))}]}})
cue('v32_gaveta', 'drawer', S('regulamento interno', 590) - 0.6, Ee('ele não implementa', 603) + 1.2, {
    'kicker': 'Ela recebe toda a parte normativa', 'caption': '…mas guarda numa gaveta.',
    'docs': [{'text': 'Regulamento interno', 't': T(S('regulamento interno', 590))}, {'text': 'Código de conduta', 't': T(S('código de', 591.5))},
             {'text': 'Política de gestão de conflito', 't': T(S('política de gestão de conflito', 593))}, {'text': 'Política antiassédio', 't': T(S('assédio moral e sexual', 597) - .9)},
             {'text': 'Manual de cultura', 't': T(S('manual de cultura', 598.5))}],
    'tDrawer': T(S('numa gaveta', 601.5) - .3)}, sfx=[('whoosh_down', S('numa gaveta', 601.5) - .2, -24)])
cue('v34_loop', 'loop', S('uma coisa complementa a outra', 620) - 0.3, Ee('vira conteúdo e treinamento', 632) + 0.5, {
    'cy': 400,
    'left': {'kicker': 'Indira', 'title': 'Regra', 'sub': 'o que a Indira escreve', 't': T(S('uma coisa complementa a outra', 620))},
    'right': {'kicker': 'Hellen', 'title': 'Comportamento', 'sub': 'o que eu escuto na sala', 't': T(S('eu escuto na sala', 623.2))},
    'tTop': T(S('vira escrita', 625.3)), 'topText': 'vira cláusula', 'tBottom': T(S('vira conteúdo', 631)), 'bottomText': 'vira conteúdo de treinamento', 'reverse': True})
cue('v35_documento', 'lettering', S('o documento ele muda a regra', 633) - 0.1, Ee('não muda o comportamento', 637) + 1.6, {'top': 215,
    'lines': [L('o documento ele muda a regra', 633.5, size=54, weight=650, display='O documento muda a regra,' if False else 'O documento, ele muda a regra,'),
              L('mas não muda o comportamento', 636, font='serif', size=70, cls='serif gold', display='mas não muda o comportamento.', gap=10)]})
cue('v36_improviso', 'lettering', S('a gente dá um nome', 645) - 0.3, Ee('gestão no improviso', 646.5) + 2.2, {'top': 250,
    'kicker': 'A gente dá um nome', 'kickerT': T(S('a gente dá um nome', 645)),
    'lines': [L('gestão no improviso', 646.5, font='serif', size=108, cls='serif gold', pop=(2,), display='Gestão no improviso.')]},
    sfx=[('impact', S('gestão no improviso', 646.5), -24)])
cue('v37_etapas', 'steps4', S('o método que a gente aplica', 649.5) - 0.3, Ee('perder o efeito', 674.5) + 0.25, {
    'tSteps': [T(S('o diagnóstico', 653)), T(S('a estrutura', 654.5)), T(S('a implementação', 655.8)), T(S('a liderança', 657.2))],
    'tMarket': T(S('começarem pela liderança', 661)), 'marketText': '↑ o mais comum no mercado: começar por aqui'})
# nota: a fala "três semanas depois vai perder o efeito" foi mantida no áudio, mas sem destaque gráfico,
# porque a versão 2 do roteiro retira "três semanas" da aula (decisão de conteúdo do cliente).
# ---------------- ETAPA 1 · DIAGNÓSTICO ----------------
cue('v38_etapa1', 'stepCard', S('falando sobre o diagnóstico', 677) - 0.6, S('tudo começa', 678.5) + 2.6, {'n': 1})
cue('v39_culpado', 'quote', S('ele vai falar que já sabe', 687) - 0.2, Ee('quem é o culpado', 690.5) + 1.2, {
    'text': 'Já sei o que está acontecendo.<br>Já sei quem é o culpado.', 'attrib': 'o dono, com o diagnóstico pré-pronto', 'size': 58})
cue('v40_sobe', 'elevMini', S('sobe até ele', 696) - 1.5, S('o chefe é o problema', 702.5) - 1.6, {'mode': 'up', 'text': 'ele só sabe aquilo que sobe até ele.', 'top': 190, 'size': 50, 'tMove': T(S('sobe até ele', 696) - .3), 'moveDur': 1.2, 'tText': T(S('só sabe aquilo', 695))})
cue('v41_chefe', 'lettering', S('o chefe é o problema', 702.5) - 1.5, Ee('anonimato', 709) + 1.2, {'top': 220,
    'lines': [Lfix('Ninguém vai à sala do chefe dizer que o chefe é o problema.', S('o chefe é o problema', 702.5) - 1.2, size=46, weight=650, step=.05),
              Lfix('Por isso o diagnóstico vem de fora.', S('nosso diagnóstico vem de', 706.5), font='serif', size=70, cls='serif gold', gap=18, step=.08)]})
cue('v42_clima', 'contrast', S('pesquisa de crime', 711.5) - 0.4, Ee('influencia essas decisões', 726) + 1.4, {
    'top': 180, 'divH': 330,
    'left': {'kicker': 'Pesquisa de clima', 'title': 'Como você se sente?', 'size': 50, 't': T(S('pesquisa de crime', 711.5)), 'dimAt': T(S('diagnóstico organizacional', 718)),
             'items': []},
    'right': {'kicker': 'Diagnóstico organizacional', 'title': 'Como as decisões são tomadas?', 'size': 50, 't': T(S('diagnóstico organizacional', 718)),
              'items': [{'text': 'e o que influencia essas decisões', 'mark': 'ok', 't': T(S('o que influencia essas decisões', 724.5))}]}})
cue('v43_medico', 'list', S('ir ao médico', 733) - 0.5, Ee('esses exames são o diagnóstico', 743.5) + 1.6, {
    'kicker': 'A analogia do médico', 'kickerT': T(S('ir ao médico', 733) - .4), 'top': 180, 'size': 46,
    'items': [{'n': '✕', 'text': 'ir ao médico e já pedir uma cirurgia', 't': T(S('pede uma cirurgia', 736)), 'strikeT': T(S('nenhum médico', 737.5)), 'dimAt': T(S('pedir exames', 741))},
              {'n': '✓', 'numColor': '#9FD3C7', 'text': 'nenhum médico trata sem pedir exames', 't': T(S('pedir exames', 741))},
              {'n': '=', 'text': 'Esses exames são o diagnóstico.', 't': T(S('esses exames são o diagnóstico', 743)), 'color': '#E2C88F', 'size': 56}]})
# ---------------- ETAPA 2 · ESTRUTURA ----------------
cue('v44_etapa2', 'stepCard', S('segunda etapa', 749.5) - 0.8, S('segunda etapa', 749.5) + 3.6, {'n': 2})
cue('v45_estrutura', 'lettering', S('com o diagnóstico na mão', 754) - 0.3, Ee('estrutura escrita', 762) + 1.8, {'top': 235,
    'lines': [L('com o diagnóstico na mão', 754, size=52, weight=650, display='Com o diagnóstico na mão,'),
              L('vai virar uma estrutura escrita', 761.5, font='serif', size=80, cls='serif gold', display='vira uma estrutura escrita.' if False else 'vai virar uma estrutura escrita.', gap=12)]})
cue('v46_aplicavel', 'lettering', S('o documento ele', 784.5) - 0.3, Ee('protege por ser aplicável', 789.5) + 1.8, {'top': 240,
    'lines': [L('o documento ele não protege por existir', 786, size=54, weight=650, display='O documento, ele não protege por existir.' if False else 'O documento não protege por existir.' if False else 'O documento, ele não protege por existir,'),
              L('ele protege por ser aplicável', 789, font='serif', size=84, cls='serif gold', pop=(4,), display='ele protege por ser aplicável.', gap=14)]},
    sfx=[('impact', S('protege por ser aplicável', 789) + 1.0, -26)])
# ---------------- ETAPA 3 · IMPLEMENTAÇÃO ----------------
cue('v47_etapa3', 'stepCard', S('terceira etapa', 791.5) - 0.15, S('terceira etapa', 791.5) + 3.4, {'n': 3})
cue('v49_advertencia', 'chain', S('só adverte', 826) - 0.6, Ee('anulada', 838.5) + 2.2, {
    'kicker': 'Orientação jurídica', 'kickerT': T(S('como advogada', 820.5)), 'top': 150, 'size': 40, 'arrowH': 24,
    'nodes': [{'text': 'Advertência por descumprir uma norma', 't': T(S('só adverte', 826))},
              {'text': 'sem comprovar que todos tinham ciência', 't': T(S('sem comprovar', 829.5))},
              {'text': 'a punição pode ser anulada nos tribunais do trabalho', 't': T(S('anulada', 838)), 'color': '#F2B3A3', 'size': 40}]})
cue('v50_ciencia', 'list', S('linguagem acessível', 851) - 1.3, Ee('tinham ciência', 858.5) + 1.6, {
    'kicker': 'Na implementação', 'kickerT': T(S('linguagem acessível', 851) - 1.2), 'top': 185, 'size': 44,
    'items': [{'n': '01', 'text': 'treinamento com linguagem acessível', 't': T(S('linguagem acessível', 851))},
              {'n': '02', 'text': 'todos conhecem as regras', 't': T(S('conhecimento das regras', 855))},
              {'n': '03', 'text': 'a empresa fica com a comprovação de ciência', 't': T(S('comprovação de que eles tinham ciência', 858)), 'color': '#E2C88F'}]})
# ---------------- ETAPA 4 · LIDERANÇA ----------------
cue('v52_etapa4', 'stepCard', S('quarta etapa', 881.5) - 0.6, S('quarta etapa', 881.5) + 3.4, {'n': 4})
cue('v53_promovido', 'chain', S('competência técnica', 899) - 2.4, Ee('vai subir', 915) + 1.6, {
    'kicker': 'Por que o conflito sobe', 'kickerT': T(S('competência técnica', 899) - 2.3), 'top': 150, 'size': 40, 'arrowH': 22,
    'nodes': [{'text': 'promovido pela competência técnica', 't': T(S('competência técnica', 899) - .4)},
              {'text': 'não sabe conduzir conversas difíceis', 't': T(S('conversas difíceis', 904))},
              {'text': 'adia a conversa', 't': T(S('adiar essas conversas', 909.5))},
              {'text': 'o conflito sobe de andar', 't': T(S('vai subir', 915)), 'color': '#E2C88F', 'size': 48}]})
cue('v54_mapeia', 'contrast', S('mapeia essa liderança', 920.5) - 0.6, Ee('para poder resolver esse conflito', 935) + 1.2, {
    'top': 175, 'divH': 330,
    'left': {'kicker': 'Antes de treinar, mapear', 'title': 'Não sabe lidar com conflitos', 'size': 44, 't': T(S('não sabe lidar com conflitos', 924.5)),
             'items': [{'text': 'aprende a lidar com o conflito', 'mark': 'ok', 't': T(S('lidar com conflitos', 927))}]},
    'right': {'kicker': ' ', 'title': 'Atropela os conflitos', 'size': 44, 't': T(S('atropela os conflitos', 930.5)),
              'items': [{'text': 'aprende a esperar', 'mark': 'ok', 't': T(S('ensinar ele a esperar', 932.5))}]}})
cue('v55_ferramenta', 'tool', S('auxílio da ia', 951.5) - 0.6, Ee('conversas difíceis', 975) + 1.0, {
    'title': 'Ferramenta do líder · com IA',
    'items': [{'text': 'Advertir, suspender ou demitir por justa causa?', 't': T(S('advertir', 954))},
              {'text': 'Guia de conversas difíceis', 't': T(S('guia de conversas', 962))},
              {'text': 'Do relato do caso ao PDI', 't': T(S('relato do caso', 967))},
              {'text': 'Como dar feedback', 't': T(S('dar feedback', 973.5))}]})
# ---------------- MANDALA ----------------
t_m0 = S('uma mandala', 983) - 0.9
cue('v56_mandala', 'mandala', t_m0, Ee('realizado dentro do programa', 1016) + 0.6, {
    'title': 'a gente pinta de dentro para fora',
    'tMarket': T(S('insiste em pintar a mandala', 988)), 'tInside': T(S('de dentro pra fora', 993.5)),
    'rings': [T(S('de dentro pra fora', 993.5) + k * 0.45) for k in range(4)],
    'marketText': '✕  o mercado insiste em pintar de fora para dentro',
    'deps': [{'t': T(S('treinar a liderança sem antes eu estruturar', 996.5)), 'text': 'Não tem como treinar a liderança sem antes estruturar.'},
             {'t': T(S('estruturar sem antes eu diagnosticar', 1001)), 'text': 'Não tem como estruturar sem antes diagnosticar.'},
             {'t': T(S('preciso também implementar', 1005.5)), 'text': 'Estruturar e implementar o que foi escrito.'},
             {'t': T(S('preparar a liderança para sustentar', 1011)), 'text': 'E preparar a liderança para sustentar tudo isso.'}]},
    layout='split', sfx=[('whoosh_down', t_m0, -20)])
# ---------------- TESTE ----------------
cue('v57_teste', 'lettering', S('fazer o teste', 1021) - 0.5, Ee('uma pra cada etapa', 1030) + 1.0, {'top': 210,
    'kicker': 'O teste', 'kickerT': T(S('fazer o teste', 1021) - .4),
    'lines': [L('pegue uma caneta um papel', 1024.5, font='serif', size=74, cls='serif', color='#FFFFFF', display='Pegue uma caneta, um papel.'),
              Lfix('Quatro perguntas — uma para cada etapa.', S('quatro perguntas', 1028), size=44, weight=600, color='#E2C88F', gap=16)]})
QS = [(1, 'Diagnóstico', 'Eu sei como a minha equipe percebe as decisões — por dado, ou só pelo que chega à minha mesa?', S('a primeira pergunta é', 1037), Ee('minha mesa', 1046.5), None),
      (2, 'Estrutura', 'Duas pessoas que fazem a mesma coisa recebem a mesma resposta, mesmo com líderes diferentes?', S('a segunda pergunta', 1048), Ee('líderes diferentes', 1055.5), None),
      (3, 'Implementação', 'A minha equipe conhece as regras antes da primeira advertência?', S('pergunta número 3', 1058), Ee('ela conhece', 1066.5), ('Existe registro e comprovação de que ela conhece?', S('existe registro', 1064))),
      (4, 'Liderança', 'Os meus líderes sabem conduzir conversas difíceis, em vez de deixar que elas subam?', S('quarta pergunta', 1069), Ee('que elas suban', 1074), None)]
for n, step, q, a, b, q2 in QS:
    p = {'n': n, 'step': step, 'q': q, 'size': 50 if len(q) < 90 else 46}
    if q2: p.update({'q2': q2[0], 'tQ2': T(q2[1])})
    cue(f'v58_q{n}', 'question', a - 0.3, b + (0.7 if n < 4 else 0.9), p, sfx=[('tick', a - 0.2, -24)])
cue('v59_partida', 'lettering', S('se o seu primeiro não', 1075.5) - 0.2, Ee('ponto de partida', 1081) + 1.8, {'top': 235,
    'lines': [L('esse primeiro não', 1077, size=56, weight=650, display='Esse primeiro “não”'),
              L('é o seu ponto de partida', 1079.5, font='serif', size=84, cls='serif gold', pop=(4,), display='é o seu ponto de partida.', gap=12)]})
cue('v61_semana', 'roles', S('para o dono', 1093.5) - 0.9, Ee('realizá-la', 1118) + 1.0, {
    'kicker': 'Para fazer durante a semana',
    'cards': [{'role': 'Dono', 'text': 'Anote de que andar veio cada problema de gente que chegou até você.', 't': T(S('para o dono', 1093.5))},
              {'role': 'RH', 'text': 'Liste as três situações que mais se repetem e não têm regra escrita.', 't': T(S('do rh', 1102.5))},
              {'role': 'Líder', 'text': 'Escolha a conversa que está adiando e marque uma data na agenda.', 't': T(S('um líder', 1109))}]})
# ---------------- CTA ----------------
cue('v62_experiencia', 'lettering', S('te presentear', 1141.5) - 0.4, Ee('experiência cultura em ação', 1145) + 2.8, {'top': 225,
    'kicker': 'Um presente para quem ficou até o final', 'kickerT': T(S('te presentear', 1141.5) - .3),
    'lines': [L('experiência cultura em ação', 1145, font='serif', size=88, cls='serif gold', display='Experiência Cultura em Ação')]})
cue('v63_passos', 'cta', S('o primeiro passo', 1159.5) - 0.3, Ee('reunião de direcionamento', 1184) + 6.5, {
    'kicker': 'Como funciona a Experiência',
    'steps': [{'text': 'Escuta', 'sub': 'a realidade da sua empresa', 't': T(S('escutar e saber', 1163))},
              {'text': 'Panorama executivo', 'sub': 'uma leitura integral do que encontramos', 't': T(S('panorama executivo', 1173))},
              {'text': 'Reunião de direcionamento', 'sub': 'o que priorizar primeiro + passo a passo', 't': T(S('reunião de direcionamento', 1184))}]})
cue('v63b_vagas', 'lettering', S('três vagas', 1203) - 1.4, Ee('ganhar de presente', 1209) + 0.6, {'top': 230,
    'kicker': 'Nesta edição', 'kickerT': T(S('três vagas', 1203) - 1.3),
    'lines': [L('três vagas', 1203, font='serif', size=110, cls='serif gold', display='3 vagas'),
              L('100% custeado', 1205, size=56, weight=700, display='100% custeado', gap=10)]})
cue('v64_link', 'linkDown', S('clique no link aqui embaixo', 1213) - 0.2, Ee('vencedor', 1222) + 0.4, {'text': 'Clique no link aqui embaixo', 'top': 1250})
cue('v65_final', 'lettering', S('empresa organizada', 1225) - 0.5, Ee('e tudo começa sabendo o', 1231.5) + 0.7, {'top': 215,
    'lines': [L('uma empresa organizada ela não acontece', 1225, size=50, weight=650, display='Uma empresa organizada, ela não acontece'),
              L('por acaso', 1228, size=50, weight=650, display='por acaso.'),
              L('construída', 1230, font='serif', size=104, cls='serif gold', pop=(0,), display='Construída.', gap=14),
              L('e tudo começa sabendo o', 1231.5, size=46, weight=600, display='E tudo começa sabendo ouvir.', gap=20, color='#F5F0E6')]})
cue('v66_fim', 'lettering', S('muito obrigada', 1234.5) - 0.2, 1245.2, {'top': 300,
    'kicker': 'Experiência', 'kickerT': T(S('muito obrigada', 1234.5)),
    'lines': [Lfix('Cultura em Ação', S('muito obrigada', 1234.5) + 0.2, font='serif', size=100, cls='serif', color='#FFFFFF'),
              Lfix('Inscreva-se no link abaixo', S('se inscrevam', 1238), size=40, weight=600, color='#E2C88F', gap=20)]})

if __name__ == '__main__':
    import json
    json.dump(CUES, open('/home/user/work/project/visual_map.json', 'w'), ensure_ascii=False, indent=1)
    tot = sum(c['end'] - c['start'] for c in CUES)
    print(len(CUES), 'cues', f'{tot:.0f}s covered of 1245s ({tot/12.45:.0f}%)')
    for c in CUES: print(f"{c['id']:20s} {c['scene']:10s} {c['start']:8.2f} {c['end']:8.2f} {c['end']-c['start']:5.1f}s {c['layout']}")

# Projeto editável — "O elevador do conflito"

Todo o vídeo final é gerado por código, a partir do arquivo bruto (`IMG_0623.MOV`). Isso permite mudar uma animação, um corte ou a cor e renderizar de novo sem refazer o resto.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `scripts/` | pipeline em Python: transcrição, análise, cortes, cor, áudio, legendas, montagem e controle de qualidade |
| `motion/` | motor de motion graphics (HTML/SVG renderizado quadro a quadro no Chromium) e as cenas (`engine/scenes/*.js`) |
| `dados/` | transcrição com tempos, mapa de edição (`visual_map.json`), lista de cortes com justificativa (`cut_report.json`), plano de montagem (`plan.json`) |
| `cor/` | LUTs 3D do color grading: `fg.cube` (pessoas) e `bg.cube` (fundo) |
| `fontes/` | Inter Tight e Fraunces (licença SIL Open Font License) |
| `sfx/` | efeitos sonoros sintetizados para este projeto (sem amostras de terceiros) |
| `legendas/` | legendas estilizadas (`.ass`) usadas na versão com legenda gravada |

## Como o vídeo é montado

1. `asr.py`: segmenta a fala (Silero VAD) e transcreve com marcação de tempo por sílaba (NVIDIA Parakeet TDT v3, local).
2. `diarize.py` e `analyze_video.py`: identificam quem fala (voz + movimento da boca), recortam as pessoas (MediaPipe) e localizam os rostos.
3. `finalize_cuts.py`: aplica os cortes de fala aprovados e ajusta cada emenda ao quadro de vídeo e ao ponto mais silencioso do áudio (deslocamento máximo de 20 ms, imperceptível).
4. `visual_map.py`: mapa de edição. Cada animação está ancorada nas palavras realmente faladas.
5. `build_plan.py`: converte cortes + mapa de edição no plano de montagem (EDL, enquadramentos, tela dividida, efeitos sonoros).
6. `motion/engine/render.mjs`: renderiza as animações com fundo transparente.
7. `audio_master.py`: monta o áudio com crossfades de 12 ms, equaliza, comprime de leve, equilibra as duas vozes e normaliza em -14 LUFS / -1 dBTP.
8. `render.py`: decodifica o bruto, aplica a cor (ffmpeg: 2 LUTs + máscara das pessoas + contraste local), reenquadra, sobrepõe as animações e codifica as duas versões (com e sem legenda).
9. `qa.py`: controle de qualidade (quadros pretos, congelamentos, loudness, re-transcrição de cada emenda).

## Para alterar

- **Texto ou tempo de uma animação:** edite `scripts/visual_map.py` e rode `visual_map.py` → `build_plan.py` → `render.mjs` → `render.py`.
- **Desfazer um corte:** remova a entrada correspondente em `dados/cuts.json` e rode `finalize_cuts.py` → `build_plan.py`.
- **Cor:** ajuste `scripts/grade.py`, gere as LUTs com `make_luts.py` e renderize.

Os caminhos nos scripts apontam para `/home/user/work` (o ambiente onde a edição foi feita).

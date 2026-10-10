#!/bin/bash
# Copia o projeto editável (scripts, cenas, mapa de edição, dados) para a pasta de entrega do repositório.
set -e
W=/home/user/work
D=/home/user/editor-de-v-deo/entrega/Projeto_Editavel
mkdir -p $D/scripts $D/motion/engine/scenes $D/dados $D/cor $D/fontes $D/sfx $D/legendas
cp $W/project/*.py $W/project/*.sh $D/scripts/
cp $W/project/fg.cube $W/project/bg.cube $D/cor/
cp $W/project/fonts/*.ttf $D/fontes/
cp $W/project/sfx/*.wav $D/sfx/
cp $W/gfx/engine/lib.js $W/gfx/engine/stage.html $W/gfx/engine/style.css $W/gfx/engine/render.mjs $D/motion/engine/
cp $W/gfx/engine/scenes/*.js $D/motion/engine/scenes/
cp $W/gfx/fonts.css $W/gfx/package.json $D/motion/
cp $W/gfx/jobs.json $D/motion/jobs.json
cp $W/project/visual_map.json $D/dados/
for f in plan.json cuts.json edl_refined.json cut_report.json out_words.json; do [ -f $W/build/$f ] && cp $W/build/$f $D/dados/; done
for f in asr_parakeet.json words.json vad_segments.json roteiro.txt transcricao_final.md transcricao_final.json; do [ -f $W/analysis/$f ] && cp $W/analysis/$f $D/dados/; done
[ -f $W/build/subs.ass ] && cp $W/build/subs.ass $D/legendas/legendas_estilizadas.ass
echo "exportado para $D"

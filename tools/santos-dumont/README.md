# Gerador do Santos Dumont jogável

Scripts do Blender (5.2) que produzem `lib/santos-dumont.js`, a malha com esqueleto do personagem.

**Base:** corpo masculino realista do pacote *Human Base Meshes* v1.4.1 da Blender Studio (CC0),
baixado de `https://mirror.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip`.
O pacote não fica no repositório (cerca de 50 MB): guarde o `human_base_meshes_bundle.blend` em `base/` (ignorada pelo git).

**O que cada etapa faz**

| script | etapa |
|---|---|
| `stage1.py` | esculpe o rosto a partir das fotos de época (rosto estreito e comprido, mandíbula fina, nariz longo, bochechas magras, orelhas de abano), cria o esqueleto, afina o corpo (cerca de 50 kg), baixa os braços e escala para **1,52 m**. Cria também os **dedos** (`fingers.py`): 15 ossos por mão — polegar desde o pulso e 3 falanges por dedo —, com as juntas tiradas dos *face sets* de cada falange da malha base (64–103), os pesos da mão repartidos entre palma e falanges pela geometria de cada falange, e o **eixo de flexão** de cada dedo (vai para o `.js` como `ax`: + fecha para a palma). A mão relaxada de repouso é feita dobrando esses ossos |
| `stage2a.py` | paletó de 4 botões com decote em V e lapelas (tronco em fatias, sem os braços), **mangas separadas com "bola" de ombro** (nada estica embaixo do braço), saia do paletó, calças e botinas |
| `stage2b.py` | camisa, **colarinho alto engomado**, gravata xadrez (fotos do 14-bis, nov/1906), botões, bolsos, punhos, **relógio Cartier Santos** no pulso esquerdo, cabelo repartido ao meio, sobrancelhas, **bigode**, **panamá desabado** e sola grossa com salto, **arnês de voo** (alças de couro e argolas nos ombros onde se prendem os cabos dos ailerons, visível só a bordo) e **pálpebras** que piscam (ossos `lid.L/lid.R`) |
| `stage3.py` | recorta o corpo escondido, reduz a malha, calcula os pesos de skinning e as cores dos vértices, depois exporta tudo quantizado em base64 para o arquivo `.js` (ossos dos dedos com `ax`, eixo de flexão, e `t`, ponta da falange) |

A textura risca-de-giz, a palha do panamá, os fios de cabelo, a íris e o xadrez da gravata são desenhados em canvas
no próprio jogo (bloco `SANTOS DUMONT jogável` em `v2/index.html`).

O **movimento** não é animação do Blender: é feito em código no mesmo bloco — pernas por IK com o pé travado no chão
(caminhada e corrida casadas com a velocidade), braços em pêndulo, poses de mão (relaxada, punho, aberta) e, no 14-bis,
a pega calculada: a mão se orienta pela peça, o braço faz IK até o pulso e cada falange fecha até encostar nela
(a manete do acelerador, tipo freio de bicicleta, fecha o indicador e o médio).

**Como regenerar**

```sh
B=".../blender-5.2.2-windows-x64/blender.exe"
"$B" -b base/human_base_meshes_bundle.blend --python stage1.py
"$B" -b --python stage2a.py
"$B" -b --python stage2b.py
"$B" -b --python stage3.py        # grava build/santos-dumont.js; copie para lib/
```

Os arquivos intermediários (`.blend`, juntas em `.json` e prévias em `.png`) vão para `build/` (ignorada pelo git). Para usar outra pasta, defina `SD_WORK`.
Cada etapa leva poucos segundos. `build/original-2026-09-26/` guarda os `.blend` da primeira versão (sem dedos), recuperados da
pasta temporária da sessão que criou o personagem.

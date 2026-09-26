# Gerador do Santos Dumont jogável

Scripts do Blender (5.2) que produzem `lib/santos-dumont.js`, a malha com esqueleto do personagem.

**Base:** corpo masculino realista do pacote *Human Base Meshes* v1.4.1 da Blender Studio (CC0),
baixado de `https://mirror.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip`.
O pacote não fica no repositório (cerca de 50 MB).

**O que cada etapa faz**

| script | etapa |
|---|---|
| `stage1.py` | esculpe o rosto a partir das fotos de época (rosto estreito e comprido, mandíbula fina, nariz longo, bochechas magras, orelhas de abano), cria o esqueleto, afina o corpo (cerca de 50 kg), baixa os braços, curva os dedos e escala para **1,52 m** |
| `stage2a.py` | paletó de 4 botões com decote em V e lapelas (tronco em fatias, sem os braços), **mangas separadas com "bola" de ombro** (nada estica embaixo do braço), saia do paletó, calças e botinas |
| `stage2b.py` | camisa, **colarinho alto engomado**, gravata xadrez (fotos do 14-bis, nov/1906), botões, bolsos, punhos, **relógio Cartier Santos** no pulso esquerdo, cabelo repartido ao meio, sobrancelhas, **bigode**, **panamá desabado** e sola grossa com salto, **arnês de voo** (alças de couro e argolas nos ombros onde se prendem os cabos dos ailerons, visível só a bordo) e **pálpebras** que piscam (ossos `lid.L/lid.R`) |
| `stage3.py` | recorta o corpo escondido, reduz a malha, calcula os pesos de skinning e as cores dos vértices, depois exporta tudo quantizado em base64 para o arquivo `.js` |

A textura risca-de-giz, a palha do panamá, os fios de cabelo, a íris e o xadrez da gravata são desenhados em canvas
no próprio jogo (bloco `SANTOS DUMONT jogável` em `v2.html`).

**Como regenerar**

```sh
B=".../blender-5.2.2-windows-x64/blender.exe"
"$B" -b human_base_meshes_bundle.blend --python stage1.py
"$B" -b --python stage2a.py
"$B" -b --python stage2b.py
"$B" -b --python stage3.py        # grava build/santos-dumont.js; copie para lib/
```

Os arquivos intermediários (`.blend`, juntas em `.json` e prévias em `.png`) vão para `build/`. Para usar outra pasta, defina `SD_WORK`.

# 14 Bis do Dumont 🇧🇷✈️

Jogo de exploração 3D da Encantada, casa de Santos Dumont em Petrópolis/RJ
(1918), feito com Three.js a partir de um acervo local de fotos e plantas (não
incluído no repositório por direitos de imagem) e da pesquisa documentada em
[PESQUISA.md](PESQUISA.md). Inclui a réplica voável do **14-bis**
([14BIS.md](14BIS.md)) e uma **serra de Petrópolis de ~5 × 5 km** para voar,
com a cidade, os marcos históricos e a Mata Atlântica — e, descendo a serra para o sul,
a **Pequena Rio de Janeiro**, onde termina a missão **"Por céus nunca dantes navegados"**.

## Como abrir
Basta dar **duplo clique em `index.html`**: ele abre a página de escolha de
versão. Funciona offline (o Three.js está em `lib/three.min.js`, a capa é
local e as texturas da cena são geradas por código). Não há
nenhuma dependência externa: nada de CDN, fontes remotas ou rastreadores.

## Versões
| Arquivo | Versão | O que é |
|---|---|---|
| `index.html` | — | Página de abertura para escolher a versão |
| `v2.html` | **Versão 2** (atual) | A serra de Petrópolis para voar, o 14-bis com física real, a cidade e os marcos (este README descreve esta versão) |
| `v1.html` | **Versão 1.0** (histórico) | A primeira versão: a casa A Encantada e o 14-bis no Campo de Bagatelle, congelada como estava na tag git `v1.0` |

**Autoria:** a versão 1 foi criada pelo **Claude Fable 5**. A versão 2 é a
continuação do projeto do Fable 5, feita pelo **Claude Opus 5.5**.

A versão 1 é guardada só como registro, então não a edite. O código original
dela fica na tag: `git checkout v1.0`. Links antigos com parâmetros
(`index.html?shot=…`) são redirecionados para `v2.html`.

## Jogar online (GitHub Pages)
O jogo é 100% estático, então basta servir a raiz do repositório:
1. Crie o repositório no GitHub e envie estes arquivos.
2. Em **Settings → Pages**, escolha *Deploy from a branch*, branch `main`,
   pasta `/ (root)`.
3. Acesse `https://SEU-USUARIO.github.io/NOME-DO-REPO/`.

## Controles
No jogo, abra **⚙ Configurações** para consultar e remapear as teclas, além de
acessar o mapa, o modo noturno e os destinos. As preferências ficam salvas no navegador.

| Tecla | Ação |
|---|---|
| Clique | ativa o mouse (olhar em 1ª pessoa) |
| `W A S D` | andar |
| `Shift` | correr |
| `Espaço` | pular |
| `E` | abrir/fechar a porta ou as venezianas da janela mais próxima; acender a lareira; **conversar** com o Chapin e com a Virgínia (missão) |
| `F` | **entrar/sair do 14-bis** (como no GTA — para sair, pouse e pare) |
| `C` | troca a câmera: 3ª pessoa (Santos Dumont de terno e panamá) → 3ª pessoa aberta → 3ª pessoa bem perto (no ombro) → 1ª pessoa; pilotando, alterna os pontos de vista do 14-bis |
| Rodinha do mouse | zoom: a pé, aproxima/afasta a câmera de 3ª pessoa (cada câmera lembra o seu zoom) e, na 1ª pessoa, vira luneta (até 2,8×); pilotando, zoom das câmeras do 14-bis |
| `V` | alterna rapidamente entre a câmera externa e a 1ª pessoa |
| `G` | voo livre (`Espaço` sobe, `Shift` desce; acelera com a altura) |
| `M` | mapa da serra (o minimapa com bússola e rumo aparece ao voar) |
| `R` | pilotando: volta ao Campo de Bagatelle |
| `↑ ↓ ← →` | pilotando: controlar a célula dianteira |
| `Q / Z` | pilotando: ajustar o compensador |
| `I / O` | pilotando: ignição / som do motor |
| `N` | dia ↔ noite |
| `1`–`0` | teleporte: Jardim, Rua & Relógio, Porão, Sala, Mezanino, Passarela, Observatório, **Campo de Bagatelle**, **Centro** (Catedral), **Mirante** (capela do morro) |
| `Esc` | abre/fecha Configurações e fecha o mapa |

## ✉️ Missão: "Por céus nunca dantes navegados"

Petrópolis, novembro de 1906 — dias depois dos 220 m de Bagatelle. Um telegrama
chama Santos Dumont à **tenda-oficina do Campo de Bagatelle** (atrás do público),
onde o mecânico **Albert Chapin** conta a história dos recordes e entrega uma
encomenda para **Virgínia**, a irmã que ensinou Alberto a ler: um exemplar de
*Dans l'air* embrulhado na seda japonesa das asas. O pacote vai na mão do
Santos Dumont até o 14-bis e depois **amarrado no cesto**. Voe para o sul (siga o
rio Piabanha até o lago do Quitandinha e a Estrada da Serra até a baía), **pouse
na areia de Copacabana, entre as fogueiras**, desça (`F`) e leve o pacote até o
**coreto da Avenida Atlântica**, onde ela espera para completar a história.

- `E` conversa (perto da pessoa) e avança o diálogo; `Esc` fecha.
- O objetivo aparece no alto da tela, com distância e direção; uma **coluna de luz
  dourada** marca o destino no mundo e uma ★ aponta no minimapa e no mapa (`M`).
- Se o 14-bis quebrar, o pacote continua a salvo no cesto: `R` volta ao campo.
- A encomenda tem de chegar **pelo céu** — a pé ou por teleporte, a Virgínia pede
  para ver o aeroplano chegar.
- No fim, a *Gazeta da Pequena Rio* conta o feito (distância, tempo, altura) e uma
  **nota histórica** separa o que é fato do que é licença poética; o povo corre para
  a praia e há fogos sobre o mar. Para voar de novo, fale outra vez com o Chapin.

## 🏖 A Pequena Rio de Janeiro (1906, em miniatura)

Ao sul da serra, uma capital de brinquedo (~1:10) com os marcos no lugar certo do
mapa: a **baía de Guanabara** com o **Pão de Açúcar** e o Morro da Urca na barra, o
**Cristo Redentor** no Corcovado (licença poética: o de verdade é de 1931), a
**Avenida Central** e o **Obelisco** de 1906, o **Theatro Municipal em obras**
(inaugurado em 1909), a **Candelária**, a **Praça XV** com o Paço Imperial (em 1906,
Correios e Telégrafos), o chafariz do Mestre Valentim e o Cais Pharoux, a **Ilha
Fiscal**, os **Arcos da Lapa com o bonde**, o Outeiro da Glória, o Palácio do
Catete, a **Avenida Beira-Mar** (inaugurada em novembro de 1906), Botafogo, a
**praia de Copacabana** com a igrejinha no rochedo, Niterói e a Fortaleza de Santa
Cruz — com povo, tílburis, a barca de Niterói, vapores e saveiros. Em
**Configurações → Visitar um lugar** há atalhos para Copacabana, a Praça XV e o
Cristo. O mar vai até o horizonte; pousar nele derruba o 14-bis.

## ✈️ Pilote o 14-bis!

No **Campo de Bagatelle** (tecla `8`) está a réplica voável do *Oiseau de
Proie*, com as medidas e o desempenho do avião real — documentação completa
e fontes em [14BIS.md](14BIS.md). `F` junto ao cesto embarca. `W` abre o gás:
o mecânico gira a hélice ("Contato!"), os ajudantes seguram as asas até o
Antoinette encher e soltam o avião. A ~37 km/h, `↑` levanta o canard e ele
decola; `↓` abaixa; `Q/Z` compensam a alavanca; `←/→` giram a roda de direção
à esquerda do cesto (guinada pela célula dianteira); `A/D` **inclina o corpo do piloto** (é assim que os
ailerons octogonais funcionavam!); `I` corta a ignição para pousar, como em
12/11/1906; `O` liga/desliga o som. Todas as teclas podem ser trocadas em
**Configurações**.

A física é de verdade: cada célula de seda, as paredes das células, o canard
na junta cardã e os ailerons geram sustentação e arrasto; o motor de 50 cv
move uma hélice de pás-remo com rendimento de época, e o avião voa entre
~35 e ~47 km/h, sobe menos de 1 m/s e é instável em guinada (Santos Dumont:
"como atirar uma flecha com as penas na frente") — corrija sempre com a
roda de direção. Câmeras: `C` troca entre 9 pontos de vista (perseguição, lateral
como nas fotos de 1906, frente, espectador no gramado, no canard, na ponta
da asa, atrás da hélice, órbita livre, de cima), `V` vai para o cesto (olhos
de Santos Dumont) e a **rodinha do mouse dá zoom** — de pertinho, até ver as mãos dele na
roda de direção e na manete do acelerador. Os dados de voo aparecem num **painel de
instrumentos de época** (mostradores de latão e esmalte, relógio Cartier, contadores de
tambor); `H` esconde o painel. Voe 25 m para a **Taça
Archdeacon** e 100 m para o **Prêmio do Aeroclube da França** — há marcos
de 25, 60, 100 e 220 m ao lado da pista. Cuidado para não capotar, não
arrastar a asa nem acertar a casa! A pista segue ~180 m além do campo,
sempre livre, e a biruta mostra o vento de oeste: decole contra ele.

## 🗺️ A serra para voar
Um mapa de ~5,2 × 5,2 km (norte = vale em frente à casa) com relevo baixo de
propósito — morros de 15–80 m e cristas de fundo em camadas que somem na
névoa —, para que voando se veja longe. Marcos que servem de referência de
navegação (todos com legenda histórica ao se aproximar):
- **Catedral de São Pedro de Alcântara** — a agulha de ~70 m, farol do Centro,
  com o **dirigível Nº 6** dando voltas por cima.
- **Museu Imperial** (palácio rosa, jardim e alameda de palmeiras-imperiais),
  **Palácio de Cristal** (acende à noite) e a **praça do Obelisco**.
- O **rio Piabanha** em canal de pedra pelo Centro, seguindo para o norte até
  as lavouras de **Itaipava**; o córrego que vem do leste ao lado da pista.
- **Estação de Petrópolis** e a **ferrovia** com o trem de cremalheira subindo
  a serra (a locomotiva empurra na subida), com ponte de treliça.
- **Quitandinha**, o palácio normando diante do **lago com o formato do mapa
  do Brasil**.
- **Capela do morro** (em frente à casa, marca o norte), **Trono de Fátima**
  (ao sul) e o **Dedo de Deus** na Serra dos Órgãos (nordeste).
- ~700 casas coloniais e chalés, vilarejos, fazendas, lampiões, urubus nas
  térmicas e ~45 mil árvores da Mata Atlântica — ipês-amarelos, quaresmeiras,
  embaúbas e araucárias.

## 🎬 Visual
Céu físico em shader (sol dourado de fim de tarde, nuvens, estrelas, lua e
Via Láctea), névoa de altitude com dispersão solar, sombras das montanhas
pré-calculadas, luz ambiente do próprio céu (IBL), pós-processamento HDR
(bloom, raios crepusculares, curva de filme ACES, gradação de cor, vinheta) e
texturas procedurais com mapas de normais, calibradas pelas fotos do acervo.
A resolução se ajusta sozinha se o computador não der conta.

## O que explorar
- **Escada do Vencedor** (externa, verde): degraus recortados — só dá para
  começar a subir com o **pé direito**. Ela sobe pela lateral esquerda e
  desemboca no terraço da frente. A interna, de madeira escura, é espelhada
  (começa-se com o pé esquerdo) e sobe **da sala para o fundo**, como nas
  plantas.
- **Sala sem divisórias** com pé-direito duplo, lareira de canto, mesa-asa com
  as cartas emolduradas e um modelo do Demoiselle pendurado no vão.
- **Mezanino**: cama-cômoda com escadinha, a escrivaninha com o telefone de
  castiçal e o **puxadinho do banheiro** — anexo apoiado em escoras, com
  empena própria, janelão de guilhotina e o **chuveiro a álcool** (tido como
  o primeiro chuveiro quente do Brasil).
- **Entrada pela rua de cima**: a encosta chega no nível do mezanino — a
  passarela em treliça X leva à porta dupla sob o alpendre de frontão
  **encravado no próprio pano do telhado** (entrada do museu até hoje).
- **Observatório na cumeeira**: suba a escada-ponte de degraus alternados que
  sobe **em linha reta** da encosta lateral direita, por cima do telhado (ou
  use o teleporte `7`), para ver a luneta e a bandeira do Brasil. Experimente
  à noite!
- **Relógio de Flores** na rua de baixo, vizinho real da casa.
- Chegue perto dos pontos de interesse para ver as **legendas históricas**.

## Extras para depuração
`v2.html?shot=N` (0–9) abre direto em um dos pontos de vista;
`v2.html?cam=x,y,z,yaw,pitch` posiciona a câmera livremente;
`&night=1` modo noturno; `&closed=1` fecha portas e janelas;
`&fire=0` lareira apagada; `&fly14=1` abre com o 14-bis em pleno voo;
`&map=1` abre o mapa; `&wcam=N` (0–3) escolhe a câmera a pé; `&wheel=N` simula N giros da rodinha; `&dbg=1` mostra no DOM (`#dbg`) triângulos, draw
calls e tempos de carga. Qualidade: `?hq` (resolução até 2×), `?nopost`
(sem pós-processamento), `?lowshadow` (sombra 2048), `?noadapt` (sem
ajuste automático de resolução).

## Licença
Código sob [licença MIT](LICENSE). Inclui a biblioteca
[three.js](https://threejs.org) (MIT, `lib/three.min.js`). O acervo de fotos
e plantas usado como referência **não** faz parte do repositório. A arte da
capa (`assets/cover.png`) foi gerada por IA (ChatGPT, gpt-image); o prompt está
em [assets/cover-prompt.txt](assets/cover-prompt.txt).

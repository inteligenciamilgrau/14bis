# A Encantada — Casa 3D de Santos Dumont 🇧🇷✈️

Reconstrução 3D navegável da casa de Santos Dumont em Petrópolis/RJ (1918),
feita com Three.js a partir de um acervo local de fotos e plantas (não
incluído no repositório por direitos de imagem) e da pesquisa documentada em
[PESQUISA.md](PESQUISA.md). Inclui a réplica voável do **14-bis**
([14BIS.md](14BIS.md)).

## Como abrir
Basta dar **duplo clique em `index.html`** — funciona offline (o Three.js está
em `lib/three.min.js`, e todas as texturas são geradas por código). Não há
nenhuma dependência externa: nada de CDN, fontes remotas ou rastreadores.

## Jogar online (GitHub Pages)
O jogo é 100% estático, então basta servir a raiz do repositório:
1. Crie o repositório no GitHub e envie estes arquivos.
2. Em **Settings → Pages**, escolha *Deploy from a branch*, branch `main`,
   pasta `/ (root)`.
3. Acesse `https://SEU-USUARIO.github.io/NOME-DO-REPO/`.

## Controles
| Tecla | Ação |
|---|---|
| Clique | ativa o mouse (olhar em 1ª pessoa) |
| `W A S D` | andar |
| `Shift` | correr |
| `Espaço` | pular |
| `E` | abrir/fechar a porta ou as venezianas da janela mais próxima (estilo GTA) |
| `V` | câmera em 3ª pessoa — jogue como o próprio Santos Dumont, de terno e panamá |
| `F` | alternar modo voo (`Espaço` sobe, `Shift` desce) |
| `N` | dia ↔ noite |
| `1`–`8` | teleporte: Jardim, Rua & Relógio, Porão, Sala, Mezanino, Passarela, Observatório, **Campo de Bagatelle** |
| `Esc` | libera o mouse (para usar os botões) |

## ✈️ Pilote o 14-bis!

No **Campo de Bagatelle** (tecla `8`) está a réplica voável do *Oiseau de
Proie* — documentação completa em [14BIS.md](14BIS.md). `E` junto ao cesto
embarca; `W/S` gás; com velocidade, `↑` inclina a célula dianteira e o canard
decola; `←/→` guinada; `A/D` **inclina o corpo do piloto** (é assim que os
ailerons octogonais funcionavam!). Voe 25 m para a **Taça Archdeacon** e
100 m para o **Prêmio do Aeroclube da França** — e cuidado para não capotar
nem acertar a casa!

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
`index.html?shot=N` (0–6) abre direto em um dos pontos de vista;
`index.html?cam=x,y,z,yaw,pitch` posiciona a câmera livremente;
`&night=1` modo noturno; `&closed=1` fecha portas e janelas;
`&fire=0` lareira apagada; `&fly14=1` abre com o 14-bis em pleno voo.

## Licença
Código sob [licença MIT](LICENSE). Inclui a biblioteca
[three.js](https://threejs.org) (MIT, `lib/three.min.js`). O acervo de fotos
e plantas usado como referência **não** faz parte do repositório.

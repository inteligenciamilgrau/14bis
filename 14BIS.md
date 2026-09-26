# 14-bis — "Oiseau de Proie" — Documentação para o Simulador

Dossiê técnico para a réplica voável do 14-bis no mundo 3D da Encantada.
Cada peça é numerada para conferência durante a construção.

> **STATUS: v2 — física real ✅** — integrada ao `v2.html` (seção
> `14-BIS`, entre `/*FM14-BEGIN*/` e "luzes internas"). Modelo de voo de 6
> graus de liberdade com as medidas publicadas do avião (seção 6), modelo 3D
> refeito a partir das fotos de 1906 e 9 câmeras. As peças [1]–[47] estão
> marcadas por número nos comentários do código. Tecla `8` teleporta ao
> Campo de Bagatelle; `F` junto ao cesto embarca.

## 1. Ficha histórica

- **Nome**: Santos-Dumont Nº 14-bis, apelidado *Oiseau de Proie* ("Ave de Rapina").
  O nome vem de ter sido testado pendurado sob o dirigível Nº 14.
- **13/09/1906**: primeiro salto diante do Aeroclube (7 a 13 m); pouso violento
  que quebrou a hélice e o trem.
- **23/10/1906**, Campo de Bagatelle, Paris: decolou por meios próprios, voou
  **~60 m a ~3 m de altura em ~7 s**, fez uma leve curva à esquerda e ganhou a
  **Taça Archdeacon** (primeiro voo de 25 m).
- **12/11/1906**: com os **ailerons octogonais** recém-instalados, quatro voos;
  o último, às 16h45, decolou **contra o vento**, subiu a **~6 m quase
  estolando**, fez uma curva à direita, **cortou o motor** e pousou — a asa
  direita tocou o chão sem danos. **220 m em 21,5 s** (~37 km/h): prêmio do
  Aeroclube da França (primeiro voo de 100 m) e primeiro recorde da aviação.
- Diferente do Flyer dos Wright (catapulta/trilho), o 14-bis decolou **por
  meios próprios, com rodas**, diante de testemunhas oficiais — por isso o
  Brasil o celebra como o primeiro avião.

## 2. Como ele voa — o "ganso de pescoço esticado"

O 14-bis é um **canard**: voa "de costas" em relação aos aviões modernos.

- A **cauda fica na FRENTE**: uma célula-caixa (pipa Hargrave) de 2 × 2 × 1,5 m
  na ponta de uma fuselagem de seda de seção quadrada — o *pescoço do ganso*.
  Essa célula é o **profundor E leme** ao mesmo tempo: montada numa **junta
  cardã**, gira pra cima/baixo (arfagem) e pros lados (guinada).
- As **asas ficam ATRÁS**: biplano de 3 células Hargrave por lado, com
  **diedro de 10°** — as pontas sobem em "V", dando estabilidade lateral.
- A **hélice fica atrás de tudo** (configuração *pusher*): empurra em vez de puxar.
- O piloto vai **EM PÉ num cesto de vime de balão** (retangular, 0,94 m de
  altura — o original está no museu), logo à frente do motor.
- Para **subir**: o canard inclina o bordo de ataque para CIMA.
- É **quase neutro em arfagem** (CG a ~7 m do nariz, junto ao bordo de ataque
  da asa) e **instável em guinada**: as paredes do canard, à frente do CG, têm
  mais braço que as das asas. Santos Dumont: *"era como atirar uma flecha com
  as penas na frente"*.

## 3. Controles reais (1906) → teclas

| Comando de 1906 | O que faz | Tecla (padrão, remapeável em Configurações) |
|---|---|---|
| Alavanca (canard, mão direita) | inclina a célula dianteira → **arfagem** | `↑` / `↓` (volta ao neutro ao soltar) · `Q`/`Z` compensador |
| **Roda de direção** (mão esquerda, na lateral do cesto) | gira a célula dianteira pros lados → **guinada** | `←` / `→` |
| **Colete/arnês** (nov/1906) | cabos nos ombros do paletó acionam os **ailerons octogonais**: o piloto **inclina o corpo** e o avião rola | `A` / `D` |
| Gás do Antoinette | manete na alavanca (cabo Bowden até o motor) | `W` / `S` |
| Mecânico na hélice | partida à mão ("Contato!") | automática ao abrir o gás |
| Ajudantes | seguram as asas até o motor encher | soltam sozinhos com gás > 60% e ~1150 rpm |
| Corte da ignição | usado no pouso de 12/11 | `I` |

Câmeras: `C` troca entre 9 vistas (perseguição, lateral como nas fotos de
1906, frente ¾, espectador no gramado com teleobjetiva, no canard olhando o
piloto, ponta da asa, atrás da hélice, órbita livre, de cima); `V` vai para o
cesto (olhos de Santos Dumont, 1,52 m); **rodinha do mouse = zoom** — nas vistas externas ela
aproxima até ~0,6 m e o foco desliza para o cesto (roda de direção, alavanca e manete); o mouse
olha em volta / orbita. `H` esconde/mostra o painel de instrumentos. `O` liga o som do motor. `F` desembarca parado; `R`
volta à linha de largada.

## 4. Ficha técnica (valores usados no simulador)

| Item | Valor | Fonte |
|---|---|---|
| Envergadura | 11,5 m (3 células de 1,75 m por lado + vão central) | Wikipedia EN; Bitencourt et al. |
| Corda da asa / vão entre planos | 2,5 m / 1,5 m | Greco & Catalano |
| Área alar | 52 m² (+ canard 8 m²) | Wikipedia; Bitencourt et al. |
| Diedro / incidência | 10° / 3° | Bitencourt et al. (diedro); incidência reduzida por SD |
| Perfil da asa | placa de seda com 5% de curvatura | Greco & Catalano |
| Canard | 2 × 2 m, 1,5 m de altura, placas planas, junta cardã | Greco & Catalano |
| Comprimento | ~10 m (nariz do canard ao cubo da hélice) | todas |
| Peso em voo | 300 kg (Santos Dumont pesava ~50 kg) | 290–315 kg nas fontes |
| CG | ~7,2 m do nariz (logo à frente do bordo de ataque) | Greco & Catalano: 7,0–7,5 m |
| Motor | Antoinette V8 a 90°, 50 cv a 1500 rpm, camisas d'água de cobre | Vilares; Wikipedia PT |
| Hélice | 2 pás-remo de alumínio em braços de tubo de aço, Ø 2,2 m, rendimento ~20–30% | Wikipedia PT (20–40%) |
| Trem | 2 rodas de bicicleta lado a lado sob o motor + vara de proa + varas sob as asas | Greco & Catalano; fotos |
| Estrutura | bambu e pinho, juntas de alumínio, estais de corda de piano, seda japonesa envernizada | todas |

## 5. LISTA NUMERADA DE PEÇAS (conferência da construção)

### A. Fuselagem e estrutura
1. Fuselagem em caixa de seda afunilada (da junta cardã ao cesto), 4 longarinas de bambu
2. Quadros de pinho e juntas de alumínio
3. Estais de arame (corda de piano) e cabos de comando sobre a fuselagem

### B. Célula dianteira (canard — a "cabeça do ganso")
4. Caixa Hargrave 2 × 2 × 1,5 m: topo, fundo e duas paredes de seda
5. Junta cardã (cruzeta de aço) no fim da fuselagem
6. Cabos de comando do canard até a roda de direção e a alavanca
7. Molduras de bambu da célula com X de arame nas paredes

### C. Asas principais (células Hargrave traseiras)
8. Plano superior — 3 células de 1,75 m por lado, **diedro 10°**, curvatura de 5%
9. Plano inferior — idem
10. Quatro paredes verticais por lado (raiz, duas internas, ponta)
11. Montantes de bambu com juntas de alumínio
12. X de arame nas faces das células + estais de voo
13. Revestimento de seda japonesa envernizada (translúcida contra o sol, com costuras e nervuras)
14. **Ailerons octogonais** (2 m²) no meio do vão das células externas, girando no eixo da envergadura
15. Chifres, roldanas e cabos dos ailerons até os ombros do piloto

### D. Motopropulsor
16. Motor **Antoinette V8** a 90°: cárter de alumínio, 8 cilindros com camisas de cobre, balancins, tubos d'água
17. **Hélice bipá pusher** de pás-remo, Ø 2,2 m (disco borrado acima de ~300 rpm)
18. Eixo longo da hélice com mancal preso ao bordo de fuga
19. Condensador de tubos de latão
20. Tanque de gasolina elevado (latão) acima do motor
21. Escapamentos curtos (fumaça azulada em voo)
22. Cavalete do motor (longarinas de pinho e escoras de aço)

### E. Posto de pilotagem
23. **Cesto de vime retangular** (losangos vazados, borda de couro, cantoneiras) — piloto EM PÉ
24. **Roda de direção** raiada no lado esquerdo do cesto, girando para frente e para trás (mão esquerda)
25. **Alavanca** à direita do cesto (mão direita), com manete de acelerador tipo freio de bicicleta
26. **Arnês/colete** ligado aos ailerons (o avatar inclina o corpo)
27. Roldanas de latão na raiz das asas

### F. Trem de pouso
28. 2 rodas de bicicleta raiadas lado a lado (bitola 0,7 m), pneus de borracha
29. Garfos e **amortecedores telescópicos** (sobem com a compressão)
30. Vara de proa com patim curvo (o avião descansa de nariz alto, ~4°) e varas sob as asas

### G. Física do simulador (seção 6)
31. Sustentação e arrasto por superfície (asas, paredes, canard, ailerons, fuselagem), com estol e pós-estol de placa plana
32. Motor com curva de torque e hélice com CT/CP pela razão de avanço J (rpm dinâmico)
33. Arrasto de forma (montantes, arames, piloto, motor, trem) + efeito solo
34. **Arfagem via canard** na junta cardã
35. **Guinada via canard** (instabilidade direcional real)
36. **Rolagem via inclinação do corpo** (ailerons) + efeito diedro + torque de reação da hélice
37. Corrida com rodas, vara de proa arrastando, ajudantes segurando o avião
38. Pouso, pouso duro, asa raspando, cavalo de pau, capotagem e colisões com o mapa

### H. Interação e jogo
39. Campo de Bagatelle com marcos de 25, 60, 100 e 220 m
40. Tecla **F** para embarcar/desembarcar do cesto
41. Teclas da seção 3 (remapeáveis em Configurações)
42. 9 câmeras + cesto, zoom na rodinha do mouse
43. **Painel de instrumentos de época** (nogueira, couro costurado, aros de latão, esmalte envelhecido, vidro): velocímetro (ponteiro vermelho = velocidade no solo; faixas de estol e de voo), altímetro de 2 ponteiros, conta-giros do Antoinette (faixa vermelha acima de 1500 rpm), variômetro, bússola com rosa dos ventos e seta do vento, relógio **Cartier Santos** (feito para Santos Dumont em 1904) com a hora real, contadores de tambor (voo, tempo, melhor voo), corrediças de gás/canard/compensador/roda/corpo, lâmpadas (motor, ajudantes, estol, no ar) e plaqueta de avisos; ponteiros com inércia e tremor do motor
44. Animações: hélice, canard, ailerons, volante, alavanca, rodas, amortecedores, Santos Dumont inclinando o corpo, ajudantes e mecânico
45. Poeira das rodas e do sopro da hélice, fumaça do escape, sombra
46. **Desafios históricos**: Taça Archdeacon (25 m), 23/10 (60 m), Aeroclube (100 m), 12/11 (220 m) — medido da decolagem ao toque, como faziam os comissários
47. Vento de oeste com rajadas e perfil logarítmico junto ao chão; ar padrão (densidade cai com a altitude)

## 6. Modelo de voo (FM14)

- **Corpo rígido de 6 graus de liberdade**, integrado a 300 Hz (Euler
  semi-implícito); massa 300 kg; inércias 1300 (arfagem), 1900 (guinada) e
  750 kg·m² (rolagem); momento angular da hélice incluído (giroscópio).
- **28 superfícies**: 12 painéis de asa (3 células × 2 planos × 2 lados, com
  diedro), 8 paredes verticais, 4 faces do canard (giram com a cardã), 2
  ailerons e 2 superfícies da fuselagem. Cada uma calcula o ângulo de ataque
  com a velocidade local (incluindo a rotação do avião), CL linear até o
  estol e curva de placa plana depois (vale para qualquer ângulo, até de
  costas). Asas: dCL/dα = 3,9/rad, α₀ = −5° (5% de curvatura), CLmáx 1,22.
- **Arrasto de forma** ≈ 3,2 m² de placa plana (montantes, arames, piloto,
  motor, trem), distribuído nos lugares certos; **efeito solo** reduz o
  arrasto induzido e aumenta a sustentação perto do chão.
- **Antoinette**: torque máx. ~255 N·m (50 cv a ~1500 rpm), inércia do
  conjunto, marcha lenta e "morte" do motor abaixo de 140 rpm; a **hélice**
  usa CT e CP em função de J = V/(nD) — tração estática ~960 N, ~700 N a 40 km/h.
- **Contato com o chão**: molas-amortecedores nas rodas (com resistência ao
  rolamento na grama e atrito lateral), na vara de proa e nas varas das asas;
  pontos "duros" (pontas das asas, hélice, canard, cesto, fuselagem) detectam
  batidas e arrasto.

### Validação (testes automáticos no Chrome headless)

| Grandeza | Simulador | Referência |
|---|---|---|
| Atitude parado | 4,4° de nariz alto, sobre rodas + vara | fotos de 1906 |
| Corrida de decolagem (sem vento) | ~36 m, ~9 s, decola a **37 km/h** | 220 m / 21,5 s = 37 km/h (12/11) |
| Velocidade de trim (alavanca neutra) | 41 km/h (11,5 m/s) | 9–12 m/s (Bitencourt et al.) |
| Velocidade máxima nivelada | **46–47 km/h** | ~40 km/h (Wikipedia); 11–14 m/s (CFD) |
| Estol do canard | ~35 km/h | — |
| Razão de subida (gás todo) | ~0,6–0,9 m/s | subiu a ~6 m em 12/11 |
| Planeio (motor cortado) | ~2,3 m/s de descida, L/D ≈ 4,6 | — |
| Margem estática | ~5% da corda (quase neutro) | "marginalmente estável" (Greco & Catalano) |
| Guinada | instável (Cnβ < 0) — deriva e exige volante | Cnβ = −0,12/rad (Greco & Catalano) |
| Amortecimento em arfagem | ~6200 N·m·s/rad | Cmq = −5,4 (idem) |
| Salto roteirizado (6 s de motor + planeio) | "Voo de 92 m em 9,6 s" | 60 m em ~7 s (23/10) |

## 7. Fontes

- P. C. Greco Jr. & F. M. Catalano, *Analysis of Geometric and Flying
  Characteristics of Santos-Dumont's 14-Bis*, ENCIT 2006 (CIT06-0601), e
  *Historical Review and Analysis of Santos Dumont's 14-Bis*, CEAS 2007 —
  geometria, CG, derivadas de estabilidade.
- L. O. Bitencourt, R. M. de Freitas, G. Pogorzelski & J. L. F. Azevedo,
  *CFD-Based Analysis of the 14-Bis Aircraft Aerodynamics and Stability*,
  ENCIT 2006 (CIT06-0249) — áreas, velocidades de voo, potência.
- [Santos-Dumont 14-bis — Wikipedia (EN)](https://en.wikipedia.org/wiki/Santos-Dumont_14-bis)
- [14-bis — Wikipédia (PT)](https://pt.wikipedia.org/wiki/14-bis)
- [14-bis — Britannica](https://www.britannica.com/topic/Santos-Dumont-No-14-bis)
- [14-bis — MUSAL (Museu Aeroespacial da FAB)](https://www2.fab.mil.br/musal/index.php/aeronaves-em-exposicao?catid=55&id=142&view=article)
- [Museu Virtual Santos Dumont — 14 bis](http://www.museuvirtualsantosdumont.com.br/14-bis.html)
- [This Day in Aviation — Nº 14 bis](https://www.thisdayinaviation.com/tag/n-14-bis/)
- [Relato de Santos Dumont sobre o 14-bis — Gazeta do Povo](https://www.gazetadopovo.com.br/ideias/relato-santos-dumont-criacao-14-bis/)
- [DUMONT'S 14-BIS — ABCM/ENCIT 2006 (PDF)](https://www.abcm.org.br/anais/encit/2006/arquivos/Juntos/16.pdf)
- [Historical Review and Analysis of Santos Dumont's 14-Bis — CEAS 2007 (PDF)](https://www.fzt.haw-hamburg.de/pers/Scholz/ewade/2007/CEAS2007/papers2007/ceas-2007-065.pdf)
- Fotografias de 1906 (Collection Jules Beau / BnF; Museu Casa Natal de Santos
  Dumont) e o modelo em escala do Museu do Ar, via Wikimedia Commons — usadas
  só como referência visual, não incluídas no repositório.

# 14-bis — "Oiseau de Proie" — Documentação para o Simulador

Dossiê técnico para a réplica voável do 14-bis no mundo 3D da Encantada.
Cada peça é numerada para conferência durante a construção.

> **STATUS: CONSTRUÍDO ✅** — v1 voável integrada ao `index.html` (seção
> `14-BIS`). As peças [1]–[47] estão marcadas por número nos comentários do
> código. Tecla `8` teleporta ao Campo de Bagatelle; `E` junto ao cesto embarca.

## 1. Ficha histórica

- **Nome**: Santos-Dumont Nº 14-bis, apelidado *Oiseau de Proie* ("Ave de Rapina").
  O nome vem de ter sido testado pendurado sob o dirigível Nº 14.
- **Primeiro voo público da história em aparelho mais-pesado-que-o-ar (Europa)**:
  **23/10/1906**, Campo de Bagatelle, Paris — decolou por meios próprios após
  ~100 m de corrida, voou **~60 m a ~3 m de altura** a ~30-37 km/h e ganhou a
  **Taça Archdeacon** (primeiro voo de 25 m).
- **12/11/1906**: voo recorde de **220 m em 21,5 s** (~37 km/h), conquistando o
  prêmio do Aeroclube da França (primeiro voo de 100 m) — com os ailerons
  octogonais recém-instalados.
- Diferente do Flyer dos Wright (catapulta/trilho), o 14-bis decolou **por
  meios próprios, com rodas**, diante de testemunhas oficiais — por isso o
  Brasil o celebra como o primeiro avião.

## 2. Como ele voa — o "ganso de pescoço esticado"

O 14-bis é um **canard**: voa "de costas" em relação aos aviões modernos.

- A **cauda fica na FRENTE**: uma pequena célula-caixa (tipo pipa Hargrave) na
  ponta de uma longa treliça que aponta pra frente — o *pescoço do ganso*.
  Essa célula é o **profundor E leme** ao mesmo tempo: montada numa **junta
  cardã**, gira pra cima/baixo (arfagem) e pros lados (guinada).
- As **asas ficam ATRÁS**: biplano em células Hargrave com **diedro acentuado
  (~10°)** — as pontas sobem em "V", dando estabilidade lateral.
- A **hélice fica atrás de tudo** (configuração *pusher*): empurra em vez de
  puxar.
- O piloto vai **EM PÉ num cesto de vime de balão**, na frente do motor,
  olhando o pescoção à sua frente.
- Para **subir**: o canard inclina o bordo de ataque para CIMA (o contrário
  do profundor de cauda moderno).

## 3. Controles reais (1906)

| Comando | O que faz |
|---|---|
| **Volante (mão esquerda)** | gira a célula dianteira pros lados → **guinada** |
| **Alavanca (mão direita)** | inclina a célula dianteira → **arfagem** (sobe/desce o nariz) + acelerador |
| **Arnês no corpo (nov/1906)** | colete costurado ao paletó ligado por cabos aos **ailerons octogonais**: o piloto **inclina o corpo** para o lado e o avião **rola** — precursor dos sistemas modernos! |

## 4. Ficha técnica

| Item | Valor |
|---|---|
| Envergadura | 12,0 m (asas em células Hargrave) |
| Comprimento | 10,0 m |
| Altura | ~3,4-4,8 m (cesto abaixo, célula acima) |
| Área alar | ~50-52 m² |
| Peso | ~160 kg (vazio) / ~300 kg com piloto e combustível |
| Motor | Antoinette 8V (V8) — 24 cv no início, **50 cv** nos voos históricos |
| Hélice | bipá, **propulsora (pusher)**, atrás das asas |
| Estrutura | bambu-da-índia e pinho, juntas de alumínio, arames de aço |
| Revestimento | **seda japonesa** |
| Trem de pouso | 2 rodas raiadas (tipo bicicleta) sob as asas + patim sob a proa |
| Velocidade | ~30-40 km/h |

## 5. LISTA NUMERADA DE PEÇAS (conferência da construção)

### A. Fuselagem e estrutura
1. Longarina-treliça central (seção triangular, bambu/pinho, ~10 m) — o "pescoço"
2. Nós/junções da treliça (amarrações e ferragens)
3. Estais de arame de aço da fuselagem

### B. Célula dianteira (canard — a "cabeça do ganso")
4. Caixa Hargrave dianteira: 2 superfícies horizontais + laterais verticais
5. Junta cardã (pivô universal) na ponta da longarina
6. Cabos de comando do canard até o posto do piloto
7. Molduras de bambu da célula

### C. Asas principais (células Hargrave traseiras)
8. Plano superior — envergadura 12 m, com **diedro ~10°**
9. Plano inferior — idem
10. Fechamentos verticais das baias externas (paredes das células)
11. Montantes interplanos de bambu (struts)
12. Estais/tirantes de arame entre os planos
13. Revestimento de seda japonesa (cor creme/âmbar translúcida)
14. **Ailerons octogonais** nas baias externas (novidade de nov/1906)
15. Articulações + cabos dos ailerons até o arnês do piloto

### D. Motopropulsor
16. Motor **Antoinette 8V** (bloco em V, 2 bancadas de 4 cilindros) atrás do cesto
17. **Hélice bipá pusher** na traseira
18. Cubo/eixo da hélice no virabrequim
19. Radiador e tubulação de refrigeração
20. Tanque de combustível
21. Escapamentos curtos
22. Bancada/suporte do motor na treliça

### E. Posto de pilotagem
23. **Cesto de vime** (de balão) — piloto EM PÉ
24. **Volante** à esquerda (leme/célula lateral)
25. **Alavanca** à direita (profundor + acelerador)
26. **Arnês/colete** ligado aos ailerons (rolagem por inclinação do corpo!)
27. Polias e roldanas dos cabos

### F. Trem de pouso
28. 2 rodas raiadas tipo bicicleta sob as asas
29. Garfos das rodas
30. Patim (skid) sob a proa

### G. Física do simulador
31. Sustentação (asas + canard) com estol simples
32. Empuxo da hélice (50 cv, aceleração gradual)
33. Arrasto aerodinâmico + efeito solo
34. **Arfagem via canard** (lógica invertida da convencional!)
35. Guinada via célula dianteira
36. **Rolagem via inclinação do corpo** (ailerons octogonais)
37. Corrida de decolagem com rodas (decola a ~30-40 km/h)
38. Pouso, quique e colisão com terreno/obstáculos

### H. Interação e jogo
39. 14-bis estacionado no gramado plano (nosso "Campo de Bagatelle")
40. Tecla **E** para embarcar/desembarcar do cesto
41. Teclas: W/S acelerador · setas ou mouse arfagem/guinada · A/D corpo (rolagem)
42. Câmeras: 1ª pessoa no cesto + 3ª pessoa (V)
43. HUD de época: velocidade, altura, distância do voo atual
44. Animações: hélice girando, canard/ailerons defletindo, rodas rolando,
    avatar do SD em pé no cesto inclinando o corpo
45. Sombra do avião + poeira na corrida de decolagem
46. **Desafios históricos**: Taça Archdeacon (voe 25 m+) e Prêmio do Aeroclube
    (voe 100 m+) com medalha na tela — recriar 23/10 (60 m) e 12/11 (220 m)
47. Vento/balanço leve para dar vida ao voo

## 6. Fontes

- [Santos-Dumont 14-bis — Wikipedia (EN)](https://en.wikipedia.org/wiki/Santos-Dumont_14-bis)
- [14-bis — Wikipédia (PT)](https://pt.m.wikipedia.org/wiki/14-bis)
- [14-bis — Britannica](https://www.britannica.com/topic/Santos-Dumont-No-14-bis)
- [14-bis — MUSAL (Museu Aeroespacial da FAB)](https://www2.fab.mil.br/musal/index.php/aeronaves-em-exposicao?catid=55&id=142&view=article)
- [Museu Virtual Santos Dumont — 14 bis](http://www.museuvirtualsantosdumont.com.br/14-bis.html)
- [This Day in Aviation — Nº 14 bis](https://www.thisdayinaviation.com/tag/n-14-bis/)
- [Relato de Santos Dumont sobre o 14-bis — Gazeta do Povo](https://www.gazetadopovo.com.br/ideias/relato-santos-dumont-criacao-14-bis/)
- [DUMONT'S 14-BIS — análise de engenharia (ABCM/ENCIT 2006, PDF)](https://www.abcm.org.br/anais/encit/2006/arquivos/Juntos/16.pdf)
- [Aircraft Investigation — Santos Dumont 14-bis](https://aircraftinvestigation.info/airplanes/Santos_Dumont_14-bis.html)

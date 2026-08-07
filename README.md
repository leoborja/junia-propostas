# Gerador de Propostas — Junia Vaz Arquitetura

Ferramenta web para montar propostas de arquitetura, design de interiores e
administração de obra, prontas para exportar em PDF.

**No ar:** https://leoborja.github.io/junia-propostas/

## Como usar

1. Preencha cliente, imóvel, tipo de trabalho e porte.
2. Marque os ambientes e os entregáveis.
3. Escolha a foto da capa e os projetos do portfólio.
4. Escolha como calcular o valor: fechado, por ambiente ou por m².
5. Defina a condição de pagamento.
6. **Exportar PDF** — imprime as páginas.

Os dados ficam salvos no navegador (localStorage). Fechar e reabrir mantém a
última proposta. "Nova proposta" limpa tudo.

## A proposta gerada

Seis ou sete páginas em **16:9** (338 × 190 mm), o mesmo formato do material
original. A sétima ("O seu projeto") só aparece se o briefing for preenchido.

1. **Capa** — tipo de trabalho, cliente em caligráfico, foto
2. **O seu projeto** — o que ela entendeu da conversa, nas palavras dela
3. **Etapas** — as 3 fases com ilustração, prazo por porte
4. **Escopo** — programa de ambientes e entregáveis
5. **Investimento** — valor, condições e imagem
6. **Projetos realizados** — portfólio, até 6 imagens
7. **Minha História** — bio e retrato

**A ordem tem motivo.** Abre pelo cliente, não pela arquiteta: quem lê quer saber
se você entendeu o problema *dele*; o currículo convence depois. O escopo fica
colado no preço, porque introdução + preço somam ~67% do tempo de leitura. E o
portfólio vem **depois** do preço, como justificativa, não como vitrine.

## Identidade visual

Tudo extraído do `.pptx` original dela, não inventado:

| | |
|---|---|
| Fundo | `#F3F3F3` |
| Faixas taupe | `#D9CCBF` |
| Bronze (única cor de texto que não é preto) | `#7D6039` |
| Texto | `#0E0E0E` |
| Fonte | **Poppins** (a real dela, 310 usos no pptx) |
| Caligráfica | **Parisienne** (substitui a Brittany, que é comercial) |

Os contrastes foram todos medidos: mínimo 3:1 para texto grande e 4,5:1 para
texto normal. **O original dela não passava** — títulos a 1,33:1 e script branco
sobre taupe a 1,57:1, que somem no celular e na impressão.

### Escala tipográfica — 6 tamanhos, não 25

Havia 25 tamanhos diferentes misturando `pt` e `px`: deriva, não escala — e
misturar unidades inconsiste a exportação do PDF. Hoje são **6 tokens para o
documento** (`--t-xs` 8pt … `--t-2xl` 44pt, sempre em pt) e **3 para a interface**
(`--i-*`, sempre em px).

**Precisando de um tamanho novo, reveja a escala — não acrescente valor solto.**

O corpo está em **11pt**, não 10: 58% das propostas são abertas no celular, e num
slide 16:9 a escala é `390/960 = 0,41` — 9pt vira ~4pt na tela.

### Cor: um bronze só

Eram quatro quase idênticos (`#A88C68`, `#9C8055`, `#7D6039`, `#8F7449`) e três
reprovavam em contraste sobre o osso — `#A88C68` dava 2,86, que reprova até em
texto grande. Sobrou `#7D6039` (5,25). **`--taupe` e `--faixa` são fundo, nunca
cor de texto.** Bronze sobre taupe reprova abaixo de 18pt — é a estética "dourado
sobre bege" que faz proposta parecer template comprado.

## Armadilhas que custaram tempo

**Faltava `<!DOCTYPE html>`.** O arquivo nasceu no formato de artifact, que proíbe
doctype. Sem ele o navegador entra em *quirks mode*, onde **tabelas não herdam a
cor do pai** — a tabela de investimento pegava a cor da interface e ficava
**invisível no tema escuro**. Se editar, não remova o doctype.

**Mudar um valor padrão exige subir a versão do localStorage.** O estado salvo
sobrescreve o novo padrão e o usuário continua vendo o antigo. A chave está em
`CHAVE` no script — hoje `propostas-junia-v2`.

**`index.html` é cópia de `gerador.html`.** Editar o gerador e copiar:
`cp gerador.html index.html`.

**Nome de classe do app não pode colidir com o do documento.** `.painel` era ao
mesmo tempo o painel de controle e as caixas das etapas — e a regra
`@media print{.painel{display:none}}` **apagaria as etapas e a bio do PDF
exportado**, sem quebrar nada na tela. Hoje o app usa `#painel` (id).

**Espaço em branco vem de `flex:1` + `margin-top:auto`.** Esse par gruda um
elemento no topo e outro no rodapé e joga o sobrante para o meio. Com conteúdo
curto vira buraco — chegou a 22,7% da altura na página de investimento.

## Imagens

`img/` — renders extraídos dos PDFs e do pptx dela, mais o retrato.

As três ilustrações das etapas (`etapa-planta`, `etapa-moodboard`,
`etapa-executivo`) são **geradas por IA** (`gerar_ilustracoes.py`, Gemini
`gemini-3-pro-image`). Substituíram imagens de terceiros que estavam no material
original — um print do site trichada.com com a barra do navegador aparecendo, um
desenho isométrico com legendas em russo e um moodboard coletado.

**Ressalva:** continuam sendo ilustração genérica, não projeto dela. O ideal é
material real da Júnia. E a planta gerada tem imprecisões que aparecem se der
zoom (sala sem circulação definida, portas de banheiro que se atrapalham) — no
tamanho do slide, 66 mm de altura, não se percebe.

Backups: `img/originais-terceiros/` e `out/` — ambos fora do repo.

## Privacidade

**GitHub Pages é sempre público**, mesmo em repositório privado. Então:

- nada de nome de cliente ou valor real dentro do arquivo;
- `.gitignore` bloqueia `*.pdf`, `exemplos/`, `out/` e as pastas de backup;
- as propostas reais dos clientes **nunca** entram aqui.

## O que falta decidir com a Júnia

1. **Régua de preço** — os padrões de hoje (R$ 900/ambiente, R$ 75/m², R$ 5.400
   fechado) foram inferidos das 6 propostas antigas. **O de m² está abaixo do piso
   de mercado**: fontes de 2026 apontam R$ 80–180/m² para interiores. Padrão baixo
   numa ferramenta vira âncora e institucionaliza o subpreço — é o item mais
   urgente. O CAU tem calculadora gratuita: `honorario.caubr.gov.br` (CUB-MG).
2. **Taxa de administração de obra** — está em 15%, mas a recomendação para
   escritório pequeno é **valor fixo mensal** (R$ 1.500–4.000) com número de
   visitas e prazo definidos. Percentual cria incentivo perverso e expõe a atraso:
   a obra estoura seis meses e ela trabalha de graça.
3. **Condição de pagamento padrão** — 30/40/30 é o que ela pratica?
4. **3 arquivos dela** para substituir as ilustrações genéricas das etapas.

## Proteções jurídicas que faltam

- **RRT** — obrigação intransferível do arquiteto (Lei 12.378/2010). A proposta
  precisa declarar que será emitido e se o custo (R$ 150–350) está incluso.
- **Direito autoral** — projeto é obra protegida (Lei 9.610/98, art. 7º, X). Sem
  cláusula, o cliente pode reusar o projeto em outro terreno. Precisa de
  titularidade, licença restrita àquele imóvel e autorização de publicar no portfólio.
- **Preço em reais da revisão extra.** Hoje diz "2 rodadas" sem dizer quanto custa
  a terceira. Contra pessoa física vale o CDC: ambiguidade é lida contra quem redigiu.
- **Travamento de etapa** — aprovação assinada de cada fase; mudança depois disso é
  serviço novo. Sem isso o cliente muda a planta no executivo e ela refaz de graça.

## Arquivos

```
gerador.html            fonte — editar aqui
index.html              cópia servida pelo GitHub Pages
gerar_ilustracoes.py    gera as ilustrações das etapas (Gemini)
img/                    imagens publicadas
out/                    gerações e backups (fora do repo)
```

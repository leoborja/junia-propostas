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
6. **Exportar PDF** — imprime as 6 páginas.

Os dados ficam salvos no navegador (localStorage). Fechar e reabrir mantém a
última proposta. "Nova proposta" limpa tudo.

## A proposta gerada

Seis páginas em **16:9** (338 × 190 mm), o mesmo formato do material original:

1. **Capa** — tipo de trabalho, cliente em caligráfico, foto
2. **Minha História** — bio e retrato
3. **Projetos realizados** — portfólio, até 6 imagens
4. **Etapas** — as 3 fases com ilustração, prazo por porte
5. **Escopo** — programa de ambientes e entregáveis
6. **Investimento** — tabela, condições e imagem

## Identidade visual

Tudo extraído do `.pptx` original dela, não inventado:

| | |
|---|---|
| Fundo | `#F3F3F3` |
| Faixas taupe | `#D9CCBF` |
| Títulos display | `#9C8055` |
| Bronze | `#7D6039` |
| Texto | `#0E0E0E` |
| Fonte | **Poppins** (a real dela, 310 usos no pptx) |
| Caligráfica | **Parisienne** (substitui a Brittany, que é comercial) |

Os contrastes foram todos medidos: mínimo 3:1 para texto grande e 4,5:1 para
texto normal. **O original dela não passava** — títulos a 1,33:1 e script branco
sobre taupe a 1,57:1, que somem no celular e na impressão.

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
tamanho do slide, 48 mm, não se percebe.

Backups: `img/originais-terceiros/` e `out/` — ambos fora do repo.

## Privacidade

**GitHub Pages é sempre público**, mesmo em repositório privado. Então:

- nada de nome de cliente ou valor real dentro do arquivo;
- `.gitignore` bloqueia `*.pdf`, `exemplos/`, `out/` e as pastas de backup;
- as propostas reais dos clientes **nunca** entram aqui.

## O que falta decidir com a Júnia

1. **Régua de preço** — por ambiente, por m² ou por porte? Os padrões de hoje
   (R$ 900/ambiente, R$ 75/m², R$ 5.400 fechado) foram inferidos das 6 propostas
   antigas e precisam de validação.
2. **Taxa de administração de obra** — 15% é o número certo?
3. **Condição de pagamento padrão** — 30/40/30 é o que ela pratica?
4. **3 arquivos dela** para substituir as ilustrações genéricas das etapas.

## Arquivos

```
gerador.html            fonte — editar aqui
index.html              cópia servida pelo GitHub Pages
gerar_ilustracoes.py    gera as ilustrações das etapas (Gemini)
img/                    imagens publicadas
out/                    gerações e backups (fora do repo)
```

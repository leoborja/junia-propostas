# Gerador de Propostas — Junia Vaz Arquitetura

Ferramenta web para montar propostas comerciais de arquitetura, design de
interiores e administração de obra, prontas para exportar em PDF.

**No ar:** https://leoborja.github.io/junia-propostas/

## Como usar

1. Preencha cliente, imóvel, tipo de trabalho e porte.
2. Marque os ambientes e os entregáveis.
3. Escolha como calcular o valor (fechado, por ambiente ou por m²).
4. Defina a condição de pagamento.
5. **Exportar PDF** — imprime as 4 páginas em A4 paisagem.

Os dados ficam salvos no navegador (localStorage). Fechar e reabrir mantém
a última proposta.

## Estrutura

Arquivo único, sem dependências externas. `index.html` é cópia de
`gerador.html` — editar o `gerador.html` e copiar.

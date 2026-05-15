# Wurm Market Observatory — Identity Manifesto & Development Guardrails

Este documento define a identidade filosófica e visual do projeto.
Qualquer decisão de desenvolvimento deve ser filtrada por ele.
Ele tem precedência sobre preferências estéticas genéricas, tendências de design,
e qualquer sugestão que não tenha sido validada contra estes princípios.

---

## O que este projeto É

Um **observatório arqueológico de dados econômicos** do jogo Wurm Online.

Mais especificamente:
- Uma publicação de pesquisa histórica informal
- Um atlas de dados parciais
- Um arquivo de arqueologia computacional
- Um laboratório vivo de interpretação

A metáfora central é **o atlas antigo**: mapas que mostram território conhecido,
território parcialmente explorado, e território desconhecido — sem fingir
que as lacunas não existem.

---

## O que este projeto NÃO É

- ❌ Dashboard corporativo
- ❌ Plataforma de market surveillance
- ❌ Ferramenta de trading em tempo real
- ❌ SaaS / fintech / admin panel
- ❌ Aplicativo de analytics genérico
- ❌ Qualquer coisa que pareça uma startup de 2023

Se uma decisão de design fizer o projeto parecer qualquer uma dessas coisas,
a decisão está errada.

---

## A regra de ouro epistemológica

> **Tudo neste site comunica parcialidade, interpretação e incerteza.**

Nunca:
- Apresentar dados como completos quando são parciais
- Interpolar períodos sem dados
- Usar linguagem de certeza ("os dados mostram que X")
- Esconder lacunas ou suavizá-las visualmente

Sempre:
- Mostrar cobertura junto a qualquer número
- Marcar gaps visualmente de forma honesta
- Usar linguagem de observação ("observado em", "identificado em corpus parcial")
- Deixar claro que este site é derivado do Historical Archive, não canônico

A frase **"observed mentions, not confirmed transactions"** deve permanecer
sempre visível ou acessível. É a âncora epistemológica do projeto.

---

## Arquitetura dos dados — nunca violar

```
Historical Archive (Projeto 1 — separado)
↓
corpus restaurado baixado (.txt)
↓
pipeline Python local
↓
JSON/Parquet estáticos em src/data/
↓
Observable Framework renderiza
↓
site estático no Cloudflare Pages
```

**Nunca:**
- Consultar o banco do Historical Archive diretamente
- Adicionar backend, API, ou banco de dados ao vivo
- Fazer queries pesadas em runtime
- Criar dependência do Supabase do archive

Todo processamento acontece **antes** do build. O site serve resultados,
não computa ao vivo.

---

## Stack — manter coerente

| Camada | Tecnologia | Nunca substituir por |
|---|---|---|
| Site | Observable Framework | Next.js, React SPA, Vite standalone |
| Gráficos | Observable Plot | Chart.js pesado, D3 raw sem necessidade |
| Queries interativas | DuckDB-WASM | Backend SQL, Supabase, Firebase |
| Hosting | Cloudflare Pages | Vercel pago, AWS, servidores próprios |
| Dados | JSON + Parquet estáticos | Banco ao vivo, REST API própria |

---

## Identidade visual — princípios inegociáveis

### Tom
Editorial histórico. Publicação científica informal. Caderno de campo.
**Não:** produto digital, dashboard, app.

### Tipografia
- Títulos e texto editorial: **Playfair Display** (serifada)
- Notas de campo, observações, anotações: **IM Fell English** (serifada itálica)
- Dados, labels, código, metadados: **JetBrains Mono** (monoespaçada)

Nunca usar sans-serif moderna como fonte principal de display.
Nunca usar Inter, Geist, ou similares como fonte de título.

### Paleta — tema claro (padrão)
- Fundo: pergaminho envelhecido (`#f4efe4`) — não branco puro
- Texto: quase-preto (`#1a1814`) — não preto absoluto
- Accent: âmbar/ocre (`#a87228` a `#b07d2a`)
- Gaps/lacunas: cinza médio com hachura diagonal — nunca vermelho

### Paleta — tema escuro
- Fundo: não preto absoluto — escuro envelhecido (ex: `#1a1814` ou `#1e1c17`)
- Accent: âmbar mais claro para contraste
- Mesma hierarquia tipográfica
- Gaps continuam hachura diagonal, agora em cinza escuro

### Gaps e lacunas
**Hachura diagonal 135° sempre.** Nunca:
- Deixar vazio/branco
- Interpolar com linha tracejada
- Usar vermelho ou cor de "erro"
- Suavizar como se o dado existisse

O gap é **território desconhecido**, não erro de sistema.

### Saturação por cobertura
Cobertura baixa → mais dessaturado/desbotado
Cobertura alta → mais saturado/sólido
Isso se aplica à timeline, aos gráficos, e aos lens cards.
**Radicalizar isso, não suavizar.**

### O que nunca adicionar
- Gradientes decorativos
- Sombras desnecessárias (box-shadow decorativo)
- Animações chamativas
- Ícones coloridos além do âmbar
- Cards com bordas arredondadas grandes (>8px)
- Qualquer elemento que pareça Material Design ou Tailwind UI padrão

---

## Conceito de Lenses — nunca violar

Cada análise é uma **lente interpretativa**, não uma verdade.

Cada lens deve ter:
- Nota metodológica honesta e visível (o que ela faz e o que ela NÃO pode afirmar)
- Metadados de cobertura sempre visíveis
- Field annotations: pequenas notas editoriais em itálico sobre padrões e lacunas
- Versão própria (v0.1, v0.2...)
- Dataset próprio em src/data/

Lenses não se acoplam entre si.
Uma lens nova não deve exigir modificar lenses existentes.

**Status de lens:**
- `active` — dados disponíveis, cobertura razoável
- `partial` — dados disponíveis, cobertura baixa
- `uncharted` — território não restaurado ainda (nunca "unavailable" ou "error")

---

## Field Annotations — preservar sempre

As field annotations são notas editoriais em itálico abaixo dos gráficos.
Formato: timestamp/período + observação em IM Fell itálico.

Exemplo:
```
Nov 6–8    Trade visibility drops sharply. Archival absence or genuine
           market lull — indeterminate from corpus alone.
```

Elas transformam gráficos em leitura histórica.
**Nunca remover. Nunca transformar em tooltip genérico.**

---

## Recent Observations — preservar

Seção na home com mini insights em IM Fell itálico.
Cada item tem metadado de origem (lens · período · cobertura).

Tom: laboratório vivo, não feed de notícias.
**Nunca transformar em cards coloridos, badges, ou alerts.**

---

## "Derived — not canonical"

Esta frase (ou equivalente) deve aparecer em toda página.
O link para o Historical Archive deve estar sempre no footer ou nav.

O site **nunca** deve parecer ser a fonte primária dos dados.
Ele é sempre derivado.

---

## Checklist para qualquer nova feature

Antes de implementar qualquer coisa, responder:

1. **Isso comunica parcialidade e incerteza, ou sugere certeza?**
   Se sugere certeza → revisar ou rejeitar.

2. **Isso parece publicação histórica ou parece SaaS/dashboard?**
   Se parece SaaS → revisar ou rejeitar.

3. **Isso adiciona backend, API, ou banco ao vivo?**
   Se sim → rejeitar. Tudo é estático e pré-computado.

4. **Isso esconde ou suaviza uma lacuna de dados?**
   Se sim → rejeitar. Gaps são visíveis e honestos.

5. **Isso quebra a separação entre o Archive (Projeto 1) e o Observatory (Projeto 2)?**
   Se sim → rejeitar.

6. **Isso quebra a identidade visual (tipografia, cores, componentes)?**
   Se sim → revisar contra a identidade visual.

---

## O que o GPT-4 disse sobre o protótipo (guardar como referência)

> "Você criou uma estética epistemológica. Tudo comunica parcialidade,
> interpretação, preservação, reconstrução, observação indireta.
> Isso é muito raro em projetos de dados."

Esta frase é o norte. Qualquer decisão que enfraqueça essa característica
está indo na direção errada.

---

## Versioning deste documento

`IDENTITY.md` v1.0 — gerado durante desenvolvimento inicial com Claude Sonnet 3.5
Atualizado em 2026-05-15 para refletir a maturidade do projeto.

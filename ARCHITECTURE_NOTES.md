# Wurm Market Observatory — Architectural & Stability Notes

Este documento registra as soluções técnicas e "lições aprendidas" durante o desenvolvimento do Observatório para garantir a estabilidade a longo prazo.

## 1. Estabilidade do Frontend (Zero-Indent Rule)
**Problema**: O parser de Markdown do Observable Framework interpreta qualquer bloco de HTML com 4+ espaços de indentação como um `Indented Code Block` (CommonMark). Isso quebrava a renderização dos componentes Plot e gerava erros de `RuntimeError: d is not defined`.
**Solução**: Todos os blocos HTML/Markdown nos arquivos `.md` devem ter **zero indentação à esquerda**. 
- **Errado**:
    <div>
        ${Plot.plot(...)}
    </div>
- **Correto**:
<div>
${Plot.plot(...)}
</div>

## 2. Carregamento de Dados Multi-Servidor (NFI/SFI)
**Problema**: O framework exige que `FileAttachment` use caminhos estáticos (string literals) para rastreamento de dependências.
**Solução**: Carregamos ambos os servidores explicitamente e alternamos via lógica JS reativa:
```javascript
const nfi_data = await FileAttachment("data/nfi-activity.json").json();
const sfi_data = await FileAttachment("data/sfi-activity.json").json();
const data = server.value === "NFI" ? nfi_data : sfi_data;
```

## 3. Saneamento Semântico (Item Identity)
**Problema**: Palavras como "Toolbelt" disparavam falsos positivos para o termo "lb". Prefixos como "Wtb" eram incluídos nos nomes dos itens.
**Solução**:
- **Word Boundaries**: Usamos regex `\b` para garantir que palavras curtas não sejam encontradas dentro de outras maiores.
- **Explicit Stripping**: O `parser_utils.py` possui uma lista de `wts_keywords` e `wtb_keywords` que são removidos do início das strings antes da identificação do item.

## 4. Internacionalização (i18n)
O sistema usa um motor reativo baseado em `Mutable` no arquivo `src/components/i18n.js`.
- **Dicionário**: Centralizado em `translations`.
- **Uso**: As páginas Markdown usam `${t("chave")}` ou condicionais `${lang.value === "pt" ? "..." : "..."}` para blocos de texto longos.

## 5. Estrutura do Pipeline
- `pipeline/core.py`: Orquestração.
- `pipeline/lenses.py`: Lógica de extração por "lente" (Vendedor/Comprador).
- `pipeline/parser_utils.py`: Limpeza e identificação semântica.
- `scratch/run_pipeline_headless.py`: Script de execução rápida para gerar os JSONs prefixados.

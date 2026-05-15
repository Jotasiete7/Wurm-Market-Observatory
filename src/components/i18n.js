import { Mutable } from "npm:@observablehq/stdlib";

// Estado global do idioma (padrão Português como solicitado)
export const lang = Mutable("pt");

// Estado global do servidor (NFI por padrão)
export const server = Mutable("NFI");

const translations = {
  pt: {
    back: "← Observatório",
    lens_v: "Lens · v0.1",
    seller_title: "Atividade de Vendedores",
    buyer_title: "Atividade de Compradores",
    description: "Quem vende, o que vendem e quando aparecem no corpus do canal de trade.",
    methodology_note: "Nota Metodológica — Esta lente conta menções no canal de trade, não transações confirmadas.",
    coverage: "Cobertura do Corpus",
    unique_sellers: "Vendedores únicos",
    unique_buyers: "Compradores únicos",
    total_listings: "Total de listagens",
    top_category: "Categoria principal",
    peak_day: "Dia de pico",
    daily_activity: "Atividade diária",
    observed: "atividade observada",
    no_data: "sem dados (gap)",
    rank: "Ranking",
    mentions: "Menções",
    items_title: "Itens Extraídos (Motor Semântico)",
    item_name: "Item (Nome Canônico)",
    total_qty: "Qtd Total",
    avg_price: "Preço Médio (C)",
    source_corpus: "Corpus de origem",
    known_gaps: "Gaps conhecidos:",
    no_interpolation: "período de lacuna (não interpolado)",
    server: "Servidor",
    log_lines: "Linhas de Log",
    generated: "gerado em",
    confidence: "Confiança",
    signals: "Sinais de Demanda",
    explorer_title: "Explorador de Corpus",
    methodology_title: "Metodologia Arqueológica"
  },
  en: {
    back: "← Observatory",
    lens_v: "Lens · v0.1",
    seller_title: "Seller Activity",
    buyer_title: "Buyer Activity",
    description: "Who sells, what they sell, and when they appear in the trade channel corpus.",
    methodology_note: "Methodological Note — This lens counts trade channel mentions, not confirmed transactions.",
    coverage: "Corpus Coverage",
    unique_sellers: "Unique Sellers",
    unique_buyers: "Unique Buyers",
    total_listings: "Total Listings",
    top_category: "Top Category",
    peak_day: "Peak Day",
    daily_activity: "Daily Activity",
    observed: "observed activity",
    no_data: "no data (gap)",
    rank: "Rank",
    mentions: "Mentions",
    items_title: "Extracted Items (Semantic Engine)",
    item_name: "Item (Canonical Name)",
    total_qty: "Total Qty",
    avg_price: "Avg Price (C)",
    source_corpus: "Source Corpus",
    known_gaps: "Known gaps:",
    no_interpolation: "gap period (not interpolated)",
    server: "Server",
    log_lines: "Log Lines",
    generated: "generated on",
    confidence: "Confidence",
    signals: "Demand Signals",
    explorer_title: "Corpus Explorer",
    methodology_title: "Archaeological Methodology"
  }
};

export function t(key) {
  return translations[lang.value][key] || key;
}

export function LanguageSelector() {
  const select = document.createElement("select");
  select.style.cssText = "background:transparent;border:1px solid var(--border);color:var(--amber);font-size:0.7rem;padding:2px 4px;border-radius:4px;cursor:pointer;font-family:var(--font-mono);margin-left:8px;";
  
  const optPt = document.createElement("option");
  optPt.value = "pt";
  optPt.textContent = "PT";
  optPt.selected = lang.value === "pt";
  
  const optEn = document.createElement("option");
  optEn.value = "en";
  optEn.textContent = "EN";
  optEn.selected = lang.value === "en";
  
  select.appendChild(optPt);
  select.appendChild(optEn);
  
  select.addEventListener("change", (e) => {
    lang.value = e.target.value;
  });
  
  return select;
}

export function ServerSelector() {
  const select = document.createElement("select");
  select.style.cssText = "background:var(--bg-card);border:1px solid var(--border);color:var(--ink-2);font-size:0.7rem;padding:2px 4px;border-radius:4px;cursor:pointer;font-family:var(--font-mono);";
  
  const servers = ["NFI", "SFI"];
  servers.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    opt.selected = server.value === s;
    select.appendChild(opt);
  });
  
  select.addEventListener("change", (e) => {
    server.value = e.target.value;
  });
  
  return select;
}

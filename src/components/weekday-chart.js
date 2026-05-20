/**
 * weekday-chart.js — Day-of-week activity comparison chart.
 * Shows WTS and WTB side-by-side bars per weekday using Observable Plot.
 *
 * Usage:
 *   import { WeekdayChart } from "./components/weekday-chart.js";
 *   display(WeekdayChart(seller.by_weekday, buyer.by_weekday, { lang: "pt" }));
 */

import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";

const DOW_LABELS_PT = {
  Mon: "Seg", Tue: "Ter", Wed: "Qua",
  Thu: "Qui", Fri: "Sex", Sat: "Sáb", Sun: "Dom"
};

/**
 * @param {Array}  wtsWeekday   - seller by_weekday array  [{day, count, avg_per_occurrence}]
 * @param {Array}  wtbWeekday   - buyer  by_weekday array
 * @param {object} opts         - { lang: "pt"|"en", width: number }
 */
export function WeekdayChart(wtsWeekday = [], wtbWeekday = [], opts = {}) {
  const lang  = opts.lang  || "pt";
  const width  = opts.width || 680;

  // If no data, show placeholder
  if (!wtsWeekday.length && !wtbWeekday.length) {
    return html`<div style="color:var(--ink-3);font-size:0.75rem;padding:1rem 0">
      ${lang === "pt" ? "Dados de dias da semana não disponíveis." : "Weekday data not available."}
    </div>`;
  }

  // Merge both arrays into a flat dataset for Plot
  const rows = [];
  const allDays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];

  const wtsMap = Object.fromEntries((wtsWeekday || []).map(d => [d.day, d]));
  const wtbMap = Object.fromEntries((wtbWeekday  || []).map(d => [d.day, d]));

  for (const day of allDays) {
    const label = lang === "pt" ? (DOW_LABELS_PT[day] || day) : day;
    const wtsEntry = wtsMap[day];
    const wtbEntry = wtbMap[day];

    if (wtsEntry) rows.push({ day: label, type: "WTS", count: wtsEntry.count, avg: wtsEntry.avg_per_occurrence });
    if (wtbEntry) rows.push({ day: label, type: "WTB", count: wtbEntry.count, avg: wtbEntry.avg_per_occurrence });
  }

  const dayOrder = allDays.map(d => lang === "pt" ? (DOW_LABELS_PT[d] || d) : d);

  const plot = Plot.plot({
    width,
    height: 200,
    marginLeft: 44,
    marginBottom: 36,
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 10,
      background: "transparent",
      color: "var(--ink-3)"
    },
    x: {
      domain: dayOrder,
      label: null,
      tickSize: 0,
      padding: 0.2
    },
    y: {
      label: null,
      grid: true,
      tickSize: 0
    },
    color: {
      domain: ["WTS", "WTB"],
      range: ["var(--amber)", "#6a9fcf"]   // amber = seller, blue-grey = buyer
    },
    marks: [
      Plot.barY(rows, Plot.groupX(
        { y: "sum" },
        { x: "day", y: "count", fill: "type", fx: null }
      )),
      Plot.barY(rows, {
        x: "day",
        y: "count",
        fill: "type",
        sort: null,
        dx: d => d.type === "WTS" ? -14 : 14,
        clip: false,
        rx: 2
      }),
      Plot.ruleY([0], { stroke: "var(--border)" })
    ]
  });

  // Legend
  const legend = html`
    <div style="display:flex;gap:1.25rem;margin-bottom:0.6rem;font-family:var(--font-mono);font-size:0.6rem;color:var(--ink-3)">
      <span style="display:flex;align-items:center;gap:5px">
        <span style="width:10px;height:10px;border-radius:2px;background:var(--amber);display:inline-block"></span>
        WTS ${lang === "pt" ? "(Vendas)" : "(Listings)"}
      </span>
      <span style="display:flex;align-items:center;gap:5px">
        <span style="width:10px;height:10px;border-radius:2px;background:#6a9fcf;display:inline-block"></span>
        WTB ${lang === "pt" ? "(Buscas)" : "(Demand)"}
      </span>
    </div>`;

  return html`<div>${legend}${plot}</div>`;
}

/**
 * WeekdayChartSingle — single-type version (only WTS or only WTB)
 * @param {Array}  weekdayData  - by_weekday array
 * @param {string} type         - "WTS" | "WTB"
 * @param {object} opts
 */
export function WeekdayChartSingle(weekdayData = [], type = "WTS", opts = {}) {
  const lang  = opts.lang  || "pt";
  const width  = opts.width || 340;
  const color  = type === "WTS" ? "var(--amber)" : "#6a9fcf";

  if (!weekdayData.length) return html`<div></div>`;

  const allDays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  const rows = weekdayData.map(d => ({
    day: lang === "pt" ? (DOW_LABELS_PT[d.day] || d.day) : d.day,
    count: d.count,
    avg: d.avg_per_occurrence
  }));
  const dayOrder = allDays.map(d => lang === "pt" ? (DOW_LABELS_PT[d] || d) : d);

  return Plot.plot({
    width,
    height: 160,
    marginLeft: 40,
    marginBottom: 30,
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 10,
      background: "transparent",
      color: "var(--ink-3)"
    },
    x: { domain: dayOrder, label: null, tickSize: 0, padding: 0.25 },
    y: { label: null, grid: true, tickSize: 0 },
    marks: [
      Plot.barY(rows, { x: "day", y: "count", fill: color, rx: 2 }),
      Plot.ruleY([0], { stroke: "var(--border)" })
    ]
  });
}

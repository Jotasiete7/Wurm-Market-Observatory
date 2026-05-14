import { html } from "npm:htl";

export function LensCard({ href, icon, name, insight, coverage, period, status, version = null }) {
  const pct = coverage ? `${Math.round(coverage * 100)}%` : "—";
  const covColor = !coverage
    ? "color:var(--ink-4)"
    : coverage >= 0.65
    ? "color:var(--amber)"
    : coverage >= 0.4
    ? "color:#c47a3a"
    : "color:var(--ink-4)";

  const statusLabels = {
    active: "active",
    partial: "partial",
    unavail: "unavailable",
    uncharted: "uncharted"
  };

  return html`
    <a href="${href}" class="lens-card ${status === 'unavail' || status === 'uncharted' ? 'unavailable' : ''}" style="position:relative">
      ${version ? html`<div class="lens-version">${version}</div>` : null}
      <i class="ti ${icon} lens-icon" aria-hidden="true"></i>
      <div class="lens-card-name">${name}</div>
      <div class="lens-card-insight">${insight}</div>
      <div class="lens-card-footer">
        <span class="lens-card-cov" style="${covColor}">
          ${pct}${period ? ` · ${period}` : ""}
        </span>
        <span class="lens-status ${status}">${statusLabels[status] ?? status}</span>
      </div>
    </a>
  `;
}

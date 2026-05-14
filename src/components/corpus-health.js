import { html } from "npm:htl";

export function CorpusHealthCard(corpus) {
  const pct = Math.round(corpus.coverage * 100);

  // Build gap overlays for the coverage bar (approximate visual positions)
  const gapOverlays = corpus.gaps.map(g => {
    const start = new Date(g.start);
    const end   = new Date(g.end);
    const monthStart = new Date(corpus.period_start);
    const monthEnd   = new Date(corpus.period_end);
    const totalDays  = (monthEnd - monthStart) / 86400000 + 1;
    const gapStart   = ((start - monthStart) / 86400000) / totalDays * 100;
    const gapWidth   = ((end - start)   / 86400000 + 1) / totalDays * 100;
    return { left: gapStart, width: gapWidth, label: g.label };
  });

  return html`
    <div class="corpus-health">
      <div class="corpus-health-header">
        <span class="corpus-name">${corpus.filename}</span>
        <span class="corpus-generated">generated ${corpus.generated_at} · pipeline v${corpus.pipeline_version}</span>
      </div>

      <div class="corpus-meta-row">
        <div>
          <div class="corpus-stat-label">Coverage</div>
          <div class="corpus-stat-val amber">${pct}%</div>
        </div>
        <div>
          <div class="corpus-stat-label">Period</div>
          <div class="corpus-stat-val">${corpus.period}</div>
        </div>
        <div>
          <div class="corpus-stat-label">Server</div>
          <div class="corpus-stat-val">${corpus.server}</div>
        </div>
        <div>
          <div class="corpus-stat-label">Known gaps</div>
          <div class="corpus-stat-val warn">${corpus.gaps.length} periods</div>
        </div>
        <div>
          <div class="corpus-stat-label">Log lines</div>
          <div class="corpus-stat-val">${corpus.log_lines.toLocaleString()}</div>
        </div>
      </div>

      <div class="cov-bar-wrap">
        <div class="cov-bar-labels">
          <span>${corpus.period_start.slice(5)}</span>
          <span>${corpus.period_end.slice(5)}</span>
        </div>
        <div class="cov-bar-track">
          <div class="cov-bar-fill" style="width:${pct}%"></div>
          ${gapOverlays.map(g => html`
            <div class="cov-bar-gap" style="left:${g.left.toFixed(1)}%;width:${g.width.toFixed(1)}%;top:0;bottom:0;height:7px" title="Gap: ${g.label}"></div>
          `)}
        </div>
        <div class="cov-legend">
          <div class="cov-legend-item">
            <div class="cov-swatch covered"></div>
            <span>covered</span>
          </div>
          <div class="cov-legend-item">
            <div class="cov-swatch gap"></div>
            <span>gap — unknown territory</span>
          </div>
          ${corpus.gaps.map(g => html`
            <div class="cov-legend-item" style="color:var(--amber)">
              <span>▲ ${g.label}</span>
            </div>
          `)}
        </div>
      </div>
    </div>
  `;
}

import sys

with open('src/style/observatory.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona estilos para o sidebar no final do arquivo
sidebar_css = '''

/* --- SIDEBAR HARMONIZATION (ARCHIVE STYLE) --- */
:root {
  --sidebar-width: 240px;
}

aside[id="observablehq-sidebar"] {
  background-color: #14120f !important; /* Mais escuro que o bg principal */
  border-right: 1px solid var(--border) !important;
  font-family: var(--font-mono) !important;
}

aside[id="observablehq-sidebar"] a {
  color: var(--ink-3) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.3px !important;
  transition: all 0.2s ease !important;
  padding: 0.4rem 1rem !important;
  border-left: 2px solid transparent !important;
}

aside[id="observablehq-sidebar"] a:hover {
  color: var(--amber) !important;
  background: rgba(212, 162, 89, 0.05) !important;
  border-left: 2px solid var(--amber) !important;
  text-decoration: none !important;
}

aside[id="observablehq-sidebar"] .observablehq-link-active a {
  color: var(--amber) !important;
  font-weight: bold !important;
  border-left: 2px solid var(--amber) !important;
}

aside[id="observablehq-sidebar"] header h1 {
  font-family: var(--font-title) !important;
  color: var(--amber) !important;
  font-size: 0.9rem !important;
  padding: 1.5rem 1rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

aside[id="observablehq-sidebar"] section {
  border-top: 1px solid var(--border-light) !important;
  margin-top: 1rem !important;
  padding-top: 1rem !important;
}
'''

if 'SIDEBAR HARMONIZATION' not in content:
    with open('src/style/observatory.css', 'a', encoding='utf-8') as f:
        f.write(sidebar_css)
    print("Sidebar styles added to observatory.css")
else:
    print("Sidebar styles already exist")

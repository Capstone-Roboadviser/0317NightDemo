from fastapi.responses import HTMLResponse


def render_homepage() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <script>(function(){var t=localStorage.getItem('theme');if(t==='dark'||(t===null&&window.matchMedia('(prefers-color-scheme: dark)').matches)){document.documentElement.classList.add('dark')}})()</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>효율적 투자선 자산배분 시뮬레이터</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {
      --background: #FFFFFF;
      --foreground: #0F172A;
      --card: #FFFFFF;
      --card-foreground: #0F172A;
      --muted: #F1F5F9;
      --muted-foreground: #64748B;
      --border: #E2E8F0;
      --input: #E2E8F0;
      --primary: #0F172A;
      --primary-foreground: #F8FAFC;
      --secondary: #F1F5F9;
      --secondary-foreground: #0F172A;
      --accent: #F1F5F9;
      --accent-foreground: #0F172A;
      --destructive: #EF4444;
      --ring: #94A3B8;
      --radius: 0.5rem;
      --chart-bg: #F8FAFC;
      --chart-grid: #E2E8F0;
      --chart-label: #94A3B8;
      --chart-line: #0F172A;
      --chart-guide: rgba(100, 116, 139, 0.75);
      --chart-scatter: rgba(15, 76, 129, 0.2);
      --chart-text: #0F172A;
      --chart-selected: #F97316;
    }

    .dark {
      --background: #020817;
      --foreground: #F8FAFC;
      --card: #0F172A;
      --card-foreground: #F8FAFC;
      --muted: #1E293B;
      --muted-foreground: #94A3B8;
      --border: #1E293B;
      --input: #1E293B;
      --primary: #F8FAFC;
      --primary-foreground: #0F172A;
      --secondary: #1E293B;
      --secondary-foreground: #F8FAFC;
      --accent: #1E293B;
      --accent-foreground: #F8FAFC;
      --destructive: #7F1D1D;
      --ring: #334155;
      --chart-bg: #1E293B;
      --chart-grid: #334155;
      --chart-label: #64748B;
      --chart-line: #F8FAFC;
      --chart-guide: rgba(148, 163, 184, 0.72);
      --chart-scatter: rgba(96, 165, 250, 0.28);
      --chart-text: #F8FAFC;
      --chart-selected: #FB923C;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      min-height: 100vh;
      color: var(--foreground);
      font-family: "Noto Sans KR", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--background);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 24px 24px 48px;
    }

    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 0;
      margin-bottom: 32px;
      border-bottom: 1px solid var(--border);
    }

    .navbar-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 16px;
      color: var(--foreground);
      text-decoration: none;
    }

    .navbar-brand svg {
      width: 28px;
      height: 28px;
    }

    .navbar-links {
      display: flex;
      align-items: center;
      gap: 24px;
    }

    .navbar-links a {
      font-size: 14px;
      color: var(--muted-foreground);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.15s;
    }

    .navbar-links a:hover {
      color: var(--foreground);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      padding: 2px 10px;
      border-radius: 9999px;
      border: 1px solid var(--border);
      font-size: 12px;
      font-weight: 500;
      color: var(--muted-foreground);
      background: var(--muted);
    }

    .hero {
      text-align: center;
      max-width: 720px;
      margin: 0 auto 48px;
    }

    .hero .badge {
      margin-bottom: 16px;
    }

    .hero h1 {
      font-size: 38px;
      font-weight: 800;
      line-height: 1.12;
      letter-spacing: -0.025em;
      margin-bottom: 16px;
    }

    .hero p {
      font-size: 16px;
      line-height: 1.7;
      color: var(--muted-foreground);
      max-width: 580px;
      margin: 0 auto 24px;
    }

    .hero-note {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 16px;
      border-radius: var(--radius);
      background: var(--muted);
      color: var(--muted-foreground);
      font-size: 13px;
      line-height: 1.5;
    }

    .hero-note svg {
      width: 16px;
      height: 16px;
      flex-shrink: 0;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }

    .card-header {
      padding: 24px 24px 0;
    }

    .card-title {
      font-size: 18px;
      font-weight: 600;
      letter-spacing: -0.01em;
      margin-bottom: 4px;
    }

    .card-description {
      font-size: 14px;
      color: var(--muted-foreground);
      line-height: 1.5;
    }

    .card-content {
      padding: 24px;
    }

    .app-grid {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 24px;
      align-items: start;
    }

    .controls {
      position: sticky;
      top: 24px;
    }

    .controls .card-content {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .field-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .field-label {
      font-size: 14px;
      font-weight: 500;
      color: var(--foreground);
    }

    .field-hint {
      font-size: 13px;
      color: var(--muted-foreground);
    }

    input[type="number"] {
      width: 100%;
      height: 40px;
      border: 1px solid var(--input);
      border-radius: var(--radius);
      padding: 0 12px;
      font-size: 14px;
      font-family: inherit;
      color: var(--foreground);
      background: var(--background);
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }

    input[type="number"]:focus {
      border-color: var(--ring);
      box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.2);
    }

    /* Custom Select (shadcn/ui Radix style) */
    .custom-select {
      position: relative;
      width: 100%;
    }

    .custom-select-trigger {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      height: 40px;
      border: 1px solid var(--input);
      border-radius: var(--radius);
      padding: 0 12px;
      font-size: 14px;
      font-family: inherit;
      color: var(--foreground);
      background: var(--background);
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s, box-shadow 0.15s;
      user-select: none;
    }

    .custom-select-trigger:focus {
      border-color: var(--ring);
      box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.2);
    }

    .custom-select-trigger[data-state="open"] {
      border-color: var(--ring);
      box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.2);
    }

    .custom-select-trigger-text {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .custom-select-chevron {
      flex-shrink: 0;
      width: 16px;
      height: 16px;
      color: var(--muted-foreground);
      transition: transform 0.2s ease;
    }

    .custom-select-trigger[data-state="open"] .custom-select-chevron {
      transform: rotate(180deg);
    }

    .custom-select-content {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      width: 100%;
      z-index: 50;
      background: var(--background);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
      padding: 4px;
      opacity: 0;
      transform: translateY(-4px) scale(0.98);
      pointer-events: none;
      transition: opacity 0.15s ease, transform 0.15s ease;
    }

    .dark .custom-select-content {
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
    }

    .custom-select-content[data-state="open"] {
      opacity: 1;
      transform: translateY(0) scale(1);
      pointer-events: auto;
    }

    .custom-select-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 8px 8px 32px;
      font-size: 14px;
      font-family: inherit;
      color: var(--foreground);
      border-radius: calc(var(--radius) - 2px);
      cursor: pointer;
      user-select: none;
      position: relative;
      transition: background-color 0.1s ease;
    }

    .custom-select-item:hover,
    .custom-select-item[data-highlighted] {
      background: var(--accent);
      color: var(--accent-foreground);
    }

    .custom-select-item[data-selected]::before {
      content: '';
      position: absolute;
      left: 8px;
      top: 50%;
      transform: translateY(-50%);
      width: 16px;
      height: 16px;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
      background-size: 16px;
      background-repeat: no-repeat;
    }

    .dark .custom-select-item[data-selected]::before {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23F8FAFC' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
    }

    .slider-card {
      padding: 16px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--muted);
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 12px;
      gap: 12px;
    }

    .slider-profile {
      font-size: 20px;
      font-weight: 700;
      color: var(--foreground);
    }

    .slider-target {
      font-size: 13px;
      font-weight: 500;
      color: var(--muted-foreground);
      background: var(--background);
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid var(--border);
      white-space: nowrap;
    }

    input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 9999px;
      background: linear-gradient(to right, var(--primary) 0%, var(--primary) var(--slider-pct, 50%), rgba(15, 23, 42, 0.2) var(--slider-pct, 50%), rgba(15, 23, 42, 0.2) 100%);
      outline: none;
      cursor: pointer;
    }

    .dark input[type="range"] {
      background: linear-gradient(to right, var(--primary) 0%, var(--primary) var(--slider-pct, 50%), rgba(248, 250, 252, 0.2) var(--slider-pct, 50%), rgba(248, 250, 252, 0.2) 100%);
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--background);
      border: 1px solid rgba(15, 23, 42, 0.5);
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
      cursor: pointer;
      transition: box-shadow 0.15s ease;
    }

    .dark input[type="range"]::-webkit-slider-thumb {
      border-color: rgba(248, 250, 252, 0.5);
    }

    input[type="range"]:focus-visible::-webkit-slider-thumb {
      outline: none;
      box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--ring);
    }

    input[type="range"]::-moz-range-thumb {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--background);
      border: 1px solid rgba(15, 23, 42, 0.5);
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
      cursor: pointer;
    }

    .dark input[type="range"]::-moz-range-thumb {
      border-color: rgba(248, 250, 252, 0.5);
    }

    .slider-labels {
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted-foreground);
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 40px;
      border: none;
      border-radius: var(--radius);
      cursor: pointer;
      font-family: inherit;
      font-size: 14px;
      font-weight: 500;
      transition: background 0.15s, opacity 0.15s;
    }

    .btn-primary {
      background: var(--primary);
      color: var(--primary-foreground);
    }

    .btn-primary:hover {
      opacity: 0.92;
    }

    .status-text {
      font-size: 13px;
      color: var(--muted-foreground);
      min-height: 20px;
      margin-top: 4px;
    }

    .combination-panel {
      margin-top: 16px;
      padding: 14px 16px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--muted);
    }

    .combination-panel[hidden] {
      display: none;
    }

    .combination-panel-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--foreground);
      margin-bottom: 6px;
    }

    .combination-panel-meta {
      font-size: 13px;
      line-height: 1.6;
      color: var(--muted-foreground);
    }

    .combination-members {
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .combination-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 10px;
      border-radius: 999px;
      background: var(--background);
      border: 1px solid var(--border);
      color: var(--foreground);
      font-size: 12px;
      line-height: 1.4;
    }

    .combination-chip strong {
      font-weight: 700;
    }

    .results {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .step-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted-foreground);
      margin-bottom: 12px;
    }

    .step-num {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--foreground);
      color: var(--primary-foreground);
      font-size: 11px;
      font-weight: 700;
    }

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      flex-wrap: wrap;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 13px;
      color: var(--muted-foreground);
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
    }

    .chart-wrap {
      margin-top: 16px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--muted);
      padding: 12px;
      position: relative;
    }

    .chart-loading {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 16px;
      padding: 80px 40px;
    }

    .chart-loading-text {
      font-size: 13px;
      font-weight: 500;
      color: var(--muted-foreground);
    }

    .progress-track {
      width: 220px;
      height: 8px;
      border-radius: 9999px;
      background: rgba(15, 23, 42, 0.2);
      overflow: hidden;
    }

    .dark .progress-track {
      background: rgba(248, 250, 252, 0.2);
    }

    .progress-indicator {
      height: 100%;
      border-radius: 9999px;
      background: var(--primary);
      width: 0%;
      transition: width 0.3s ease-out;
    }

    .chart-reveal {
      animation: chart-fade-in 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    @keyframes chart-fade-in {
      from { opacity: 0; filter: blur(6px); }
      to { opacity: 1; filter: blur(0px); }
    }

    svg {
      width: 100%;
      height: auto;
      display: block;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }

    .metric-card .card-content {
      padding: 20px 24px;
    }

    .metric-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--muted-foreground);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 8px;
    }

    .metric-value {
      font-size: 30px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--foreground);
      margin-bottom: 6px;
    }

    .metric-desc {
      font-size: 13px;
      color: var(--muted-foreground);
      line-height: 1.5;
    }

    .two-col {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
    }

    /* ── Donut Charts ── */
    .donut-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 32px;
    }
    .donut-section {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .donut-label {
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted-foreground);
      margin-bottom: 16px;
    }
    .donut-container {
      position: relative;
      width: 220px;
      height: 220px;
    }
    .donut-container svg {
      width: 220px;
      height: 220px;
    }
    .donut-center {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      pointer-events: none;
    }
    .donut-center-value {
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--foreground);
      line-height: 1;
    }
    .donut-center-label {
      font-size: 11px;
      color: var(--muted-foreground);
      margin-top: 4px;
    }
    .donut-legend {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px 20px;
      margin-top: 20px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
      width: 100%;
    }
    .donut-legend-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: var(--muted-foreground);
    }
    .donut-legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }
    .donut-legend-name {
      font-weight: 500;
      color: var(--foreground);
    }
    .donut-legend-value {
      font-weight: 600;
    }
    /* ── Allocation Tabs ── */
    .alloc-tabs {
      display: flex;
      gap: 4px;
      margin-left: auto;
      background: var(--muted);
      border-radius: 6px;
      padding: 3px;
    }
    .alloc-tab {
      padding: 4px 12px;
      border: none;
      background: none;
      font-family: inherit;
      font-size: 12px;
      font-weight: 500;
      color: var(--muted-foreground);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      line-height: 1.4;
    }
    .alloc-tab:hover {
      color: var(--foreground);
    }
    .alloc-tab.active {
      background: var(--background);
      color: var(--foreground);
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    /* ── Allocation List View ── */
    .alloc-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      table-layout: fixed;
    }
    .alloc-table col.col-asset { width: 50%; }
    .alloc-table col.col-weight { width: 14%; }
    .alloc-table col.col-bar { width: 18%; }
    .alloc-table col.col-risk { width: 18%; }
    .alloc-table th {
      text-align: left;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted-foreground);
      padding: 8px 12px;
      border-bottom: 2px solid var(--border);
    }
    .alloc-table th:not(:first-child) {
      text-align: right;
    }
    .alloc-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      color: var(--foreground);
    }
    .alloc-table td:not(:first-child) {
      text-align: right;
      font-variant-numeric: tabular-nums;
      font-weight: 600;
    }
    .alloc-table tr:last-child td {
      border-bottom: none;
    }
    .alloc-table-asset {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .alloc-table-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .alloc-table-name {
      font-weight: 500;
    }
    .alloc-table-bar-cell {
      width: 100px;
    }
    .alloc-table-bar {
      height: 6px;
      border-radius: 3px;
      transition: width 0.3s ease;
    }
    /* Expandable row toggle */
    .alloc-table-toggle {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      user-select: none;
    }
    .alloc-table-chevron {
      width: 14px;
      height: 14px;
      flex-shrink: 0;
      transition: transform 0.2s ease;
      color: var(--muted-foreground);
    }
    .alloc-table-toggle.expanded .alloc-table-chevron {
      transform: rotate(90deg);
    }
    /* Child stock rows */
    .alloc-child-row td {
      padding: 6px 12px 6px 40px;
      font-size: 12px;
      color: var(--muted-foreground);
      border-bottom: 1px solid var(--border);
    }
    .alloc-child-row td:not(:first-child) {
      text-align: right;
      font-variant-numeric: tabular-nums;
      font-weight: 500;
    }
    .alloc-child-row:last-of-type td {
      border-bottom: 1px solid var(--border);
    }
    .alloc-child-ticker {
      font-family: 'Inter', monospace;
      font-weight: 600;
      color: var(--foreground);
      margin-right: 6px;
      font-size: 11px;
      opacity: 0.7;
    }
    .alloc-child-name {
      font-weight: 400;
    }
    .alloc-children-hidden {
      display: none;
    }
    /* Donut slice hover */
    .donut-slice {
      transition: opacity 0.15s, filter 0.15s;
      cursor: pointer;
    }
    .donut-slice:hover {
      opacity: 0.85;
      filter: brightness(1.1);
    }
    /* Donut tooltip */
    .donut-tooltip {
      position: fixed;
      pointer-events: none;
      z-index: 50;
      padding: 10px 14px;
      border-radius: var(--radius);
      background: var(--foreground);
      color: var(--primary-foreground);
      font-size: 13px;
      font-weight: 500;
      line-height: 1.4;
      opacity: 0;
      transition: opacity 0.12s ease;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      min-width: 180px;
      max-width: 280px;
    }
    .donut-tooltip.visible {
      opacity: 0.95;
    }
    .donut-tooltip-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--muted-foreground);
    }
    .donut-tooltip-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .donut-tooltip-name {
      font-weight: 600;
    }
    .donut-tooltip-value {
      font-weight: 700;
      margin-left: auto;
    }
    .donut-tooltip-stocks {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .donut-tooltip-stock {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 400;
      opacity: 0.85;
    }
    .donut-tooltip-stock-ticker {
      font-family: 'Inter', monospace;
      font-weight: 500;
      opacity: 0.7;
      min-width: 36px;
    }
    .donut-tooltip-stock-pct {
      margin-left: auto;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
      opacity: 0.9;
    }

    /* ── Chart (Frontier) Tooltip ── */
    .chart-tooltip {
      position: fixed;
      pointer-events: none;
      z-index: 50;
      padding: 14px 16px;
      border-radius: var(--radius);
      background: var(--foreground);
      color: var(--primary-foreground);
      font-size: 13px;
      font-weight: 500;
      line-height: 1.5;
      opacity: 0;
      transition: opacity 0.12s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      min-width: 180px;
      max-width: 260px;
    }
    .chart-tooltip.visible { opacity: 0.9; }
    .chart-tooltip-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--muted-foreground);
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .chart-tooltip-row {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 3px 0;
    }
    .chart-tooltip-row-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .chart-tooltip-row-name {
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .chart-tooltip-row-value {
      font-weight: 700;
      white-space: nowrap;
    }
    .scatter-point {
      cursor: pointer;
      transition: r 0.12s ease;
    }
    #sel-glow, #sel-hit, #sel-dot {
      transition: cx 0.35s cubic-bezier(0.4, 0, 0.2, 1), cy 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes sel-pulse {
      0%, 100% { r: 12; opacity: 0.3; }
      50% { r: 18; opacity: 0.1; }
    }
    #sel-glow {
      animation: sel-pulse 2.5s ease-in-out infinite;
    }
    @keyframes sharpe-pulse {
      0%, 100% { r: 12; opacity: 0.35; }
      50% { r: 20; opacity: 0.08; }
    }
    #sharpe-glow {
      animation: sharpe-pulse 2.8s ease-in-out infinite;
    }
    .frontier-hit {
      cursor: pointer;
    }

    .vol-chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }


    .vol-time-toggles {
      display: flex;
      gap: 4px;
    }

    .vol-time-btn {
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 500;
      font-family: inherit;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--background);
      color: var(--muted-foreground);
      cursor: pointer;
      transition: all 0.15s;
    }

    .vol-time-btn:hover {
      background: var(--accent);
      color: var(--foreground);
    }

    .vol-time-btn.active {
      background: var(--primary);
      color: var(--primary-foreground);
      border-color: var(--primary);
    }

    .vol-chart-wrap {
      margin-top: 12px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--muted);
      padding: 12px;
      position: relative;
    }

    .vol-hover-info {
      position: absolute;
      top: 20px;
      left: 72px;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.15s;
    }

    .vol-hover-info.visible {
      opacity: 1;
    }

    .vol-hover-date {
      font-size: 11px;
      color: var(--muted-foreground);
      font-weight: 400;
    }

    .vol-hover-value {
      font-size: 20px;
      font-weight: 700;
      color: var(--foreground);
      line-height: 1.2;
    }

    .vol-chart-empty {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      color: var(--muted-foreground);
      font-size: 13px;
    }

    .options-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .option-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 16px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--background);
      font-size: 14px;
      transition: all 0.15s;
      gap: 12px;
    }

    .option-item.active {
      border-color: var(--foreground);
      background: var(--muted);
    }

    .option-item .option-label {
      font-weight: 600;
    }

    .option-item .option-stats {
      display: flex;
      gap: 16px;
      color: var(--muted-foreground);
      font-size: 13px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .option-item .option-stats span {
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .option-charts {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 16px;
    }
    .option-chart-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      padding: 16px 8px 12px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--background);
    }
    .option-chart-card.active {
      border-top: 2px solid var(--opt-color, var(--primary));
      box-shadow: 0 -4px 12px -2px color-mix(in srgb, var(--opt-color, var(--primary)) 45%, transparent);
    }
    .option-chart-label {
      font-weight: 600;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .option-chart-label .opt-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }
    .option-chart-svg {
      width: 120px;
      height: 120px;
    }
    .option-chart-stats {
      font-size: 11px;
      color: var(--muted-foreground);
      text-align: center;
      line-height: 1.5;
    }
    .option-chart-legend {
      display: flex;
      flex-direction: column;
      gap: 3px;
      width: 100%;
      padding: 0 4px;
    }
    .option-chart-legend-item {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 10px;
      color: var(--muted-foreground);
    }
    .option-chart-legend-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .option-chart-legend-name {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .option-chart-legend-val {
      font-variant-numeric: tabular-nums;
    }

    .explanation-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 10px;
    }

    .explanation-body {
      font-size: 14px;
      line-height: 1.7;
      color: var(--muted-foreground);
    }

    .summary-text {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
      font-size: 13px;
      color: var(--muted-foreground);
      line-height: 1.6;
    }

    .interpretation {
      font-size: 14px;
      line-height: 1.7;
      color: var(--muted-foreground);
    }

    /* ── Value transition animations ── */
    .metric-value {
      transition: transform 0.25s ease;
    }
    .fade-content {
      transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .fade-content.fade-out {
      opacity: 0;
      transform: translateY(4px);
    }

    .footer {
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
      color: var(--muted-foreground);
    }

    .footer a {
      color: var(--muted-foreground);
      text-decoration: none;
      font-weight: 500;
    }

    .footer a:hover {
      color: var(--foreground);
    }

    .theme-toggle {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--background);
      color: var(--foreground);
      cursor: pointer;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
    }

    .theme-toggle:hover {
      background: var(--accent);
    }

    .theme-toggle svg {
      width: 16px;
      height: 16px;
    }

    .theme-toggle .icon-sun {
      display: none;
    }

    .theme-toggle .icon-moon {
      display: block;
    }

    .dark .theme-toggle .icon-sun {
      display: block;
    }

    .dark .theme-toggle .icon-moon {
      display: none;
    }

    body,
    .card,
    .navbar,
    .footer,
    .slider-card,
    .chart-wrap,
    .vol-chart-wrap,
    .vol-time-btn,
    .option-item,
    .hero-note,
    .badge,
    .custom-select-trigger,
    .custom-select-content,
    input,
    .btn-primary,
    .slider-target,
    .theme-toggle {
      transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    }

    @media (max-width: 980px) {
      .container {
        padding: 16px 16px 32px;
      }

      .app-grid,
      .metrics-grid,
      .two-col {
        grid-template-columns: 1fr;
      }

      .controls {
        position: static;
      }

      .hero {
        margin-bottom: 32px;
      }

      .hero h1 {
        font-size: 30px;
      }

      .hero p {
        font-size: 14px;
      }

      .chart-header {
        flex-direction: column;
      }

      .footer {
        flex-direction: column;
        gap: 8px;
        text-align: center;
      }

      .navbar {
        margin-bottom: 24px;
      }

      .navbar-links a {
        display: none;
      }

      .navbar-links .badge {
        display: inline-flex;
      }

      .donut-grid {
        grid-template-columns: 1fr;
        gap: 32px;
      }

      .option-charts {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 640px) {
      .container {
        padding: 14px 14px 28px;
      }

      .hero h1 {
        font-size: 27px;
      }

      .option-item {
        flex-direction: column;
        align-items: flex-start;
      }

      .option-item .option-stats {
        justify-content: flex-start;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="navbar-brand">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
        </svg>
        자산배분 시뮬레이터
      </a>
      <div class="navbar-links">
        <a href="/admin">관리 콘솔</a>
        <a href="/docs">API 문서</a>
        <a href="/redoc">참고 문서</a>
        <span class="badge">한국어 데모</span>
        <button class="theme-toggle" id="theme-toggle" aria-label="다크 모드 전환">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
        </button>
      </div>
    </nav>

    <section class="hero">
      <span class="badge">Efficient Frontier Demo</span>
      <h1>효율적 투자선 기반<br />자산배분 시뮬레이터</h1>
      <p>
        고정된 8개 자산군을 기준으로, 사용자의 위험 성향에 따라
        효율적 투자선 위의 포트폴리오 예시를 계산하고 설명합니다.
      </p>
      <div class="hero-note">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        본 서비스는 데모용 시뮬레이션입니다. 고정 샘플 데이터 기반이며 투자 자문이나 수익 보장을 제공하지 않습니다.
      </div>
    </section>

    <section class="app-grid">
      <aside class="controls">
        <div class="card">
          <div class="card-header">
            <div class="step-badge"><span class="step-num">1</span> 위험 설정</div>
            <div class="card-title">투자 위험 수준 선택</div>
            <div class="card-description">슬라이더로 현재 포트폴리오가 프론티어 어디에 놓일지 정합니다.</div>
          </div>
          <div class="card-content">
            <form id="portfolio-form">
              <div class="field-group">
                <label class="field-label">계산 기준</label>
                <input type="hidden" id="data_source" name="data_source" value="managed_universe" />
                <input type="hidden" id="investment_horizon" name="investment_horizon" value="medium" />
                <span class="field-hint">기본값은 관리자 종목 유니버스이며, 아직 설정되지 않았으면 내장 데모 종목 유니버스로 자동 대체됩니다.</span>
              </div>

              <div class="field-group">
                <div class="slider-card">
                  <div class="slider-header">
                    <span class="slider-profile" id="risk-label">균형형</span>
                    <span class="slider-target" id="slider-target">목표 기대수익률 16.0%</span>
                  </div>
                  <input id="risk_slider" type="range" min="0" max="100" step="0.1" value="50" />
                  <div class="slider-labels">
                    <span>안정형</span>
                    <span>공격형</span>
                  </div>
                </div>
              </div>

              <span class="field-hint">슬라이더를 움직이면 현재 포트폴리오가 프론티어 위에서 바로 갱신됩니다.</span>
              <div id="status" class="status-text"></div>
            </form>
          </div>
        </div>
      </aside>

      <div class="results">
        <div class="card">
          <div class="card-header">
            <div class="step-badge"><span class="step-num">2</span> 프론티어</div>
            <div class="chart-header">
              <div>
                <div class="card-title">효율적 투자선 차트</div>
                <div class="card-description" id="chart-copy">
                  가능한 포트폴리오 점 구름 위로 효율적 투자선이 그려지고, 비교용 기준 직선보다 위쪽 경계가 효율적 구간임을 보여줍니다.
                </div>
              </div>
              <div class="legend">
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-scatter);"></i>가능한 포트폴리오</span>
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-guide);"></i>비교 기준선</span>
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-line);"></i>효율적 투자선</span>
                <span class="legend-item"><i class="legend-dot" style="background: #22c55e;"></i>안정형</span>
                <span class="legend-item"><i class="legend-dot" style="background: #3b82f6;"></i>균형형</span>
                <span class="legend-item"><i class="legend-dot" style="background: #a855f7;"></i>성장형</span>
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-selected);"></i>현재 포트폴리오</span>
                <span class="legend-item"><i class="legend-dot" style="background: #ef4444;"></i>최대 샤프</span>
              </div>
            </div>
          </div>
          <div class="card-content">
            <div class="chart-wrap">
              <div id="chart-loading" class="chart-loading">
                <div class="chart-loading-text">포트폴리오를 계산하고 있습니다</div>
                <div class="progress-track">
                  <div class="progress-indicator"></div>
                </div>
              </div>
              <svg id="frontier-chart" viewBox="0 0 900 860" aria-label="효율적 투자선 차트" style="display:none"></svg>
            </div>
          </div>
        </div>

        <div class="metrics-grid">
          <div class="card metric-card">
            <div class="card-content">
              <div class="metric-label">예상 수익률</div>
              <div class="metric-value" id="metric-return">-</div>
              <div class="metric-desc">샘플 데이터 기준 연율 기대수익률</div>
            </div>
          </div>
          <div class="card metric-card">
            <div class="card-content">
              <div class="metric-label">변동성</div>
              <div class="metric-value" id="metric-vol">-</div>
              <div class="metric-desc">현재 포트폴리오의 연율 기준 위험 수준</div>
            </div>
          </div>
          <div class="card metric-card">
            <div class="card-content">
              <div class="metric-label">샤프 지수</div>
              <div class="metric-value" id="metric-sharpe">-</div>
              <div class="metric-desc">위험 대비 효율성을 비교하는 지표</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-content" style="padding-top:16px">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:12px">
              <div>
                <div class="card-title" id="history-chart-title">포트폴리오 변동성 추이</div>
                <div class="card-description" id="history-chart-desc">선택된 포트폴리오의 과거 실현 변동성 (20일 롤링, 연율화) 추이입니다.</div>
              </div>
              <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
                <div class="alloc-tabs">
                  <button class="alloc-tab history-mode-tab active" data-mode="vol">변동성</button>
                  <button class="alloc-tab history-mode-tab" data-mode="ret">기대수익률</button>
                </div>
                <div class="vol-time-toggles" id="vol-time-toggles">
                  <button class="vol-time-btn" data-range="1w">1주</button>
                  <button class="vol-time-btn" data-range="3m">3달</button>
                  <button class="vol-time-btn active" data-range="1y">1년</button>
                  <button class="vol-time-btn" data-range="5y">5년</button>
                  <button class="vol-time-btn" data-range="all">전체</button>
                </div>
                <div class="vol-time-toggles" id="ret-time-toggles" style="display:none">
                  <button class="ret-time-btn vol-time-btn" data-range="1w">1주</button>
                  <button class="ret-time-btn vol-time-btn" data-range="3m">3달</button>
                  <button class="ret-time-btn vol-time-btn active" data-range="1y">1년</button>
                  <button class="ret-time-btn vol-time-btn" data-range="5y">5년</button>
                  <button class="ret-time-btn vol-time-btn" data-range="all">전체</button>
                </div>
              </div>
            </div>
            <div id="vol-panel">
              <div class="vol-chart-wrap">
                <div class="vol-hover-info" id="vol-hover-info">
                  <div class="vol-hover-date" id="vol-hover-date"></div>
                  <div class="vol-hover-value" id="vol-hover-value"></div>
                </div>
                <div class="vol-chart-empty" id="vol-chart-empty">포트폴리오를 먼저 계산해주세요.</div>
                <svg id="vol-chart" viewBox="0 0 900 280" aria-label="변동성 추이 차트" style="display:none"></svg>
              </div>
            </div>
            <div id="ret-panel" style="display:none">
              <div class="vol-chart-wrap">
                <div class="vol-hover-info" id="ret-hover-info">
                  <div class="vol-hover-date" id="ret-hover-date"></div>
                  <div class="vol-hover-value" id="ret-hover-value"></div>
                </div>
                <div class="vol-chart-empty" id="ret-chart-empty">포트폴리오를 먼저 계산해주세요.</div>
                <svg id="ret-chart" viewBox="0 0 900 280" aria-label="기대수익률 추이 차트" style="display:none"></svg>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="step-badge"><span class="step-num">3</span> 해석</div>
          </div>
          <div class="card-content">
            <div class="explanation-title" id="explanation-title">왜 이런 포트폴리오가 나왔을까?</div>
            <div class="explanation-body fade-content" id="explanation-body">첫 계산이 완료되면 이 위치에 설명이 표시됩니다.</div>
            <div class="summary-text fade-content" id="summary"></div>
            <div class="combination-panel fade-content" id="combination-panel" hidden>
              <div class="combination-panel-title">현재 적용된 종목 유니버스</div>
              <div class="combination-panel-meta" id="combination-meta"></div>
              <div class="combination-members" id="combination-members"></div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="step-badge"><span class="step-num">4</span> 옵션 비교</div>
            <div class="card-title">효율적 투자선 옵션</div>
            <div class="card-description">각 위험 수준별 대표 포트폴리오를 비교합니다.</div>
          </div>
          <div class="card-content">
            <div id="frontier-options" class="options-list fade-content"></div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
              <div class="step-badge"><span class="step-num">5</span> 자산배분</div>
              <div class="alloc-tabs">
                <button class="alloc-tab active" data-view="pie">차트</button>
                <button class="alloc-tab" data-view="list">목록</button>
              </div>
            </div>
            <div class="card-title">비중과 리스크 기여도</div>
            <div class="card-description">비중은 자금 배분을, 리스크 기여도는 실제 변동성의 출처를 보여줍니다. 효율적 자산배분에서는 이 둘이 다르게 나타날 수 있습니다.</div>
          </div>
          <div class="card-content">
            <div id="allocations-pie" class="donut-grid fade-content">
              <!-- JS renders two donut charts here -->
            </div>
            <div id="allocations-list" class="fade-content" style="display:none">
              <!-- JS renders table here -->
            </div>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <span>효율적 투자선 자산배분 시뮬레이터</span>
      <div style="display:flex;gap:14px;align-items:center">
        <a href="/admin">관리 콘솔</a>
        <a href="/docs">Swagger</a>
      </div>
    </footer>
  </div>

  <div class="donut-tooltip" id="donut-tooltip"></div>

  <div class="chart-tooltip" id="chart-tooltip"></div>

  <script>
    // Stock-level data by sector (loaded async)
    let stocksBySector = {};

    (async function loadStocks() {
      try {
        const res = await fetch("/portfolio/stocks");
        if (res.ok) {
          const data = await res.json();
          stocksBySector = data.sectors || {};
        }
      } catch (_) { /* ignore – tooltip just won't show stocks */ }
    })();

    const ASSET_COLORS = {
      bond: "#5B7C99",
      real_assets: "#A67C52",
      etf: "#2D6A8E",
      tech_healthcare: "#7B6ED6",
      ai_semiconductor_social: "#E76F51",
      financials: "#2A9D8F",
      energy: "#E9C46A",
      consumer_other: "#6C757D",
    };

    const slider = document.getElementById("risk_slider");
    const riskLabel = document.getElementById("risk-label");
    const sliderTarget = document.getElementById("slider-target");
    const horizonEl = document.getElementById("investment_horizon");
    const dataSourceEl = document.getElementById("data_source");
    const statusEl = document.getElementById("status");
    const summaryEl = document.getElementById("summary");
    const explanationTitleEl = document.getElementById("explanation-title");
    const explanationBodyEl = document.getElementById("explanation-body");
    const combinationPanelEl = document.getElementById("combination-panel");
    const combinationMetaEl = document.getElementById("combination-meta");
    const combinationMembersEl = document.getElementById("combination-members");
    const optionsEl = document.getElementById("frontier-options");
    const allocPieEl = document.getElementById("allocations-pie");
    const allocListEl = document.getElementById("allocations-list");
    const chartEl = document.getElementById("frontier-chart");
    const chartLoadingEl = document.getElementById("chart-loading");

    let lastData = null;
    let lastAllocations = [];
    let lastAllocFiltered = [];
    let allocView = "pie"; // "pie" or "list"
    let chartXScale = null; // stored after renderChart
    let chartYScale = null;
    let chartBounds = null;
    let debounceTimer = null;
    const activeAnimations = {};

    // ── Smooth number animation ──
    function animateNumber(el, newValue, format, duration) {
      duration = duration || 400;
      const key = el.id || el;
      if (activeAnimations[key]) cancelAnimationFrame(activeAnimations[key]);

      const oldText = el.textContent.replace(/[^0-9.\\-]/g, "");
      const oldVal = parseFloat(oldText) || 0;
      const newVal = parseFloat(String(newValue).replace(/[^0-9.\\-]/g, "")) || 0;
      if (Math.abs(oldVal - newVal) < 0.001) { el.textContent = format(newVal); return; }

      const start = performance.now();
      function tick(now) {
        const t = Math.min((now - start) / duration, 1);
        const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        const current = oldVal + (newVal - oldVal) * ease;
        el.textContent = format(current);
        if (t < 1) activeAnimations[key] = requestAnimationFrame(tick);
        else delete activeAnimations[key];
      }
      activeAnimations[key] = requestAnimationFrame(tick);
    }

    // ── Crossfade content helper ──
    function crossfade(el, updateFn, delay) {
      delay = delay || 200;
      el.classList.add("fade-out");
      setTimeout(function() {
        updateFn();
        el.classList.remove("fade-out");
      }, delay);
    }

    function percent(value) {
      return `${(value * 100).toFixed(1)}%`;
    }

    const DEFAULT_RETURN_MIN = 0.10;
    const DEFAULT_RETURN_MAX = 0.22;
    const FRONTIER_RISK_FREE_RATE = 0.02;

    function sliderProfile(position) {
      if (position <= 0.3333) return { risk_profile: "conservative", label: "안정형" };
      if (position <= 0.6667) return { risk_profile: "balanced", label: "균형형" };
      return { risk_profile: "growth", label: "성장형" };
    }

    function currentSliderPosition() {
      const raw = Number(slider.value);
      if (!Number.isFinite(raw)) return 0.5;
      return Math.min(1, Math.max(0, raw / 100));
    }

    function frontierReturnRange(frontierPoints) {
      if (!frontierPoints || !frontierPoints.length) {
        return { min: DEFAULT_RETURN_MIN, max: DEFAULT_RETURN_MAX };
      }
      const min = Math.min(...frontierPoints.map((point) => point.expected_return));
      const max = Math.max(...frontierPoints.map((point) => point.expected_return));
      if (!Number.isFinite(min) || !Number.isFinite(max) || Math.abs(max - min) < 1e-9) {
        return { min: DEFAULT_RETURN_MIN, max: DEFAULT_RETURN_MAX };
      }
      return { min, max };
    }

    function currentSliderTargetExpectedReturn(frontierPoints) {
      const position = currentSliderPosition();
      const range = frontierReturnRange(frontierPoints);
      return range.min + (range.max - range.min) * position;
    }

    function syncSliderDisplay(frontierPoints) {
      const position = currentSliderPosition();
      const target = currentSliderTargetExpectedReturn(frontierPoints);
      const profile = sliderProfile(position);
      riskLabel.textContent = profile.label;
      sliderTarget.textContent = `목표 기대수익률 ${percent(target)}`;
      return { profile, target };
    }

    function setSliderTargetExpectedReturn(target, options) {
      const range = frontierReturnRange(lastData && lastData.frontier_points ? lastData.frontier_points : null);
      const next = Number(target);
      const position = !Number.isFinite(next) || Math.abs(range.max - range.min) < 1e-9
        ? 0.5
        : (next - range.min) / (range.max - range.min);
      slider.value = (Math.min(1, Math.max(0, position)) * 100).toFixed(1);
      updateSliderTrack();
      syncSliderDisplay(lastData && lastData.frontier_points ? lastData.frontier_points : null);
      if (options && options.updateFromCache && lastData && lastData.frontier_points) {
        updateFromCache();
      }
    }

    function payloadFromInputs() {
      const { profile } = syncSliderDisplay(lastData && lastData.frontier_points ? lastData.frontier_points : null);
      return {
        risk_profile: profile.risk_profile,
        investment_horizon: horizonEl.value,
        data_source: dataSourceEl.value,
      };
    }

    function findClosestFrontierIndexByExpectedReturn(frontierPoints, targetReturn) {
      let bestIdx = 0;
      let bestDist = Infinity;
      frontierPoints.forEach(function(p, i) {
        const dist = Math.abs(p.expected_return - targetReturn);
        if (dist < bestDist) { bestDist = dist; bestIdx = i; }
      });
      return bestIdx;
    }

    function buildFrontierSelectionCopy(point, targetReturn, disclaimer) {
      const sharpeRatio = point.volatility > 0 ? (point.expected_return - FRONTIER_RISK_FREE_RATE) / point.volatility : 0;
      return {
        summary: `현재 선택은 목표 기대수익률 ${percent(targetReturn)}에 가장 가까운 효율적 투자선 포인트입니다. 예상 수익률은 ${percent(point.expected_return)}, 예상 변동성은 ${percent(point.volatility)}, 샤프지수는 ${sharpeRatio.toFixed(2)}입니다.`,
        explanation: `위험 슬라이더는 효율적 투자선 위에서 목표 기대수익률 구간을 정합니다. 현재 포인트는 목표 기대수익률 ${percent(targetReturn)}에 가장 가까운 조합이며, 예상 수익률 ${percent(point.expected_return)}, 예상 변동성 ${percent(point.volatility)}로 계산됩니다.`,
      };
    }

    function applyExpectedReturnSelection(data) {
      if (!data || !data.frontier_points || !data.frontier_points.length) return null;
      const { target } = syncSliderDisplay(data.frontier_points);
      const idx = findClosestFrontierIndexByExpectedReturn(data.frontier_points, target);
      const point = data.frontier_points[idx];
      const expectedReturn = point.expected_return;
      const volatility = point.volatility;
      const sharpeRatio = volatility > 0 ? (expectedReturn - FRONTIER_RISK_FREE_RATE) / volatility : 0;

      data.selected_point_index = idx;
      data.selected_point = Object.assign({}, point, { label: "현재 포트폴리오" });
      data.expected_return = expectedReturn;
      data.volatility = volatility;
      data.sharpe_ratio = sharpeRatio;

      if (point.weights) {
        const currentRiskMap = Object.fromEntries((data.allocations || []).map(function(a) {
          return [a.asset_code, a.risk_contribution || 0];
        }));
        data.allocations = groupStockWeightsBySector(point.weights).map(function(item) {
          return {
            asset_code: item.asset_code,
            asset_name: item.asset_name,
            weight: item.weight,
            risk_contribution: currentRiskMap[item.asset_code] || 0,
          };
        });
      }

      const copy = buildFrontierSelectionCopy(point, target, data.disclaimer);
      data.summary = copy.summary;
      data.explanation = copy.explanation;
      data.explanation_body = copy.explanation;
      return point;
    }

    function renderCombinationSelection(selection, sourceLabel) {
      if (!selection) {
        combinationPanelEl.hidden = true;
        combinationMetaEl.textContent = "";
        combinationMembersEl.innerHTML = "";
        return;
      }

      combinationPanelEl.hidden = false;
      combinationMetaEl.textContent = `${sourceLabel || "관리자 유니버스"} 기준으로 섹터별 후보군에서 대표 종목 1개씩을 선택해 최적화했습니다. 현재 적용된 유니버스 ID는 ${selection.combination_id} 입니다.`;
      combinationMembersEl.innerHTML = Object.entries(selection.members_by_sector || {})
        .map(([sectorCode, tickers]) => `<span class="combination-chip"><strong>${sectorCode}</strong>${(tickers || []).join(", ")}</span>`)
        .join("");
    }

    function buildTickerLookup() {
      const lookup = new Map();
      Object.entries(stocksBySector || {}).forEach(([sectorCode, items]) => {
        (items || []).forEach((item) => {
          lookup.set(item.ticker, {
            ticker: item.ticker,
            name: item.name || item.ticker,
            sector_code: item.sector_code || sectorCode,
            sector_name: item.sector_name || sectorCode,
          });
        });
      });

      const fallbackSelection = lastData?.selected_combination?.members_by_sector || {};
      Object.entries(fallbackSelection).forEach(([sectorCode, tickers]) => {
        (tickers || []).forEach((ticker) => {
          if (!lookup.has(ticker)) {
            lookup.set(ticker, {
              ticker,
              name: ticker,
              sector_code: sectorCode,
              sector_name: sectorCode,
            });
          }
        });
      });

      return lookup;
    }

    function groupStockWeightsBySector(stockWeights) {
      const lookup = buildTickerLookup();
      const allocationLookup = new Map((lastData?.allocations || []).map((item) => [item.asset_code, item.asset_name]));
      const grouped = new Map();

      Object.entries(stockWeights || {}).forEach(([ticker, weight]) => {
        const numericWeight = Number(weight || 0);
        if (numericWeight <= 0) return;

        const meta = lookup.get(ticker) || (
          allocationLookup.has(ticker)
            ? {
                ticker,
                name: allocationLookup.get(ticker) || ticker,
                sector_code: ticker,
                sector_name: allocationLookup.get(ticker) || ticker,
              }
            : {
                ticker,
                name: ticker,
                sector_code: "unknown",
                sector_name: "기타",
              }
        );
        const sectorCode = meta.sector_code || "unknown";
        const current = grouped.get(sectorCode) || {
          asset_code: sectorCode,
          asset_name: meta.sector_name || sectorCode,
          weight: 0,
          instruments: [],
        };
        current.weight += numericWeight;
        current.instruments.push({
          ticker,
          name: meta.name || ticker,
          weight: numericWeight,
        });
        grouped.set(sectorCode, current);
      });

      return Array.from(grouped.values())
        .map((item) => {
          item.instruments.sort((a, b) => b.weight - a.weight);
          return item;
        })
        .sort((a, b) => b.weight - a.weight);
    }

    function selectedStocksForSector(code) {
      const grouped = groupStockWeightsBySector(lastData?.selected_point?.weights || {});
      const sector = grouped.find((item) => item.asset_code === code);
      if (sector && sector.instruments?.length) {
        return sector.instruments;
      }

      const selection = lastData?.selected_combination?.members_by_sector || {};
      const selectedTickers = selection[code] || [];
      if (!selectedTickers.length) return [];

      const stockLookup = new Map((stocksBySector[code] || []).map((item) => [item.ticker, item]));
      return selectedTickers.map((ticker) => stockLookup.get(ticker) || { ticker, name: ticker, weight: 0 });
    }

    function buildDonutSVG(items, valueKey, centerText) {
      const size = 220;
      const cx = size / 2;
      const cy = size / 2;
      const outerR = 95;
      const innerR = 58;
      const total = items.reduce((s, it) => s + (it[valueKey] || 0), 0) || 1;

      let cumulativeAngle = -Math.PI / 2;
      let paths = "";

      items.forEach((item) => {
        const fraction = (item[valueKey] || 0) / total;
        if (fraction <= 0) return;
        const angle = fraction * 2 * Math.PI;
        const startAngle = cumulativeAngle;
        const endAngle = cumulativeAngle + angle;

        const x1 = cx + outerR * Math.cos(startAngle);
        const y1 = cy + outerR * Math.sin(startAngle);
        const x2 = cx + outerR * Math.cos(endAngle);
        const y2 = cy + outerR * Math.sin(endAngle);
        const x3 = cx + innerR * Math.cos(endAngle);
        const y3 = cy + innerR * Math.sin(endAngle);
        const x4 = cx + innerR * Math.cos(startAngle);
        const y4 = cy + innerR * Math.sin(startAngle);

        const largeArc = angle > Math.PI ? 1 : 0;
        const color = ASSET_COLORS[item.asset_code] || "#64748B";

        const pctLabel = (fraction * 100).toFixed(1) + "%";
        paths += '<path class="donut-slice"';
        paths += ' data-code="' + item.asset_code + '"';
        paths += ' data-name="' + (item.asset_name || item.asset_code) + '"';
        paths += ' data-value="' + pctLabel + '"';
        paths += ' data-color="' + color + '"';
        paths += ' d="';
        paths += "M " + x1.toFixed(2) + " " + y1.toFixed(2) + " ";
        paths += "A " + outerR + " " + outerR + " 0 " + largeArc + " 1 " + x2.toFixed(2) + " " + y2.toFixed(2) + " ";
        paths += "L " + x3.toFixed(2) + " " + y3.toFixed(2) + " ";
        paths += "A " + innerR + " " + innerR + " 0 " + largeArc + " 0 " + x4.toFixed(2) + " " + y4.toFixed(2) + " ";
        paths += 'Z" fill="' + color + '" />';

        cumulativeAngle = endAngle;
      });

      return '<svg viewBox="0 0 ' + size + " " + size + '" xmlns="http://www.w3.org/2000/svg">' + paths + "</svg>";
    }

    function buildLegendHTML(items, valueKey) {
      return items.map((item) => {
        const val = ((item[valueKey] || 0) * 100).toFixed(1);
        const color = ASSET_COLORS[item.asset_code] || "#64748B";
        return '<span class="donut-legend-item">' +
          '<span class="donut-legend-dot" style="background:' + color + '"></span>' +
          '<span class="donut-legend-name">' + item.asset_name + '</span>' +
          '<span class="donut-legend-value">' + val + '%</span>' +
        '</span>';
      }).join("");
    }

    function renderAllocations(items) {
      const filtered = items.filter((it) => it.weight > 0 || it.risk_contribution > 0);
      lastAllocFiltered = filtered;

      // ── Pie view ──
      const weightSVG = buildDonutSVG(filtered, "weight", "비중");
      const riskSVG = buildDonutSVG(filtered, "risk_contribution", "리스크");

      const topWeight = filtered.reduce((max, it) => it.weight > max.weight ? it : max, filtered[0] || { asset_name: "-", weight: 0 });
      const topRisk = filtered.reduce((max, it) => it.risk_contribution > max.risk_contribution ? it : max, filtered[0] || { asset_name: "-", risk_contribution: 0 });

      allocPieEl.innerHTML =
        '<div class="donut-section">' +
          '<div class="donut-label">자산 비중</div>' +
          '<div class="donut-container">' +
            weightSVG +
            '<div class="donut-center">' +
              '<div class="donut-center-value">' + ((topWeight.weight || 0) * 100).toFixed(0) + '%</div>' +
              '<div class="donut-center-label">' + (topWeight.asset_name || "") + '</div>' +
            '</div>' +
          '</div>' +
          '<div class="donut-legend">' + buildLegendHTML(filtered, "weight") + '</div>' +
        '</div>' +
        '<div class="donut-section">' +
          '<div class="donut-label">리스크 기여도</div>' +
          '<div class="donut-container">' +
            riskSVG +
            '<div class="donut-center">' +
              '<div class="donut-center-value">' + ((topRisk.risk_contribution || 0) * 100).toFixed(0) + '%</div>' +
              '<div class="donut-center-label">' + (topRisk.asset_name || "") + '</div>' +
            '</div>' +
          '</div>' +
          '<div class="donut-legend">' + buildLegendHTML(filtered, "risk_contribution") + '</div>' +
        '</div>';

      // ── List view ──
      renderAllocList(filtered);
    }

    function renderAllocList(filtered) {
      const maxW = Math.max(...filtered.map(it => it.weight || 0)) || 1;

      let rows = filtered.map(function(item) {
        const color = ASSET_COLORS[item.asset_code] || "#64748B";
        const w = ((item.weight || 0) * 100).toFixed(1);
        const r = ((item.risk_contribution || 0) * 100).toFixed(1);
        const barPct = ((item.weight || 0) / maxW * 100).toFixed(0);
        const code = item.asset_code;

        // Get child stocks for this sector
        const stocks = selectedStocksForSector(code);
        const hasChildren = stocks.length > 0;
        const chevronSVG = '<svg class="alloc-table-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>';

        // Parent row
        let html = '<tr class="alloc-parent-row" data-sector="' + code + '">' +
          '<td><div class="alloc-table-asset">' +
            (hasChildren
              ? '<span class="alloc-table-toggle" data-sector="' + code + '">' + chevronSVG + '</span>'
              : '<span style="width:14px;display:inline-block"></span>') +
            '<span class="alloc-table-dot" style="background:' + color + '"></span>' +
            '<span class="alloc-table-name">' + (item.asset_name || code) + '</span>' +
          '</div></td>' +
          '<td>' + w + '%</td>' +
          '<td class="alloc-table-bar-cell"><div class="alloc-table-bar" style="width:' + barPct + '%;background:' + color + '"></div></td>' +
          '<td>' + r + '%</td>' +
        '</tr>';

        // Child rows (hidden by default)
        if (hasChildren) {
          stocks.forEach(function(s) {
            const sw = ((s.weight || 0) * 100).toFixed(1);
            html += '<tr class="alloc-child-row alloc-children-hidden" data-parent="' + code + '">' +
              '<td><span class="alloc-child-ticker">' + s.ticker + '</span><span class="alloc-child-name">' + s.name + '</span></td>' +
              '<td>' + sw + '%</td>' +
              '<td></td>' +
              '<td></td>' +
            '</tr>';
          });
        }

        return html;
      }).join("");

      allocListEl.innerHTML =
        '<table class="alloc-table">' +
          '<colgroup><col class="col-asset"><col class="col-weight"><col class="col-bar"><col class="col-risk"></colgroup>' +
          '<thead><tr>' +
            '<th>자산군</th>' +
            '<th>비중</th>' +
            '<th></th>' +
            '<th>리스크 기여도</th>' +
          '</tr></thead>' +
          '<tbody>' + rows + '</tbody>' +
        '</table>';

      // Wire up toggle clicks
      allocListEl.querySelectorAll(".alloc-table-toggle").forEach(function(toggle) {
        toggle.addEventListener("click", function() {
          const sector = toggle.dataset.sector;
          const isExpanded = toggle.classList.toggle("expanded");
          allocListEl.querySelectorAll('.alloc-child-row[data-parent="' + sector + '"]').forEach(function(row) {
            row.classList.toggle("alloc-children-hidden", !isExpanded);
          });
        });
      });
    }

    function buildMiniDonutSVG(items, valueKey) {
      const size = 120;
      const cx = size / 2;
      const cy = size / 2;
      const outerR = 52;
      const innerR = 32;
      const total = items.reduce((s, it) => s + (it[valueKey] || 0), 0) || 1;
      let cumulativeAngle = -Math.PI / 2;
      let paths = "";
      items.forEach((item) => {
        const fraction = (item[valueKey] || 0) / total;
        if (fraction <= 0) return;
        const angle = fraction * 2 * Math.PI;
        const startAngle = cumulativeAngle;
        const endAngle = cumulativeAngle + angle;
        const x1 = cx + outerR * Math.cos(startAngle);
        const y1 = cy + outerR * Math.sin(startAngle);
        const x2 = cx + outerR * Math.cos(endAngle);
        const y2 = cy + outerR * Math.sin(endAngle);
        const x3 = cx + innerR * Math.cos(endAngle);
        const y3 = cy + innerR * Math.sin(endAngle);
        const x4 = cx + innerR * Math.cos(startAngle);
        const y4 = cy + innerR * Math.sin(startAngle);
        const largeArc = angle > Math.PI ? 1 : 0;
        const color = ASSET_COLORS[item.asset_code] || "#64748B";
        paths += '<path d="M ' + x1.toFixed(2) + " " + y1.toFixed(2) +
          " A " + outerR + " " + outerR + " 0 " + largeArc + " 1 " + x2.toFixed(2) + " " + y2.toFixed(2) +
          " L " + x3.toFixed(2) + " " + y3.toFixed(2) +
          " A " + innerR + " " + innerR + " 0 " + largeArc + " 0 " + x4.toFixed(2) + " " + y4.toFixed(2) +
          'Z" fill="' + color + '" />';
        cumulativeAngle = endAngle;
      });
      return '<svg class="option-chart-svg" viewBox="0 0 ' + size + " " + size + '">' + paths + "</svg>";
    }

    const optionDotColors = { "안정형": "#22c55e", "균형형": "#3b82f6", "성장형": "#a855f7" };

    function renderOptions(items, selectedPoint) {
      // Find closest option to selected point
      let closestIdx = -1;
      let closestDist = Infinity;
      items.forEach((item, i) => {
        const dist = Math.abs(item.expected_return - selectedPoint.expected_return);
        if (dist < closestDist) { closestDist = dist; closestIdx = i; }
      });
      const cards = items.map((item, i) => {
        const active = i === closestIdx ? " active" : "";
        const grouped = groupStockWeightsBySector(item.weights || {});
        const dotColor = optionDotColors[item.label] || "#64748b";
        const donutSvg = buildMiniDonutSVG(grouped, "weight");
        const legendHtml = grouped.map((g) => {
          const pct = ((g.weight || 0) * 100).toFixed(1);
          const color = ASSET_COLORS[g.asset_code] || "#64748B";
          return '<div class="option-chart-legend-item">' +
            '<span class="option-chart-legend-dot" style="background:' + color + '"></span>' +
            '<span class="option-chart-legend-name">' + g.asset_name + '</span>' +
            '<span class="option-chart-legend-val">' + pct + '%</span>' +
            '</div>';
        }).join("");
        return '<div class="option-chart-card' + active + '" style="--opt-color:' + dotColor + '">' +
          '<div class="option-chart-label"><span class="opt-dot" style="background:' + dotColor + '"></span>' + (item.label || "옵션") + '</div>' +
          donutSvg +
          '<div class="option-chart-stats">변동성 ' + percent(item.volatility) + ' · 수익률 ' + percent(item.expected_return) + '</div>' +
          '<div class="option-chart-legend">' + legendHtml + '</div>' +
          '</div>';
      }).join("");
      optionsEl.innerHTML = '<div class="option-charts">' + cards + '</div>';
    }

    function getThemeColors() {
      const style = getComputedStyle(document.documentElement);
      return {
        bg: style.getPropertyValue("--chart-bg").trim(),
        grid: style.getPropertyValue("--chart-grid").trim(),
        label: style.getPropertyValue("--chart-label").trim(),
        line: style.getPropertyValue("--chart-line").trim(),
        guide: style.getPropertyValue("--chart-guide").trim(),
        scatter: style.getPropertyValue("--chart-scatter").trim(),
        text: style.getPropertyValue("--chart-text").trim(),
        selected: style.getPropertyValue("--chart-selected").trim(),
      };
    }

    function renderChart(data) {
      const frontier = data.frontier_points || data.frontier || [];
      const randomPortfolios = data.random_portfolios || [];
      const selectedPoint = data.selected_point;

      if (!frontier.length || !selectedPoint) {
        chartEl.innerHTML = "";
        return;
      }

      const c = getThemeColors();
      const margin = { top: 20, right: 24, bottom: 46, left: 60 };
      const width = 900;
      const height = 860;
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;
      chartEl.setAttribute("viewBox", `0 0 ${width} ${height}`);

      function guideReturnAt(volatility) {
        if (frontier.length < 2) return -Infinity;
        const firstFrontier = frontier[0];
        const lastFrontier = frontier[frontier.length - 1];
        const dx = lastFrontier.volatility - firstFrontier.volatility;
        if (Math.abs(dx) < 1e-9) return Math.min(firstFrontier.expected_return, lastFrontier.expected_return);
        const slope = (lastFrontier.expected_return - firstFrontier.expected_return) / dx;
        return firstFrontier.expected_return + slope * (volatility - firstFrontier.volatility);
      }

      const visibleRandomPortfolios = randomPortfolios.filter((point) => point.expected_return >= guideReturnAt(point.volatility) - 1e-9);

      const individualAssets = data.individual_assets || [];
      const frontierExtents = frontier.length
        ? [frontier[0], frontier[frontier.length - 1]]
        : [];
      const visiblePoints = visibleRandomPortfolios.length
        ? visibleRandomPortfolios.concat(frontierExtents, [selectedPoint]).concat(individualAssets)
        : frontier.concat([selectedPoint]).concat(individualAssets);
      const volMin = Math.min(...visiblePoints.map((p) => p.volatility)) * 0.9;
      const volMax = Math.max(...visiblePoints.map((p) => p.volatility)) * 1.1;
      const retMin = Math.min(...visiblePoints.map((p) => p.expected_return)) * 0.9;
      const retMax = Math.max(...visiblePoints.map((p) => p.expected_return)) * 1.1;

      function xScale(value) {
        return margin.left + ((value - volMin) / (volMax - volMin || 1)) * innerWidth;
      }

      function yScale(value) {
        return margin.top + innerHeight - ((value - retMin) / (retMax - retMin || 1)) * innerHeight;
      }

      let svg = "";

      svg += `<defs><clipPath id="chart-clip"><rect x="${margin.left}" y="${margin.top}" width="${innerWidth}" height="${innerHeight}" rx="6" /></clipPath></defs>`;
      svg += `<rect x="${margin.left}" y="${margin.top}" width="${innerWidth}" height="${innerHeight}" fill="${c.bg}" rx="6" />`;

      for (let i = 0; i <= 5; i++) {
        const val = volMin + ((volMax - volMin) * i) / 5;
        const x = xScale(val);
        svg += `<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${margin.top + innerHeight}" stroke="${c.grid}" stroke-dasharray="4,4" />`;
        svg += `<text x="${x}" y="${height - 14}" fill="${c.label}" font-size="11" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="middle">${(val * 100).toFixed(1)}%</text>`;
      }

      for (let j = 0; j <= 5; j++) {
        const val = retMin + ((retMax - retMin) * j) / 5;
        const y = yScale(val);
        svg += `<line x1="${margin.left}" y1="${y}" x2="${margin.left + innerWidth}" y2="${y}" stroke="${c.grid}" stroke-dasharray="4,4" />`;
        svg += `<text x="18" y="${y + 4}" fill="${c.label}" font-size="11" font-family="Inter, Noto Sans KR, sans-serif">${(val * 100).toFixed(1)}%</text>`;
      }

      function weightsToAllocJSON(weights) {
        if (!weights) return "";
        const arr = groupStockWeightsBySector(weights)
          .map((item) => ({ name: item.asset_name, code: item.asset_code, weight: item.weight }));
        return JSON.stringify(arr).replace(/"/g, '&quot;');
      }

      // Build allocation JSON for the selected portfolio
      const selectedAllocJSON = weightsToAllocJSON(selectedPoint.weights || {});

      svg += `<g clip-path="url(#chart-clip)">`;

      // Random portfolio scatter points with hover hit areas
      visibleRandomPortfolios.forEach((point) => {
        const px = xScale(point.volatility);
        const py = yScale(point.expected_return);
        const allocAttr = point.weights ? ' data-alloc="' + weightsToAllocJSON(point.weights) + '"' : '';
        svg += `<circle cx="${px}" cy="${py}" r="3" fill="${c.scatter}" />`;
        svg += `<circle class="scatter-point" cx="${px}" cy="${py}" r="8" fill="transparent" data-vol="${(point.volatility * 100).toFixed(1)}" data-ret="${(point.expected_return * 100).toFixed(1)}"${allocAttr} />`;
      });

      // Individual asset points (100% single-asset portfolios)
      individualAssets.forEach((asset) => {
        const ax = xScale(asset.volatility);
        const ay = yScale(asset.expected_return);
        const assetColor = ASSET_COLORS[asset.code] || "#64748B";
        const singleAllocJSON = JSON.stringify([{name: asset.name, code: asset.code, weight: 1}]).replace(/"/g, '&quot;');
        svg += `<circle cx="${ax}" cy="${ay}" r="10" fill="${assetColor}" fill-opacity="0.15" />`;
        svg += `<circle class="scatter-point" cx="${ax}" cy="${ay}" r="10" fill="transparent" data-vol="${(asset.volatility * 100).toFixed(1)}" data-ret="${(asset.expected_return * 100).toFixed(1)}" data-alloc="${singleAllocJSON}" data-label="${asset.name}" />`;
        svg += `<circle cx="${ax}" cy="${ay}" r="4.5" fill="${assetColor}" stroke="${c.bg}" stroke-width="1.5" pointer-events="none" />`;
        svg += `<text x="${ax}" y="${ay - 12}" text-anchor="middle" fill="${c.label}" font-size="9" font-family="Inter, Noto Sans KR, sans-serif" pointer-events="none">${asset.name}</text>`;
      });

      if (frontier.length >= 2) {
        const firstFrontier = frontier[0];
        const lastFrontier = frontier[frontier.length - 1];
        svg += `<line x1="${xScale(firstFrontier.volatility)}" y1="${yScale(firstFrontier.expected_return)}" x2="${xScale(lastFrontier.volatility)}" y2="${yScale(lastFrontier.expected_return)}" stroke="${c.guide}" stroke-width="1.5" stroke-dasharray="8 6" stroke-linecap="round" />`;
      }

      const frontierPath = frontier.map((point, index) => `${index === 0 ? "M" : "L"} ${xScale(point.volatility)} ${yScale(point.expected_return)}`).join(" ");
      svg += `<path d="${frontierPath}" fill="none" stroke="${c.line}" stroke-width="2.5" stroke-linecap="round" />`;
      // Invisible wider path for hover hit area on frontier line
      svg += `<path class="frontier-hit" d="${frontierPath}" fill="none" stroke="transparent" stroke-width="16" stroke-linecap="round" />`;

      // Max Sharpe ratio portfolio (red glowing dot)
      const riskFreeRate = 0.02;
      let maxSharpe = -Infinity;
      let maxSharpePoint = null;
      frontier.forEach((point) => {
        const sharpe = point.volatility > 0 ? (point.expected_return - riskFreeRate) / point.volatility : 0;
        if (sharpe > maxSharpe) { maxSharpe = sharpe; maxSharpePoint = point; }
      });
      if (maxSharpePoint) {
        const sx = xScale(maxSharpePoint.volatility);
        const sy = yScale(maxSharpePoint.expected_return);
        const sharpeAllocJSON = weightsToAllocJSON(maxSharpePoint.weights || {});
        svg += `<circle id="sharpe-glow" cx="${sx}" cy="${sy}" r="12" fill="rgba(239, 68, 68, 0.18)" />`;
        svg += `<circle class="scatter-point" cx="${sx}" cy="${sy}" r="10" fill="transparent" data-vol="${(maxSharpePoint.volatility * 100).toFixed(1)}" data-ret="${(maxSharpePoint.expected_return * 100).toFixed(1)}" data-alloc="${sharpeAllocJSON}" data-label="최대 샤프 포트폴리오 (${maxSharpe.toFixed(2)})" data-role="max-sharpe" data-target-return="${maxSharpePoint.expected_return.toFixed(6)}" />`;
        svg += `<circle id="sharpe-dot" cx="${sx}" cy="${sy}" r="6" fill="#ef4444" stroke="${c.bg}" stroke-width="2.5" pointer-events="none" />`;
      }

      // Frontier option dots (안정형, 균형형, 성장형)
      const optionColors = { "안정형": "#22c55e", "균형형": "#3b82f6", "성장형": "#a855f7" };
      const frontierOptions = data.frontier_options || [];
      frontierOptions.forEach((opt) => {
        const ox = xScale(opt.volatility);
        const oy = yScale(opt.expected_return);
        const col = optionColors[opt.label] || "#64748b";
        const optAllocJSON = weightsToAllocJSON(opt.weights || {});
        svg += `<circle cx="${ox}" cy="${oy}" r="10" fill="${col}" fill-opacity="0.15" />`;
        svg += `<circle class="scatter-point" cx="${ox}" cy="${oy}" r="10" fill="transparent" data-vol="${(opt.volatility * 100).toFixed(1)}" data-ret="${(opt.expected_return * 100).toFixed(1)}" data-alloc="${optAllocJSON}" data-label="${opt.label}" data-target-return="${opt.expected_return.toFixed(6)}" />`;
        svg += `<circle cx="${ox}" cy="${oy}" r="5" fill="${col}" stroke="${c.bg}" stroke-width="2" pointer-events="none" />`;
      });

      const cx = xScale(selectedPoint.volatility);
      const cy = yScale(selectedPoint.expected_return);
      svg += `<circle id="sel-glow" cx="${cx}" cy="${cy}" r="12" fill="rgba(249, 115, 22, 0.15)" />`;
      svg += `<circle id="sel-hit" class="scatter-point" cx="${cx}" cy="${cy}" r="10" fill="transparent" data-vol="${(selectedPoint.volatility * 100).toFixed(1)}" data-ret="${(selectedPoint.expected_return * 100).toFixed(1)}" data-alloc="${selectedAllocJSON}" data-label="현재 포트폴리오" />`;
      svg += `<circle id="sel-dot" cx="${cx}" cy="${cy}" r="6" fill="${c.selected}" stroke="${c.bg}" stroke-width="2.5" pointer-events="none" />`;
      svg += `</g>`;
      svg += `<text x="${width / 2}" y="${height - 2}" text-anchor="middle" fill="${c.label}" font-size="12" font-family="Inter, Noto Sans KR, sans-serif">위험 (변동성)</text>`;
      svg += `<text x="14" y="${height / 2}" text-anchor="middle" fill="${c.label}" font-size="12" font-family="Inter, Noto Sans KR, sans-serif" transform="rotate(-90 14 ${height / 2})">예상 수익률</text>`;

      chartEl.innerHTML = svg;

      // Store scale functions for slider animation
      chartXScale = xScale;
      chartYScale = yScale;
      chartBounds = { volMin, volMax, retMin, retMax };
    }

    // Animate the selected portfolio dot to a new frontier point
    function animateSelectedDot(point, allocJSON) {
      if (!chartXScale || !chartYScale) return;
      const newCx = chartXScale(point.volatility);
      const newCy = chartYScale(point.expected_return);

      const glow = document.getElementById("sel-glow");
      const hit = document.getElementById("sel-hit");
      const dot = document.getElementById("sel-dot");
      if (!glow || !dot) return;

      glow.setAttribute("cx", newCx);
      glow.setAttribute("cy", newCy);
      hit.setAttribute("cx", newCx);
      hit.setAttribute("cy", newCy);
      hit.setAttribute("data-vol", (point.volatility * 100).toFixed(1));
      hit.setAttribute("data-ret", (point.expected_return * 100).toFixed(1));
      if (allocJSON) hit.setAttribute("data-alloc", allocJSON);
      dot.setAttribute("cx", newCx);
      dot.setAttribute("cy", newCy);
    }

    // Update UI from cached data when slider changes (no API call)
    function updateFromCache() {
      if (!lastData || !lastData.frontier_points || !lastData.frontier_points.length) return;
      const point = applyExpectedReturnSelection(lastData);
      if (!point) return;

      const expectedReturn = lastData.expected_return || point.expected_return;
      const volatility = lastData.volatility || point.volatility;
      const sharpeRatio = lastData.sharpe_ratio || (volatility > 0 ? (expectedReturn - FRONTIER_RISK_FREE_RATE) / volatility : 0);

      // Animate metrics
      const metricReturnEl = document.getElementById("metric-return");
      const metricVolEl = document.getElementById("metric-vol");
      const metricSharpeEl = document.getElementById("metric-sharpe");
      animateNumber(metricReturnEl, expectedReturn * 100, function(v) { return v.toFixed(1) + "%"; });
      animateNumber(metricVolEl, volatility * 100, function(v) { return v.toFixed(1) + "%"; });
      animateNumber(metricSharpeEl, sharpeRatio, function(v) { return v.toFixed(2); });

      const updatedSummary = document.getElementById("summary");
      const updatedExplanation = document.getElementById("explanation-body");
      if (updatedSummary) updatedSummary.textContent = [lastData.summary, lastData.disclaimer].filter(Boolean).join(" ");
      if (updatedExplanation) updatedExplanation.textContent = lastData.explanation || lastData.explanation_body || "";

      if (point.weights) {
        lastAllocations = lastData.allocations || [];
        const activeAllocEl = allocView === "pie" ? allocPieEl : allocListEl;
        crossfade(activeAllocEl, function() {
          renderAllocations(lastAllocations);
        });
      }

      // Update options highlight
      renderOptions(lastData.frontier_options || [], point);

      if (
        chartBounds
        && (
          point.volatility < chartBounds.volMin
          || point.volatility > chartBounds.volMax
          || point.expected_return < chartBounds.retMin
          || point.expected_return > chartBounds.retMax
        )
      ) {
        renderChart(lastData);
        return;
      }

      // Animate selected dot to new position (no full chart re-render)
      const allocArr = groupStockWeightsBySector(point.weights || {})
        .map((item) => ({ name: item.asset_name, code: item.asset_code, weight: item.weight }));
      const allocJSON = JSON.stringify(allocArr).replace(/"/g, '&quot;');
      animateSelectedDot(point, allocJSON);

      // Update volatility & return history with new weights
      if (point.weights) {
        if (typeof window.loadVolatilityHistory === "function") {
          window.loadVolatilityHistory(point.weights, lastData.data_source);
        }
        if (typeof window.loadReturnHistory === "function") {
          window.loadReturnHistory(point.weights, lastData.data_source);
        }
      }
    }

    let progressTimer = null;

    function startProgress() {
      const bar = chartLoadingEl.querySelector(".progress-indicator");
      bar.style.transition = "none";
      bar.style.width = "0%";
      void bar.offsetWidth; // force reflow
      let pct = 0;
      clearInterval(progressTimer);
      progressTimer = setInterval(function() {
        // Ease toward 90% — slows down as it approaches
        pct += (90 - pct) * 0.08;
        bar.style.transition = "width 0.3s ease-out";
        bar.style.width = pct + "%";
        if (pct >= 89) clearInterval(progressTimer);
      }, 100);
    }

    function finishProgress() {
      clearInterval(progressTimer);
      const bar = chartLoadingEl.querySelector(".progress-indicator");
      bar.style.transition = "width 0.25s ease-out";
      bar.style.width = "100%";
    }

    async function loadPortfolio() {
      statusEl.textContent = "계산 중...";
      chartLoadingEl.style.display = "";
      chartEl.style.display = "none";
      chartEl.classList.remove("chart-reveal");
      startProgress();

      try {
        const response = await fetch("/portfolio/simulate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payloadFromInputs()),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "요청 처리에 실패했습니다.");
        }
        finishProgress();

        lastData = data;
        applyExpectedReturnSelection(lastData);
        lastAllocations = lastData.allocations || [];

        const expectedReturn = lastData.expected_return ?? lastData.metrics?.expected_return ?? 0;
        const volatility = lastData.volatility ?? lastData.metrics?.volatility ?? 0;
        const sharpeRatio = lastData.sharpe_ratio ?? lastData.metrics?.sharpe_ratio ?? 0;
        const explanationTitle = lastData.explanation_title ?? lastData.explanation?.title ?? "왜 이런 포트폴리오가 나왔을까?";
        const explanationBody = lastData.explanation ?? lastData.explanation?.body ?? "";

        // Animate metric numbers
        const metricReturnEl = document.getElementById("metric-return");
        const metricVolEl = document.getElementById("metric-vol");
        const metricSharpeEl = document.getElementById("metric-sharpe");
        animateNumber(metricReturnEl, expectedReturn * 100, function(v) { return v.toFixed(1) + "%"; });
        animateNumber(metricVolEl, volatility * 100, function(v) { return v.toFixed(1) + "%"; });
        animateNumber(metricSharpeEl, sharpeRatio, function(v) { return v.toFixed(2); });

        // Crossfade text content
        crossfade(explanationBodyEl, function() {
          explanationTitleEl.textContent = explanationTitle;
          explanationBodyEl.textContent = explanationBody;
        });
        crossfade(summaryEl, function() {
          summaryEl.textContent = [lastData.summary, lastData.disclaimer].filter(Boolean).join(" ");
        });
        renderCombinationSelection(data.selected_combination, data.data_source_label);
        crossfade(optionsEl, function() {
          renderOptions(lastData.frontier_options || [], lastData.selected_point);
        });
        const activeAllocEl = allocView === "pie" ? allocPieEl : allocListEl;
        crossfade(activeAllocEl, function() {
          renderAllocations(lastData.allocations || []);
        });

        renderChart(lastData);
        // Load volatility & return history charts
        if (lastData.selected_point?.weights) {
          if (typeof window.loadVolatilityHistory === "function") {
            window.loadVolatilityHistory(lastData.selected_point.weights, lastData.data_source);
          }
          if (typeof window.loadReturnHistory === "function") {
            window.loadReturnHistory(lastData.selected_point.weights, lastData.data_source);
          }
        }
        // Brief pause to show 100%, then reveal chart with blur fade
        setTimeout(function() {
          chartLoadingEl.style.display = "none";
          chartEl.style.display = "block";
          chartEl.classList.add("chart-reveal");
          statusEl.textContent = "";
        }, 300);
      } catch (error) {
        finishProgress();
        setTimeout(function() {
          chartLoadingEl.style.display = "none";
          chartEl.style.display = "block";
          statusEl.textContent = error.message;
        }, 300);
      }
    }

    function updateSliderTrack() {
      const min = Number(slider.min || 0);
      const max = Number(slider.max || 100);
      const value = Number(slider.value || min);
      const pct = max > min ? ((value - min) / (max - min)) * 100 : 0;
      slider.style.setProperty("--slider-pct", pct + "%");
    }
    updateSliderTrack();

    slider.addEventListener("input", () => {
      updateSliderTrack();
      syncSliderDisplay(lastData && lastData.frontier_points ? lastData.frontier_points : null);
      clearTimeout(debounceTimer);
      // Use cached frontier if available, otherwise fetch the initial portfolio
      if (lastData && lastData.frontier_points) {
        debounceTimer = setTimeout(updateFromCache, 30);
      } else {
        debounceTimer = setTimeout(loadPortfolio, 150);
      }
    });

    // ── Allocation Tab Switcher ──
    (function() {
      const tabs = document.querySelectorAll(".alloc-tab");
      tabs.forEach(function(tab) {
        tab.addEventListener("click", function() {
          const view = tab.dataset.view;
          if (view === allocView) return;
          allocView = view;
          tabs.forEach(function(t) { t.classList.toggle("active", t.dataset.view === view); });
          if (view === "pie") {
            allocListEl.style.display = "none";
            allocPieEl.style.display = "";
          } else {
            allocPieEl.style.display = "none";
            allocListEl.style.display = "";
          }
        });
      });
    })();

    // ── Custom Select Component ──
    (function() {
      const selectRoot = document.getElementById("horizon-select");
      if (!selectRoot) return;
      const trigger = selectRoot.querySelector(".custom-select-trigger");
      const content = selectRoot.querySelector(".custom-select-content");
      const triggerText = selectRoot.querySelector(".custom-select-trigger-text");
      const items = selectRoot.querySelectorAll(".custom-select-item");
      let highlightedIndex = -1;

      function open() {
        trigger.setAttribute("data-state", "open");
        trigger.setAttribute("aria-expanded", "true");
        content.setAttribute("data-state", "open");
        // Highlight current selected item
        const selectedItem = content.querySelector("[data-selected]");
        items.forEach((item, i) => {
          item.removeAttribute("data-highlighted");
          if (item === selectedItem) highlightedIndex = i;
        });
        if (selectedItem) selectedItem.setAttribute("data-highlighted", "");
      }

      function close() {
        trigger.setAttribute("data-state", "closed");
        trigger.setAttribute("aria-expanded", "false");
        content.setAttribute("data-state", "closed");
        items.forEach(item => item.removeAttribute("data-highlighted"));
        highlightedIndex = -1;
      }

      function isOpen() {
        return trigger.getAttribute("data-state") === "open";
      }

      function selectItem(item) {
        items.forEach(i => i.removeAttribute("data-selected"));
        item.setAttribute("data-selected", "");
        triggerText.textContent = item.textContent;
        horizonEl.value = item.dataset.value;
        close();
        trigger.focus();
        loadPortfolio();
      }

      function highlightItem(index) {
        items.forEach(i => i.removeAttribute("data-highlighted"));
        if (index >= 0 && index < items.length) {
          highlightedIndex = index;
          items[index].setAttribute("data-highlighted", "");
        }
      }

      trigger.addEventListener("click", function(e) {
        e.preventDefault();
        if (isOpen()) close(); else open();
      });

      trigger.addEventListener("keydown", function(e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          if (isOpen()) {
            if (highlightedIndex >= 0) selectItem(items[highlightedIndex]);
            else close();
          } else {
            open();
          }
        } else if (e.key === "Escape") {
          close();
        } else if (e.key === "ArrowDown") {
          e.preventDefault();
          if (!isOpen()) { open(); return; }
          highlightItem(Math.min(highlightedIndex + 1, items.length - 1));
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          if (!isOpen()) { open(); return; }
          highlightItem(Math.max(highlightedIndex - 1, 0));
        }
      });

      items.forEach(function(item) {
        item.addEventListener("click", function(e) {
          e.preventDefault();
          selectItem(item);
        });
        item.addEventListener("mouseenter", function() {
          items.forEach(i => i.removeAttribute("data-highlighted"));
          item.setAttribute("data-highlighted", "");
          highlightedIndex = Array.from(items).indexOf(item);
        });
      });

      document.addEventListener("click", function(e) {
        if (!selectRoot.contains(e.target) && isOpen()) {
          close();
        }
      });
    })();

    document.getElementById("portfolio-form").addEventListener("submit", (event) => {
      event.preventDefault();
      loadPortfolio();
    });

    // ── Volatility History Chart ──
    (function() {
      const volChartEl = document.getElementById("vol-chart");
      const volEmptyEl = document.getElementById("vol-chart-empty");
      const volHoverInfo = document.getElementById("vol-hover-info");
      const volHoverDate = document.getElementById("vol-hover-date");
      const volHoverValue = document.getElementById("vol-hover-value");
      const volTimeBtns = document.querySelectorAll(".vol-time-btn");

      let volData = null;       // full points array from API
      let volRange = "1y";      // active time range
      let volCurrentWeights = null;

      function getThemeColorsVol() {
        const s = getComputedStyle(document.documentElement);
        return {
          bg: s.getPropertyValue("--chart-bg").trim() || "#F8FAFC",
          grid: s.getPropertyValue("--chart-grid").trim() || "#E2E8F0",
          label: s.getPropertyValue("--chart-label").trim() || "#94A3B8",
          line: s.getPropertyValue("--chart-line").trim() || "#0F172A",
          text: s.getPropertyValue("--chart-text").trim() || "#0F172A",
          muted: s.getPropertyValue("--muted-foreground").trim() || "#64748B",
          selected: s.getPropertyValue("--chart-selected").trim() || "#F97316",
          border: s.getPropertyValue("--border").trim() || "#E2E8F0",
        };
      }

      function rangeToDays(range) {
        switch (range) {
          case "1w": return 7;
          case "3m": return 90;
          case "1y": return 365;
          case "5y": return 365 * 5;
          case "all": return Infinity;
          default: return 365;
        }
      }

      function filterByRange(points, range) {
        if (!points || !points.length) return [];
        const days = rangeToDays(range);
        if (days === Infinity) return points;
        const lastDate = new Date(points[points.length - 1].date);
        const cutoff = new Date(lastDate);
        cutoff.setDate(cutoff.getDate() - days);
        return points.filter(function(p) { return new Date(p.date) >= cutoff; });
      }

      function renderVolChart(points) {
        if (!points || points.length < 2) {
          volChartEl.style.display = "none";
          volEmptyEl.style.display = "";
          volEmptyEl.textContent = volData ? "선택 기간에 데이터가 부족합니다." : "포트폴리오를 먼저 계산해주세요.";
          volHoverInfo.classList.remove("visible");
          return;
        }

        volEmptyEl.style.display = "none";
        volChartEl.style.display = "block";

        const c = getThemeColorsVol();
        const width = 900;
        const height = 280;
        const margin = { top: 48, right: 24, bottom: 36, left: 56 };
        const innerW = width - margin.left - margin.right;
        const innerH = height - margin.top - margin.bottom;

        const dates = points.map(function(p) { return new Date(p.date); });
        const vols = points.map(function(p) { return p.volatility; });
        const minDate = dates[0].getTime();
        const maxDate = dates[dates.length - 1].getTime();
        const dateSpan = maxDate - minDate || 1;
        const volMin = Math.max(0, Math.min(...vols) * 0.85);
        const volMax = Math.max(...vols) * 1.1;
        const volSpan = volMax - volMin || 0.01;

        function xScale(d) { return margin.left + ((d.getTime() - minDate) / dateSpan) * innerW; }
        function yScale(v) { return margin.top + innerH - ((v - volMin) / volSpan) * innerH; }

        let svg = "";

        // Background
        svg += '<rect x="' + margin.left + '" y="' + margin.top + '" width="' + innerW + '" height="' + innerH + '" fill="' + c.bg + '" rx="6" />';

        // Y-axis grid lines and labels
        const yTicks = 5;
        for (let i = 0; i <= yTicks; i++) {
          const val = volMin + (volSpan * i) / yTicks;
          const y = yScale(val);
          svg += '<line x1="' + margin.left + '" y1="' + y + '" x2="' + (margin.left + innerW) + '" y2="' + y + '" stroke="' + c.grid + '" stroke-dasharray="4,4" />';
          svg += '<text x="' + (margin.left - 8) + '" y="' + (y + 4) + '" fill="' + c.label + '" font-size="11" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="end">' + (val * 100).toFixed(1) + '%</text>';
        }

        // X-axis date labels
        const xTickCount = Math.min(6, points.length);
        for (let i = 0; i < xTickCount; i++) {
          const idx = Math.round((i / (xTickCount - 1)) * (points.length - 1));
          const d = dates[idx];
          const x = xScale(d);
          const label = d.getFullYear() + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + String(d.getDate()).padStart(2, "0");
          svg += '<text x="' + x + '" y="' + (height - 10) + '" fill="' + c.label + '" font-size="10" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="middle">' + label + '</text>';
        }

        // Clip path
        svg += '<defs><clipPath id="vol-clip"><rect x="' + margin.left + '" y="' + margin.top + '" width="' + innerW + '" height="' + innerH + '" /></clipPath></defs>';

        // Current portfolio volatility dotted horizontal line
        const currentVol = lastData ? (lastData.volatility || 0) : 0;
        if (currentVol > volMin && currentVol < volMax) {
          const refY = yScale(currentVol);
          svg += '<g clip-path="url(#vol-clip)">';
          svg += '<line x1="' + margin.left + '" y1="' + refY + '" x2="' + (margin.left + innerW) + '" y2="' + refY + '" stroke="' + c.selected + '" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.7" />';
          svg += '<text x="' + (margin.left + innerW - 4) + '" y="' + (refY - 6) + '" fill="' + c.selected + '" font-size="10" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="end" font-weight="600">현재 ' + (currentVol * 100).toFixed(1) + '%</text>';
          svg += '</g>';
        }

        // Area fill under the line
        svg += '<g clip-path="url(#vol-clip)">';
        let areaPath = "M" + xScale(dates[0]) + "," + (margin.top + innerH);
        for (let i = 0; i < points.length; i++) {
          areaPath += " L" + xScale(dates[i]) + "," + yScale(vols[i]);
        }
        areaPath += " L" + xScale(dates[dates.length - 1]) + "," + (margin.top + innerH) + " Z";
        svg += '<path d="' + areaPath + '" fill="' + c.line + '" opacity="0.06" />';

        // Volatility line
        let linePath = "M" + xScale(dates[0]) + "," + yScale(vols[0]);
        for (let i = 1; i < points.length; i++) {
          linePath += " L" + xScale(dates[i]) + "," + yScale(vols[i]);
        }
        svg += '<path d="' + linePath + '" fill="none" stroke="' + c.line + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />';

        // End dot (TODAY)
        const lastX = xScale(dates[dates.length - 1]);
        const lastY = yScale(vols[vols.length - 1]);
        svg += '<circle cx="' + lastX + '" cy="' + lastY + '" r="4" fill="' + c.line + '" />';
        svg += '<circle cx="' + lastX + '" cy="' + lastY + '" r="7" fill="' + c.line + '" opacity="0.15" />';
        svg += '</g>';

        // Invisible hit areas for hover
        svg += '<g clip-path="url(#vol-clip)">';
        for (let i = 0; i < points.length; i++) {
          const x = xScale(dates[i]);
          svg += '<line class="vol-hit" x1="' + x + '" y1="' + margin.top + '" x2="' + x + '" y2="' + (margin.top + innerH) + '" stroke="transparent" stroke-width="' + Math.max(2, innerW / points.length) + '" data-idx="' + i + '" />';
        }
        svg += '</g>';

        volChartEl.innerHTML = svg;

        // Hover crosshair handling
        const crosshairLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        crosshairLine.setAttribute("y1", margin.top);
        crosshairLine.setAttribute("y2", margin.top + innerH);
        crosshairLine.setAttribute("stroke", c.muted);
        crosshairLine.setAttribute("stroke-width", "1");
        crosshairLine.setAttribute("stroke-dasharray", "3,3");
        crosshairLine.setAttribute("pointer-events", "none");
        crosshairLine.style.display = "none";
        volChartEl.appendChild(crosshairLine);

        const crosshairDot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        crosshairDot.setAttribute("r", "5");
        crosshairDot.setAttribute("fill", c.line);
        crosshairDot.setAttribute("stroke", c.bg);
        crosshairDot.setAttribute("stroke-width", "2");
        crosshairDot.setAttribute("pointer-events", "none");
        crosshairDot.style.display = "none";
        volChartEl.appendChild(crosshairDot);

        volChartEl.addEventListener("mousemove", function(e) {
          const rect = volChartEl.getBoundingClientRect();
          const scaleX = width / rect.width;
          const mouseX = (e.clientX - rect.left) * scaleX;

          if (mouseX < margin.left || mouseX > margin.left + innerW) {
            crosshairLine.style.display = "none";
            crosshairDot.style.display = "none";
            volHoverInfo.classList.remove("visible");
            return;
          }

          // Find closest point
          let closest = 0;
          let closestDist = Infinity;
          for (let i = 0; i < points.length; i++) {
            const px = xScale(dates[i]);
            const dist = Math.abs(px - mouseX);
            if (dist < closestDist) {
              closestDist = dist;
              closest = i;
            }
          }

          const px = xScale(dates[closest]);
          const py = yScale(vols[closest]);
          crosshairLine.setAttribute("x1", px);
          crosshairLine.setAttribute("x2", px);
          crosshairLine.style.display = "";
          crosshairDot.setAttribute("cx", px);
          crosshairDot.setAttribute("cy", py);
          crosshairDot.style.display = "";

          const d = dates[closest];
          volHoverDate.textContent = d.getFullYear() + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + String(d.getDate()).padStart(2, "0");
          volHoverValue.textContent = (vols[closest] * 100).toFixed(1) + "%";
          volHoverInfo.classList.add("visible");
        });

        volChartEl.addEventListener("mouseleave", function() {
          crosshairLine.style.display = "none";
          crosshairDot.style.display = "none";
          volHoverInfo.classList.remove("visible");
        });
      }

      // Time range toggle buttons
      volTimeBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
          volTimeBtns.forEach(function(b) { b.classList.remove("active"); });
          btn.classList.add("active");
          volRange = btn.dataset.range;
          if (volData) {
            renderVolChart(filterByRange(volData, volRange));
          }
        });
      });

      // Fetch volatility data after portfolio simulation
      let volLastKey = "";
      window.loadVolatilityHistory = async function(weights, dataSource) {
        if (!weights || Object.keys(weights).length === 0) return;
        const key = JSON.stringify(weights);
        if (key === volLastKey) return; // skip if weights unchanged
        volLastKey = key;
        volCurrentWeights = weights;
        try {
          const res = await fetch("/portfolio/volatility-history", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ weights: weights, data_source: dataSource || "stock_combination_demo" }),
          });
          if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            volData = null;
            volChartEl.style.display = "none";
            volEmptyEl.style.display = "";
            volEmptyEl.textContent = err.detail || "변동성 데이터를 불러오지 못했습니다.";
            volHoverInfo.classList.remove("visible");
            return;
          }
          const data = await res.json();
          volData = data.points || [];
          renderVolChart(filterByRange(volData, volRange));
        } catch (_) {
          volData = null;
          renderVolChart(null);
        }
      };

      // Re-render on theme toggle
      window.rerenderVolChart = function() {
        if (volData) {
          renderVolChart(filterByRange(volData, volRange));
        }
      };
    })();

    // ── Return History Chart ──
    (function() {
      const retChartEl = document.getElementById("ret-chart");
      const retEmptyEl = document.getElementById("ret-chart-empty");
      const retHoverInfo = document.getElementById("ret-hover-info");
      const retHoverDate = document.getElementById("ret-hover-date");
      const retHoverValue = document.getElementById("ret-hover-value");
      const retTimeBtns = document.querySelectorAll(".ret-time-btn");

      let retData = null;
      let retRange = "1y";

      function getThemeColorsRet() {
        const s = getComputedStyle(document.documentElement);
        return {
          bg: s.getPropertyValue("--chart-bg").trim() || "#F8FAFC",
          grid: s.getPropertyValue("--chart-grid").trim() || "#E2E8F0",
          label: s.getPropertyValue("--chart-label").trim() || "#94A3B8",
          line: "#10b981",
          text: s.getPropertyValue("--chart-text").trim() || "#0F172A",
          muted: s.getPropertyValue("--muted-foreground").trim() || "#64748B",
          selected: s.getPropertyValue("--chart-selected").trim() || "#F97316",
          border: s.getPropertyValue("--border").trim() || "#E2E8F0",
        };
      }

      function rangeToDays(range) {
        switch (range) {
          case "1w": return 7;
          case "3m": return 90;
          case "1y": return 365;
          case "5y": return 365 * 5;
          case "all": return Infinity;
          default: return 365;
        }
      }

      function filterByRange(points, range) {
        if (!points || !points.length) return [];
        const days = rangeToDays(range);
        if (days === Infinity) return points;
        const lastDate = new Date(points[points.length - 1].date);
        const cutoff = new Date(lastDate);
        cutoff.setDate(cutoff.getDate() - days);
        return points.filter(function(p) { return new Date(p.date) >= cutoff; });
      }

      function renderRetChart(points) {
        if (!points || points.length < 2) {
          retChartEl.style.display = "none";
          retEmptyEl.style.display = "";
          retEmptyEl.textContent = retData ? "선택 기간에 데이터가 부족합니다." : "포트폴리오를 먼저 계산해주세요.";
          retHoverInfo.classList.remove("visible");
          return;
        }

        retEmptyEl.style.display = "none";
        retChartEl.style.display = "block";

        const c = getThemeColorsRet();
        const width = 900;
        const height = 280;
        const margin = { top: 48, right: 24, bottom: 36, left: 56 };
        const innerW = width - margin.left - margin.right;
        const innerH = height - margin.top - margin.bottom;

        const dates = points.map(function(p) { return new Date(p.date); });
        const rets = points.map(function(p) { return p.expected_return; });
        const minDate = dates[0].getTime();
        const maxDate = dates[dates.length - 1].getTime();
        const dateSpan = maxDate - minDate || 1;
        const retMin = Math.min(...rets) - Math.abs(Math.min(...rets)) * 0.15;
        const retMax = Math.max(...rets) + Math.abs(Math.max(...rets)) * 0.15;
        const retSpan = retMax - retMin || 0.01;

        function xScale(d) { return margin.left + ((d.getTime() - minDate) / dateSpan) * innerW; }
        function yScale(v) { return margin.top + innerH - ((v - retMin) / retSpan) * innerH; }

        let svg = "";

        // Background
        svg += '<rect x="' + margin.left + '" y="' + margin.top + '" width="' + innerW + '" height="' + innerH + '" fill="' + c.bg + '" rx="6" />';

        // Y-axis grid lines and labels
        const yTicks = 5;
        for (let i = 0; i <= yTicks; i++) {
          const val = retMin + (retSpan * i) / yTicks;
          const y = yScale(val);
          svg += '<line x1="' + margin.left + '" y1="' + y + '" x2="' + (margin.left + innerW) + '" y2="' + y + '" stroke="' + c.grid + '" stroke-dasharray="4,4" />';
          svg += '<text x="' + (margin.left - 8) + '" y="' + (y + 4) + '" fill="' + c.label + '" font-size="11" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="end">' + (val * 100).toFixed(1) + '%</text>';
        }

        // Zero line
        if (retMin < 0 && retMax > 0) {
          const zeroY = yScale(0);
          svg += '<line x1="' + margin.left + '" y1="' + zeroY + '" x2="' + (margin.left + innerW) + '" y2="' + zeroY + '" stroke="' + c.muted + '" stroke-width="1" opacity="0.5" />';
        }

        // X-axis date labels
        const xTickCount = Math.min(6, points.length);
        for (let i = 0; i < xTickCount; i++) {
          const idx = Math.round((i / (xTickCount - 1)) * (points.length - 1));
          const d = dates[idx];
          const x = xScale(d);
          const label = d.getFullYear() + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + String(d.getDate()).padStart(2, "0");
          svg += '<text x="' + x + '" y="' + (height - 10) + '" fill="' + c.label + '" font-size="10" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="middle">' + label + '</text>';
        }

        // Clip path
        svg += '<defs><clipPath id="ret-clip"><rect x="' + margin.left + '" y="' + margin.top + '" width="' + innerW + '" height="' + innerH + '" /></clipPath></defs>';

        // Current expected return dotted horizontal line
        const currentRet = lastData ? (lastData.expected_return || 0) : 0;
        if (currentRet > retMin && currentRet < retMax) {
          const refY = yScale(currentRet);
          svg += '<g clip-path="url(#ret-clip)">';
          svg += '<line x1="' + margin.left + '" y1="' + refY + '" x2="' + (margin.left + innerW) + '" y2="' + refY + '" stroke="' + c.selected + '" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.7" />';
          svg += '<text x="' + (margin.left + innerW - 4) + '" y="' + (refY - 6) + '" fill="' + c.selected + '" font-size="10" font-family="Inter, Noto Sans KR, sans-serif" text-anchor="end" font-weight="600">현재 ' + (currentRet * 100).toFixed(1) + '%</text>';
          svg += '</g>';
        }

        // Area fill under the line
        svg += '<g clip-path="url(#ret-clip)">';
        let areaPath = "M" + xScale(dates[0]) + "," + (margin.top + innerH);
        for (let i = 0; i < points.length; i++) {
          areaPath += " L" + xScale(dates[i]) + "," + yScale(rets[i]);
        }
        areaPath += " L" + xScale(dates[dates.length - 1]) + "," + (margin.top + innerH) + " Z";
        svg += '<path d="' + areaPath + '" fill="' + c.line + '" opacity="0.08" />';

        // Return line
        let linePath = "M" + xScale(dates[0]) + "," + yScale(rets[0]);
        for (let i = 1; i < points.length; i++) {
          linePath += " L" + xScale(dates[i]) + "," + yScale(rets[i]);
        }
        svg += '<path d="' + linePath + '" fill="none" stroke="' + c.line + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />';

        // End dot (TODAY)
        const lastX = xScale(dates[dates.length - 1]);
        const lastY = yScale(rets[rets.length - 1]);
        svg += '<circle cx="' + lastX + '" cy="' + lastY + '" r="4" fill="' + c.line + '" />';
        svg += '<circle cx="' + lastX + '" cy="' + lastY + '" r="7" fill="' + c.line + '" opacity="0.15" />';
        svg += '</g>';

        // Invisible hit areas for hover
        svg += '<g clip-path="url(#ret-clip)">';
        for (let i = 0; i < points.length; i++) {
          const x = xScale(dates[i]);
          svg += '<line class="ret-hit" x1="' + x + '" y1="' + margin.top + '" x2="' + x + '" y2="' + (margin.top + innerH) + '" stroke="transparent" stroke-width="' + Math.max(2, innerW / points.length) + '" data-idx="' + i + '" />';
        }
        svg += '</g>';

        retChartEl.innerHTML = svg;

        // Hover crosshair
        const crosshairLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        crosshairLine.setAttribute("y1", margin.top);
        crosshairLine.setAttribute("y2", margin.top + innerH);
        crosshairLine.setAttribute("stroke", c.muted);
        crosshairLine.setAttribute("stroke-width", "1");
        crosshairLine.setAttribute("stroke-dasharray", "3,3");
        crosshairLine.setAttribute("pointer-events", "none");
        crosshairLine.style.display = "none";
        retChartEl.appendChild(crosshairLine);

        const crosshairDot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        crosshairDot.setAttribute("r", "5");
        crosshairDot.setAttribute("fill", c.line);
        crosshairDot.setAttribute("stroke", c.bg);
        crosshairDot.setAttribute("stroke-width", "2");
        crosshairDot.setAttribute("pointer-events", "none");
        crosshairDot.style.display = "none";
        retChartEl.appendChild(crosshairDot);

        retChartEl.addEventListener("mousemove", function(e) {
          const rect = retChartEl.getBoundingClientRect();
          const scaleX = width / rect.width;
          const mouseX = (e.clientX - rect.left) * scaleX;

          if (mouseX < margin.left || mouseX > margin.left + innerW) {
            crosshairLine.style.display = "none";
            crosshairDot.style.display = "none";
            retHoverInfo.classList.remove("visible");
            return;
          }

          let closest = 0;
          let closestDist = Infinity;
          for (let i = 0; i < points.length; i++) {
            const px = xScale(dates[i]);
            const dist = Math.abs(px - mouseX);
            if (dist < closestDist) { closestDist = dist; closest = i; }
          }

          const px = xScale(dates[closest]);
          const py = yScale(rets[closest]);
          crosshairLine.setAttribute("x1", px);
          crosshairLine.setAttribute("x2", px);
          crosshairLine.style.display = "";
          crosshairDot.setAttribute("cx", px);
          crosshairDot.setAttribute("cy", py);
          crosshairDot.style.display = "";

          const d = dates[closest];
          retHoverDate.textContent = d.getFullYear() + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + String(d.getDate()).padStart(2, "0");
          retHoverValue.textContent = (rets[closest] * 100).toFixed(1) + "%";
          retHoverInfo.classList.add("visible");
        });

        retChartEl.addEventListener("mouseleave", function() {
          crosshairLine.style.display = "none";
          crosshairDot.style.display = "none";
          retHoverInfo.classList.remove("visible");
        });
      }

      // Time range toggle buttons
      retTimeBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
          retTimeBtns.forEach(function(b) { b.classList.remove("active"); });
          btn.classList.add("active");
          retRange = btn.dataset.range;
          if (retData) {
            renderRetChart(filterByRange(retData, retRange));
          }
        });
      });

      // Fetch return data after portfolio simulation
      let retLastKey = "";
      window.loadReturnHistory = async function(weights, dataSource) {
        if (!weights || Object.keys(weights).length === 0) return;
        const key = JSON.stringify(weights);
        if (key === retLastKey) return;
        retLastKey = key;
        try {
          const res = await fetch("/portfolio/return-history", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ weights: weights, data_source: dataSource || "stock_combination_demo" }),
          });
          if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            retData = null;
            retChartEl.style.display = "none";
            retEmptyEl.style.display = "";
            retEmptyEl.textContent = err.detail || "기대수익률 데이터를 불러오지 못했습니다.";
            retHoverInfo.classList.remove("visible");
            return;
          }
          const data = await res.json();
          retData = data.points || [];
          renderRetChart(filterByRange(retData, retRange));
        } catch (_) {
          retData = null;
          renderRetChart(null);
        }
      };

      window.rerenderRetChart = function() {
        if (retData) {
          renderRetChart(filterByRange(retData, retRange));
        }
      };
    })();

    // ── History Chart Mode Toggle (Vol / Return) ──
    (function() {
      const modeTabs = document.querySelectorAll(".history-mode-tab");
      const volPanel = document.getElementById("vol-panel");
      const retPanel = document.getElementById("ret-panel");
      const volToggles = document.getElementById("vol-time-toggles");
      const retToggles = document.getElementById("ret-time-toggles");
      const titleEl = document.getElementById("history-chart-title");
      const descEl = document.getElementById("history-chart-desc");

      modeTabs.forEach(function(tab) {
        tab.addEventListener("click", function() {
          modeTabs.forEach(function(t) { t.classList.remove("active"); });
          tab.classList.add("active");
          const mode = tab.dataset.mode;
          if (mode === "vol") {
            volPanel.style.display = "";
            retPanel.style.display = "none";
            volToggles.style.display = "";
            retToggles.style.display = "none";
            titleEl.textContent = "포트폴리오 변동성 추이";
            descEl.textContent = "선택된 포트폴리오의 과거 실현 변동성 (20일 롤링, 연율화) 추이입니다.";
          } else {
            volPanel.style.display = "none";
            retPanel.style.display = "";
            volToggles.style.display = "none";
            retToggles.style.display = "";
            titleEl.textContent = "포트폴리오 기대수익률 추이";
            descEl.textContent = "선택된 포트폴리오의 과거 실현 수익률 (20일 롤링, 연율화) 추이입니다.";
          }
        });
      });
    })();

    (function() {
      const toggle = document.getElementById("theme-toggle");
      const html = document.documentElement;

      function rerenderChart() {
        if (lastData) {
          setTimeout(() => renderChart(lastData), 50);
        }
        if (typeof window.rerenderVolChart === "function") {
          setTimeout(window.rerenderVolChart, 60);
        }
        if (typeof window.rerenderRetChart === "function") {
          setTimeout(window.rerenderRetChart, 70);
        }
      }

      const saved = localStorage.getItem("theme");
      if (saved === "dark" || (!saved && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        html.classList.add("dark");
      }

      toggle.addEventListener("click", () => {
        const isDark = html.classList.toggle("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        rerenderChart();
      });
    })();

    // ── Donut Tooltip ──
    (function() {
      const tip = document.getElementById("donut-tooltip");

      function buildDonutTooltipHTML(slice) {
        const color = slice.dataset.color;
        const name = slice.dataset.name;
        const value = slice.dataset.value;
        const code = slice.dataset.code;

        let html = '<div class="donut-tooltip-header">';
        html += '<span class="donut-tooltip-dot" style="background:' + color + '"></span>';
        html += '<span class="donut-tooltip-name">' + name + '</span>';
        html += '<span class="donut-tooltip-value">' + value + '</span>';
        html += '</div>';

        const stocks = selectedStocksForSector(code);
        if (stocks && stocks.length > 0) {
          html += '<div class="donut-tooltip-stocks">';
          stocks.forEach(function(s) {
            const stockPct = ((s.weight || 0) * 100).toFixed(1);
            html += '<div class="donut-tooltip-stock">';
            html += '<span class="donut-tooltip-stock-ticker">' + s.ticker + '</span>';
            html += '<span>' + s.name + '</span>';
            html += '<span class="donut-tooltip-stock-pct">' + stockPct + '%</span>';
            html += '</div>';
          });
          html += '</div>';
        }

        return html;
      }

      document.addEventListener("mouseover", function(e) {
        const slice = e.target.closest(".donut-slice");
        if (!slice) return;
        tip.innerHTML = buildDonutTooltipHTML(slice);
        tip.classList.add("visible");
      });

      document.addEventListener("mousemove", function(e) {
        if (!tip.classList.contains("visible")) return;
        const offsetX = 14;
        const offsetY = 14;
        let x = e.clientX + offsetX;
        let y = e.clientY + offsetY;
        const rect = tip.getBoundingClientRect();
        if (x + rect.width > window.innerWidth - 8) x = e.clientX - rect.width - offsetX;
        if (y + rect.height > window.innerHeight - 8) y = e.clientY - rect.height - offsetY;
        tip.style.left = x + "px";
        tip.style.top = y + "px";
      });

      document.addEventListener("mouseout", function(e) {
        const slice = e.target.closest(".donut-slice");
        if (!slice) return;
        tip.classList.remove("visible");
      });
    })();

    // ── Chart (Frontier) Tooltip ──
    (function() {
      const tip = document.getElementById("chart-tooltip");

      function buildChartTooltipHTML(vol, ret, allocData, label) {
        let html = '<div class="chart-tooltip-header">';
        html += '<span>' + (label || '포트폴리오') + '</span>';
        html += '</div>';
        html += '<div class="chart-tooltip-row"><span class="chart-tooltip-row-name">수익률</span><span class="chart-tooltip-row-value">' + ret + '%</span></div>';
        html += '<div class="chart-tooltip-row"><span class="chart-tooltip-row-name">변동성</span><span class="chart-tooltip-row-value">' + vol + '%</span></div>';
        if (allocData && allocData.length > 0) {
          html += '<div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--muted-foreground)">';
          allocData.forEach(function(a) {
            var color = ASSET_COLORS[a.code] || "#64748B";
            var pct = (a.weight * 100).toFixed(1);
            html += '<div class="chart-tooltip-row">';
            html += '<span class="chart-tooltip-row-dot" style="background:' + color + '"></span>';
            html += '<span class="chart-tooltip-row-name">' + a.name + '</span>';
            html += '<span class="chart-tooltip-row-value">' + pct + '%</span>';
            html += '</div>';
          });
          html += '</div>';
        }
        return html;
      }

      function positionTip(e) {
        var ox = 16, oy = 16;
        var x = e.clientX + ox;
        var y = e.clientY + oy;
        var rect = tip.getBoundingClientRect();
        if (x + rect.width > window.innerWidth - 8) x = e.clientX - rect.width - ox;
        if (y + rect.height > window.innerHeight - 8) y = e.clientY - rect.height - oy;
        tip.style.left = x + "px";
        tip.style.top = y + "px";
      }

      document.addEventListener("mouseover", function(e) {
        var pt = e.target.closest(".scatter-point");
        if (!pt) return;
        var vol = pt.dataset.vol;
        var ret = pt.dataset.ret;
        var label = pt.dataset.label || null;
        var allocData = null;
        try { allocData = JSON.parse(pt.dataset.alloc || "null"); } catch(ex) {}
        // For points without allocation data, use the global allocations if it's the selected point
        if (!allocData && label) {
          allocData = lastAllocations.filter(function(a) { return a.weight > 0; }).map(function(a) {
            return { name: a.asset_name, code: a.asset_code, weight: a.weight };
          });
        }
        tip.innerHTML = buildChartTooltipHTML(vol, ret, allocData, label);
        tip.classList.add("visible");
        positionTip(e);
      });

      document.addEventListener("mousemove", function(e) {
        if (!tip.classList.contains("visible")) return;
        positionTip(e);
      });

      document.addEventListener("mouseout", function(e) {
        var pt = e.target.closest(".scatter-point");
        if (!pt) return;
        tip.classList.remove("visible");
      });

      document.addEventListener("click", function(e) {
        const pt = e.target.closest('.scatter-point[data-target-return]');
        if (!pt) return;
        const targetReturn = Number(pt.dataset.targetReturn || "NaN");
        if (!Number.isFinite(targetReturn)) return;
        setSliderTargetExpectedReturn(targetReturn, { updateFromCache: true });
      });
    })();

    syncSliderDisplay(null);
    loadPortfolio();
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)

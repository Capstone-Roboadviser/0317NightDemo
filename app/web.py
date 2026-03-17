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

    select,
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

    select:focus,
    input[type="number"]:focus {
      border-color: var(--ring);
      box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.2);
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
      border-radius: 3px;
      background: var(--border);
      outline: none;
      cursor: pointer;
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--primary);
      border: 2px solid var(--background);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
      cursor: pointer;
    }

    input[type="range"]::-moz-range-thumb {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--primary);
      border: 2px solid var(--background);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
      cursor: pointer;
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

    .alloc-table {
      width: 100%;
      border-collapse: collapse;
    }

    .alloc-table thead th {
      text-align: left;
      padding: 10px 16px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted-foreground);
      border-bottom: 1px solid var(--border);
    }

    .alloc-table tbody td {
      padding: 12px 16px;
      font-size: 14px;
      border-bottom: 1px solid var(--border);
    }

    .alloc-table tbody tr:last-child td {
      border-bottom: none;
    }

    .alloc-table tbody tr:hover {
      background: var(--muted);
    }

    .asset-name {
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .asset-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }

    .weight-bar-cell {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .weight-bar-bg {
      flex: 1;
      height: 6px;
      border-radius: 3px;
      background: var(--border);
      overflow: hidden;
    }

    .weight-bar-fill {
      height: 100%;
      border-radius: 3px;
      background: var(--foreground);
      transition: width 0.4s ease;
    }

    .weight-value {
      font-size: 14px;
      font-weight: 600;
      min-width: 48px;
      text-align: right;
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
    .option-item,
    .hero-note,
    .badge,
    select,
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

      .alloc-table thead th:nth-child(2),
      .alloc-table tbody td:nth-child(2) {
        min-width: 80px;
      }

      .weight-bar-bg {
        display: none;
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
        고정된 8개 자산군을 기준으로, 사용자의 위험 성향과 투자 기간에 따라
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
            <div class="card-description">슬라이더와 투자 기간으로 현재 포트폴리오가 프론티어 어디에 놓일지 정합니다.</div>
          </div>
          <div class="card-content">
            <form id="portfolio-form">
              <div class="field-group">
                <div class="slider-card">
                  <div class="slider-header">
                    <span class="slider-profile" id="risk-label">균형형</span>
                    <span class="slider-target" id="slider-target">11.0% 목표</span>
                  </div>
                  <input id="risk_slider" type="range" min="0" max="100" step="1" value="50" />
                  <div class="slider-labels">
                    <span>안정형</span>
                    <span>공격형</span>
                  </div>
                </div>
              </div>

              <div class="field-group">
                <label class="field-label" for="investment_horizon">투자 기간</label>
                <select id="investment_horizon" name="investment_horizon">
                  <option value="short">단기 (1~2년)</option>
                  <option value="medium" selected>중기 (3~5년)</option>
                  <option value="long">장기 (5년 이상)</option>
                </select>
              </div>

              <div class="field-group">
                <label class="field-label" for="target_volatility">목표 변동성 직접 입력</label>
                <input id="target_volatility" name="target_volatility" type="number" step="0.01" min="0.03" max="0.25" placeholder="예: 0.11" />
                <span class="field-hint">0.03 ~ 0.25 범위. 비워두면 슬라이더 기준 목표 변동성을 사용합니다.</span>
              </div>

              <button type="submit" class="btn btn-primary">포트폴리오 계산하기</button>
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
                  가능한 포트폴리오 점 구름 위로 효율적 투자선이 그려지고, 현재 선택된 포트폴리오가 그 위의 지점으로 강조됩니다.
                </div>
              </div>
              <div class="legend">
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-scatter);"></i>가능한 포트폴리오</span>
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-line);"></i>효율적 투자선</span>
                <span class="legend-item"><i class="legend-dot" style="background: var(--chart-selected);"></i>현재 포트폴리오</span>
              </div>
            </div>
          </div>
          <div class="card-content">
            <div class="chart-wrap">
              <svg id="frontier-chart" viewBox="0 0 900 460" aria-label="효율적 투자선 차트"></svg>
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

        <div class="two-col">
          <div class="card">
            <div class="card-header">
              <div class="step-badge"><span class="step-num">3</span> 해석</div>
            </div>
            <div class="card-content">
              <div class="explanation-title" id="explanation-title">왜 이런 포트폴리오가 나왔을까?</div>
              <div class="explanation-body" id="explanation-body">첫 계산이 완료되면 이 위치에 설명이 표시됩니다.</div>
              <div class="summary-text" id="summary"></div>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div class="step-badge"><span class="step-num">4</span> 옵션 비교</div>
              <div class="card-title">효율적 투자선 옵션</div>
              <div class="card-description">각 위험 수준별 대표 포트폴리오를 비교합니다.</div>
            </div>
            <div class="card-content">
              <div id="frontier-options" class="options-list"></div>
            </div>
          </div>
        </div>

        <div class="two-col">
          <div class="card">
            <div class="card-header">
              <div class="step-badge"><span class="step-num">5</span> 자산배분</div>
              <div class="card-title">비중과 리스크 기여도</div>
            </div>
            <div class="card-content" style="padding-top: 0;">
              <table class="alloc-table">
                <thead>
                  <tr>
                    <th>자산군</th>
                    <th>비중</th>
                    <th>리스크 기여도</th>
                  </tr>
                </thead>
                <tbody id="allocations"></tbody>
              </table>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div class="card-title">해석 포인트</div>
              <div class="card-description">결과를 어떻게 읽어야 할까</div>
            </div>
            <div class="card-content">
              <div class="interpretation">
                <p style="margin-bottom: 12px;">
                  <strong style="color: var(--foreground);">비중</strong>은 자금이 어디에 배분되는지를 보여주고,
                  <strong style="color: var(--foreground);">리스크 기여도</strong>는 실제 변동성이 어디에서 나오는지를 보여줍니다.
                </p>
                <p>
                  효율적 자산배분에서는 이 둘이 다르게 나타날 수 있고, 그 차이를 이해하는 것이 이 시뮬레이터의 중요한 포인트입니다.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <span>효율적 투자선 자산배분 시뮬레이터</span>
      <div><a href="/docs">Swagger</a></div>
    </footer>
  </div>

  <script>
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
    const targetVolInput = document.getElementById("target_volatility");
    const statusEl = document.getElementById("status");
    const summaryEl = document.getElementById("summary");
    const explanationTitleEl = document.getElementById("explanation-title");
    const explanationBodyEl = document.getElementById("explanation-body");
    const optionsEl = document.getElementById("frontier-options");
    const allocationsEl = document.getElementById("allocations");
    const chartEl = document.getElementById("frontier-chart");

    let lastData = null;
    let debounceTimer = null;

    function percent(value) {
      return `${(value * 100).toFixed(1)}%`;
    }

    function sliderProfile(value) {
      if (value < 34) return { risk_profile: "conservative", label: "안정형", base: 0.07 };
      if (value < 67) return { risk_profile: "balanced", label: "균형형", base: 0.11 };
      return { risk_profile: "growth", label: "성장형", base: 0.16 };
    }

    function horizonAdjustment(horizon) {
      if (horizon === "short") return -0.01;
      if (horizon === "long") return 0.01;
      return 0;
    }

    function suggestedVolatility() {
      const profile = sliderProfile(Number(slider.value));
      const exact = profile.base + horizonAdjustment(horizonEl.value);
      const clamped = Math.min(Math.max(exact, 0.04), 0.22);
      riskLabel.textContent = profile.label;
      sliderTarget.textContent = `${percent(clamped)} 목표`;
      return { profile, target: clamped };
    }

    function payloadFromInputs() {
      const { profile, target } = suggestedVolatility();
      const payload = {
        risk_profile: profile.risk_profile,
        investment_horizon: horizonEl.value,
      };
      const manualTarget = targetVolInput.value.trim();
      payload.target_volatility = manualTarget ? Number(manualTarget) : target;
      return payload;
    }

    function renderAllocations(items) {
      allocationsEl.innerHTML = items.map((item) => {
        const pct = (item.weight * 100).toFixed(1);
        const riskPct = (item.risk_contribution * 100).toFixed(1);
        const color = ASSET_COLORS[item.asset_code] || "#64748B";
        return `<tr>
          <td><span class="asset-name"><span class="asset-dot" style="background:${color}"></span>${item.asset_name}</span></td>
          <td>
            <div class="weight-bar-cell">
              <div class="weight-bar-bg"><div class="weight-bar-fill" style="width:${pct}%; background:${color}"></div></div>
              <span class="weight-value">${pct}%</span>
            </div>
          </td>
          <td>${riskPct}%</td>
        </tr>`;
      }).join("");
    }

    function renderOptions(items, selectedPoint) {
      optionsEl.innerHTML = items.map((item) => {
        const active = Math.abs(item.volatility - selectedPoint.volatility) < 0.02 ? " active" : "";
        return `<div class="option-item${active}">
          <span class="option-label">${item.label || "옵션"}</span>
          <div class="option-stats">
            <span>변동성 ${percent(item.volatility)}</span>
            <span>수익률 ${percent(item.expected_return)}</span>
          </div>
        </div>`;
      }).join("");
    }

    function getThemeColors() {
      const style = getComputedStyle(document.documentElement);
      return {
        bg: style.getPropertyValue("--chart-bg").trim(),
        grid: style.getPropertyValue("--chart-grid").trim(),
        label: style.getPropertyValue("--chart-label").trim(),
        line: style.getPropertyValue("--chart-line").trim(),
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
      const height = 460;
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const allPoints = randomPortfolios.concat(frontier).concat([selectedPoint]);
      const volMin = Math.min(...allPoints.map((p) => p.volatility)) * 0.9;
      const volMax = Math.max(...allPoints.map((p) => p.volatility)) * 1.1;
      const retMin = Math.min(...allPoints.map((p) => p.expected_return)) * 0.9;
      const retMax = Math.max(...allPoints.map((p) => p.expected_return)) * 1.1;

      function xScale(value) {
        return margin.left + ((value - volMin) / (volMax - volMin || 1)) * innerWidth;
      }

      function yScale(value) {
        return margin.top + innerHeight - ((value - retMin) / (retMax - retMin || 1)) * innerHeight;
      }

      let svg = "";

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

      randomPortfolios.forEach((point) => {
        svg += `<circle cx="${xScale(point.volatility)}" cy="${yScale(point.expected_return)}" r="3" fill="${c.scatter}" />`;
      });

      const frontierPath = frontier.map((point, index) => `${index === 0 ? "M" : "L"} ${xScale(point.volatility)} ${yScale(point.expected_return)}`).join(" ");
      svg += `<path d="${frontierPath}" fill="none" stroke="${c.line}" stroke-width="2.5" stroke-linecap="round" />`;

      const cx = xScale(selectedPoint.volatility);
      const cy = yScale(selectedPoint.expected_return);
      svg += `<circle cx="${cx}" cy="${cy}" r="12" fill="rgba(249, 115, 22, 0.15)" />`;
      svg += `<circle cx="${cx}" cy="${cy}" r="6" fill="${c.selected}" stroke="${c.bg}" stroke-width="2.5" />`;
      svg += `<text x="${cx + 16}" y="${cy - 12}" font-size="12" font-family="Inter, Noto Sans KR, sans-serif" fill="${c.text}" font-weight="600">현재 포트폴리오</text>`;
      svg += `<text x="${width / 2}" y="${height - 2}" text-anchor="middle" fill="${c.label}" font-size="12" font-family="Inter, Noto Sans KR, sans-serif">위험 (변동성)</text>`;
      svg += `<text x="14" y="${height / 2}" text-anchor="middle" fill="${c.label}" font-size="12" font-family="Inter, Noto Sans KR, sans-serif" transform="rotate(-90 14 ${height / 2})">예상 수익률</text>`;

      chartEl.innerHTML = svg;
    }

    async function loadPortfolio() {
      statusEl.textContent = "계산 중...";

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

        const expectedReturn = data.expected_return ?? data.metrics?.expected_return ?? 0;
        const volatility = data.volatility ?? data.metrics?.volatility ?? 0;
        const sharpeRatio = data.sharpe_ratio ?? data.metrics?.sharpe_ratio ?? 0;
        const explanationTitle = data.explanation_title ?? data.explanation?.title ?? "왜 이런 포트폴리오가 나왔을까?";
        const explanationBody = data.explanation ?? data.explanation?.body ?? "";

        lastData = data;
        document.getElementById("metric-return").textContent = percent(expectedReturn);
        document.getElementById("metric-vol").textContent = percent(volatility);
        document.getElementById("metric-sharpe").textContent = Number(sharpeRatio).toFixed(2);
        explanationTitleEl.textContent = explanationTitle;
        explanationBodyEl.textContent = explanationBody;
        summaryEl.textContent = [data.summary, data.disclaimer].filter(Boolean).join(" ");
        renderAllocations(data.allocations || []);
        renderOptions(data.frontier_options || [], data.selected_point);
        renderChart(data);
        statusEl.textContent = "";
      } catch (error) {
        statusEl.textContent = error.message;
      }
    }

    slider.addEventListener("input", () => {
      suggestedVolatility();
      clearTimeout(debounceTimer);
      if (!targetVolInput.value.trim()) {
        debounceTimer = setTimeout(loadPortfolio, 150);
      }
    });

    horizonEl.addEventListener("change", loadPortfolio);

    document.getElementById("portfolio-form").addEventListener("submit", (event) => {
      event.preventDefault();
      loadPortfolio();
    });

    (function() {
      const toggle = document.getElementById("theme-toggle");
      const html = document.documentElement;

      function rerenderChart() {
        if (lastData) {
          setTimeout(() => renderChart(lastData), 50);
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

    suggestedVolatility();
    loadPortfolio();
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)

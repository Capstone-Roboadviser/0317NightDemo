from fastapi.responses import HTMLResponse


def render_admin_page() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>관리자 유니버스 콘솔</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #f8fafc;
      --card: #ffffff;
      --line: #dbe3ef;
      --text: #0f172a;
      --muted: #64748b;
      --primary: #111827;
      --primary-contrast: #f8fafc;
      --accent: #2563eb;
      --success: #166534;
      --success-bg: #dcfce7;
      --warn: #92400e;
      --warn-bg: #fef3c7;
      --danger: #991b1b;
      --danger-bg: #fee2e2;
      --shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
      --radius: 20px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 32%),
        radial-gradient(circle at bottom right, rgba(16, 185, 129, 0.08), transparent 28%),
        var(--bg);
      color: var(--text);
      font-family: "Noto Sans KR", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .shell {
      max-width: 1280px;
      margin: 0 auto;
      padding: 32px 24px 56px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 28px;
    }

    .brand {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .eyebrow {
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.18em;
      color: var(--accent);
      text-transform: uppercase;
    }

    .title {
      font-size: clamp(28px, 4vw, 42px);
      font-weight: 800;
      line-height: 1.05;
    }

    .subtitle {
      max-width: 720px;
      font-size: 15px;
      line-height: 1.7;
      color: var(--muted);
    }

    .link-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .link-row a,
    .ghost-btn,
    .primary-btn,
    .secondary-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      border: 1px solid var(--line);
      padding: 10px 16px;
      font-size: 14px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
    }

    .ghost-btn,
    .secondary-btn,
    .link-row a {
      background: rgba(255, 255, 255, 0.9);
      color: var(--text);
    }

    .primary-btn {
      background: var(--primary);
      color: var(--primary-contrast);
      border-color: var(--primary);
      box-shadow: 0 12px 24px rgba(15, 23, 42, 0.16);
    }

    .secondary-btn:hover,
    .primary-btn:hover,
    .ghost-btn:hover,
    .link-row a:hover {
      transform: translateY(-1px);
    }

    .secondary-btn:disabled,
    .primary-btn:disabled,
    .ghost-btn:disabled {
      opacity: 0.62;
      cursor: wait;
      transform: none;
      box-shadow: none;
    }

    .grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 20px;
    }

    .stack {
      display: grid;
      gap: 20px;
    }

    .card {
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(219, 227, 239, 0.9);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 22px;
      backdrop-filter: blur(14px);
    }

    .card h2 {
      font-size: 20px;
      font-weight: 800;
      margin-bottom: 10px;
    }

    .card p.card-copy {
      color: var(--muted);
      line-height: 1.65;
      margin-bottom: 18px;
      font-size: 14px;
    }

    .status-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }

    .status-tile {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: #f8fafc;
      padding: 14px;
      min-height: 110px;
    }

    .status-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--muted);
      margin-bottom: 8px;
    }

    .status-value {
      font-size: 19px;
      font-weight: 800;
      line-height: 1.2;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
    }

    .pill.success {
      color: var(--success);
      background: var(--success-bg);
    }

    .pill.warn {
      color: var(--warn);
      background: var(--warn-bg);
    }

    .pill.danger {
      color: var(--danger);
      background: var(--danger-bg);
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }

    .field {
      display: grid;
      gap: 8px;
    }

    .field label {
      font-size: 13px;
      font-weight: 700;
      color: var(--muted);
    }

    .job-detail {
      margin-top: 16px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #f8fafc;
      padding: 14px;
    }

    .job-detail-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }

    .job-detail-title {
      font-size: 13px;
      font-weight: 800;
      color: var(--muted);
      letter-spacing: 0.03em;
    }

    .job-detail-list {
      display: grid;
      gap: 10px;
      max-height: 280px;
      overflow: auto;
    }

    .job-item {
      border: 1px solid var(--line);
      border-radius: 14px;
      background: #fff;
      padding: 12px;
      display: grid;
      gap: 6px;
    }

    .job-item-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }

    .job-item-ticker {
      font-size: 15px;
      font-weight: 800;
    }

    .job-item-meta {
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
      word-break: break-word;
    }

    .readiness-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }

    .readiness-tile {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: #f8fafc;
      padding: 14px;
      min-height: 92px;
    }

    .readiness-section {
      display: grid;
      gap: 10px;
      margin-top: 14px;
    }

    .readiness-title {
      font-size: 13px;
      font-weight: 800;
      color: var(--muted);
      letter-spacing: 0.03em;
    }

    .issue-list,
    .sector-check-list {
      display: grid;
      gap: 10px;
    }

    .issue-item,
    .sector-check-item {
      border-radius: 16px;
      border: 1px solid var(--line);
      background: #f8fafc;
      padding: 12px 14px;
    }

    .issue-item {
      color: var(--danger);
      background: #fff7f7;
      border-color: #fecaca;
    }

    .sector-check-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }

    .sector-check-copy {
      display: grid;
      gap: 4px;
    }

    .sector-check-name {
      font-size: 15px;
      font-weight: 800;
    }

    .sector-check-meta {
      font-size: 12px;
      color: var(--muted);
    }

    input,
    select,
    textarea {
      width: 100%;
      border-radius: 14px;
      border: 1px solid var(--line);
      padding: 12px 14px;
      font-size: 14px;
      font-family: inherit;
      color: var(--text);
      background: #fff;
    }

    textarea {
      min-height: 120px;
      resize: vertical;
    }

    .table-wrap {
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #fff;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 760px;
    }

    th,
    td {
      padding: 13px 14px;
      text-align: left;
      border-bottom: 1px solid var(--line);
      font-size: 13px;
      vertical-align: middle;
    }

    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      background: #f8fafc;
    }

    .row-actions {
      display: flex;
      gap: 8px;
    }

    .mini-btn {
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      padding: 7px 10px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }

    .mini-btn.primary {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }

    .builder-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }

    .builder-summary {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }

    .builder-summary .summary-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f8fafc;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }

    .sector-tabs {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }

    .sector-tab {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #ffffff;
      color: var(--text);
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
    }

    .sector-tab:hover {
      transform: translateY(-1px);
    }

    .sector-tab.active {
      background: var(--primary);
      color: var(--primary-contrast);
      border-color: var(--primary);
    }

    .sector-tab-count {
      display: inline-flex;
      min-width: 22px;
      justify-content: center;
      border-radius: 999px;
      padding: 2px 8px;
      background: rgba(15, 23, 42, 0.08);
      font-size: 11px;
      font-weight: 800;
    }

    .sector-tab.active .sector-tab-count {
      background: rgba(248, 250, 252, 0.16);
    }

    .sector-panel-wrap {
      display: grid;
      gap: 12px;
    }

    .sector-panel {
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #ffffff;
      padding: 18px;
      display: grid;
      gap: 12px;
    }

    .sector-panel[hidden] {
      display: none;
    }

    .sector-head {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: flex-start;
    }

    .sector-head > div:first-child {
      min-width: 0;
    }

    .sector-name {
      font-size: 22px;
      font-weight: 800;
      line-height: 1.2;
      overflow-wrap: anywhere;
    }

    .sector-code {
      font-size: 12px;
      color: var(--muted);
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-top: 6px;
      overflow-wrap: anywhere;
    }

    .sector-count {
      font-size: 13px;
      color: var(--muted);
      font-weight: 800;
      white-space: nowrap;
      text-align: right;
    }

    .sector-actions {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      gap: 10px;
      flex-wrap: wrap;
    }

    .sector-copy {
      color: var(--muted);
      line-height: 1.65;
      font-size: 14px;
    }

    .sector-search {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      align-items: center;
    }

    .search-results {
      display: grid;
      gap: 8px;
    }

    .search-results[hidden] {
      display: none;
    }

    .search-result-item {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: #f8fafc;
    }

    .search-result-main {
      min-width: 0;
      display: grid;
      gap: 4px;
    }

    .search-result-symbol {
      font-size: 14px;
      font-weight: 800;
      color: var(--text);
    }

    .search-result-name {
      font-size: 13px;
      color: var(--muted);
      line-height: 1.5;
      overflow-wrap: anywhere;
    }

    .search-result-meta {
      font-size: 11px;
      color: var(--muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    .sector-rows {
      display: grid;
      gap: 8px;
    }

    .sector-empty {
      padding: 14px;
      border-radius: 14px;
      border: 1px dashed var(--line);
      background: #ffffff;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.6;
    }

    .builder-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      align-items: center;
      padding: 10px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: #ffffff;
    }

    .builder-row-main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto auto;
      gap: 8px;
      align-items: center;
      grid-column: 1 / -1;
    }

    .builder-row-meta {
      display: grid;
      grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr);
      gap: 8px;
      grid-column: 1 / -1;
    }

    .builder-row .tiny {
      font-size: 12px;
      padding: 10px 11px;
      border-radius: 12px;
      min-width: 0;
    }

    .builder-row .assist {
      background: #f8fafc;
      color: var(--text);
    }

    .builder-row .mini-btn {
      justify-self: end;
    }

    .log-box {
      margin-top: 14px;
      border-radius: 16px;
      padding: 14px 16px;
      background: #0f172a;
      color: #e2e8f0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
      line-height: 1.7;
      white-space: pre-wrap;
      min-height: 82px;
    }

    .empty {
      padding: 22px;
      border: 1px dashed var(--line);
      border-radius: 18px;
      color: var(--muted);
      font-size: 14px;
      background: #fff;
    }

    @media (max-width: 1080px) {
      .grid,
      .status-grid,
      .form-grid {
        grid-template-columns: 1fr;
      }

      .builder-row {
        grid-template-columns: 1fr;
      }

      .builder-row-main,
      .builder-row-meta,
      .sector-search,
      .search-result-item {
        grid-template-columns: 1fr;
      }

      .sector-head {
        grid-template-columns: 1fr;
      }

      .sector-count {
        text-align: left;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="eyebrow">Admin Console</div>
        <div class="title">관리자 유니버스 콘솔</div>
        <div class="subtitle">
          로그인 없이 섹터별 종목 후보군, 관리자 유니버스 버전, 가격 갱신을 브라우저에서 바로 관리하는 데모용 화면입니다.
          실제 계산은 active 유니버스와 누적 price history를 기준으로 수행됩니다.
        </div>
      </div>
      <div class="link-row">
        <a href="/">시뮬레이터</a>
        <a href="/docs">Swagger</a>
      </div>
    </div>

    <div class="grid">
      <div class="stack">
        <section class="card">
          <h2>현재 상태</h2>
          <p class="card-copy">Postgres 연결 여부, active 버전, 저장된 가격 이력 범위, 마지막 갱신 잡 상태를 보여줍니다.</p>
          <div class="status-grid">
            <div class="status-tile">
              <div class="status-label">DB 연결</div>
              <div class="status-value" id="db-status">확인 중</div>
            </div>
            <div class="status-tile">
              <div class="status-label">활성 버전</div>
              <div class="status-value" id="active-version-name">없음</div>
            </div>
            <div class="status-tile">
              <div class="status-label">가격 행 수</div>
              <div class="status-value" id="price-row-count">0</div>
            </div>
            <div class="status-tile">
              <div class="status-label">최근 가격일</div>
              <div class="status-value" id="price-max-date">-</div>
            </div>
          </div>
          <div id="status-pill"></div>
          <div class="toolbar" style="margin: 14px 0 12px;">
            <button class="ghost-btn" id="reload-status-btn">상태 새로고침</button>
          </div>
          <div class="log-box" id="admin-log">콘솔 준비 완료</div>
        </section>

        <section class="card">
          <h2>시뮬레이션 준비 상태</h2>
          <p class="card-copy">가격 적재와는 별도로, 현재 active 유니버스가 실제 조합 탐색과 Efficient Frontier 계산까지 가능한지 점검합니다.</p>
          <div class="toolbar" style="margin-bottom: 14px;">
            <button class="ghost-btn" id="reload-readiness-btn">준비 상태 점검</button>
          </div>
          <div id="readiness-pill"><span class="pill warn">점검 전</span></div>
          <p class="card-copy" id="readiness-summary-copy" style="margin-top: 12px; margin-bottom: 14px;">
            아직 시뮬레이션 준비 상태를 점검하지 않았습니다.
          </p>
          <div class="readiness-grid">
            <div class="readiness-tile">
              <div class="status-label">active 버전</div>
              <div class="status-value" id="readiness-version-name">-</div>
            </div>
            <div class="readiness-tile">
              <div class="status-label">가격 티커 수</div>
              <div class="status-value" id="readiness-priced-ticker-count">0</div>
            </div>
            <div class="readiness-tile">
              <div class="status-label">유효 수익률 행 수</div>
              <div class="status-value" id="readiness-return-rows">0</div>
            </div>
          </div>
          <div class="readiness-section">
            <div class="readiness-title">차단 사유</div>
            <div class="issue-list" id="readiness-issues">
              <div class="empty">아직 진단 결과가 없습니다.</div>
            </div>
          </div>
          <div class="readiness-section">
            <div class="readiness-title">섹터별 준비 상태</div>
            <div class="sector-check-list" id="readiness-sector-checks">
              <div class="empty">섹터별 진단 결과가 없습니다.</div>
            </div>
          </div>
        </section>

        <section class="card">
          <div class="builder-head">
            <div>
              <h2>수기 유니버스 생성</h2>
              <p class="card-copy">관리자는 섹터 탭을 눌러 각 섹터의 종목 후보군을 관리합니다. 티커를 직접 입력한 뒤 자동채움을 누르거나, 검색 결과에서 바로 추가할 수 있습니다.</p>
            </div>
            <span class="pill warn">섹터 탭 관리</span>
          </div>

          <div class="form-grid">
            <div class="field">
              <label for="manual-version-name">버전명</label>
              <input id="manual-version-name" placeholder="manual-20260318-v1" />
            </div>
            <div class="field">
              <label for="manual-notes">버전 메모</label>
              <input id="manual-notes" placeholder="관리자 수기 입력 버전" />
            </div>
          </div>

          <div class="builder-summary">
            <div class="summary-pill">총 섹터 수 <span id="sector-count-summary">8</span></div>
            <div class="summary-pill">입력 종목 수 <span id="instrument-count-summary">0</span></div>
          </div>
          <div class="sector-tabs" id="sector-tabs"></div>
          <div class="sector-panel-wrap" id="builder-rows"></div>
          <div class="toolbar" style="margin-top: 14px;">
            <button class="primary-btn" id="create-version-btn">버전 생성 및 활성화</button>
          </div>
        </section>
      </div>

      <div class="stack">
        <section class="card">
          <h2>가격 데이터 갱신</h2>
          <p class="card-copy">active 유니버스의 티커를 기준으로 `yfinance`에서 가격을 가져와 Postgres에 누적 저장합니다.</p>
          <div class="form-grid">
            <div class="field">
              <label for="refresh-mode">갱신 모드</label>
              <select id="refresh-mode">
                <option value="incremental">incremental</option>
                <option value="full">full</option>
              </select>
            </div>
            <div class="field">
              <label for="lookback-years">full 모드 백필 연수</label>
              <input id="lookback-years" type="number" min="1" max="20" value="5" />
            </div>
          </div>
          <div class="toolbar">
            <button class="primary-btn" id="refresh-prices-btn">가격 갱신 실행</button>
            <button class="ghost-btn" id="check-price-status-btn">최근 갱신 상태 보기</button>
          </div>
          <p class="card-copy" style="margin-top: 14px; margin-bottom: 0;">
            `full` 모드에서는 active 종목 수와 조회 상태에 따라 1~2분 이상 걸릴 수 있습니다. 실행 중에는 버튼이 잠시 비활성화됩니다.
          </p>
          <div class="job-detail">
            <div class="job-detail-head">
              <div class="job-detail-title">최근 갱신 상세</div>
              <div id="job-detail-summary" class="pill warn">아직 갱신 기록 없음</div>
            </div>
            <div id="job-detail-list" class="job-detail-list">
              <div class="empty">최근 갱신 잡이 없어서 상세 내역을 표시할 수 없습니다.</div>
            </div>
          </div>
        </section>

        <section class="card">
          <h2>유니버스 버전 목록</h2>
          <p class="card-copy">현재 저장된 버전과 active 여부를 확인하고, 필요한 버전을 바로 활성화할 수 있습니다.</p>
          <div id="version-table-wrap" class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>버전명</th>
                  <th>Source</th>
                  <th>종목 수</th>
                  <th>상태</th>
                  <th>생성 시각</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody id="versions-body">
                <tr><td colspan="7">로딩 중...</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="card">
          <h2>빠른 가이드</h2>
          <p class="card-copy">데모에서는 아래 순서면 충분합니다.</p>
          <div class="empty">
            1. DATABASE_URL 연결<br/>
            2. 수기 유니버스 생성<br/>
            3. 가격 갱신 실행<br/>
            4. 메인 시뮬레이터(`/`)에서 결과 확인
          </div>
        </section>
      </div>
    </div>
  </div>

  <script>
    const sectorOptions = [
      { code: "bond", name: "채권" },
      { code: "real_assets", name: "실물" },
      { code: "etf", name: "ETF" },
      { code: "tech_healthcare", name: "기술주 및 헬스케어" },
      { code: "ai_semiconductor_social", name: "AI반도체 및 소셜미디어" },
      { code: "financials", name: "금융" },
      { code: "energy", name: "에너지" },
      { code: "consumer_other", name: "소비재 및 기타" }
    ];

    const builderRowsEl = document.getElementById("builder-rows");
    const sectorTabsEl = document.getElementById("sector-tabs");
    const adminLogEl = document.getElementById("admin-log");
    const versionsBodyEl = document.getElementById("versions-body");
    const instrumentCountSummaryEl = document.getElementById("instrument-count-summary");
    const sectorCountSummaryEl = document.getElementById("sector-count-summary");
    const jobDetailListEl = document.getElementById("job-detail-list");
    const jobDetailSummaryEl = document.getElementById("job-detail-summary");
    const readinessPillEl = document.getElementById("readiness-pill");
    const readinessSummaryCopyEl = document.getElementById("readiness-summary-copy");
    const readinessVersionNameEl = document.getElementById("readiness-version-name");
    const readinessPricedTickerCountEl = document.getElementById("readiness-priced-ticker-count");
    const readinessReturnRowsEl = document.getElementById("readiness-return-rows");
    const readinessIssuesEl = document.getElementById("readiness-issues");
    const readinessSectorChecksEl = document.getElementById("readiness-sector-checks");
    const reloadReadinessBtn = document.getElementById("reload-readiness-btn");
    const refreshPricesBtn = document.getElementById("refresh-prices-btn");
    const checkPriceStatusBtn = document.getElementById("check-price-status-btn");
    let activeSectorCode = sectorOptions[0].code;

    function logMessage(message, payload) {
      const lines = [message];
      if (payload !== undefined) {
        lines.push(typeof payload === "string" ? payload : JSON.stringify(payload, null, 2));
      }
      adminLogEl.textContent = lines.join("\\n\\n");
    }

    function updateSectorSummary() {
      const allRows = Array.from(builderRowsEl.querySelectorAll(".builder-row"));
      instrumentCountSummaryEl.textContent = String(allRows.length);
      sectorCountSummaryEl.textContent = String(sectorOptions.length);

      sectorOptions.forEach((sector) => {
        const rows = builderRowsEl.querySelectorAll(`.builder-row[data-sector-code="${sector.code}"]`);
        const panel = builderRowsEl.querySelector(`.sector-panel[data-sector-code="${sector.code}"]`);
        const countEl = panel?.querySelector(".sector-count strong");
        const emptyEl = panel?.querySelector(".sector-empty");
        const tabCountEl = sectorTabsEl.querySelector(`.sector-tab[data-sector-code="${sector.code}"] .sector-tab-count`);
        if (countEl) {
          countEl.textContent = String(rows.length);
        }
        if (emptyEl) {
          emptyEl.hidden = rows.length > 0;
        }
        if (tabCountEl) {
          tabCountEl.textContent = String(rows.length);
        }
      });
    }

    function setActiveSector(sectorCode) {
      activeSectorCode = sectorCode;
      Array.from(sectorTabsEl.querySelectorAll(".sector-tab")).forEach((button) => {
        const isActive = button.dataset.sectorCode === sectorCode;
        button.classList.toggle("active", isActive);
        button.setAttribute("aria-selected", String(isActive));
      });
      Array.from(builderRowsEl.querySelectorAll(".sector-panel")).forEach((panel) => {
        panel.hidden = panel.dataset.sectorCode !== sectorCode;
      });
    }

    function ensureSectorPanel(sectorCode) {
      let panel = builderRowsEl.querySelector(`.sector-panel[data-sector-code="${sectorCode}"]`);
      if (panel) {
        return panel;
      }
      const sector = sectorOptions.find((item) => item.code === sectorCode);
      if (!sector) {
        throw new Error(`알 수 없는 섹터 코드: ${sectorCode}`);
      }
      panel = document.createElement("div");
      panel.className = "sector-panel";
      panel.dataset.sectorCode = sector.code;
      panel.hidden = sector.code !== activeSectorCode;
      panel.innerHTML = `
        <div class="sector-head">
          <div>
            <div class="sector-name">${sector.name}</div>
            <div class="sector-code">${sector.code}</div>
          </div>
          <div class="sector-count"><strong>0</strong>개 종목</div>
        </div>
        <div class="sector-copy">이 섹터에 포함할 종목 후보군을 관리합니다. 저장하면 현재 입력된 전체 섹터 구성이 하나의 유니버스 버전으로 생성됩니다.</div>
        <div class="sector-search">
          <input class="sector-search-input" data-search-input="${sector.code}" placeholder="티커 또는 회사명 검색 (예: NVDA, Microsoft)" />
          <button class="secondary-btn" type="button" data-search-sector="${sector.code}">검색</button>
        </div>
        <div class="search-results" data-search-results="${sector.code}" hidden></div>
        <div class="sector-actions">
          <span class="pill warn">섹터 후보군</span>
          <button class="secondary-btn" type="button" data-add-sector="${sector.code}">종목 추가</button>
        </div>
        <div class="sector-empty">아직 등록된 종목이 없습니다. 이 섹터에 티커를 추가하면 다음 유니버스 버전에 포함됩니다.</div>
        <div class="sector-rows" data-sector-rows="${sector.code}"></div>
      `;
      panel.querySelector(`[data-add-sector="${sector.code}"]`).addEventListener("click", () => addBuilderRow({ sector_code: sector.code }));
      panel.querySelector(`[data-search-sector="${sector.code}"]`).addEventListener("click", () => searchSectorTickers(sector.code));
      panel.querySelector(`[data-search-input="${sector.code}"]`).addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          searchSectorTickers(sector.code);
        }
      });
      builderRowsEl.appendChild(panel);
      return panel;
    }

    function renderSectorTabs() {
      sectorTabsEl.innerHTML = sectorOptions.map((sector) => `
        <button
          type="button"
          class="sector-tab"
          data-sector-code="${sector.code}"
          aria-selected="false"
        >
          <span>${sector.name}</span>
          <span class="sector-tab-count">0</span>
        </button>
      `).join("");

      Array.from(sectorTabsEl.querySelectorAll(".sector-tab")).forEach((button) => {
        button.addEventListener("click", () => setActiveSector(button.dataset.sectorCode));
      });
    }

    function renderSectorPanels() {
      builderRowsEl.innerHTML = "";
      sectorOptions.forEach((sector) => ensureSectorPanel(sector.code));
      setActiveSector(activeSectorCode);
      updateSectorSummary();
    }

    function addBuilderRow(seed = {}) {
      const sectorCode = seed.sector_code || "etf";
      const panel = ensureSectorPanel(sectorCode);
      const rowsWrap = panel.querySelector(`[data-sector-rows="${sectorCode}"]`);
      const row = document.createElement("div");
      row.className = "builder-row";
      row.dataset.sectorCode = sectorCode;
      row.innerHTML = `
        <div class="builder-row-main">
          <input class="tiny ticker" placeholder="SPY" value="${seed.ticker || ""}" />
          <button class="mini-btn primary autofill-btn" type="button">자동채움</button>
          <button class="mini-btn delete-btn" type="button">삭제</button>
        </div>
        <div class="builder-row-meta">
          <input class="tiny name assist" placeholder="종목명 자동채움 또는 수기 입력" value="${seed.name || ""}" />
          <input class="tiny market assist" placeholder="시장 자동채움 또는 수기 입력" value="${seed.market || ""}" />
          <input class="tiny currency assist" placeholder="통화 자동채움 또는 수기 입력" value="${seed.currency || ""}" />
          <input class="tiny weight" type="number" step="0.01" min="0" placeholder="비중(선택)" value="${seed.base_weight ?? ""}" />
        </div>
      `;
      row.querySelector(".delete-btn").addEventListener("click", () => {
        row.remove();
        updateSectorSummary();
      });
      row.querySelector(".autofill-btn").addEventListener("click", async () => {
        await autofillRowFromTicker(row);
      });
      row.querySelector(".ticker").addEventListener("blur", async () => {
        const ticker = normalizeTicker(row.querySelector(".ticker").value);
        const name = row.querySelector(".name").value.trim();
        if (ticker && !name) {
          await autofillRowFromTicker(row, { silent: true });
        }
      });
      rowsWrap.appendChild(row);
      setActiveSector(sectorCode);
      updateSectorSummary();
    }

    function normalizeTicker(value) {
      return (value || "").trim().toUpperCase();
    }

    function findDuplicateTicker(ticker, currentRow = null) {
      const normalized = normalizeTicker(ticker);
      if (!normalized) return null;
      return Array.from(builderRowsEl.querySelectorAll(".builder-row")).find((row) => {
        if (currentRow && row === currentRow) return false;
        return normalizeTicker(row.querySelector(".ticker").value) === normalized;
      }) || null;
    }

    async function lookupTicker(ticker) {
      const normalized = normalizeTicker(ticker);
      return apiRequest(`/admin/tickers/lookup?ticker=${encodeURIComponent(normalized)}`);
    }

    async function autofillRowFromTicker(row, { silent = false } = {}) {
      const tickerInput = row.querySelector(".ticker");
      const ticker = normalizeTicker(tickerInput.value);
      tickerInput.value = ticker;
      if (!ticker) {
        if (!silent) logMessage("자동채움 실패", "티커를 먼저 입력해주세요.");
        return;
      }

      const duplicate = findDuplicateTicker(ticker, row);
      if (duplicate) {
        if (!silent) logMessage("중복 티커", `${ticker} 는 이미 다른 섹터 또는 동일 섹터에 추가되어 있습니다.`);
        return;
      }

      try {
        const data = await lookupTicker(ticker);
        row.querySelector(".name").value = data.name || ticker;
        row.querySelector(".market").value = data.market || "";
        row.querySelector(".currency").value = data.currency || "";
        if (!silent) {
          logMessage("티커 자동채움 완료", data);
        }
      } catch (error) {
        if (!silent) {
          logMessage("티커 자동채움 실패", `${error.message}\n필요하면 종목명/시장/통화를 직접 입력한 뒤 저장할 수 있습니다.`);
        }
      }
    }

    function renderSearchResults(sectorCode, results) {
      const panel = ensureSectorPanel(sectorCode);
      const resultsEl = panel.querySelector(`[data-search-results="${sectorCode}"]`);
      if (!results.length) {
        resultsEl.hidden = false;
        resultsEl.innerHTML = '<div class="sector-empty">검색 결과가 없습니다. 정확한 티커를 입력하고 자동채움을 사용해보세요.</div>';
        return;
      }

      resultsEl.hidden = false;
      resultsEl.innerHTML = results.map((item) => `
        <div class="search-result-item">
          <div class="search-result-main">
            <div class="search-result-symbol">${item.ticker}</div>
            <div class="search-result-name">${item.name}</div>
            <div class="search-result-meta">${[item.exchange, item.currency, item.quote_type].filter(Boolean).join(" · ")}</div>
          </div>
          <button class="mini-btn primary" type="button" data-add-result="${item.ticker}">추가</button>
        </div>
      `).join("");

      Array.from(resultsEl.querySelectorAll("[data-add-result]")).forEach((button) => {
        button.addEventListener("click", async () => {
          const ticker = button.getAttribute("data-add-result");
          if (findDuplicateTicker(ticker)) {
            logMessage("중복 티커", `${ticker} 는 이미 추가되어 있습니다.`);
            return;
          }
          const match = results.find((item) => item.ticker === ticker);
          addBuilderRow({
            ticker: ticker,
            name: match?.name || "",
            sector_code: sectorCode,
            market: match?.market || match?.exchange || "",
            currency: match?.currency || "",
          });
          const addedRow = Array.from(builderRowsEl.querySelectorAll(`.builder-row[data-sector-code="${sectorCode}"]`)).pop();
          if (addedRow && (!match?.market || !match?.currency)) {
            await autofillRowFromTicker(addedRow, { silent: true });
          }
          logMessage("검색 결과 추가 완료", { sector_code: sectorCode, ticker });
        });
      });
    }

    async function searchSectorTickers(sectorCode) {
      const panel = ensureSectorPanel(sectorCode);
      const input = panel.querySelector(`[data-search-input="${sectorCode}"]`);
      const query = input.value.trim();
      const resultsEl = panel.querySelector(`[data-search-results="${sectorCode}"]`);
      if (!query) {
        resultsEl.hidden = true;
        resultsEl.innerHTML = "";
        logMessage("티커 검색 실패", "검색어를 입력해주세요.");
        return;
      }
      try {
        const data = await apiRequest(`/admin/tickers/search?query=${encodeURIComponent(query)}&max_results=8`);
        renderSearchResults(sectorCode, data.results || []);
        logMessage("티커 검색 완료", { query, result_count: (data.results || []).length });
      } catch (error) {
        resultsEl.hidden = true;
        resultsEl.innerHTML = "";
        logMessage("티커 검색 실패", error.message);
      }
    }

    function collectBuilderRows() {
      return Array.from(builderRowsEl.querySelectorAll(".builder-row")).map((row) => {
        const sectorCode = row.dataset.sectorCode;
        const sectorMeta = sectorOptions.find((item) => item.code === sectorCode);
        const baseWeightRaw = row.querySelector(".weight").value.trim();
        return {
          ticker: normalizeTicker(row.querySelector(".ticker").value),
          name: row.querySelector(".name").value.trim(),
          sector_code: sectorCode,
          sector_name: sectorMeta ? sectorMeta.name : sectorCode,
          market: row.querySelector(".market").value.trim() || "USA",
          currency: row.querySelector(".currency").value.trim() || "USD",
          base_weight: baseWeightRaw === "" ? null : Number(baseWeightRaw)
        };
      }).filter((item) => item.ticker || item.name || item.market || item.currency || item.base_weight !== null);
    }

    async function apiRequest(path, options = {}) {
      const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || `HTTP ${response.status}`);
      }
      return data;
    }

    function renderStatus(data) {
      document.getElementById("db-status").textContent = data.database_configured ? "연결됨" : "미설정";
      document.getElementById("active-version-name").textContent = data.active_version?.version_name || "없음";
      document.getElementById("price-row-count").textContent = data.price_stats?.total_rows?.toLocaleString?.() || "0";
      document.getElementById("price-max-date").textContent = data.price_stats?.max_date || "-";

      const pillEl = document.getElementById("status-pill");
      let pillClass = "warn";
      let pillText = "데모 fallback 모드";
      if (data.database_configured && data.active_version) {
        pillClass = "success";
        pillText = `active 버전 ${data.active_version.version_name}`;
      } else if (!data.database_configured) {
        pillClass = "danger";
        pillText = "DATABASE_URL 미설정";
      }
      pillEl.innerHTML = `<span class="pill ${pillClass}">${pillText}</span>`;
    }

    function renderReadiness(data) {
      const readinessClass = data.ready ? "success" : "danger";
      readinessPillEl.innerHTML = `<span class="pill ${readinessClass}">${data.ready ? "계산 가능" : "계산 차단"}</span>`;
      readinessSummaryCopyEl.textContent = data.summary || "준비 상태 요약이 없습니다.";
      readinessVersionNameEl.textContent = data.active_version_name || "-";
      readinessPricedTickerCountEl.textContent = `${data.priced_ticker_count}/${data.instrument_count}`;

      const effectiveRows = data.effective_history_rows;
      const rowsText = effectiveRows === null
        ? `${data.stock_return_rows}행`
        : `${effectiveRows}행`;
      readinessReturnRowsEl.textContent = rowsText;

      if (data.issues?.length) {
        readinessIssuesEl.innerHTML = data.issues.map((issue) => `
          <div class="issue-item">${issue}</div>
        `).join("");
      } else {
        readinessIssuesEl.innerHTML = '<div class="empty">현재 차단 사유가 없습니다.</div>';
      }

      if (data.sector_checks?.length) {
        readinessSectorChecksEl.innerHTML = data.sector_checks.map((item) => `
          <div class="sector-check-item">
            <div class="sector-check-copy">
              <div class="sector-check-name">${item.sector_name}</div>
              <div class="sector-check-meta">${item.sector_code}</div>
            </div>
            <span class="pill ${item.ready ? "success" : "danger"}">
              필요 ${item.required_count} / 현재 ${item.actual_count}
            </span>
          </div>
        `).join("");
      } else {
        readinessSectorChecksEl.innerHTML = '<div class="empty">섹터별 진단 결과가 없습니다.</div>';
      }
    }

    function renderReadinessError(message) {
      readinessPillEl.innerHTML = '<span class="pill danger">진단 실패</span>';
      readinessSummaryCopyEl.textContent = message;
      readinessVersionNameEl.textContent = "-";
      readinessPricedTickerCountEl.textContent = "0";
      readinessReturnRowsEl.textContent = "0";
      readinessIssuesEl.innerHTML = `<div class="issue-item">${message}</div>`;
      readinessSectorChecksEl.innerHTML = '<div class="empty">섹터별 진단 결과를 불러오지 못했습니다.</div>';
    }

    function renderJobItems(job, items) {
      if (!job) {
        jobDetailSummaryEl.className = "pill warn";
        jobDetailSummaryEl.textContent = "아직 갱신 기록 없음";
        jobDetailListEl.innerHTML = '<div class="empty">최근 갱신 잡이 없어서 상세 내역을 표시할 수 없습니다.</div>';
        return;
      }

      const jobStatusClass = job.status === "success"
        ? "success"
        : (job.status === "partial_success" ? "warn" : "danger");
      jobDetailSummaryEl.className = `pill ${jobStatusClass}`;
      jobDetailSummaryEl.textContent = `${job.status} · 성공 ${job.success_count} / 실패 ${job.failure_count}`;

      if (!items.length) {
        jobDetailListEl.innerHTML = '<div class="empty">표시할 갱신 상세 항목이 없습니다.</div>';
        return;
      }

      jobDetailListEl.innerHTML = items.map((item) => `
        <div class="job-item">
          <div class="job-item-top">
            <div class="job-item-ticker">${item.ticker}</div>
            <span class="pill ${item.status === "success" ? "success" : "danger"}">${item.status}</span>
          </div>
          <div class="job-item-meta">rows_upserted: ${item.rows_upserted}</div>
          ${item.error_message ? `<div class="job-item-meta">error: ${item.error_message}</div>` : ""}
        </div>
      `).join("");
    }

    function renderVersions(versions) {
      if (!versions.length) {
        versionsBodyEl.innerHTML = '<tr><td colspan="7">저장된 유니버스 버전이 없습니다.</td></tr>';
        return;
      }
      versionsBodyEl.innerHTML = versions.map((item) => `
        <tr>
          <td>${item.version_id}</td>
          <td>${item.version_name}</td>
          <td>${item.source_type}</td>
          <td>${item.instrument_count}</td>
          <td>${item.is_active ? '<span class="pill success">ACTIVE</span>' : '<span class="pill warn">INACTIVE</span>'}</td>
          <td>${item.created_at}</td>
          <td>
            <div class="row-actions">
              <button class="mini-btn ${item.is_active ? '' : 'primary'}" data-activate="${item.version_id}">
                ${item.is_active ? '활성중' : '활성화'}
              </button>
            </div>
          </td>
        </tr>
      `).join("");

      Array.from(document.querySelectorAll("[data-activate]")).forEach((button) => {
        button.addEventListener("click", async () => {
          const versionId = button.getAttribute("data-activate");
          try {
            const data = await apiRequest(`/admin/universe/versions/${versionId}/activate`, { method: "POST" });
            logMessage("버전을 활성화했습니다.", data);
            await reloadAll();
          } catch (error) {
            logMessage("버전 활성화 실패", error.message);
          }
        });
      });
    }

    async function reloadStatus() {
      const status = await apiRequest("/admin/universe/status");
      renderStatus(status);
      return status;
    }

    async function reloadVersions() {
      const versions = await apiRequest("/admin/universe/versions");
      renderVersions(versions);
      return versions;
    }

    async function reloadReadiness() {
      try {
        const readiness = await apiRequest("/admin/universe/readiness");
        renderReadiness(readiness);
        return readiness;
      } catch (error) {
        renderReadinessError(error.message);
        throw error;
      }
    }

    async function reloadLatestJobItems(status) {
      const latestJob = status?.latest_refresh_job;
      if (!latestJob) {
        renderJobItems(null, []);
        return [];
      }
      const failedOnly = latestJob.status !== "success";
      try {
        const items = await apiRequest(`/admin/prices/jobs/${latestJob.job_id}/items?failed_only=${failedOnly ? "true" : "false"}&limit=40`);
        renderJobItems(latestJob, items);
        return items;
      } catch (error) {
        renderJobItems(latestJob, []);
        logMessage("최근 갱신 상세 조회 실패", error.message);
        return [];
      }
    }

    async function reloadAll() {
      try {
        const [status, versions, readiness] = await Promise.all([reloadStatus(), reloadVersions(), reloadReadiness()]);
        const jobItems = await reloadLatestJobItems(status);
        logMessage("상태 새로고침 완료", {
          status,
          readiness,
          version_count: versions.length,
          latest_job_item_count: jobItems.length
        });
      } catch (error) {
        logMessage("상태 새로고침 실패", error.message);
      }
    }

    function setPriceRefreshBusy(isBusy) {
      refreshPricesBtn.disabled = isBusy;
      checkPriceStatusBtn.disabled = isBusy;
      refreshPricesBtn.textContent = isBusy ? "가격 갱신 실행 중..." : "가격 갱신 실행";
      refreshPricesBtn.setAttribute("aria-busy", String(isBusy));
    }

    document.getElementById("reload-status-btn").addEventListener("click", reloadAll);
    checkPriceStatusBtn.addEventListener("click", reloadAll);
    reloadReadinessBtn.addEventListener("click", reloadReadiness);

    document.getElementById("create-version-btn").addEventListener("click", async () => {
      const instruments = collectBuilderRows();
      if (!instruments.length) {
        logMessage("수기 버전 생성 실패", "최소 1개 종목을 입력해주세요.");
        return;
      }
      const missingTicker = instruments.find((item) => !item.ticker);
      if (missingTicker) {
        logMessage("수기 버전 생성 실패", "비어 있는 티커 행이 있습니다. 빈 행을 지우거나 티커를 입력해주세요.");
        return;
      }
      const invalidRows = instruments.filter((item) => !item.name || !item.market || !item.currency);
      if (invalidRows.length) {
        logMessage("수기 버전 생성 실패", "자동채움이 완료되지 않은 종목이 있습니다. 각 행의 티커를 검증해주세요.");
        return;
      }
      const seenTickers = new Set();
      for (const item of instruments) {
        if (seenTickers.has(item.ticker)) {
          logMessage("수기 버전 생성 실패", `중복 ticker가 있습니다: ${item.ticker}`);
          return;
        }
        seenTickers.add(item.ticker);
      }
      const payload = {
        version_name: document.getElementById("manual-version-name").value.trim() || `manual-${Date.now()}`,
        notes: document.getElementById("manual-notes").value.trim() || null,
        activate: true,
        instruments
      };
      try {
        const data = await apiRequest("/admin/universe/versions", {
          method: "POST",
          body: JSON.stringify(payload)
        });
        logMessage("수기 유니버스 생성 완료", data);
        await reloadAll();
      } catch (error) {
        logMessage("수기 유니버스 생성 실패", error.message);
      }
    });

    refreshPricesBtn.addEventListener("click", async () => {
      const payload = {
        refresh_mode: document.getElementById("refresh-mode").value,
        full_lookback_years: Number(document.getElementById("lookback-years").value || 5)
      };
      const startedAt = Date.now();
      setPriceRefreshBusy(true);
      logMessage("가격 갱신 시작", {
        ...payload,
        note: "외부 시세 조회와 DB 저장이 끝날 때까지 잠시 기다려주세요."
      });
      try {
        const data = await apiRequest("/admin/prices/refresh", {
          method: "POST",
          body: JSON.stringify(payload)
        });
        const elapsedSeconds = ((Date.now() - startedAt) / 1000).toFixed(1);
        logMessage("가격 갱신 완료", {
          ...data,
          elapsed_seconds: Number(elapsedSeconds)
        });
        await reloadAll();
      } catch (error) {
        logMessage("가격 갱신 실패", error.message);
      } finally {
        setPriceRefreshBusy(false);
      }
    });

    renderSectorTabs();
    renderSectorPanels();
    addBuilderRow({ ticker: "SPY", name: "SPDR S&P 500 ETF Trust", sector_code: "etf" });
    addBuilderRow({ ticker: "NVDA", name: "NVIDIA Corp", sector_code: "ai_semiconductor_social" });
    addBuilderRow({ ticker: "JPM", name: "JPMorgan Chase", sector_code: "financials" });
    reloadAll();
  </script>
</body>
</html>"""
    return HTMLResponse(content=html)

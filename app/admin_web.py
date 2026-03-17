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

    .sector-board {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }

    .sector-card {
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #f8fafc;
      padding: 14px;
      display: grid;
      gap: 12px;
    }

    .sector-card.empty {
      border-style: dashed;
    }

    .sector-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }

    .sector-name {
      font-size: 16px;
      font-weight: 800;
      line-height: 1.2;
    }

    .sector-code {
      font-size: 11px;
      color: var(--muted);
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-top: 4px;
    }

    .sector-count {
      font-size: 12px;
      color: var(--muted);
      font-weight: 800;
      white-space: nowrap;
    }

    .sector-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
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
      grid-template-columns: 1fr 1.4fr 0.9fr 0.9fr 0.8fr auto;
      gap: 8px;
      align-items: center;
      padding: 10px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: #ffffff;
    }

    .builder-row .tiny {
      font-size: 12px;
      padding: 10px 11px;
      border-radius: 12px;
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

      .sector-board {
        grid-template-columns: 1fr;
      }

      .builder-row {
        grid-template-columns: 1fr;
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
          <div class="builder-head">
            <div>
              <h2>수기 유니버스 생성</h2>
              <p class="card-copy">관리자는 섹터별 카드 안에서 종목을 추가하고, 전체를 하나의 유니버스 버전으로 저장합니다. 가격 데이터는 이후 별도 갱신 버튼으로 가져옵니다.</p>
            </div>
            <span class="pill warn">섹터별 관리</span>
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
          <div class="sector-board" id="builder-rows"></div>
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
    const adminLogEl = document.getElementById("admin-log");
    const versionsBodyEl = document.getElementById("versions-body");
    const instrumentCountSummaryEl = document.getElementById("instrument-count-summary");
    const sectorCountSummaryEl = document.getElementById("sector-count-summary");

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
        const card = builderRowsEl.querySelector(`.sector-card[data-sector-code="${sector.code}"]`);
        const countEl = card?.querySelector(".sector-count strong");
        const emptyEl = card?.querySelector(".sector-empty");
        if (countEl) {
          countEl.textContent = String(rows.length);
        }
        if (card) {
          card.classList.toggle("empty", rows.length === 0);
        }
        if (emptyEl) {
          emptyEl.hidden = rows.length > 0;
        }
      });
    }

    function ensureSectorCard(sectorCode) {
      let card = builderRowsEl.querySelector(`.sector-card[data-sector-code="${sectorCode}"]`);
      if (card) {
        return card;
      }
      const sector = sectorOptions.find((item) => item.code === sectorCode);
      if (!sector) {
        throw new Error(`알 수 없는 섹터 코드: ${sectorCode}`);
      }
      card = document.createElement("div");
      card.className = "sector-card empty";
      card.dataset.sectorCode = sector.code;
      card.innerHTML = `
        <div class="sector-head">
          <div>
            <div class="sector-name">${sector.name}</div>
            <div class="sector-code">${sector.code}</div>
          </div>
          <div class="sector-count"><strong>0</strong>개 종목</div>
        </div>
        <div class="sector-actions">
          <span class="pill warn">섹터 후보군</span>
          <button class="secondary-btn" type="button" data-add-sector="${sector.code}">종목 추가</button>
        </div>
        <div class="sector-empty">아직 등록된 종목이 없습니다. 이 섹터에 티커를 추가하면 다음 유니버스 버전에 포함됩니다.</div>
        <div class="sector-rows" data-sector-rows="${sector.code}"></div>
      `;
      card.querySelector(`[data-add-sector="${sector.code}"]`).addEventListener("click", () => addBuilderRow({ sector_code: sector.code }));
      builderRowsEl.appendChild(card);
      return card;
    }

    function renderSectorCards() {
      builderRowsEl.innerHTML = "";
      sectorOptions.forEach((sector) => ensureSectorCard(sector.code));
      updateSectorSummary();
    }

    function addBuilderRow(seed = {}) {
      const sectorCode = seed.sector_code || "etf";
      const card = ensureSectorCard(sectorCode);
      const rowsWrap = card.querySelector(`[data-sector-rows="${sectorCode}"]`);
      const row = document.createElement("div");
      row.className = "builder-row";
      row.dataset.sectorCode = sectorCode;
      row.innerHTML = `
        <input class="tiny ticker" placeholder="SPY" value="${seed.ticker || ""}" />
        <input class="tiny name" placeholder="SPDR S&P 500 ETF Trust" value="${seed.name || ""}" />
        <input class="tiny market" placeholder="USA" value="${seed.market || "USA"}" />
        <input class="tiny currency" placeholder="USD" value="${seed.currency || "USD"}" />
        <input class="tiny weight" type="number" step="0.01" min="0" placeholder="0.25" value="${seed.base_weight ?? ""}" />
        <button class="mini-btn" type="button">삭제</button>
      `;
      row.querySelector(".mini-btn").addEventListener("click", () => {
        row.remove();
        updateSectorSummary();
      });
      rowsWrap.appendChild(row);
      updateSectorSummary();
    }

    function collectBuilderRows() {
      return Array.from(builderRowsEl.querySelectorAll(".builder-row")).map((row) => {
        const sectorCode = row.dataset.sectorCode;
        const sectorMeta = sectorOptions.find((item) => item.code === sectorCode);
        const baseWeightRaw = row.querySelector(".weight").value.trim();
        return {
          ticker: row.querySelector(".ticker").value.trim(),
          name: row.querySelector(".name").value.trim(),
          sector_code: sectorCode,
          sector_name: sectorMeta ? sectorMeta.name : sectorCode,
          market: row.querySelector(".market").value.trim() || "USA",
          currency: row.querySelector(".currency").value.trim() || "USD",
          base_weight: baseWeightRaw === "" ? null : Number(baseWeightRaw)
        };
      }).filter((item) => item.ticker && item.name);
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

    async function reloadAll() {
      try {
        const [status, versions] = await Promise.all([reloadStatus(), reloadVersions()]);
        logMessage("상태 새로고침 완료", { status, version_count: versions.length });
      } catch (error) {
        logMessage("상태 새로고침 실패", error.message);
      }
    }

    document.getElementById("reload-status-btn").addEventListener("click", reloadAll);
    document.getElementById("check-price-status-btn").addEventListener("click", reloadAll);

    document.getElementById("create-version-btn").addEventListener("click", async () => {
      const instruments = collectBuilderRows();
      if (!instruments.length) {
        logMessage("수기 버전 생성 실패", "최소 1개 종목을 입력해주세요.");
        return;
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

    document.getElementById("refresh-prices-btn").addEventListener("click", async () => {
      const payload = {
        refresh_mode: document.getElementById("refresh-mode").value,
        full_lookback_years: Number(document.getElementById("lookback-years").value || 5)
      };
      try {
        const data = await apiRequest("/admin/prices/refresh", {
          method: "POST",
          body: JSON.stringify(payload)
        });
        logMessage("가격 갱신 완료", data);
        await reloadAll();
      } catch (error) {
        logMessage("가격 갱신 실패", error.message);
      }
    });

    renderSectorCards();
    addBuilderRow({ ticker: "SPY", name: "SPDR S&P 500 ETF Trust", sector_code: "etf" });
    addBuilderRow({ ticker: "NVDA", name: "NVIDIA Corp", sector_code: "ai_semiconductor_social" });
    addBuilderRow({ ticker: "JPM", name: "JPMorgan Chase", sector_code: "financials" });
    reloadAll();
  </script>
</body>
</html>"""
    return HTMLResponse(content=html)

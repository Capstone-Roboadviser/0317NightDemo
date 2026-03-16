from fastapi.responses import HTMLResponse


def render_homepage() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>효율적 투자선 자산배분 시뮬레이터</title>
  <style>
    :root {
      --bg: #f6f1e8;
      --panel: rgba(255, 252, 246, 0.9);
      --text: #18211e;
      --muted: #61706a;
      --line: rgba(24, 33, 30, 0.12);
      --primary: #173f35;
      --accent: #d58532;
      --accent-soft: rgba(213, 133, 50, 0.12);
      --blue: #1f5f8b;
      --blue-soft: rgba(31, 95, 139, 0.12);
      --shadow: 0 28px 70px rgba(36, 48, 40, 0.12);
      --radius: 24px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: Georgia, "Iowan Old Style", "Noto Serif KR", serif;
      background:
        radial-gradient(circle at top left, rgba(213, 133, 50, 0.18), transparent 28%),
        radial-gradient(circle at right 20%, rgba(23, 63, 53, 0.14), transparent 26%),
        linear-gradient(180deg, #f9f4eb 0%, var(--bg) 100%);
    }

    .shell {
      max-width: 1280px;
      margin: 0 auto;
      padding: 36px 20px 56px;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }

    .hero {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
      margin-bottom: 24px;
    }

    .hero-copy {
      padding: 34px;
    }

    .eyebrow {
      display: inline-block;
      margin-bottom: 14px;
      font-size: 12px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--primary);
    }

    h1 {
      margin: 0 0 16px;
      font-size: clamp(2.5rem, 6vw, 4.8rem);
      line-height: 0.96;
      font-weight: 700;
    }

    .lead {
      max-width: 60ch;
      margin: 0 0 16px;
      color: var(--muted);
      line-height: 1.75;
      font-size: 1.04rem;
    }

    .hero-note {
      padding: 16px 18px;
      border-radius: 18px;
      background: rgba(23, 63, 53, 0.08);
      color: var(--primary);
      line-height: 1.65;
    }

    .hero-side {
      padding: 28px;
      background:
        linear-gradient(145deg, rgba(23, 63, 53, 0.97), rgba(14, 33, 43, 0.95));
      color: #f8f3ea;
      position: relative;
      overflow: hidden;
    }

    .hero-side::after {
      content: "";
      position: absolute;
      right: -46px;
      bottom: -70px;
      width: 220px;
      height: 220px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(213, 133, 50, 0.34), transparent 68%);
    }

    .hero-side h2 {
      margin: 0 0 10px;
      color: rgba(248, 243, 234, 0.76);
      font-size: 1rem;
      font-weight: 600;
    }

    .hero-side strong {
      display: block;
      font-size: 2.3rem;
      line-height: 1.05;
      margin-bottom: 12px;
    }

    .hero-side p {
      margin: 0;
      color: rgba(248, 243, 234, 0.84);
      line-height: 1.75;
    }

    .app-grid {
      display: grid;
      grid-template-columns: 330px 1fr;
      gap: 24px;
    }

    .controls {
      padding: 24px;
      align-self: start;
      position: sticky;
      top: 20px;
    }

    .kicker {
      margin: 0 0 6px;
      color: var(--primary);
      font-size: 0.84rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .section-title {
      margin: 0 0 16px;
      font-size: 1.15rem;
      color: var(--text);
    }

    .step {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border-radius: 999px;
      margin-right: 10px;
      font-size: 0.88rem;
      color: white;
      background: linear-gradient(135deg, var(--accent), #e3b362);
    }

    .field {
      margin-bottom: 18px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 0.92rem;
    }

    select, input[type="number"] {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 13px 14px;
      font-size: 0.98rem;
      color: var(--text);
      background: rgba(255, 255, 255, 0.84);
    }

    .slider-wrap {
      padding: 16px 16px 14px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.56);
    }

    .slider-value {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 12px;
    }

    .slider-value strong {
      font-size: 1.6rem;
      color: var(--primary);
    }

    .slider-labels {
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 0.82rem;
      margin-top: 10px;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--accent);
    }

    button {
      width: 100%;
      padding: 14px 16px;
      border: none;
      border-radius: 16px;
      cursor: pointer;
      color: white;
      background: linear-gradient(135deg, var(--primary), #255f4e);
      box-shadow: 0 14px 30px rgba(23, 63, 53, 0.24);
      font-weight: 600;
      font-size: 0.98rem;
    }

    .hint, .status {
      color: var(--muted);
      line-height: 1.6;
      font-size: 0.9rem;
    }

    .status {
      min-height: 24px;
      margin-top: 12px;
      color: var(--primary);
    }

    .results {
      display: grid;
      gap: 24px;
    }

    .chart-card {
      padding: 24px;
    }

    .chart-head {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      margin-bottom: 14px;
    }

    .chart-copy {
      max-width: 60ch;
      color: var(--muted);
      line-height: 1.65;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px 16px;
      color: var(--muted);
      font-size: 0.88rem;
    }

    .legend span {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .swatch {
      width: 12px;
      height: 12px;
      border-radius: 999px;
      display: inline-block;
    }

    .chart-wrap {
      border-radius: 20px;
      padding: 12px;
      background: linear-gradient(180deg, rgba(255,255,255,0.7), rgba(247,242,233,0.84));
      border: 1px solid var(--line);
    }

    svg {
      width: 100%;
      height: auto;
      display: block;
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }

    .metric {
      padding: 22px;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.84rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .metric strong {
      display: block;
      font-size: 2rem;
      color: var(--primary);
      margin-bottom: 10px;
    }

    .metric p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: 0.92rem;
    }

    .explain-grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
    }

    .card {
      padding: 24px;
    }

    .story {
      line-height: 1.75;
      color: var(--muted);
    }

    .story strong {
      color: var(--text);
      display: block;
      margin-bottom: 10px;
      font-size: 1.16rem;
    }

    .alloc-table, .options-list {
      display: grid;
      gap: 12px;
    }

    .alloc-row {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr 0.9fr;
      gap: 10px;
      align-items: center;
      padding: 14px 16px;
      border-radius: 18px;
      background: rgba(23, 63, 53, 0.05);
      border: 1px solid rgba(23, 63, 53, 0.08);
    }

    .alloc-row.header {
      background: transparent;
      border: none;
      padding: 0 2px 4px;
      color: var(--muted);
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .asset-name {
      font-weight: 600;
    }

    .options-item {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid rgba(31, 95, 139, 0.12);
      background: rgba(31, 95, 139, 0.06);
      color: var(--muted);
    }

    .options-item.active {
      border-color: rgba(213, 133, 50, 0.36);
      background: var(--accent-soft);
      color: var(--text);
    }

    .footer {
      margin-top: 22px;
      text-align: center;
      color: var(--muted);
      font-size: 0.9rem;
    }

    a { color: var(--blue); }

    @media (max-width: 980px) {
      .hero, .app-grid, .metrics, .explain-grid {
        grid-template-columns: 1fr;
      }

      .controls {
        position: static;
      }

      .chart-head {
        flex-direction: column;
      }

      .alloc-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="panel hero-copy">
        <div class="eyebrow">위험-수익 구조 기반 데모</div>
        <h1>효율적 투자선<br />자산배분 시뮬레이터</h1>
        <p class="lead">
          이 데모의 핵심은 선택된 포트폴리오가 효율적 투자선 위의 한 점이라는 사실을
          직관적으로 보여주는 것입니다. 위험 수준을 바꾸면 점의 위치와 비중, 리스크 기여도가 함께 변합니다.
        </p>
        <div class="hero-note">
          본 서비스는 발표와 시연을 위한 데모입니다. 결과는 고정된 샘플 데이터를 기반으로 계산되며,
          시장 예측이나 투자 자문을 제공하지 않습니다.
        </div>
      </div>
      <div class="panel hero-side">
        <h2>데모 핵심</h2>
        <strong>먼저 구조를 보고,<br />그 다음 숫자를 봅니다.</strong>
        <p>
          차트, 선택된 포인트, 설명 카드가 같은 메시지를 반복합니다.
          이 포트폴리오는 샘플 자산군 안에서 위험 대비 가장 효율적인 구간 위에 놓여 있습니다.
        </p>
      </div>
    </section>

    <section class="app-grid">
      <aside class="panel controls">
        <p class="kicker"><span class="step">1</span>위험 선택</p>
        <h2 class="section-title">원하는 위험 수준을 정하세요</h2>
        <form id="portfolio-form">
          <div class="field slider-wrap">
            <div class="slider-value">
              <div>
                <label for="risk_slider">위험 슬라이더</label>
                <strong id="risk-label">균형형</strong>
              </div>
              <div id="slider-target">11.0% 목표 변동성</div>
            </div>
            <input id="risk_slider" type="range" min="0" max="100" step="1" value="50" />
            <div class="slider-labels">
              <span>안정형</span>
              <span>공격형</span>
            </div>
          </div>

          <div class="field">
            <label for="investment_horizon">Investment Horizon</label>
            <select id="investment_horizon" name="investment_horizon">
              <option value="short">단기</option>
              <option value="medium" selected>중기</option>
              <option value="long">장기</option>
            </select>
          </div>

          <div class="field">
            <label for="target_volatility">목표 변동성 직접 입력</label>
            <input id="target_volatility" name="target_volatility" type="number" step="0.01" min="0.03" max="0.25" placeholder="예: 0.11" />
          </div>

          <button type="submit">포트폴리오 다시 계산하기</button>
          <div id="status" class="status"></div>
        </form>

        <p class="hint">
          슬라이더를 움직이면 효율적 투자선 위에서 현재 포트폴리오 위치가 바뀝니다.
          필요하면 목표 변동성을 직접 숫자로 입력할 수도 있습니다.
        </p>
      </aside>

      <div class="results">
        <section class="panel chart-card">
          <p class="kicker"><span class="step">2</span>프론티어 보기</p>
          <div class="chart-head">
            <div>
              <h2 class="section-title">효율적 투자선 차트</h2>
              <div class="chart-copy" id="chart-copy">
                선택된 포트폴리오는 가능한 포트폴리오 점 구름 위쪽의 효율적 투자선 위에 표시됩니다.
              </div>
            </div>
            <div class="legend">
              <span><i class="swatch" style="background: rgba(31,95,139,0.28);"></i>가능한 포트폴리오</span>
              <span><i class="swatch" style="background: #173f35;"></i>효율적 투자선</span>
              <span><i class="swatch" style="background: #d58532;"></i>현재 포트폴리오</span>
            </div>
          </div>
          <div class="chart-wrap">
            <svg id="frontier-chart" viewBox="0 0 900 460" aria-label="효율적 투자선 차트"></svg>
          </div>
        </section>

        <section class="metrics">
          <div class="panel metric">
            <span>예상 수익률</span>
            <strong id="metric-return">-</strong>
            <p>샘플 데이터를 바탕으로 계산한 연율 기준 기대수익률입니다.</p>
          </div>
          <div class="panel metric">
            <span>변동성</span>
            <strong id="metric-vol">-</strong>
            <p>효율적 투자선 위 포트폴리오 위치를 결정하는 연율 기준 위험 수준입니다.</p>
          </div>
          <div class="panel metric">
            <span>샤프 지수</span>
            <strong id="metric-sharpe">-</strong>
            <p>위험을 감안한 상대적 효율을 비교하는 지표입니다.</p>
          </div>
        </section>

        <section class="explain-grid">
          <div class="panel card story">
            <p class="kicker"><span class="step">3</span>설명 보기</p>
            <strong id="explanation-title">왜 이런 포트폴리오가 나왔을까?</strong>
            <div id="explanation-body">
              첫 계산이 완료되면 이 위치에 설명이 표시됩니다.
            </div>
            <div style="margin-top: 16px;" id="summary"></div>
          </div>

          <div class="panel card">
            <p class="kicker"><span class="step">4</span>옵션 비교</p>
            <h2 class="section-title">효율적 투자선 옵션</h2>
            <div id="frontier-options" class="options-list"></div>
          </div>
        </section>

        <section class="explain-grid">
          <div class="panel card">
            <p class="kicker"><span class="step">5</span>자산배분</p>
            <h2 class="section-title">비중과 리스크 기여도</h2>
            <div class="alloc-table">
              <div class="alloc-row header">
                <div>자산군</div>
                <div>비중</div>
                <div>리스크 기여도</div>
              </div>
              <div id="allocations"></div>
            </div>
          </div>

          <div class="panel card">
            <p class="kicker">해석 포인트</p>
            <h2 class="section-title">어떻게 보면 좋을까</h2>
            <div class="story">
              비중은 자금이 어디에 배분되는지를 보여주고, 리스크 기여도는 실제 변동성이 어디에서 나오는지를 보여줍니다.
              효율적 자산배분에서는 이 둘이 다르게 나타날 수 있고, 그 차이를 이해하는 것이 이 데모의 중요한 포인트입니다.
            </div>
          </div>
        </section>
      </div>
    </section>

    <div class="footer">
      효율적 투자선 자산배분 시뮬레이터 · <a href="/docs">Swagger 문서</a>
    </div>
  </div>

  <script>
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
      sliderTarget.textContent = `${percent(clamped)} 목표 변동성`;
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
      allocationsEl.innerHTML = items.map((item) => `
        <div class="alloc-row">
          <div class="asset-name">${item.asset_name}</div>
          <div>${percent(item.weight)}</div>
          <div>${percent(item.risk_contribution)}</div>
        </div>
      `).join("");
    }

    function renderOptions(items, selectedPoint) {
      optionsEl.innerHTML = items.map((item) => {
        const active = Math.abs(item.volatility - selectedPoint.volatility) < 0.02 ? "active" : "";
        return `
          <div class="options-item ${active}">
            <strong>${item.label || "옵션"}</strong>
            <span>변동성 ${percent(item.volatility)}</span>
            <span>수익률 ${percent(item.expected_return)}</span>
          </div>
        `;
      }).join("");
    }

    function renderChart(data) {
      const margin = { top: 20, right: 24, bottom: 46, left: 60 };
      const width = 900;
      const height = 460;
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const allPoints = [
        ...data.random_portfolios,
        ...data.frontier,
        data.selected_point,
      ];

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

      const xTicks = 5;
      const yTicks = 5;

      let axes = "";
      for (let i = 0; i <= xTicks; i++) {
        const value = volMin + ((volMax - volMin) * i) / xTicks;
        const x = xScale(value);
        axes += `<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${margin.top + innerHeight}" stroke="rgba(24,33,30,0.08)" />`;
        axes += `<text x="${x}" y="${height - 14}" fill="#61706a" font-size="12" text-anchor="middle">${(value * 100).toFixed(1)}%</text>`;
      }
      for (let i = 0; i <= yTicks; i++) {
        const value = retMin + ((retMax - retMin) * i) / yTicks;
        const y = yScale(value);
        axes += `<line x1="${margin.left}" y1="${y}" x2="${margin.left + innerWidth}" y2="${y}" stroke="rgba(24,33,30,0.08)" />`;
        axes += `<text x="18" y="${y + 4}" fill="#61706a" font-size="12">${(value * 100).toFixed(1)}%</text>`;
      }

      const randomDots = data.random_portfolios.map((point) =>
        `<circle cx="${xScale(point.volatility)}" cy="${yScale(point.expected_return)}" r="3.2" fill="rgba(31,95,139,0.24)" />`
      ).join("");

      const frontierPath = data.frontier.map((point, index) =>
        `${index === 0 ? "M" : "L"} ${xScale(point.volatility)} ${yScale(point.expected_return)}`
      ).join(" ");

      const currentX = xScale(data.selected_point.volatility);
      const currentY = yScale(data.selected_point.expected_return);

      chartEl.innerHTML = `
        <rect x="${margin.left}" y="${margin.top}" width="${innerWidth}" height="${innerHeight}" fill="rgba(255,255,255,0.65)" rx="18" />
        ${axes}
        <path d="${frontierPath}" fill="none" stroke="#173f35" stroke-width="4" stroke-linecap="round" />
        ${randomDots}
        <circle cx="${currentX}" cy="${currentY}" r="8" fill="#d58532" stroke="#ffffff" stroke-width="4" />
        <text x="${currentX + 14}" y="${currentY - 14}" font-size="13" fill="#173f35" font-weight="700">현재 포트폴리오</text>
        <text x="${width / 2}" y="${height - 2}" text-anchor="middle" fill="#61706a" font-size="13">위험(변동성)</text>
        <text x="18" y="${height / 2}" text-anchor="middle" fill="#61706a" font-size="13" transform="rotate(-90 18 ${height / 2})">예상 수익률</text>
      `;
    }

    async function loadPortfolio() {
      statusEl.textContent = "효율적 투자선 위치를 계산하고 있습니다...";
      try {
        const payload = payloadFromInputs();
        const response = await fetch("/v1/portfolio/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "요청 처리에 실패했습니다.");
        }

        document.getElementById("metric-return").textContent = percent(data.metrics.expected_return);
        document.getElementById("metric-vol").textContent = percent(data.metrics.volatility);
        document.getElementById("metric-sharpe").textContent = data.metrics.sharpe_ratio.toFixed(2);
        explanationTitleEl.textContent = data.explanation.title;
        explanationBodyEl.textContent = data.explanation.body;
        summaryEl.textContent = `${data.summary} ${data.disclaimer}`;
        renderAllocations(data.allocations);
        renderOptions(data.frontier_options, data.selected_point);
        renderChart(data);
        statusEl.textContent = "포트폴리오 계산이 완료되었습니다.";
      } catch (error) {
        statusEl.textContent = error.message;
      }
    }

    slider.addEventListener("input", () => {
      suggestedVolatility();
      if (!targetVolInput.value.trim()) {
        loadPortfolio();
      }
    });
    horizonEl.addEventListener("change", loadPortfolio);

    document.getElementById("portfolio-form").addEventListener("submit", (event) => {
      event.preventDefault();
      loadPortfolio();
    });

    suggestedVolatility();
    loadPortfolio();
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)

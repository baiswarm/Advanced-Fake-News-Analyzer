document.addEventListener('DOMContentLoaded', () => {
  // ── DOM refs ───────────────────────────────────────────────────
  const form         = document.getElementById('analyze-form');
  const contentField = document.getElementById('content');
  const submitBtn    = document.getElementById('submit-btn');
  const resultBox    = document.getElementById('result');
  const errorBox     = document.getElementById('error');
  const errorText    = document.getElementById('error-text');
  const loading      = document.getElementById('loading');
  const charCount    = document.getElementById('char-count');

  // Result elements
  const verdictBadge = document.getElementById('verdict-badge');
  const verdictIcon  = document.getElementById('verdict-icon');
  const verdictLabel = document.getElementById('verdict-label');
  const gaugeValue   = document.getElementById('gauge-value');
  const gaugeFill    = document.getElementById('gauge-fill');
  const gaugeNeedle  = document.getElementById('gauge-needle');
  const barFake      = document.getElementById('bar-fake');
  const barReal      = document.getElementById('bar-real');
  const pctFake      = document.getElementById('pct-fake');
  const pctReal      = document.getElementById('pct-real');
  const metaType     = document.getElementById('meta-type');
  const metaTime     = document.getElementById('meta-time');

  // ── Char counter ───────────────────────────────────────────────
  contentField.addEventListener('input', () => {
    const n = contentField.value.length;
    charCount.textContent = n === 1 ? '1 character' : `${n.toLocaleString()} characters`;
  });

  // ── Gauge helpers ──────────────────────────────────────────────
  // The gauge arc spans a half-circle (π · r = π · 55 ≈ 172.8 px of arc).
  const GAUGE_ARC_LEN = Math.PI * 55;

  function setGauge(pct, isFake) {
    const offset = GAUGE_ARC_LEN * (1 - pct / 100);
    gaugeFill.style.strokeDasharray  = `${GAUGE_ARC_LEN}`;
    gaugeFill.style.strokeDashoffset = `${offset}`;
    gaugeFill.style.stroke  = isFake ? 'var(--fake)' : 'var(--real)';
    gaugeFill.style.filter  = isFake
      ? 'drop-shadow(0 0 4px rgba(245,158,11,0.7))'
      : 'drop-shadow(0 0 4px rgba(16,185,129,0.7))';

    // Needle: -90deg (left, 0%) to +90deg (right, 100%)
    const angle = -90 + (pct / 100) * 180;
    gaugeNeedle.style.transform = `rotate(${angle}deg)`;

    gaugeValue.textContent = `${pct}%`;
    gaugeValue.style.color = isFake ? 'var(--fake)' : 'var(--real)';
  }

  // ── Form submit ────────────────────────────────────────────────
  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    resultBox.classList.add('hidden');
    errorBox.classList.add('hidden');

    const type    = form.querySelector('input[name="type"]:checked').value;
    const content = contentField.value.trim();

    if (!content) {
      showError('Please enter some text or a URL before running the analysis.');
      return;
    }

    loading.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-icon').innerHTML = `
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"
          stroke-dasharray="30" stroke-dashoffset="10"
          style="animation:spin .8s linear infinite;transform-origin:center"/>
      </svg>`;

    try {
      // Same-origin proxy route — the browser never sees or sends the
      // server's API key. /api/analyze (which does require the key) stays
      // reserved for external/programmatic clients.
      const response = await fetch('/web/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, content }),
      });

      const data = await response.json();

      if (!response.ok) {
        showError(data.error || 'Something went wrong. Please try again.');
        return;
      }

      showResult(data, type);

    } catch (err) {
      showError('Could not reach the server. Please check your connection and try again.');
    } finally {
      loading.classList.add('hidden');
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-icon').innerHTML = `
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.4"/>
          <path d="M5.5 8l1.8 1.8L10.5 6" stroke="currentColor" stroke-width="1.4"
            stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    }
  });

  // ── showResult ─────────────────────────────────────────────────
  function showResult(data, inputType) {
    const isFake     = String(data.prediction).toLowerCase().includes('fake');
    const confidence = Number(data.confidence) || 0;
    const fakePct    = Number(data.probabilities?.fake) || 0;
    const realPct    = Number(data.probabilities?.real) || 0;

    // Verdict badge
    verdictBadge.className      = 'verdict-badge ' + (isFake ? 'is-fake' : 'is-real');
    verdictIcon.textContent     = isFake ? '⚠' : '✔';
    verdictLabel.textContent    = isFake ? 'LIKELY FAKE' : 'LIKELY REAL';

    // Gauge — reset then animate on next paint
    setGauge(0, isFake);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => setGauge(confidence, isFake));
    });

    // Probability bars — reset then animate on next paint
    pctFake.textContent = fakePct + '%';
    pctReal.textContent = realPct + '%';
    barFake.style.width = '0%';
    barReal.style.width = '0%';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        barFake.style.width = fakePct + '%';
        barReal.style.width = realPct + '%';
      });
    });

    // Meta
    metaType.textContent = inputType === 'url' ? 'URL (fetched)' : 'Plain text';
    metaTime.textContent = new Date().toLocaleTimeString([], {
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });

    resultBox.classList.remove('hidden');
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // ── showError ──────────────────────────────────────────────────
  function showError(message) {
    errorText.textContent = message;
    errorBox.classList.remove('hidden');
    errorBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
});
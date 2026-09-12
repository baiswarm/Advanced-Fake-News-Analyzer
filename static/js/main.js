document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('analyze-form');
  const contentField = document.getElementById('content');
  const submitBtn = document.getElementById('submit-btn');
  const resultBox = document.getElementById('result');
  const errorBox = document.getElementById('error');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    resultBox.classList.add('hidden');
    errorBox.classList.add('hidden');
    resultBox.innerHTML = '';
    errorBox.textContent = '';

    const type = form.querySelector('input[name="type"]:checked').value;
    const content = contentField.value.trim();

    if (!content) {
      showError('Please enter some text or a URL.');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing...';

    try {
      // Same-origin proxy route - the browser never sees or sends the
      // server's API key. /api/analyze (which does require the key) stays
      // reserved for external/programmatic clients.
      const response = await fetch('/web/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type, content }),
      });

      const data = await response.json();

      if (!response.ok) {
        showError(data.error || 'Something went wrong. Please try again.');
        return;
      }

      showResult(data);
    } catch (err) {
      showError('Could not reach the server. Please try again.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Analyze';
    }
  });

  function showResult(data) {
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = `
      <h2>${data.prediction}</h2>
      <p>Confidence: ${data.confidence}%</p>
      <p>Fake probability: ${data.probabilities.fake}% &middot; Real probability: ${data.probabilities.real}%</p>
    `;
  }

  function showError(message) {
    errorBox.classList.remove('hidden');
    errorBox.textContent = message;
  }
});

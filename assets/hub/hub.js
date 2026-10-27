(() => {
  const search = document.querySelector('#article-search');
  if (search) {
    const topic = document.querySelector('#topic-select');
    const buttons = [...document.querySelectorAll('[data-hub-category]')];
    const cards = [...document.querySelectorAll('.hub-card,.legacy-note')];
    const params = new URLSearchParams(location.search);
    let category = params.get('category') || '';
    search.value = params.get('q') || '';
    topic.value = params.get('topic') || '';
    if (!buttons.some(b => b.dataset.hubCategory === category)) category = '';
    function filter(updateURL = true) {
      const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const text = card.dataset.search || card.textContent.toLowerCase();
        const topicMatch = !topic.value || card.dataset.topic === topic.value || (topic.value === 'Supervised Learning' && card.dataset.topic === 'Regression');
        const match = (!category || card.dataset.category === category) && topicMatch && terms.every(t => text.includes(t));
        card.hidden = !match;
        count += Number(match);
      });
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.hubCategory === category)));
      document.querySelector('#hub-results').textContent = `${count} ${count === 1 ? 'article' : 'articles'}`;
      document.querySelector('#hub-empty').hidden = count !== 0;
      document.querySelector('.legacy-notes').hidden = !cards.some(c => c.classList.contains('legacy-note') && !c.hidden);
      if (updateURL) {
        const next = new URLSearchParams();
        if (category) next.set('category', category);
        if (topic.value) next.set('topic', topic.value);
        if (search.value) next.set('q', search.value);
        history.replaceState(null, '', location.pathname + (next.size ? '?' + next : '') + location.hash);
      }
    }
    buttons.forEach(b => b.addEventListener('click', () => { category = b.dataset.hubCategory; filter(); }));
    search.addEventListener('input', () => filter());
    topic.addEventListener('change', () => filter());
    document.querySelector('.hub-search').addEventListener('submit', e => e.preventDefault());
    document.querySelector('.hub-search').addEventListener('reset', () => { category = ''; search.value = ''; topic.value = ''; filter(); });
    function openLegacy() {
      const entry = cards.find(c => c.classList.contains('legacy-note') && '#' + c.id === location.hash);
      if (entry) { category = ''; search.value = ''; topic.value = ''; filter(); entry.open = true; entry.scrollIntoView({block: 'start'}); }
    }
    filter(false);
    openLegacy();
    window.addEventListener('hashchange', openLegacy);
    window.addEventListener('popstate', () => {
      const p = new URLSearchParams(location.search);
      category = p.get('category') || ''; search.value = p.get('q') || ''; topic.value = p.get('topic') || '';
      filter(false); openLegacy();
    });
  }
  document.querySelectorAll('.math').forEach(node => {
    if (window.katex) window.katex.render(node.textContent, node, {displayMode:true, throwOnError:false, output:'htmlAndMathml', strict:'warn'});
  });
  // Small Python lexer: text nodes are escaped before markup is inserted.
  const escape = text => text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  document.querySelectorAll('.language-python').forEach(code => {
    const source = code.textContent;
    code.dataset.source = source;
    const tokens = /(#.*$|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:import|from|as|def|return|for|in|if|else|elif|while|break|raise|assert|with|True|False|None|and|or|not)\b|\b\d+(?:\.\d+)?(?:e[-+]?\d+)?\b)/gm;
    let cursor = 0, result = '';
    for (const match of source.matchAll(tokens)) {
      result += escape(source.slice(cursor, match.index));
      const t = match[0], type = t.startsWith('#') ? 'comment' : /^["']/.test(t) ? 'string' : /^\d/.test(t) ? 'number' : 'keyword';
      result += `<span class="py-${type}">${escape(t)}</span>`;
      cursor = match.index + t.length;
    }
    code.innerHTML = result + escape(source.slice(cursor));
  });
  document.querySelectorAll('.copy-code').forEach(button => button.addEventListener('click', async () => {
    const code = button.parentElement.querySelector('code');
    try { await navigator.clipboard.writeText(code.dataset.source || code.textContent); button.textContent = 'Copied'; }
    catch { const range = document.createRange(); range.selectNodeContents(code); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); button.textContent = 'Code selected — copy manually'; }
    setTimeout(() => { button.textContent = 'Copy code'; }, 2500);
  }));
  const tutorial = document.querySelector('.tutorial');
  if (tutorial) {
    const bar = document.querySelector('.reading-progress');
    let queued = false;
    function progress() {
      const start = tutorial.getBoundingClientRect().top + window.scrollY;
      const distance = tutorial.offsetHeight - window.innerHeight;
      bar.style.width = `${Math.max(0, Math.min(1, (window.scrollY - start) / Math.max(1,distance))) * 100}%`;
      queued = false;
    }
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(progress); } }, {passive:true});
    window.addEventListener('resize', progress); progress();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) {
        document.querySelectorAll('.toc a').forEach(a => a.removeAttribute('aria-current'));
        document.querySelector(`.toc a[href="#${entry.target.id}"]`)?.setAttribute('aria-current','true');
      } });
    }, {rootMargin:'0px 0px -70% 0px'});
    tutorial.querySelectorAll('h2[id]').forEach(h => observer.observe(h));
  }
})();

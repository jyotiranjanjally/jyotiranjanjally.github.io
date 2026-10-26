const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open menu');
  nav.classList.remove('is-open');
}
menuButton.addEventListener('click', () => {
  const opening = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(opening));
  menuButton.setAttribute('aria-label', opening ? 'Close menu' : 'Open menu');
  nav.classList.toggle('is-open', opening);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
window.matchMedia('(min-width: 681px)').addEventListener('change', closeMenu);
document.querySelector('#year').textContent = new Date().getFullYear();

const modules = {
  data: {
    number: '01', title: 'Start with the right data.',
    description: 'Make the prediction task and its inputs explicit.',
    steps: [
      ['Define the problem', 'Specify the target and what is known at prediction time.'],
      ['Check the inputs', 'Inspect schema, missing values, duplicates, and label quality.'],
      ['Separate evaluation data', 'Design the split before learning transformations.']
    ],
    outcome: 'Useful inputs. A credible evaluation boundary.'
  },
  model: {
    number: '02', title: 'Make the experiment meaningful.',
    description: 'Compare model behaviour against a clear reference point.',
    steps: [
      ['Establish a baseline', 'Choose a simple comparison and a relevant metric.'],
      ['Track the experiment', 'Record the data, preprocessing, and model configuration.'],
      ['Inspect failure cases', 'Look beyond the headline score to the errors that matter.']
    ],
    outcome: 'Comparable experiments. Understandable trade-offs.'
  },
  application: {
    number: '03', title: 'Connect the model to the product.',
    description: 'Design for the user and the surrounding software system.',
    steps: [
      ['Define the interface', 'Make inputs, outputs, and error handling explicit.'],
      ['Integrate the workflow', 'Connect inference, tools, and the application experience.'],
      ['Observe & improve', 'Inspect behaviour and use the evidence for the next iteration.']
    ],
    outcome: 'Useful software. Observable behaviour. A clear feedback loop.'
  }
};
const tabs = [...document.querySelectorAll('[data-module]')];
function selectModule(tab) {
  const module = modules[tab.dataset.module];
  tabs.forEach(item => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
  });
  document.querySelector('#module-panel').setAttribute('aria-labelledby', tab.id);
  document.querySelector('.module-number').textContent = module.number;
  document.querySelector('#module-title').textContent = module.title;
  document.querySelector('#module-description').textContent = module.description;
  document.querySelector('#module-pipeline').replaceChildren(...module.steps.map((step, index) => {
    const li = document.createElement('li');
    const number = document.createElement('span'); number.textContent = String(index + 1).padStart(2, '0');
    const text = document.createElement('div');
    const title = document.createElement('strong'); title.textContent = step[0];
    const description = document.createElement('p'); description.textContent = step[1];
    text.append(title, description); li.append(number, text); return li;
  }));
  document.querySelector('#module-outcome').textContent = module.outcome;
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectModule(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectModule(tabs[next]); tabs[next].focus(); }
  });
});

const cases = {
  ocr: {
    kicker: '01 / IMAGE-TO-TEXT ML',
    title: 'From pixels to usable text.',
    summary: 'An image-to-text ML model developed and deployed within an internal test automation workflow.',
    sections: [
      ['THE APPLICATION', 'Extract text from image inputs and connect the model output to an existing software workflow. The work brought applied machine learning into a practical automation use case.'],
      ['MY CONTRIBUTION', 'Designed and deployed the image-to-text model and integrated its output into the surrounding automation.'],
      ['THE ENGINEERING LENS', 'Model development and application integration belong to the same story. The model output becomes useful when the surrounding system can consume it consistently.'],
      ['PROJECT SCOPE', 'The portfolio summarises the implementation at a high level. The image-to-text example shown on this page is illustrative; no model accuracy, latency, or training-dataset claims are implied.']
    ],
    callout: 'Applied ML becomes useful through its connection to a real software workflow.'
  },
  agent: {
    kicker: '02 / AGENTIC AI LAB',
    title: 'A model with a useful toolkit.',
    summary: 'A Python and Streamlit prototype connecting Llama 3.2 with Tavily search and Weatherstack tools.',
    sections: [
      ['THE IDEA', 'Explore how a local language model can interact with external tools through a simple application interface.'],
      ['THE COMPONENTS', ['Llama 3.2 for the language-model component.', 'Tavily for search and Weatherstack for weather information.', 'Streamlit for the application interface.']],
      ['THE DEVELOPMENT QUESTION', 'The lab surfaced an iteration-limit issue. It provides a concrete opportunity to inspect repeated tool use, define completion, and make execution behaviour easier to understand.'],
      ['STATUS', 'Experimental prototype. The portfolio illustration is a conceptual view and does not make live model or tool requests.']
    ],
    callout: 'Tool access is one part of the application. Execution boundaries and a useful stopping rule deserve equal attention.'
  },
  data: {
    kicker: '03 / DATA + MODEL VALIDATION',
    title: 'Better inputs. Stronger foundations.',
    summary: 'Engineering work across Python data generation, ETL automation, database checks, and support for ML validation.',
    sections: [
      ['THE FOUNDATION', 'Data-intensive systems depend on more than a successful request. Data generation, transformation, and validation help make downstream behaviour inspectable.'],
      ['MY CONTRIBUTION', ['Developed Python scripts for test-data generation supporting ML validation.', 'Worked with data science teams to validate AI-powered models within QA pipelines.', 'Built ETL automation and database validation capabilities.']],
      ['WHY IT MATTERS FOR ML', 'These capabilities bring a software engineering perspective to the inputs, interfaces, and evidence surrounding a model. They complement model development with repeatable validation.'],
      ['EXPERIENCE CONTEXT', 'This work comes from software quality and automation roles. Those roles are listed with their original titles in the career timeline.']
    ],
    callout: 'A useful model starts with data and a surrounding system that deserve the same engineering attention.'
  }
};
const dialog = document.querySelector('#case-dialog');
let caseTrigger;
function openCase(key, trigger) {
  const detail = cases[key];
  if (!detail) return;
  caseTrigger = trigger;
  document.querySelector('#case-kicker').textContent = detail.kicker;
  document.querySelector('#case-title').textContent = detail.title;
  document.querySelector('#case-summary').textContent = detail.summary;
  const sections = detail.sections.map(([heading, content]) => {
    const section = document.createElement('section'); section.className = 'case-section';
    const title = document.createElement('h3'); title.textContent = heading; section.append(title);
    if (Array.isArray(content)) {
      const list = document.createElement('ul');
      content.forEach(text => { const item = document.createElement('li'); item.textContent = text; list.append(item); });
      section.append(list);
    } else { const p = document.createElement('p'); p.textContent = content; section.append(p); }
    return section;
  });
  const callout = document.createElement('p'); callout.className = 'case-callout'; callout.textContent = detail.callout;
  document.querySelector('#case-body').replaceChildren(...sections, callout);
  dialog.showModal(); dialog.scrollTop = 0; document.body.classList.add('dialog-open');
}
document.querySelectorAll('[data-case]').forEach(button => button.addEventListener('click', () => openCase(button.dataset.case, button)));
document.querySelectorAll('.close-dialog,.close-case').forEach(button => button.addEventListener('click', () => dialog.close()));
dialog?.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } });
dialog?.addEventListener('close', () => { document.body.classList.remove('dialog-open'); caseTrigger?.focus(); });

// The articles page is a static reading surface with topic filters and shareable anchors.
const articleEntries = [...document.querySelectorAll('.article-entry')];
const articleFilters = [...document.querySelectorAll('[data-filter]')];
function filterArticles(category) {
  let count = 0;
  articleEntries.forEach(entry => {
    entry.hidden = category !== 'all' && entry.dataset.category !== category;
    if (!entry.hidden) count++;
  });
  articleFilters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  const countLabel = document.querySelector('#article-count');
  if (countLabel) countLabel.textContent = `${count} ${count === 1 ? 'article' : 'articles'}`;
}
articleFilters.forEach(button => button.addEventListener('click', () => filterArticles(button.dataset.filter)));
function openLinkedArticle() {
  const entry = articleEntries.find(item => '#' + item.id === window.location.hash);
  if (entry) { filterArticles('all'); entry.open = true; entry.scrollIntoView({block:'start'}); }
}
window.addEventListener('hashchange', openLinkedArticle);
openLinkedArticle();

const themeToggle = document.querySelector('.theme-toggle');
const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)');
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const label = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
  themeToggle?.setAttribute('aria-label', label);
  themeToggle?.setAttribute('title', label);
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#171717' : '#f5f4f1');
}
applyTheme(document.documentElement.dataset.theme || 'light');
themeToggle?.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(theme);
  try { localStorage.setItem('portfolio-theme', theme); } catch {}
});
preferredTheme.addEventListener('change', event => {
  try { if (localStorage.getItem('portfolio-theme')) return; } catch {}
  applyTheme(event.matches ? 'dark' : 'light');
});
window.addEventListener('storage', event => { if (event.key === 'portfolio-theme') applyTheme(event.newValue || (preferredTheme.matches ? 'dark' : 'light')); });

"use strict";

// Static HTML is the fallback. Each enhancement exposes its controls only after
// its handlers and initial state are ready; a failed enhancement leaves content.
const header = document.querySelector('.nav');
const updateAnchorOffset = () => {
  if (!header) return;
  const sticky = getComputedStyle(header).position === 'sticky';
  const offset = sticky ? Math.ceil(header.getBoundingClientRect().height) + 20 : 16;
  document.documentElement.style.setProperty('--anchor-offset', `${offset}px`);
};
try {
  updateAnchorOffset();
  window.addEventListener('resize', updateAnchorOffset);
  if (header && 'ResizeObserver' in window) new ResizeObserver(updateAnchorOffset).observe(header);
} catch {
  // CSS supplies a header offset even if this optional measurement is unavailable.
}

for (const group of document.querySelectorAll('[data-tabs]')) {
  const bar = group.querySelector('.tabbar');
  const buttons = [...group.querySelectorAll('.tabbar button[aria-controls]')];
  const panels = [...group.querySelectorAll('.tabpanel')];
  if (!bar || buttons.length < 2 || buttons.length !== panels.length) continue;
  const matches = buttons.map(button => panels.find(panel => panel.id === button.getAttribute('aria-controls')));
  if (matches.some(panel => !panel) || new Set(matches).size !== panels.length) continue;

  const reset = () => {
    bar.hidden = true;
    bar.removeAttribute('role');
    group.classList.remove('tabs-ready');
    for (const button of buttons) {
      button.removeAttribute('role');
      button.removeAttribute('aria-selected');
      button.removeAttribute('tabindex');
    }
    for (const panel of panels) {
      panel.hidden = false;
      panel.removeAttribute('role');
      panel.removeAttribute('tabindex');
      panel.removeAttribute('aria-labelledby');
    }
  };
  const select = (button) => {
    for (const candidate of buttons) {
      const selected = candidate === button;
      candidate.setAttribute('aria-selected', String(selected));
      candidate.tabIndex = selected ? 0 : -1;
    }
    for (const panel of panels) panel.hidden = panel.id !== button.getAttribute('aria-controls');
  };
  const selectFragment = () => {
    const target = document.getElementById(window.location.hash.slice(1));
    const panel = panels.find(candidate => candidate === target || candidate.contains(target));
    const button = panel ? buttons.find(candidate => candidate.getAttribute('aria-controls') === panel.id)
      : buttons.find(candidate => candidate === target);
    if (button) select(button);
  };

  try {
    for (const [index, button] of buttons.entries()) {
      button.setAttribute('role', 'tab');
      matches[index].setAttribute('role', 'tabpanel');
      matches[index].setAttribute('aria-labelledby', button.id);
      matches[index].tabIndex = 0;
      button.addEventListener('click', () => select(button));
      button.addEventListener('keydown', (event) => {
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = buttons.length - 1;
        else return;
        event.preventDefault();
        select(buttons[next]);
        buttons[next].focus();
      });
    }
    select(buttons[0]);
    selectFragment();
    window.addEventListener('hashchange', selectFragment);
    bar.setAttribute('role', 'tablist');
    group.classList.add('tabs-ready');
    bar.hidden = false;
  } catch {
    reset();
  }
}

// The cue follows measured content overflow, including a newly opened disclosure.
const tableRegions = [...document.querySelectorAll('.table-wrap[data-scroll-hint]')];
const updateTableOverflow = () => {
  for (const region of tableRegions) {
    const hint = document.getElementById(region.dataset.scrollHint);
    if (!hint) continue;
    const overflowing = region.clientWidth > 0 && region.scrollWidth > region.clientWidth + 1;
    hint.hidden = !overflowing;
    if (overflowing) region.setAttribute('aria-describedby', hint.id);
    else region.removeAttribute('aria-describedby');
  }
};
try {
  updateTableOverflow();
  window.addEventListener('resize', updateTableOverflow);
  window.addEventListener('load', updateTableOverflow);
  document.addEventListener('toggle', updateTableOverflow, true);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(updateTableOverflow);
    for (const region of tableRegions) {
      observer.observe(region);
      if (region.firstElementChild) observer.observe(region.firstElementChild);
    }
  }
  if (document.fonts) document.fonts.ready.then(updateTableOverflow);
} catch {
  // Tables remain native, labelled, focusable scroll regions without measurement.
}

const table = document.getElementById('ranking-table');
const filters = document.querySelector('[data-ranking-filters]');
if (table && filters) {
  const buttons = [...filters.querySelectorAll('[data-filter]')];
  const rows = [...table.querySelectorAll('tbody tr')];
  const status = document.getElementById('ranking-status');
  const filter = (button) => {
    const kind = button.dataset.filter;
    for (const candidate of buttons) candidate.setAttribute('aria-pressed', String(candidate === button));
    for (const row of rows) row.hidden = kind !== 'all' && row.dataset.kind !== kind;
    const visible = rows.filter(row => !row.hidden).length;
    if (status) status.textContent = kind === 'all'
      ? `Showing all ${rows.length} configurations.`
      : `Showing ${visible} ${kind === 'cloud' ? 'hosted' : 'local'} configurations of ${rows.length}. Original ranks are retained.`;
    updateTableOverflow();
  };
  try {
    const all = buttons.find(button => button.dataset.filter === 'all');
    if (all && rows.length) {
      for (const button of buttons) button.addEventListener('click', () => filter(button));
      filter(all);
      filters.hidden = false;
    }
  } catch {
    filters.hidden = true;
    for (const row of rows) row.hidden = false;
    if (status) status.textContent = `Showing all ${rows.length} configurations.`;
  }
}

// Close the version menu on Escape or on a click elsewhere; it works without this too.
try {
  const menus = [...document.querySelectorAll('details.version-switch')];
  document.addEventListener('click', event => {
    for (const menu of menus) if (!menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    for (const menu of menus) if (menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
  });
} catch {
  // The menu stays a plain disclosure.
}

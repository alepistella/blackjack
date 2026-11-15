// Progressive enhancement only: every post is readable without JavaScript.
// Select one film before playback. Keep that source when rotating/resizing so a
// playing film is not restarted and the other rendition is not downloaded.
if (window.matchMedia('(max-width: 700px)').matches) {
  for (const video of document.querySelectorAll('video[data-portrait-src]')) {
    const source = video.querySelector('source');
    source.src = video.dataset.portraitSrc;
    video.poster = video.dataset.portraitPoster;
    video.width = 1080;
    video.height = 1350;
    video.classList.add('portrait-film');
    video.load();
  }
}
const search = document.querySelector('#search');
const category = document.querySelector('#category');
const items = [...document.querySelectorAll('[data-post]')];
if (search && category) {
  document.querySelector('.filters').hidden = false;
  const update = () => {
    const q = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const item of items) {
      const show = item.dataset.search.includes(q) && (!category.value || item.dataset.category === category.value);
      item.hidden = !show;
      if (show) count++;
    }
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'note' : 'notes'}`;
    document.querySelector('#empty').hidden = count !== 0;
  };
  search.addEventListener('input', update);category.addEventListener('change', update);update();
}
// Theme switch is confined to the component reference. Project pages keep their theme.
for (const button of document.querySelectorAll('[data-set-theme]')) {
  button.addEventListener('click', () => {
    document.documentElement.dataset.theme = button.dataset.setTheme;
    for (const other of document.querySelectorAll('[data-set-theme]')) other.setAttribute('aria-pressed', String(other === button));
  });
}

'use strict';
const input = document.querySelector('#url-input');
const content = document.querySelector('#result-content');
const resultPanel = document.querySelector('#result-panel');
const counter = document.querySelector('#char-count');
const sampleButtons = document.querySelector('#sample-buttons');
function updateCount() {counter.textContent = Array.from(input.value.trim()).length + ' characters';}
input.addEventListener('input', updateCount);
function element(tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}
function check() {
  const result = LinkLens.inspect(input.value);
  content.replaceChildren();
  content.className = '';
  resultPanel.classList.add('has-results');
  if (result.warnings.length) {
    const head = element('div','','result-head');
    head.append(element('h2','Review carefully.'),element('span',result.warnings.length + ' sign' + (result.warnings.length === 1 ? '' : 's'),'count-badge'));
    content.append(head,element('p','Here’s what stands out in the URL text.','result-intro'));
    result.warnings.forEach((warning, i) => {
      const item = element('article','','finding');
      item.append(element('h3',String(i+1).padStart(2,'0') + ' / ' + warning.message),element('p',warning.explanation));
      content.append(item);
    });
  } else {
    content.append(element('h2',result.notice.startsWith('No listed') ? 'No listed signs found.' : 'Check your input.','result-head'));
    content.append(element('p',result.notice,'result-notice'));
  }
  if (result.assumedHttp) content.append(element('p','No scheme separator supplied: assumed http:// for parsing.','assumption'));
  content.append(element('p','Awareness only. These clues do not prove a URL safe or malicious. Never enter passwords from unexpected links.','result-caution'));
}
document.querySelector('#checker-form').addEventListener('submit', event => {event.preventDefault();check();});
LinkLens.samples.forEach(([label, url]) => {
  const button = element('button',label,'sample');
  button.type = 'button';
  button.title = url;
  button.addEventListener('click', () => {input.value = url;updateCount();check();});
  sampleButtons.append(button);
});

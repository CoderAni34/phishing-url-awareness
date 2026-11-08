/* Local text heuristics adapted from the EWB Python workbook. No URL is fetched. */
(function (root) {
  'use strict';
  const signs = [
    {code:'at',message:'Contains an @ symbol; inspect carefully.',explanation:'Before @ in the authority, text is user information, not the destination. This broad check also flags @ in a path or query.'},
    {code:'long',message:'Unusually long URL (over 100 characters).',explanation:'Long text can make a destination harder to read. Honest links can be long too.'},
    {code:'ip',message:'Uses an IP address instead of a familiar domain.',explanation:'A numeric-looking host can obscure identity. This workbook rule matches IPv4-style text, not valid IP ranges or IPv6.'},
    {code:'segments',message:'Contains many hostname segments/subdomains.',explanation:'Five or more hostname parts can make a link confusing. Legitimate services may also use many parts.'},
    {code:'punycode',message:'Contains a punycode-style hostname.',explanation:'The xn-- marker can represent international names, including look-alike letters. These names also have legitimate uses.'},
    {code:'http',message:'Uses HTTP. HTTPS alone does not prove trust.',explanation:'HTTP does not encrypt traffic. HTTPS encryption alone does not establish honesty.'}
  ];
  const samples = [
    ['No listed signs','https://www.example.com/login'],
    ['IP + HTTP','http://192.0.2.10/account'],
    ['@ symbol','http://example.com@sample.invalid/login'],
    ['Many parts','https://a.b.c.d.e.example.invalid/path'],
    ['Punycode','https://xn--example.invalid/']
  ];
  function inspect(raw) {
    const url = raw.trim();
    const result = {warnings:[],notice:'',assumedHttp:false};
    if (!url) {result.notice='No URL entered.'; return result;}
    result.assumedHttp = !url.includes('://');
    const candidate = (result.assumedHttp ? 'http://' : '') + url;
    // Avoid the browser URL constructor: it normalizes numeric hosts and IDNs,
    // which would silently change these workbook text rules.
    const cleaned = candidate.replace(/[\t\r\n]/g,'').replace(/^[\u0000-\u0020]+/,'');
    const match = /^([a-z][a-z0-9+.-]*):\/\/([^/?#]*)/i.exec(cleaned);
    if (!match) {result.notice='Could not identify a hostname.'; return result;}
    const authority = match[2];
    const normalized = authority.replace(/[@:#?]/g, '').normalize('NFKC');
    if (/[/?#@:]/.test(normalized)) {
      result.notice='This text is not a valid URL format.'; return result;
    }
    let host = authority.slice(authority.lastIndexOf('@') + 1);
    if (host.includes('[') || host.includes(']')) {
      const bracketed = /^\[([^\]]+)\](?::[^:]*)?$/.exec(host);
      if (!bracketed || !validBracketHost(bracketed[1])) {
        result.notice='This text is not a valid URL format.'; return result;
      }
      host = bracketed[1];
    } else {host = host.split(':')[0];}
    host = host.toLowerCase();
    if (!host) {result.notice='Could not identify a hostname.'; return result;}
    const found = [candidate.includes('@'),Array.from(url).length > 100,/^(?:\d{1,3}\.){3}\d{1,3}$/.test(host),host.split('.').filter(Boolean).length >= 5,host.includes('xn--'),match[1].toLowerCase() === 'http'];
    result.warnings = signs.filter((_, i) => found[i]);
    if (!result.warnings.length) result.notice='No listed warning signs found. This does NOT prove safety.';
    return result;
  }
  function validBracketHost(host) {
    if (/^v[0-9a-f]+\..+$/i.test(host)) return true;
    if (!host.includes(':')) return false;
    try {new URL('http://[' + host + ']/');return true;} catch (_) {return false;}
  }
  const api = {inspect,samples};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.LinkLens = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);

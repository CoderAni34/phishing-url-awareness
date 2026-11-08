const assert = require('node:assert/strict');
const {inspect,samples} = require('../docs/rules.js');
const codes = url => inspect(url).warnings.map(w => w.code);
const cases = [
  [samples[0][1],[]], [samples[1][1],['ip','http']],
  [samples[2][1],['at','http']], [samples[3][1],['segments']],
  [samples[4][1],['punycode']],
  ['https://example.com/'.padEnd(100,'a'),[]],
  ['https://example.com/'.padEnd(101,'a'),['long']],
  ['  '+'https://example.com/'.padEnd(100,'a')+'  ',[]],
  ['https://a.b.example.invalid',[]],
  ['https://a.b.c.example.invalid',['segments']],
  ['https://a..b.example.invalid.',[]],
  ['https://example.com/a@b',['at']],
  ['https://example.com/192.0.2.10',[]],
  ['https://999.999.999.999/',['ip']],
  ['https://[2001:db8::1]/',[]],
  ['https://example.com/xn--example',[]],
  ['https://prefix-xn--example.invalid/',['punycode']],
  ['HTTP://XN--example.invalid/',['punycode','http']],
  ['www.example.com',['http']],
  ['http://example.com@1.2.3.4.5.xn--example.invalid/'+'a'.repeat(101),['at','long','segments','punycode','http']]
];
for (const [url, expected] of cases) assert.deepEqual(codes(url),expected,url);
assert.equal(inspect(' \t\n').notice,'No URL entered.');
assert.equal(inspect('https:///login').notice,'Could not identify a hostname.');
assert.equal(inspect('http://[bad').notice,'This text is not a valid URL format.');
assert.equal(inspect('http://example.com\uff0fpath').notice,'This text is not a valid URL format.');
assert.equal(inspect('www.example.com').assumedHttp,true);
console.log('25 browser-rule checks passed, including all 5 exact workbook samples.');

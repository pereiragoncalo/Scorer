const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
let store = {}, mails = [], quota = 100, mailFailure = false;
const context = {
  ContentService: {MimeType:{JSON:'json'},createTextOutput(text){return {text,setMimeType(){return this}}}},
  Utilities:{formatDate(_,__,format){return format === 'yyyy-MM-dd' ? '2026-10-26' : '2026-10-26 21:00'}},
  PropertiesService:{getScriptProperties(){return {getProperty(k){return store[k]},setProperty(k,v){store[k]=v}}}},
  LockService:{getScriptLock(){return {tryLock(){return true},releaseLock(){}}}},
  MailApp:{getRemainingDailyQuota(){return quota},sendEmail(message){if(mailFailure)throw Error('offline');mails.push(message)}},
};
vm.createContext(context);vm.runInContext(fs.readFileSync('server/apps_script/Code.gs','utf8'),context);
function post(counts,extra={}) {return JSON.parse(context.doPost({postData:{type:'application/json',contents:JSON.stringify({schema:1,app:'scorer_free',counts,...extra})}}).text).ok}
assert.equal(post({sessions:1}),false);assert.deepEqual(store,{});
store.SCORER_ENABLED='true';store.SCORER_RECIPIENT='owner@example.com';
for(const bad of [{name:1},{sessions:true},{sessions:-1},{sessions:10001}])assert.equal(post(bad),false);
assert.equal(post({sessions:1},{player:'private'}),false);
assert.equal(post({sessions:1},{app:'scorerworld'}),false);
assert.equal(post({sessions:1,goals_scored:5}),true);assert.equal(mails.length,0);
assert.ok(!store.SCORER_STATE.includes('goals_scored'));
context.sendScorerSessionNotices();assert.equal(mails.length,1);assert.equal(mails[0].to,'owner@example.com');
assert.ok(mails[0].body.includes('Inícios de sessão: 1'));
context.sendScorerSessionNotices();assert.equal(mails.length,1);
post({sessions_ended:1});context.sendScorerSessionNotices();assert.equal(mails.length,1); // one/minute
let state=JSON.parse(store.SCORER_STATE);delete state.minute;store.SCORER_STATE=JSON.stringify(state);
mailFailure=true;assert.throws(()=>context.sendScorerSessionNotices());assert.equal(JSON.parse(store.SCORER_STATE).ends,1);
mailFailure=false;quota=0;context.sendScorerSessionNotices();assert.equal(mails.length,1);
quota=100;context.sendScorerSessionNotices();assert.equal(mails.length,2);
post({sessions:1});state=JSON.parse(store.SCORER_STATE);state.notices=60;delete state.minute;store.SCORER_STATE=JSON.stringify(state);
context.sendScorerSessionNotices();assert.equal(mails.length,2);
store.SCORER_RECIPIENT='x@example.com\nBcc:bad@example.com';context.sendScorerSessionNotices();assert.equal(mails.length,2);
store.SCORER_ENABLED='false';assert.equal(post({sessions:1}),false);context.sendScorerSessionNotices();assert.equal(mails.length,2);
assert.equal(context.doGet().text,'{"ok":true}');assert.ok(!context.doGet().text.includes('owner'));
console.log('Apps Script mocked functional/security checks PASS; no Google account accessed, no mail sent.');

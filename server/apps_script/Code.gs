/* SCORER Free optional session notices. No player IDs or raw request storage.
 * NOT deployed. Configure private Script Properties before installing trigger.
 */
var SCORER_EVENTS = ['sessions','sessions_ended','new_careers','careers_loaded',
  'trainings_completed','matches_completed','goals_scored','load_failures','save_failures'];
function scorerReply_(ok) {
  return ContentService.createTextOutput(JSON.stringify({ok:ok})).setMimeType(ContentService.MimeType.JSON);
}
function scorerValid_(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data) ||
      Object.keys(data).sort().join(',') !== 'app,counts,schema' ||
      data.schema !== 1 || data.app !== 'scorer_free' || !data.counts ||
      typeof data.counts !== 'object' || Array.isArray(data.counts)) return false;
  var keys = Object.keys(data.counts);
  return keys.length > 0 && keys.every(function(k) {
    return SCORER_EVENTS.indexOf(k) >= 0 && Number.isInteger(data.counts[k]) && data.counts[k] > 0 && data.counts[k] <= 10000;
  });
}
function scorerDay_() { return Utilities.formatDate(new Date(),'UTC','yyyy-MM-dd'); }
function scorerState_(properties) {
  var state = JSON.parse(properties.getProperty('SCORER_STATE') || '{}');
  var day = scorerDay_();
  if (state.day !== day) { state.day = day; state.notices = 0; }
  if (!state.pendingDay || (Date.parse(day)-Date.parse(state.pendingDay)) > 7*86400000) {
    state.starts = 0; state.ends = 0; state.pendingDay = day;
  }
  return state;
}
function doPost(e) {
  try {
    var properties = PropertiesService.getScriptProperties();
    if (properties.getProperty('SCORER_ENABLED') !== 'true' || !e || !e.postData ||
        typeof e.postData.contents !== 'string' || e.postData.contents.length > 4096 ||
        String(e.postData.type).split(';')[0].trim() !== 'application/json') return scorerReply_(false);
    var data = JSON.parse(e.postData.contents);
    if (!scorerValid_(data)) return scorerReply_(false);
    var lock = LockService.getScriptLock();
    if (!lock.tryLock(1000)) return scorerReply_(false);
    try {
      var state = scorerState_(properties);
      state.starts = Math.min(10000,(state.starts || 0)+(data.counts.sessions || 0));
      state.ends = Math.min(10000,(state.ends || 0)+(data.counts.sessions_ended || 0));
      properties.setProperty('SCORER_STATE',JSON.stringify(state));
    } finally { lock.releaseLock(); }
    return scorerReply_(true);
  } catch (_) { return scorerReply_(false); }
}
function doGet() { return scorerReply_(true); } // No recipient or private totals exposed.
function sendScorerSessionNotices() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    var properties = PropertiesService.getScriptProperties();
    if (properties.getProperty('SCORER_ENABLED') !== 'true') return;
    var recipient = properties.getProperty('SCORER_RECIPIENT') || '';
    if (!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(recipient)) return;
    var state = scorerState_(properties);
    var minute = Utilities.formatDate(new Date(),'UTC','yyyy-MM-dd HH:mm');
    if (!(state.starts || state.ends) || state.minute === minute || state.notices >= 60 || MailApp.getRemainingDailyQuota() < 1) return;
    var body = 'SCORER Free — atividade recebida\n\nInícios de sessão: '+(state.starts || 0)+
      '\nFechos normais: '+(state.ends || 0)+
      '\n\nContadores opcionais e aproximados, sem nomes ou IDs. Eventos offline podem chegar com atraso; um fecho forçado pode não produzir aviso final. Inícios e fins não são associados a uma pessoa.';
    MailApp.sendEmail({to:recipient,subject:'SCORER Free — início/fim de sessões',body:body});
    state.starts = 0; state.ends = 0; state.pendingDay = state.day;
    state.notices += 1; state.minute = minute;
    properties.setProperty('SCORER_STATE',JSON.stringify(state));
  } finally { lock.releaseLock(); }
}
function installScorerTrigger() {
  // Run explicitly in your Google account; never invoked by public requests.
  ScriptApp.getProjectTriggers().forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'sendScorerSessionNotices') ScriptApp.deleteTrigger(trigger);
  });
  ScriptApp.newTrigger('sendScorerSessionNotices').timeBased().everyMinutes(1).create();
}

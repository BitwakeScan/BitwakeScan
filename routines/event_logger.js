/**
 * Logs a single event with customizable logger and time formatter
 * @param {string} category - Event category or type
 * @param {*} details - Payload/details to log
 * @param {object} [options]
 * @param {function(string, ...any):void} [options.logger=console.log] - Logging function
 * @param {function(Date):string} [options.formatTime=date=>date.toISOString()] - Time formatting function
 */
function logEvent(category, details, options = {}) {
  const {
    logger = console.log,
    formatTime = date => date.toISOString(),
  } = options;
  const time = formatTime(new Date());
  logger(`[${category}] ${time}:`, details);
}

/**
 * Batch-log an array of events, passing the same options to each
 * @param {Array<{type:string,payload:any}>} events
 * @param {object} [options] - Passed through to logEvent
 */
function batchLog(events, options) {
  events.forEach(event =>
    logEvent(event.type, event.payload, options)
  );
}

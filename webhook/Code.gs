function doPost(e) {
  const body = JSON.parse(e.postData.contents);
  const call = body.call;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Encuestas_Base');

  // transcript para fecha/hora/duración
  const transcript = call.transcript || [];
  let fecha = '';
  let hora = '';
  let duracionSegundos = '';

  if (transcript.length > 0) {
    const first = new Date(transcript[0].created_at);
    const last = new Date(transcript[transcript.length - 1].created_at);
    fecha = Utilities.formatDate(last, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    hora  = Utilities.formatDate(last, Session.getScriptTimeZone(), 'HH:mm:ss');
    const diffMs = last.getTime() - first.getTime();
    duracionSegundos = Math.round(diffMs / 1000);
  }

  const analysis = call.analysis || {};
  const row = [
    call.id,
    call.to,
    call.from,
    fecha,
    hora,
    analysis.calificacion_servicio,
    analysis.nps,
    analysis.tiempo_atencion,
    analysis.amabilidad_tecnico,
    analysis.opinion_cliente,
    analysis.estado_llamada_completada_rechazada_reprogramada_o_erronea,
    call.summary,
    duracionSegundos,
    call.credits
  ];

  sheet.appendRow(row);

  return ContentService
    .createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}




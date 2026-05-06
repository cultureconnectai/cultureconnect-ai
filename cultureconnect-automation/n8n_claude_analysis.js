// ============================================
// NODO 3 — CLAUDE API CON RETRY LOGIC
// CultureConnect AI — n8n Code Node
// ============================================
// Pega este código en un nodo "Code" en n8n
// después del nodo de Google Sheets
// ============================================

const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 10000; // 10 segundos

const SYSTEM_PROMPT = `Eres el Estratega Senior de CultureConnect AI, una agencia de marketing bilingüe basada en San Antonio, TX.

Tu misión: Analizar el perfil JSON de un cliente hispano y generar un Plan de Crecimiento de 30 días.

REGLAS DE ORO:
1. Responde ÚNICAMENTE con JSON válido — sin texto adicional, sin markdown.
2. Si un campo dice [INFO_REQUERIDA], márcalo como null en tu análisis y agrega un flag.
3. Idioma: Spanglish profesional Texas-style. Directo y honesto.
4. Sé brutalmente honesto sobre por qué el negocio está perdiendo dinero HOY.
5. Prioriza el canal con más tracción orgánica actual.
6. No inventes seguidores ni estadísticas — usa solo lo que viene en el JSON.

ESTRUCTURA OBLIGATORIA DE RESPUESTA:
{
  "score_diagnostico": number (1-10),
  "score_justificacion": "string — por qué ese score en 1-2 oraciones",
  "analisis_canales": {
    "canal_principal": "string — cuál tiene más tracción y por qué",
    "instagram": "string — crítica constructiva",
    "facebook": "string — crítica constructiva",
    "tiktok": "string — crítica constructiva",
    "oportunidad_inmediata": "string — qué hacer ESTA semana"
  },
  "flags_riesgo": [
    "string — problema detectado 1",
    "string — problema detectado 2"
  ],
  "estrategia_manychat": {
    "keyword_1": { "palabra": "string", "accion": "string", "respuesta_automatica": "string" },
    "keyword_2": { "palabra": "string", "accion": "string", "respuesta_automatica": "string" },
    "keyword_3": { "palabra": "string", "accion": "string", "respuesta_automatica": "string" }
  },
  "calendario_semana_1": [
    {
      "dia": "Lunes",
      "plataforma": "string",
      "tipo_contenido": "Reel / Post / Story",
      "hook": "string — primera línea del video que detiene el scroll",
      "caption_es": "string — caption en español listo para publicar",
      "caption_en": "string — caption en inglés listo para publicar",
      "cta": "string — call to action específico"
    },
    { "dia": "Miércoles", "plataforma": "string", "tipo_contenido": "string", "hook": "string", "caption_es": "string", "caption_en": "string", "cta": "string" },
    { "dia": "Viernes", "plataforma": "string", "tipo_contenido": "string", "hook": "string", "caption_es": "string", "caption_en": "string", "cta": "string" }
  ],
  "recomendacion_tier": {
    "tier_actual": "string",
    "tier_recomendado": "string",
    "justificacion": "string"
  },
  "proximos_30_dias": {
    "semana_1": "string — enfoque principal",
    "semana_2": "string — enfoque principal",
    "semana_3": "string — enfoque principal",
    "semana_4": "string — enfoque principal"
  },
  "info_requerida": ["string — campo que falta y por qué es importante"]
}`;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function callClaudeWithRetry(clientJson, attempt = 1) {
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-6',
        max_tokens: parseInt(process.env.ANTHROPIC_MAX_TOKENS) || 3500,
        system: SYSTEM_PROMPT,
        messages: [
          {
            role: 'user',
            content: `Analiza este cliente de CultureConnect AI y genera el plan estratégico:\n\n${JSON.stringify(clientJson, null, 2)}`
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Claude API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    const content = result.content[0].text;

    // Parsear JSON de respuesta
    const analysis = JSON.parse(content);
    return { success: true, analysis, tokens_used: result.usage };

  } catch (error) {
    if (attempt < MAX_RETRIES) {
      console.log(`Intento ${attempt} falló. Reintentando en ${RETRY_DELAY_MS / 1000}s...`);
      await sleep(RETRY_DELAY_MS);
      return callClaudeWithRetry(clientJson, attempt + 1);
    }

    // Si falla 3 veces — retornar error estructurado
    return {
      success: false,
      error: error.message,
      attempts: attempt,
      alert: {
        type: 'CRITICAL_ERROR',
        message: `Claude API falló después de ${MAX_RETRIES} intentos para cliente ${$input.first().json.client_id}`,
        send_whatsapp: true,
        admin_number: process.env.WHATSAPP_ADMIN_NUMBER
      }
    };
  }
}

// --- Ejecutar ---
const clientData = $input.first().json;

if (clientData.status === 'ERROR') {
  return [{ json: clientData }];
}

const result = await callClaudeWithRetry(clientData);

return [{
  json: {
    client_id: clientData.client_id,
    client_name: clientData.client_info?.legal_name,
    client_email: clientData.client_info?.email,
    package: clientData.package_info?.package_selected,
    timestamp: new Date().toISOString(),
    ...result
  }
}];

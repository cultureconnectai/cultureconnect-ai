// ============================================
// NODO 1 — VALIDACIÓN DE SEGURIDAD Y DATOS
// CultureConnect AI — n8n Code Node
// ============================================
// Pega este código en un nodo "Code" en n8n
// justo después del nodo Webhook
// ============================================

const REQUIRED_FIELDS = ['email', 'legal_name', 'biz_type', 'phone', 'package'];

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function sanitize(value) {
  if (!value || value === '') return '[INFO_REQUERIDA]';
  return String(value).trim();
}

// --- Validación de Seguridad ---
const headers = $input.first().json.headers || {};
const signature = headers['x-netlify-signature'] || headers['x-webhook-secret'];
const SECRET = process.env.NETLIFY_WEBHOOK_SECRET;

if (SECRET && signature !== SECRET) {
  throw new Error('SECURITY: Webhook signature inválida. Acceso denegado.');
}

// --- Extraer datos del form ---
const body = $input.first().json.body || $input.first().json;

// --- Validar campos obligatorios ---
const missingFields = [];
for (const field of REQUIRED_FIELDS) {
  if (!body[field] || body[field] === '') {
    missingFields.push(field);
  }
}

if (missingFields.length > 0) {
  return [{
    json: {
      status: 'ERROR',
      message: `Faltan campos obligatorios: ${missingFields.join(', ')}`,
      timestamp: new Date().toISOString(),
      raw_data: body
    }
  }];
}

// --- Validar email ---
if (!validateEmail(body.email || body.biz_email)) {
  return [{
    json: {
      status: 'ERROR',
      message: 'Email inválido. No se puede procesar el cliente.',
      email_received: body.email || body.biz_email
    }
  }];
}

// --- Generar client_id único ---
const clientId = `CC-${Date.now()}-${Math.random().toString(36).substr(2, 5).toUpperCase()}`;

// --- Construir JSON limpio y estructurado ---
const clientData = {
  status: 'OK',
  client_id: clientId,
  timestamp: new Date().toISOString(),

  client_info: {
    legal_name: sanitize(body.legal_name),
    dba_name: sanitize(body.dba_name),
    email: sanitize(body.biz_email || body.email),
    phone: sanitize(body.phone),
    whatsapp: sanitize(body.whatsapp),
    address: sanitize(body.address),
    hours: sanitize(body.hours),
    website: sanitize(body.website),
    industry: sanitize(body.biz_type),
    description: sanitize(body.biz_description),
    main_contact: sanitize(body.main_contact)
  },

  social_assets: {
    instagram_handle: sanitize(body.ig_handle),
    instagram_followers: sanitize(body.ig_followers),
    facebook_page: sanitize(body.fb_page),
    facebook_followers: sanitize(body.fb_followers),
    youtube_channel: sanitize(body.yt_channel),
    youtube_subs: sanitize(body.yt_subs),
    tiktok_handle: sanitize(body.tt_handle),
    tiktok_followers: sanitize(body.tt_followers),
    threads_handle: sanitize(body.threads_handle),
    google_business_status: sanitize(body.gbp_status),
    google_reviews: sanitize(body.google_reviews),
    google_rating: sanitize(body.google_rating)
  },

  brand_assets: {
    has_logo: sanitize(body.has_logo),
    logo_delivery: sanitize(body.logo_delivery),
    primary_color: sanitize(body.color1),
    secondary_color: sanitize(body.color2),
    font: sanitize(body.font),
    visual_style: sanitize(body.visual_style),
    visual_references: sanitize(body.visual_references)
  },

  content_info: {
    has_existing_content: sanitize(body.has_content),
    content_location: sanitize(body.content_location),
    recording_frequency: sanitize(body.content_frequency),
    willing_on_camera: sanitize(body.on_camera),
    has_employees_for_content: sanitize(body.has_employees_content),
    business_story: sanitize(body.business_story),
    existing_testimonials: sanitize(body.testimonials)
  },

  package_info: {
    package_selected: sanitize(body.package),
    start_date: sanitize(body.start_date),
    payment_method: sanitize(body.payment_method),
    content_approver: sanitize(body.content_approver),
    ads_budget: sanitize(body.ads_budget),
    report_frequency: sanitize(body.report_frequency),
    comm_preference: sanitize(body.comm_preference),
    response_time: sanitize(body.response_time)
  },

  goals: {
    primary_goals: sanitize(body.goals),
    slow_months: sanitize(body.slow_months),
    busy_months: sanitize(body.busy_months),
    special_dates: sanitize(body.special_dates),
    priority_product: sanitize(body.priority_product),
    wants_online_sales: sanitize(body.online_sales),
    additional_notes: sanitize(body.additional_notes)
  }
};

return [{ json: clientData }];

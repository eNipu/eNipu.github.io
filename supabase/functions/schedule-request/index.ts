import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.45.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const OWNER_EMAIL = "hire.credibly374@passinbox.com";
const SITE_URL    = "https://al-am.in";

interface SchedulePayload {
  name?: string;
  email?: string;
  company?: string;
  topic?: string;
  note?: string;
  date?: string;           // 'YYYY-MM-DD'
  slot_start?: string;     // 'HH:MM'
  slot_end?: string;       // 'HH:MM'
  duration_minutes?: number;
  timezone?: string;
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c] as string)
  );
}

function formatDateTime(date: string, start: string, end: string, tz: string): string {
  // date: 'YYYY-MM-DD', start/end: 'HH:MM'
  const [y, m, d] = date.split("-").map(Number);
  const dateObj = new Date(y, m - 1, d);
  const dayNames = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
  const monthNames = ["January","February","March","April","May","June",
                      "July","August","September","October","November","December"];
  return `${dayNames[dateObj.getDay()]}, ${monthNames[m-1]} ${d}, ${y} · ${start}–${end} (${tz})`;
}

async function sendEmail(
  apiKey: string,
  from: string,
  to: string,
  subject: string,
  html: string,
  replyTo?: string,
): Promise<void> {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ from, to: [to], subject, html, reply_to: replyTo }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Resend failed: ${res.status} ${body}`);
  }
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "method_not_allowed" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    const raw = (await req.json()) as SchedulePayload;

    const name     = (raw.name     ?? "").trim().slice(0, 200);
    const email    = (raw.email    ?? "").trim().slice(0, 200);
    const company  = (raw.company  ?? "").trim().slice(0, 200);
    const topic    = (raw.topic    ?? "").trim().slice(0, 100);
    const note     = (raw.note     ?? "").trim().slice(0, 2000);
    const date     = (raw.date     ?? "").trim().slice(0, 20);
    const slotStart= (raw.slot_start ?? "").trim().slice(0, 10);
    const slotEnd  = (raw.slot_end   ?? "").trim().slice(0, 10);
    const duration = Number(raw.duration_minutes ?? 30);
    const timezone = (raw.timezone ?? "Europe/Berlin").slice(0, 60);

    // Basic validation
    if (!name || !email || !date || !slotStart || !slotEnd) {
      return new Response(JSON.stringify({ error: "invalid_input" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(JSON.stringify({ error: "invalid_email" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Persist to Supabase
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const { error: insertError } = await supabase
      .from("meeting_requests")
      .insert({ name, email, company, topic, note, date, slot_start: slotStart,
                slot_end: slotEnd, duration_minutes: duration, timezone });

    if (insertError) {
      console.error("insert error", insertError);
      return new Response(JSON.stringify({ error: "persist_failed" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Send emails via Resend
    const resendKey = Deno.env.get("RESEND_API_KEY");
    const mailFrom  = Deno.env.get("HIRE_FROM_EMAIL") ?? "Al-Amin <onboarding@resend.dev>";

    if (resendKey) {
      const safeName    = escapeHtml(name);
      const safeEmail   = escapeHtml(email);
      const safeCompany = escapeHtml(company || "(not provided)");
      const safeTopic   = escapeHtml(topic   || "(not specified)");
      const safeNote    = escapeHtml(note    || "(none)").replace(/\n/g, "<br>");
      const safeSlot    = escapeHtml(formatDateTime(date, slotStart, slotEnd, timezone));

      // Owner notification
      const ownerHtml = `
        <h2 style="margin-bottom:16px">New meeting request from al-am.in/schedule/</h2>
        <table style="border-collapse:collapse;font-size:15px">
          <tr><td style="padding:6px 16px 6px 0;color:#667380;font-weight:600">Name</td>
              <td>${safeName}</td></tr>
          <tr><td style="padding:6px 16px 6px 0;color:#667380;font-weight:600">Email</td>
              <td><a href="mailto:${safeEmail}">${safeEmail}</a></td></tr>
          <tr><td style="padding:6px 16px 6px 0;color:#667380;font-weight:600">Company</td>
              <td>${safeCompany}</td></tr>
          <tr><td style="padding:6px 16px 6px 0;color:#667380;font-weight:600">Topic</td>
              <td>${safeTopic}</td></tr>
          <tr><td style="padding:6px 16px 6px 0;color:#667380;font-weight:600">Requested slot</td>
              <td><strong>${safeSlot}</strong> (${duration} min)</td></tr>
        </table>
        <hr style="margin:20px 0;border:0;border-top:1px solid #e8e2d5">
        <p style="color:#667380;font-size:14px"><strong>Note:</strong></p>
        <p>${safeNote}</p>
        <hr style="margin:20px 0;border:0;border-top:1px solid #e8e2d5">
        <p style="font-size:13px;color:#8a949f">
          Reply directly to this email to respond to ${safeName}.<br>
          View all requests in the
          <a href="https://supabase.com">Supabase dashboard</a> → Table Editor → meeting_requests.
        </p>
      `;

      // Requester acknowledgement
      const replyHtml = `
        <p>Hi ${safeName},</p>
        <p>Thanks for requesting a meeting through <a href="${SITE_URL}/schedule/">${SITE_URL}/schedule/</a>.</p>
        <p>Your requested slot: <strong>${safeSlot}</strong> (${duration} min)</p>
        <p>I will confirm or suggest an alternative within one business day. For anything urgent, feel free to reach me on
           <a href="https://www.linkedin.com/in/khandakermd/">LinkedIn</a>.</p>
        <p>&mdash; Khandaker Md. Al-Amin<br>
           <a href="${SITE_URL}/">${SITE_URL}</a></p>
      `;

      try {
        await sendEmail(resendKey, mailFrom, OWNER_EMAIL,
          `[al-am.in] Meeting request: ${name} — ${date} ${slotStart}`,
          ownerHtml, email);
      } catch (err) { console.error("owner email failed", err); }

      try {
        await sendEmail(resendKey, mailFrom, email,
          "Your meeting request — Khandaker Md. Al-Amin",
          replyHtml, OWNER_EMAIL);
      } catch (err) { console.error("ack email failed", err); }
    }

    return new Response(
      JSON.stringify({ ok: true }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
    );
  } catch (err) {
    console.error("schedule-request error", err);
    return new Response(JSON.stringify({ error: "unexpected" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});

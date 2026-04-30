import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.45.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const OWNER_EMAIL = "hire.credibly374@passinbox.com";
const LINKEDIN_URL = "https://www.linkedin.com/in/khandakermd/";

interface ContactPayload {
  name?: string;
  email?: string;
  company?: string;
  role_type?: string;
  message?: string;
  source?: string;
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c] as string
  ));
}

async function sendEmailViaResend(
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
    body: JSON.stringify({
      from,
      to: [to],
      subject,
      html,
      reply_to: replyTo,
    }),
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
    const payload = (await req.json()) as ContactPayload;

    const name = (payload.name ?? "").trim().slice(0, 200);
    const email = (payload.email ?? "").trim().slice(0, 200);
    const company = (payload.company ?? "").trim().slice(0, 200);
    const role_type = (payload.role_type ?? "").trim().slice(0, 100);
    const message = (payload.message ?? "").trim().slice(0, 5000);
    const source = (payload.source ?? "").trim().slice(0, 300);

    if (!name || !email || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(JSON.stringify({ error: "invalid_input" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceKey);

    const { error: insertError } = await supabase
      .from("contact_requests")
      .insert({ name, email, company, role_type, message, source });

    if (insertError) {
      console.error("insert error", insertError);
      return new Response(JSON.stringify({ error: "persist_failed" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const resendKey = Deno.env.get("RESEND_API_KEY");
    const mailFrom = Deno.env.get("HIRE_FROM_EMAIL") ?? "Al-Amin <onboarding@resend.dev>";

    if (resendKey) {
      const safeName = escapeHtml(name);
      const safeEmail = escapeHtml(email);
      const safeCompany = escapeHtml(company || "(not provided)");
      const safeRole = escapeHtml(role_type || "(not specified)");
      const safeMessage = escapeHtml(message).replace(/\n/g, "<br>");
      const safeSource = escapeHtml(source || "(direct)");

      const ownerHtml = `
        <h2>New hire enquiry from al-am.in</h2>
        <p><strong>Name:</strong> ${safeName}<br>
           <strong>Email:</strong> <a href="mailto:${safeEmail}">${safeEmail}</a><br>
           <strong>Company:</strong> ${safeCompany}<br>
           <strong>Engagement:</strong> ${safeRole}<br>
           <strong>Source:</strong> ${safeSource}</p>
        <hr>
        <p>${safeMessage}</p>
      `;

      const replyHtml = `
        <p>Hi ${safeName},</p>
        <p>Thanks for reaching out through <a href="https://al-am.in/hire/">al-am.in</a>. I have received your message and will get back to you within 2&ndash;3 business days.</p>
        <p>For a faster response, or if your matter is time-sensitive, feel free to message me directly on <a href="${LINKEDIN_URL}">LinkedIn</a>.</p>
        <p>&mdash; Khandaker Md. Al-Amin<br>
        <a href="${LINKEDIN_URL}">LinkedIn</a> &middot; <a href="https://al-am.in/">al-am.in</a></p>
      `;

      try {
        await sendEmailViaResend(
          resendKey,
          mailFrom,
          OWNER_EMAIL,
          `[al-am.in] ${name} &mdash; ${role_type || "contact"}`,
          ownerHtml,
          email,
        );
      } catch (err) {
        console.error("owner email failed", err);
      }

      try {
        await sendEmailViaResend(
          resendKey,
          mailFrom,
          email,
          "Thanks for reaching out",
          replyHtml,
          OWNER_EMAIL,
        );
      } catch (err) {
        console.error("ack email failed", err);
      }
    }

    return new Response(
      JSON.stringify({ ok: true, linkedin: LINKEDIN_URL }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
    );
  } catch (err) {
    console.error("hire-contact error", err);
    return new Response(JSON.stringify({ error: "unexpected" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});

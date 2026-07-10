import "jsr:@supabase/functions-js/edge-runtime.d.ts";

/**
 * calendar-freebusy
 *
 * Proxy for the Google Calendar FreeBusy API.
 * The Google API key is stored as a Supabase secret (GOOGLE_CALENDAR_API_KEY)
 * and never exposed to the browser or the public GitHub repo.
 *
 * Request body (JSON):
 *   { timeMin: string, timeMax: string, timeZone: string }
 *
 * Response body (JSON):
 *   { busy: [{ start: string, end: string }, ...] }
 *   — only the busy array is returned; no other calendar data is forwarded.
 */

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, Apikey",
};

const CALENDAR_ID = "tokhandakeralamin@gmail.com";

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

  const apiKey = Deno.env.get("GOOGLE_CALENDAR_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "calendar_not_configured" }), {
      status: 503,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    const { timeMin, timeMax, timeZone } = await req.json();

    if (!timeMin || !timeMax) {
      return new Response(JSON.stringify({ error: "missing_params" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const body = {
      timeMin,
      timeMax,
      timeZone: timeZone ?? "Europe/Berlin",
      items: [{ id: CALENDAR_ID }],
    };

    const res = await fetch(
      `https://www.googleapis.com/calendar/v3/freeBusy?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    );

    if (!res.ok) {
      const errText = await res.text();
      console.error("Google FreeBusy error:", res.status, errText);
      return new Response(JSON.stringify({ error: "upstream_error" }), {
        status: 502,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const data = await res.json();

    // Return ONLY the busy array — no other calendar data is forwarded
    const busy: { start: string; end: string }[] =
      data.calendars?.[CALENDAR_ID]?.busy ?? [];

    return new Response(JSON.stringify({ busy }), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("calendar-freebusy error:", err);
    return new Response(JSON.stringify({ error: "unexpected" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});

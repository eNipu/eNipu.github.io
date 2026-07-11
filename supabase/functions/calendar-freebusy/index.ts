import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import ical from "npm:node-ical@0.18.0";

/**
 * calendar-freebusy
 *
 * Returns busy blocks for the owner's calendar. Two sources, tried in order:
 *
 * 1. GOOGLE_CALENDAR_ICS_URL secret — the calendar's "Secret address in
 *    iCal format" (Google Calendar settings → Integrate calendar). Needs
 *    no public sharing. Preferred.
 * 2. GOOGLE_CALENDAR_API_KEY secret — Google FreeBusy API. Only works if
 *    the calendar shares free/busy publicly.
 *
 * Request body (JSON):
 *   { timeMin: string, timeMax: string, timeZone: string }
 *
 * Response body (JSON):
 *   { busy: [{ start: string, end: string }, ...] }
 *   — only busy intervals are returned; titles/details never leave here.
 */

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, Apikey",
};

const CALENDAR_ID = "tokhandakeralamin@gmail.com";

type Busy = { start: string; end: string };

async function busyFromIcs(icsUrl: string, min: Date, max: Date): Promise<Busy[]> {
  const res = await fetch(icsUrl);
  if (!res.ok) throw new Error(`ICS fetch failed: ${res.status}`);
  const events = ical.sync.parseICS(await res.text());
  const busy: Busy[] = [];

  for (const ev of Object.values(events) as any[]) {
    if (ev.type !== "VEVENT") continue;
    if (ev.transparency === "TRANSPARENT") continue; // marked "free"
    if (!ev.start || !ev.end) continue;
    const durMs = ev.end.getTime() - ev.start.getTime();

    if (ev.rrule) {
      // ponytail: rrule.between covers plain recurrences; per-instance
      // overrides/EXDATE edge cases fall back to slightly conservative
      // (extra busy), which is the safe direction for a booking page.
      const exdates = new Set(
        Object.values(ev.exdate ?? {}).map((d: any) => d.getTime()),
      );
      for (const s of ev.rrule.between(min, max, true) as Date[]) {
        if (exdates.has(s.getTime())) continue;
        busy.push({
          start: s.toISOString(),
          end: new Date(s.getTime() + durMs).toISOString(),
        });
      }
    } else if (ev.start < max && ev.end > min) {
      busy.push({ start: ev.start.toISOString(), end: ev.end.toISOString() });
    }
  }
  return busy;
}

async function busyFromFreeBusyApi(
  apiKey: string,
  timeMin: string,
  timeMax: string,
  timeZone: string,
): Promise<Busy[]> {
  const res = await fetch(
    `https://www.googleapis.com/calendar/v3/freeBusy?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        timeMin,
        timeMax,
        timeZone,
        items: [{ id: CALENDAR_ID }],
      }),
    },
  );
  if (!res.ok) {
    console.error("Google FreeBusy error:", res.status, await res.text());
    throw new Error("freebusy upstream error");
  }
  const data = await res.json();
  const cal = data.calendars?.[CALENDAR_ID];
  if (cal?.errors?.length) {
    console.error("FreeBusy calendar errors:", JSON.stringify(cal.errors));
  }
  return cal?.busy ?? [];
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
    const { timeMin, timeMax, timeZone } = await req.json();

    if (!timeMin || !timeMax) {
      return new Response(JSON.stringify({ error: "missing_params" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const icsUrl = Deno.env.get("GOOGLE_CALENDAR_ICS_URL");
    const apiKey = Deno.env.get("GOOGLE_CALENDAR_API_KEY");

    let busy: Busy[];
    if (icsUrl) {
      busy = await busyFromIcs(icsUrl, new Date(timeMin), new Date(timeMax));
    } else if (apiKey) {
      busy = await busyFromFreeBusyApi(
        apiKey,
        timeMin,
        timeMax,
        timeZone ?? "Europe/Berlin",
      );
    } else {
      return new Response(JSON.stringify({ error: "calendar_not_configured" }), {
        status: 503,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ busy }), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("calendar-freebusy error:", err);
    return new Response(JSON.stringify({ error: "upstream_error" }), {
      status: 502,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});

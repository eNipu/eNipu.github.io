/*
  # Meeting requests table for /schedule/ page

  1. New Table
     - `meeting_requests` — stores inbound meeting slot requests
       - `id`               (uuid, PK)
       - `name`             (text, required)
       - `email`            (text, required)
       - `company`          (text, nullable)
       - `topic`            (text) — e.g. "consulting", "eu-cra", "crypto"
       - `note`             (text) — optional context from requester
       - `date`             (date) — requested date 'YYYY-MM-DD'
       - `slot_start`       (text) — 'HH:MM' in Europe/Berlin
       - `slot_end`         (text) — 'HH:MM' in Europe/Berlin
       - `duration_minutes` (int)  — 30 or 60
       - `timezone`         (text) — always 'Europe/Berlin' from the UI
       - `status`           (text) — 'pending' | 'confirmed' | 'declined' | 'rescheduled'
       - `created_at`       (timestamptz)

  2. Security
     - RLS enabled
     - Public anon may INSERT (submit a request)
     - SELECT is blocked for anon/authenticated — only service role (owner via
       Supabase dashboard) can read submissions
*/

CREATE TABLE IF NOT EXISTS meeting_requests (
  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  name             text        NOT NULL DEFAULT '',
  email            text        NOT NULL DEFAULT '',
  company          text        DEFAULT '',
  topic            text        DEFAULT '',
  note             text        DEFAULT '',
  date             date        NOT NULL,
  slot_start       text        NOT NULL DEFAULT '',
  slot_end         text        NOT NULL DEFAULT '',
  duration_minutes integer     NOT NULL DEFAULT 30,
  timezone         text        NOT NULL DEFAULT 'Europe/Berlin',
  status           text        NOT NULL DEFAULT 'pending',
  created_at       timestamptz DEFAULT now()
);

ALTER TABLE meeting_requests ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE tablename = 'meeting_requests'
      AND policyname = 'Anyone can submit a meeting request'
  ) THEN
    CREATE POLICY "Anyone can submit a meeting request"
      ON meeting_requests FOR INSERT
      TO anon, authenticated
      WITH CHECK (
        char_length(name)  > 0
        AND char_length(email) > 3
        AND date IS NOT NULL
        AND char_length(slot_start) > 0
      );
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS meeting_requests_date_idx    ON meeting_requests (date);
CREATE INDEX IF NOT EXISTS meeting_requests_created_idx ON meeting_requests (created_at DESC);
CREATE INDEX IF NOT EXISTS meeting_requests_status_idx  ON meeting_requests (status);

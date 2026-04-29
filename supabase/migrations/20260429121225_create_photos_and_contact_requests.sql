/*
  # Photography gallery + recruiter contact requests

  1. New Tables
     - `photos` - stores metadata for each published photograph
       - `id` (uuid, PK)
       - `title` (text)
       - `location` (text) - human-readable location label shown on hover
       - `country` (text) - free-form country name
       - `category` (text) - filter slug e.g. "japan", "france", "bangladesh"
       - `taken_on` (date) - when the photo was taken
       - `caption` (text) - optional longer caption
       - `image_url` (text) - full resolution image URL (Supabase Storage)
       - `thumb_url` (text) - thumbnail URL
       - `camera` (text) - optional EXIF-style camera info
       - `featured` (bool) - show on homepage highlight strip
       - `hidden` (bool) - draft mode, not shown publicly
       - `sort_order` (int) - manual ordering, lower = earlier
       - `created_at` (timestamptz)

     - `contact_requests` - inbound messages from the /hire/ page
       - `id` (uuid, PK)
       - `name` (text)
       - `email` (text)
       - `company` (text, nullable)
       - `role_type` (text) - e.g. "full-time", "contract", "consulting"
       - `message` (text)
       - `source` (text) - optional utm source
       - `created_at` (timestamptz)

  2. Security
     - RLS enabled on both tables
     - `photos`: public may SELECT non-hidden rows; writes blocked for anon/auth
       (only service role via admin tools can INSERT/UPDATE/DELETE)
     - `contact_requests`: anon may INSERT (public hire form); SELECT blocked for
       everyone except service role so only the owner can read submissions via
       the Supabase dashboard

  3. Notes
     1. No destructive changes; uses IF NOT EXISTS everywhere.
     2. Writes to `photos` must be done from the Supabase dashboard (service role)
        or from a future authenticated admin page.
*/

CREATE TABLE IF NOT EXISTS photos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text DEFAULT '',
  location text DEFAULT '',
  country text DEFAULT '',
  category text DEFAULT 'all',
  taken_on date,
  caption text DEFAULT '',
  image_url text NOT NULL,
  thumb_url text DEFAULT '',
  camera text DEFAULT '',
  featured boolean DEFAULT false,
  hidden boolean DEFAULT false,
  sort_order integer DEFAULT 100,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies WHERE tablename = 'photos' AND policyname = 'Public can view non-hidden photos'
  ) THEN
    CREATE POLICY "Public can view non-hidden photos"
      ON photos FOR SELECT
      TO anon, authenticated
      USING (hidden = false);
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS contact_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL DEFAULT '',
  email text NOT NULL DEFAULT '',
  company text DEFAULT '',
  role_type text DEFAULT '',
  message text NOT NULL DEFAULT '',
  source text DEFAULT '',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE contact_requests ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies WHERE tablename = 'contact_requests' AND policyname = 'Anyone can submit a contact request'
  ) THEN
    CREATE POLICY "Anyone can submit a contact request"
      ON contact_requests FOR INSERT
      TO anon, authenticated
      WITH CHECK (
        char_length(name) > 0
        AND char_length(email) > 3
        AND char_length(message) > 0
      );
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS photos_category_sort_idx ON photos (category, sort_order);
CREATE INDEX IF NOT EXISTS photos_created_idx ON photos (created_at DESC);
CREATE INDEX IF NOT EXISTS contact_requests_created_idx ON contact_requests (created_at DESC);

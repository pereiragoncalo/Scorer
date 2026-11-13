# Scorer — openings and normal closes, 30 days

Private /admin shows only total openings/normal closes and one row per UTC day
for the last30dates including today. Zero days are visible. Data uses the existing
receipt-day aggregates; no historical event dates or missing forced closes are
invented. Management remains at /admin/manage. Current collection choices and
legacy totals API retained. No new APK/AAB or version-policy change.

Run the SHA256-verified Scorer-Activity-Stats-Backend.py on the existing bastion
as root. Only three files under /opt/scorer/server are installed. A known-prior
file hash guard refuses unexpected installed source before stopping the service.
The installer backs up files and rolls back on failed post-restart verification.
Database, admin token and update policy are not read or rewritten.

After installation open https://stats.clemir.com/admin with the existing token.
Local test screenshots use synthetic fixture counts, not live owner data.

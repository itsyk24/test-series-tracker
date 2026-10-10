# Test Series Tracker

Personal Android app for the ESE + GATE 2027 (Civil) test-series plan: Oct 10 – Dec 15, 2026.

- `app/src/main/assets/web/` — the whole UI (HTML/CSS/JS, works offline). `seed.js` holds the schedule.
- `app/src/main/java/.../MainActivity.java` — WebView shell; saves progress to the app's private storage and handles backup export/import.
- Every push to `main` builds a signed APK (GitHub Actions) and publishes it as a Release.

Progress lives on the phone (`files/state.json`) and survives updates because every build is signed with the same key (`app/release.jks`, password in the `KEYSTORE_PASS` secret). Keep using this repo for future versions; a build signed with a different key cannot update the installed app.

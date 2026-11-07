# Scorer World0.9.37 QA — player feedback

Feedback is available from the entry menu and the main dashboard. On the normal
dashboard it occupies spare header space beside the logo, preserving the existing
Help/World/Exit group alignment and the Player/Club/Training/Play positions. The
compact dashboard includes the same action.

Feedback opens a user-controlled email draft addressed to goncalo@clemir.com with
the subject Scorer World - Feedback. Android uses ACTION_SENDTO on the activity's
UI thread. The user writes and sends the message through their own email app;
the game does not submit messages automatically or attach career data/logs.
If no handler is available, a localized modal shows the support address with
Copy Email and Close actions. Labels and fallback guidance cover nine languages.

Gameplay, career data, the restored dashboard layout and the removal of national
friendlies remain unchanged. No leaderboard server update is required.
This uses the existing debug upgrade key and remains a QA candidate. Real Android
mail-app launching and physical handset acceptance remain pending. Google Play
production1.0 and previous official club-history audit limitations are unchanged.

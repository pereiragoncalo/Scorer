# Scorer World 1.0 (1030034)

Training preparation removes the player name. The locker-room picture and seated
player now anchor at the same bottom baseline as Start Training, preserving image
aspect ratio, club kit and one-screen controls at phone sizes/densities. Existing
reserved session, progress, resume and save failure behaviour are unchanged.

Owner reports that mandatory1030033 opens Play with only Play, then returns to
the blocked splash. Public server policy was confirmed at minimum/latest1030033.
New code availability in Console/API does not prove availability to that account.
Rollback minimum to1030032 to unlock; this1030034 stays optional until Play shows
Update. A new version cannot itself guarantee Google propagation/eligibility.
No changes to gameplay, saves, stadium33 art, net physics or signing identity.

Commands: docs/play/FIXES_1030034.md. Physical Play update acceptance pending.

Validation:8native locker/localisation/density/touch/session/stadium tests pass;
32pure/update/publisher tests pass with one hostJDK skip; final publisher25tests
pass with one hostJDK skip. Actual native screenshot reviewed. Android AAB audit
passes118ELF16KiB, exact compiled source/resources and production metadata.

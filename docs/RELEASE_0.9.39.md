# Scorer World0.9.39 QA — training touch and estate portrait

International friendlies are hidden from displayed fixture history as well as
upcoming fixtures. Old queued friendly newspaper reports are skipped on reload.
Completed caps/goals remain intact in saved data; no new friendlies are generated
or selected. National attendance now uses only official results.

Training result screens wait for an explicit tap rather than auto-advancing after
2.55seconds while still saying Tap to Continue. A visible result gets input before
stale menu widgets and redraws immediately. The first tap advances once, never
launches the next shot, and the third tap presents the completed-training summary.
Match auto-advance and celebrations retain their previous behaviour.

My Assets now shows a live original retro portrait: player in the best owned
outfit outside the best owned home, with the best owned car parked on the drive.
Each category is selected independently by unit purchase price; purchase order
and item quantity cannot replace a better item. No unowned car is displayed.
Supplied starter accommodation/clothes are a visual fallback, not owned items.
The Collection button retains browsing for every purchase, including gifts.
The scene and captions fit one screen. Five outfit views and a forecourt plate
are original generated assets; owned house/car art is reused. Textures use nearest
filtering and cached CoreImage references for restoration after context changes.

The0.9.38 finishing adjustments, physics, money and purchase rules are unchanged.
Existing-debug-key QA candidate; physical Android touch/graphics acceptance remains
pending. Google Play1.0 and prior full official club-history audit limitations
are unchanged. No server update is required.

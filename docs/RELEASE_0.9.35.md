# Scorer World0.9.35 QA — dashboard, lifestyle and short injuries

The dashboard restores Player and Club above the fixture, with Training and Play
below it. These four buttons have matching sizes and column alignment. Lifestyle
occupies the right-hand slot above the season panel. The upper-right Help, World
and Exit actions and the lower navigation strip keep their previous positions.
The season panel assigns explicit proportional rows to appearances/goals,
morale/fitness, league and trust/role, avoiding overlapping anchored content.

Lifestyle opens separate Shopping and My Assets destinations. Shopping shows the
illustrated catalogue and purchase controls. My Assets displays only items
acquired in this saved career, including quantities and original purchase prices.
The club-provided studio phrase is removed. Purchases continue to use local career
money; there are no real-money transactions or attribute bonuses.

Each completed appearance has a 1–3% injury risk depending on fitness (1% at20,
3% at0). Injuries last1–3 missed fixtures: ankle sprain, calf strain, thigh knock,
groin strain, bruised knee or hamstring strain. The state survives save/reload.
While injured, Training is disabled and Simulate Match replaces Play; the team
fixture progresses using full team scoring expectations. Missed fixtures do not
add an appearance, goal drought, coach-trust penalty or attribute change. Recovery
advances once per completed missed fixture, including cup/national fixtures, not
when browsing screens or reloading. Normal training requirements resume afterwards.
The physics solver and shot controls are unchanged from0.9.34.

This is an existing-debug-key QA build. Physical Android playtesting remains
pending. The previous release's incomplete official five-season club-table audit
is still outstanding. Google Play production1.0 is unchanged. The0.9.34 bastion
installer is still the required server update for the Career leaderboard; no
additional server update is needed for this build.

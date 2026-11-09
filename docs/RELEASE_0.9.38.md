# Scorer World0.9.38 QA — situational finishing balance

Penalties are substantially easier: moving-marker speed is60% of its previous
speed and the decision allocation is2.2 times longer. The keeper needs180ms more
to read the shot and has greater horizontal reading uncertainty. One-on-ones use
80% marker speed,1.5 times the allocation,90ms extra keeper reaction and a smaller
reading-error increase.

Headers within7m radial distance receive a modest adjustment:95% marker speed,
1.12 times the decision allocation,15ms keeper delay and8% more reading error.
The benefit fades smoothly to zero at10m. Earned focus-time bonuses are added in
full after allocation/age adjustments, as before. Practice keeper behaviour uses
the same situation-specific reading/reaction tuning.

Normal shots, free kicks and headers at10m or more are neutral. Chance frequency,
progression by opponent division, age effects, training gates, the intended aim
point, ballistic launch solver and player/keeper collision dimensions stay intact.
No predetermined goal outcomes, goal quotas or extra goalkeeper arm reach.

Paired simulation:2400 physical shots,120 identical seed/target pairs per type and
keeper tier, with exact targets bypassing human marker/timer skill. Against a top
keeper penalties changed15%→72.5%, one-on-ones23.3%→53.3%, near headers40%→44.2%.
Against tier4:21.7%→77.5%,37.5%→71.7%,60.8%→63.3%. The distant-header and normal-shot
control groups retained exactly identical outcome counts. These are controlled
comparisons, not measured or guaranteed human conversion rates.

Existing-debug-key QA build. Physical Android playtesting remains pending.
Google Play production1.0 and previous official club-history audit limitations
are unchanged; no server update is needed.

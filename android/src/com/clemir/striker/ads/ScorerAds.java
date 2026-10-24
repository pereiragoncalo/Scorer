package com.clemir.striker.ads;

import android.app.Activity;
import android.os.Bundle;
import android.content.SharedPreferences;
import java.util.UUID;
import com.google.android.gms.ads.rewarded.RewardedAd;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import android.os.SystemClock;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdSize;
import com.google.android.gms.ads.AdView;
import androidx.annotation.NonNull;
import com.google.ads.mediation.admob.AdMobAdapter;
import com.google.android.gms.ads.AdError;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.FullScreenContentCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.RequestConfiguration;
import com.google.android.gms.ads.interstitial.InterstitialAd;
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.ump.ConsentInformation;
import com.google.android.ump.ConsentRequestParameters;
import com.google.android.ump.UserMessagingPlatform;

/** Official TEST ads only. Never substitute production IDs for device testing. */
public final class ScorerAds {
    public static final String TEST_UNIT = "ca-app-pub-3940256099942544/1033173712";
    public static final String TEST_BANNER = "ca-app-pub-3940256099942544/6300978111";
    private static AdView banner;
    private static boolean entryVisible = false;
    private static long bannerRetryAfter = 0;
    public static final String TEST_REWARD = "ca-app-pub-3940256099942544/5224354917";
    private static RewardedAd rewardAd;
    private static boolean rewardWanted = false, rewardLoading = false;
    private static volatile boolean rewardReady = false;
    private static long rewardRetryAfter = 0, rewardLoadedAt = 0;
    private static volatile String pendingReward = "";
    private static volatile String rewardStatus = "Open training to prepare an optional reward ad.";
    private static volatile String breakStatus = "Full-screen ad not loaded.";
    private static InterstitialAd ad;
    private static volatile boolean ready = false;
    private static volatile boolean reserved = false;
    private static volatile String status = "Test ads have not started.";
    private static ConsentInformation consent;
    private static boolean consentBusy = false, initBusy = false, initialized = false;
    private static boolean loading = false;
    private static long retryAfter = 0, loadedAt = 0;
    private static final long EXPIRY = 55 * 60 * 1000L;

    private ScorerAds() {}

    private static boolean usable(Activity activity) {
        return activity != null && !activity.isFinishing() && !activity.isDestroyed();
    }

    public static void prepare(Activity activity) {
        if (!usable(activity)) return;
        activity.runOnUiThread(() -> {
            if (!usable(activity) || reserved || consentBusy || SystemClock.elapsedRealtime() < retryAfter) return;
            // Conservative configuration for the owner's audience, including children.
            // No age/date of birth is collected; every request gets these restrictions.
            MobileAds.setRequestConfiguration(new RequestConfiguration.Builder()
                .setTagForChildDirectedTreatment(RequestConfiguration.TAG_FOR_CHILD_DIRECTED_TREATMENT_TRUE)
                .setTagForUnderAgeOfConsent(RequestConfiguration.TAG_FOR_UNDER_AGE_OF_CONSENT_TRUE)
                .setMaxAdContentRating(RequestConfiguration.MAX_AD_CONTENT_RATING_G)
                .build());
            if (consent == null) consent = UserMessagingPlatform.getConsentInformation(activity);
            if (initialized) { load(activity); return; }
            consentBusy = true;
            status = "Checking advertising privacy requirements.";
            ConsentRequestParameters params = new ConsentRequestParameters.Builder()
                .setTagForUnderAgeOfConsent(true).build();
            consent.requestConsentInfoUpdate(activity, params, () -> {
                if (!usable(activity)) { consentBusy = false; return; }
                UserMessagingPlatform.loadAndShowConsentFormIfRequired(activity, error -> {
                    consentBusy = false;
                    initializeIfAllowed(activity);
                });
            }, error -> {
                consentBusy = false;
                retryAfter = SystemClock.elapsedRealtime() + 60000;
                initializeIfAllowed(activity);
            });
        });
    }

    private static void initializeIfAllowed(Activity activity) {
        if (!usable(activity) || consent == null || !consent.canRequestAds()) {
            status = "Ads unavailable - you can keep playing.";
            return;
        }
        if (initialized) { load(activity); return; }
        if (initBusy) return;
        initBusy = true;
        MobileAds.initialize(activity.getApplicationContext(), result -> activity.runOnUiThread(() -> {
            initBusy = false;
            initialized = true;
            load(activity);
        }));
    }

    private static void load(Activity activity) {
        loadEntryBanner(activity);
        loadReward(activity);
        if (!usable(activity) || consent == null || !consent.canRequestAds() || !initialized || loading || reserved) return;
        if (ready && SystemClock.elapsedRealtime() - loadedAt < EXPIRY) return;
        ready = false;
        ad = null;
        if (SystemClock.elapsedRealtime() < retryAfter) return;
        loading = true;
        status = "Loading a Google TEST ad.";
        breakStatus = "Loading the between-match TEST ad.";
        Bundle extras = new Bundle();
        extras.putString("npa", "1");
        AdRequest request = new AdRequest.Builder().addNetworkExtrasBundle(AdMobAdapter.class, extras).build();
        InterstitialAd.load(activity, TEST_UNIT, request, new InterstitialAdLoadCallback() {
            @Override public void onAdLoaded(@NonNull InterstitialAd loaded) {
                loading = false;
                ad = loaded;
                loadedAt = SystemClock.elapsedRealtime();
                ready = true;
                status = "Google TEST ad ready. No revenue in this beta.";
                breakStatus = "Between-match TEST ad ready.";
            }
            @Override public void onAdFailedToLoad(@NonNull LoadAdError error) {
                loading = false;
                ad = null;
                ready = false;
                retryAfter = SystemClock.elapsedRealtime() + 60000;
                status = "Test ad unavailable - you can keep playing.";
                breakStatus = "Between-match ad unavailable (code " + error.getCode() + ").";
            }
        });
    }

    public static void setEntryBannerVisible(Activity activity, boolean visible) {
        if (!usable(activity)) return;
        activity.runOnUiThread(() -> {
            entryVisible = visible;
            if (!visible) { destroyBanner(); return; }
            prepare(activity);
            loadEntryBanner(activity);
        });
    }

    private static void destroyBanner() {
        if (banner == null) return;
        AdView previous = banner;
        banner = null;
        if (previous.getParent() instanceof ViewGroup) ((ViewGroup) previous.getParent()).removeView(previous);
        previous.destroy();
    }

    private static void loadEntryBanner(Activity activity) {
        if (!entryVisible || !usable(activity) || banner != null || !initialized
                || consent == null || !consent.canRequestAds()
                || SystemClock.elapsedRealtime() < bannerRetryAfter) return;
        AdView view = new AdView(activity);
        banner = view;
        view.setAdSize(AdSize.BANNER); // Fixed 320x50 dp; Kivy reserves a separate 64 dp footer.
        view.setAdUnitId(TEST_BANNER);
        FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT,
            Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL);
        params.bottomMargin = Math.round(8 * activity.getResources().getDisplayMetrics().density);
        activity.addContentView(view, params);
        view.setAdListener(new AdListener() {
            @Override public void onAdLoaded() {
                if (!entryVisible || banner != view) return;
                status = "Google TEST banner ready. No revenue in this beta.";
            }
            @Override public void onAdFailedToLoad(@NonNull LoadAdError error) {
                if (banner != view) return;
                bannerRetryAfter = SystemClock.elapsedRealtime() + 60000;
                destroyBanner();
            }
        });
        Bundle extras = new Bundle();
        extras.putString("npa", "1");
        view.loadAd(new AdRequest.Builder().addNetworkExtrasBundle(AdMobAdapter.class, extras).build());
    }

    public static synchronized boolean isReady() {
        return ready && !reserved && SystemClock.elapsedRealtime() - loadedAt < EXPIRY;
    }

    public static synchronized boolean showAtBreak(Activity activity) {
        if (!usable(activity) || !isReady()) return false;
        reserved = true;
        ready = false;
        activity.runOnUiThread(() -> {
            InterstitialAd current = ad;
            ad = null;
            if (!usable(activity) || current == null || consent == null || !consent.canRequestAds()) {
                reserved = false;
                return;
            }
            current.setFullScreenContentCallback(new FullScreenContentCallback() {
                @Override public void onAdDismissedFullScreenContent() { finish(activity); }
                @Override public void onAdFailedToShowFullScreenContent(@NonNull AdError error) { finish(activity); }
            });
            status = "Showing a Google TEST ad.";
            breakStatus = "Showing the between-match TEST ad.";
            current.show(activity);
        });
        return true;
    }

    private static void finish(Activity activity) {
        reserved = false;
        status = "Test ad closed.";
        breakStatus = "Between-match ad closed.";
        load(activity); // Prefetch only. Never show on load completion or resume.
    }

    private static SharedPreferences rewards(Activity activity) {
        return activity.getApplicationContext().getSharedPreferences("scorer_ad_rewards", 0);
    }

    public static synchronized String peekReward(Activity activity) {
        if (pendingReward.isEmpty() && activity != null)
            pendingReward = rewards(activity).getString("pending", "");
        return pendingReward;
    }

    public static synchronized void acknowledgeReward(Activity activity, String token) {
        String record = peekReward(activity);
        if (record.startsWith(token + "|") && rewards(activity).edit().remove("pending").commit())
            pendingReward = "";
    }

    public static void prepareReward(Activity activity) {
        if (!usable(activity)) return;
        activity.runOnUiThread(() -> {
            rewardWanted = true;
            prepare(activity);
            loadReward(activity);
        });
    }

    private static void loadReward(Activity activity) {
        if (!rewardWanted || !usable(activity) || !initialized || rewardLoading || reserved
                || consent == null || !consent.canRequestAds() || !peekReward(activity).isEmpty()) return;
        if (rewardReady && SystemClock.elapsedRealtime() - rewardLoadedAt < EXPIRY) return;
        rewardReady = false;
        rewardAd = null;
        if (SystemClock.elapsedRealtime() < rewardRetryAfter) return;
        rewardLoading = true;
        rewardStatus = "Loading the optional morale TEST ad.";
        Bundle extras = new Bundle();
        extras.putString("npa", "1");
        RewardedAd.load(activity, TEST_REWARD,
            new AdRequest.Builder().addNetworkExtrasBundle(AdMobAdapter.class, extras).build(),
            new RewardedAdLoadCallback() {
                @Override public void onAdLoaded(@NonNull RewardedAd loaded) {
                    rewardAd = loaded;
                    rewardLoadedAt = SystemClock.elapsedRealtime();
                    rewardReady = true;
                    rewardLoading = false;
                    rewardStatus = "Optional morale TEST ad ready.";
                }
                @Override public void onAdFailedToLoad(@NonNull LoadAdError error) {
                    rewardAd = null;
                    rewardReady = rewardLoading = false;
                    rewardRetryAfter = SystemClock.elapsedRealtime() + 60000;
                    rewardStatus = "Reward ad unavailable (code " + error.getCode() + ").";
                }
            });
    }

    public static synchronized boolean showReward(Activity activity, String context) {
        if (!usable(activity) || reserved || !rewardReady
                || SystemClock.elapsedRealtime() - rewardLoadedAt >= EXPIRY
                || context == null || !context.matches("[a-f0-9]{64}")
                || !peekReward(activity).isEmpty()) return false;
        reserved = true;
        rewardReady = false;
        activity.runOnUiThread(() -> {
            RewardedAd current = rewardAd;
            rewardAd = null;
            if (!usable(activity) || current == null || consent == null || !consent.canRequestAds()) {
                reserved = false;
                return;
            }
            final String token = UUID.randomUUID().toString();
            current.setFullScreenContentCallback(new FullScreenContentCallback() {
                @Override public void onAdDismissedFullScreenContent() {
                    reserved = false;
                    rewardStatus = "Reward ad closed. Only completed rewards grant morale.";
                }
                @Override public void onAdFailedToShowFullScreenContent(@NonNull AdError error) {
                    reserved = false;
                    rewardStatus = "Reward ad could not be shown. No morale granted.";
                }
            });
            rewardStatus = "Showing the optional morale TEST ad.";
            current.show(activity, item -> {
                // Only the Google onUserEarnedReward callback can create this record.
                // No reward on load/show/dismiss. Context stays local, not in AdRequest.
                synchronized (ScorerAds.class) {
                    if (!pendingReward.isEmpty()) return;
                    pendingReward = token + "|" + context;
                    rewards(activity).edit().putString("pending", pendingReward).commit();
                }
                rewardStatus = "Reward earned. Saving +1 morale in your career.";
            });
        });
        return true;
    }

    public static String getBreakStatus() { return breakStatus; }
    public static String getRewardStatus() { return rewardStatus; }

    public static String getStatus() { return status; }

    public static boolean isPrivacyOptionsRequired() {
        return consent != null && consent.getPrivacyOptionsRequirementStatus()
            == ConsentInformation.PrivacyOptionsRequirementStatus.REQUIRED;
    }

    public static void showPrivacyOptions(Activity activity) {
        if (!usable(activity)) return;
        activity.runOnUiThread(() -> {
            if (consent != null && consent.getPrivacyOptionsRequirementStatus()
                    == ConsentInformation.PrivacyOptionsRequirementStatus.REQUIRED) {
                ready = false;
                ad = null;
                UserMessagingPlatform.showPrivacyOptionsForm(activity, error -> {
                    if (consent.canRequestAds()) load(activity);
                });
            }
        });
    }
}

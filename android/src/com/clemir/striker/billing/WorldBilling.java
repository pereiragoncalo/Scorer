package com.clemir.striker.billing;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.util.Base64;
import com.android.billingclient.api.*;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.Signature;
import java.security.spec.X509EncodedKeySpec;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.json.JSONObject;

/** Non-consumable Play purchase. Only a server-signed, installation-bound licence grants access. */
public final class WorldBilling {
    private static BillingClient client;
    private static ProductDetails product;
    private static volatile String displayPrice = "", message = "Purchases are not activated in this build.";
    private static boolean connecting = false, flowActive = false;
    private static volatile boolean checking = false, pendingPurchase = false;
    private static final ExecutorService IO = Executors.newSingleThreadExecutor();
    private static final long MAX_OFFLINE_SECONDS = 7 * 24 * 3600;
    private static long nextReconnect = 0;
    private WorldBilling() {}

    private static SharedPreferences prefs(Context c) {
        return c.getSharedPreferences("scorer_verified_world", Context.MODE_PRIVATE);
    }
    private static synchronized String installation(Context c) {
        String id = prefs(c).getString("installation", "");
        if (id.isEmpty()) {
            id = UUID.randomUUID().toString();
            prefs(c).edit().putString("installation", id).commit();
        }
        return id;
    }
    public static boolean hasAccess(Activity a) {
        if (!BillingConfig.ENABLED || a == null) return false;
        try {
            String saved = prefs(a).getString("licence", "");
            if (saved.isEmpty()) return false;
            JSONObject licence = verify(a, new JSONObject(saved), null);
            long now = System.currentTimeMillis() / 1000;
            // Detect substantial clock rollback. Never extend expiry by changing the device date.
            long seen = prefs(a).getLong("last_seen", 0);
            if (now + 300 < seen || licence.getLong("expires_at") <= now) return false;
            if (now > seen) prefs(a).edit().putLong("last_seen", now).apply();
            return true;
        } catch (Exception e) { return false; }
    }
    public static String status(Activity a) { return message; }
    public static String price(Activity a) { return displayPrice; }
    public static boolean canPurchase(Activity a) {
        return BillingConfig.ENABLED && a != null && client != null && client.isReady()
            && product != null && !displayPrice.isEmpty() && !flowActive && !checking && !pendingPurchase && !hasAccess(a);
    }
    public static void prepare(Activity a) {
        if (!BillingConfig.ENABLED || a == null || a.isFinishing()) return;
        a.runOnUiThread(() -> connect(a));
    }
    private static void connect(Activity a) {
        if (client != null && client.isReady()) { queryProduct(); return; }
        if (connecting || android.os.SystemClock.elapsedRealtime() < nextReconnect) return;
        connecting = true;
        message = "Connecting to Google Play.";
        if (client == null) {
            client = BillingClient.newBuilder(a.getApplicationContext())
                .setListener((result, purchases) -> {
                    flowActive = false;
                    if (result.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
                        for (Purchase p : purchases) process(a, p);
                    } else if (result.getResponseCode() == BillingClient.BillingResponseCode.ITEM_ALREADY_OWNED) {
                        queryOwned(a);
                    } else if (result.getResponseCode() == BillingClient.BillingResponseCode.USER_CANCELED) {
                        message = "Purchase cancelled. Your Free career is unchanged.";
                    } else {
                        message = "Purchase unavailable. No World access granted. Try Restore purchase.";
                    }
                })
                .enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())
                .enableAutoServiceReconnection().build();
        }
        client.startConnection(new BillingClientStateListener() {
            public void onBillingSetupFinished(BillingResult r) {
                connecting = false;
                if (r.getResponseCode() == BillingClient.BillingResponseCode.OK) {
                    queryProduct(); queryOwned(a);
                } else {
                    nextReconnect = android.os.SystemClock.elapsedRealtime() + 30000;
                    message = "Google Play unavailable. Free play and valid offline World access remain available.";
                }
            }
            public void onBillingServiceDisconnected() { connecting = false; }
        });
    }
    private static void queryProduct() {
        QueryProductDetailsParams.Product item = QueryProductDetailsParams.Product.newBuilder()
            .setProductId(BillingConfig.PRODUCT).setProductType(BillingClient.ProductType.INAPP).build();
        client.queryProductDetailsAsync(QueryProductDetailsParams.newBuilder()
            .setProductList(Collections.singletonList(item)).build(), (r, result) -> {
                product = null; displayPrice = "";
                if (r.getResponseCode() == BillingClient.BillingResponseCode.OK) {
                    for (ProductDetails detail : result.getProductDetailsList()) {
                        if (!BillingConfig.PRODUCT.equals(detail.getProductId())) continue;
                        ProductDetails.OneTimePurchaseOfferDetails offer = detail.getOneTimePurchaseOfferDetails();
                        if (offer != null) { product = detail; displayPrice = offer.getFormattedPrice(); }
                    }
                }
                if (product == null) message = "World product is not available on Google Play yet.";
            });
    }
    public static void purchase(Activity a) {
        if (a == null) return;
        a.runOnUiThread(() -> {
            if (!canPurchase(a)) { prepare(a); return; }
            BillingFlowParams.ProductDetailsParams.Builder detail = BillingFlowParams.ProductDetailsParams.newBuilder().setProductDetails(product);
            ProductDetails.OneTimePurchaseOfferDetails offer = product.getOneTimePurchaseOfferDetails();
            if (offer != null && offer.getOfferToken() != null) detail.setOfferToken(offer.getOfferToken());
            BillingFlowParams flow = BillingFlowParams.newBuilder()
                .setProductDetailsParamsList(Collections.singletonList(detail.build())).build();
            flowActive = true;
            BillingResult r = client.launchBillingFlow(a, flow);
            if (r.getResponseCode() != BillingClient.BillingResponseCode.OK) {
                flowActive = false; message = "Google Play could not open the purchase confirmation.";
            }
        });
    }
    public static void restore(Activity a) {
        if (!BillingConfig.ENABLED || a == null) return;
        a.runOnUiThread(() -> {
            if (client == null || !client.isReady()) { connect(a); return; }
            queryOwned(a);
        });
    }
    private static void queryOwned(Activity a) {
        client.queryPurchasesAsync(QueryPurchasesParams.newBuilder().setProductType(BillingClient.ProductType.INAPP).build(), (r, purchases) -> {
            if (r.getResponseCode() != BillingClient.BillingResponseCode.OK) {
                message = "Could not restore purchases. Please check the purchasing Google account and retry."; return;
            }
            boolean found = false;
            for (Purchase p : purchases) {
                if (p.getProducts().contains(BillingConfig.PRODUCT)) { found = true; process(a, p); }
            }
            if (!found) {
                pendingPurchase = false;
                prefs(a).edit().remove("licence").apply();
                message = "No World purchase found for this Google account.";
            }
        });
    }
    private static void process(Activity a, Purchase p) {
        if (!p.getProducts().contains(BillingConfig.PRODUCT)) return;
        if (p.getPurchaseState() == Purchase.PurchaseState.PENDING) {
            pendingPurchase = true;
            message = "Payment pending. World unlocks only after Google confirms payment and verification."; return;
        }
        if (p.getPurchaseState() != Purchase.PurchaseState.PURCHASED || checking) return;
        pendingPurchase = false;
        checking = true; message = "Verifying your World purchase securely.";
        // Purchase tokens and server credentials never enter Python saves, logs or ad requests.
        IO.execute(() -> {
            try {
                if (!BillingConfig.VERIFY_URL.startsWith("https://")) throw new SecurityException();
                String nonce = UUID.randomUUID().toString();
                JSONObject request = new JSONObject().put("package", a.getPackageName())
                    .put("product", BillingConfig.PRODUCT).put("purchase_token", p.getPurchaseToken())
                    .put("installation", installation(a)).put("nonce", nonce);
                HttpsURLConnection c = (HttpsURLConnection) new URL(BillingConfig.VERIFY_URL).openConnection();
                try {
                    c.setInstanceFollowRedirects(false); c.setConnectTimeout(10000); c.setReadTimeout(15000);
                    c.setRequestMethod("POST"); c.setDoOutput(true); c.setRequestProperty("Content-Type", "application/json");
                    byte[] bytes = request.toString().getBytes(StandardCharsets.UTF_8);
                    c.setFixedLengthStreamingMode(bytes.length);
                    try (java.io.OutputStream out = c.getOutputStream()) { out.write(bytes); }
                    int code = c.getResponseCode();
                    if (code == 403) {
                        prefs(a).edit().remove("licence").commit();
                        throw new SecurityException();
                    }
                    if (code != 200) throw new java.io.IOException();
                    JSONObject receipt = new JSONObject(readLimited(c.getInputStream()));
                    verify(a, receipt, nonce);
                    if (!prefs(a).edit().putString("licence", receipt.toString())
                        .putLong("last_seen", System.currentTimeMillis()/1000).commit()) throw new java.io.IOException();
                    message = "World purchase verified. Returning to your career.";
                } finally { c.disconnect(); }
            } catch (Exception e) {
                message = "Purchase verification unavailable. No new access granted. Retry Restore purchase; do not pay again.";
            } finally { checking = false; }
        });
    }
    private static String readLimited(InputStream stream) throws Exception {
        try (InputStream in = stream; ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[2048]; int read;
            while ((read = in.read(buffer)) != -1) {
                if (out.size() + read > 16384) throw new SecurityException();
                out.write(buffer, 0, read);
            }
            return out.toString("UTF-8");
        }
    }
    private static JSONObject verify(Context c, JSONObject envelope, String nonce) throws Exception {
        byte[] payload = Base64.decode(envelope.getString("payload"), Base64.NO_WRAP);
        Signature sig = Signature.getInstance("SHA256withRSA");
        sig.initVerify(KeyFactory.getInstance("RSA").generatePublic(new X509EncodedKeySpec(
            Base64.decode(BillingConfig.LICENSE_PUBLIC_KEY, Base64.NO_WRAP))));
        sig.update(payload);
        if (!sig.verify(Base64.decode(envelope.getString("signature"), Base64.NO_WRAP))) throw new SecurityException();
        JSONObject data = new JSONObject(new String(payload, StandardCharsets.UTF_8));
        long now = System.currentTimeMillis()/1000, issued = data.getLong("issued_at"), expiry = data.getLong("expires_at");
        if (data.getInt("version") != 1 || !c.getPackageName().equals(data.getString("package"))
            || !BillingConfig.PRODUCT.equals(data.getString("product")) || !installation(c).equals(data.getString("installation"))
            || (nonce != null && !nonce.equals(data.getString("nonce"))) || issued > now+300
            || expiry <= now || expiry <= issued || expiry-issued > MAX_OFFLINE_SECONDS) throw new SecurityException();
        return data;
    }
}

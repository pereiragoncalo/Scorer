package com.clemir.striker.files;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.charset.CodingErrorAction;

/** User-selected SAF documents only; no storage or network permission. */
public final class LocalNameFiles {
    private static final int LIMIT = 262144;
    public static void chooseImport(Activity activity) {
        activity.runOnUiThread(() -> {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.setType("application/json");
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            activity.startActivityForResult(intent, 7241);
        });
    }
    public static void chooseExport(Activity activity) {
        activity.runOnUiThread(() -> {
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.setType("application/json");
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.putExtra(Intent.EXTRA_TITLE, "scorer-world-names.json");
            activity.startActivityForResult(intent, 7242);
        });
    }
    public static void chooseCareerImport(Activity activity) { chooseCareer(activity, false); }
    public static void chooseCareerExport(Activity activity) { chooseCareer(activity, true); }
    private static void chooseCareer(Activity activity, boolean exporting) {
        activity.runOnUiThread(() -> {
            Intent intent = new Intent(exporting ? Intent.ACTION_CREATE_DOCUMENT : Intent.ACTION_OPEN_DOCUMENT);
            intent.setType("application/json"); intent.addCategory(Intent.CATEGORY_OPENABLE);
            if (exporting) intent.putExtra(Intent.EXTRA_TITLE, "scorer-career.json");
            activity.startActivityForResult(intent, exporting ? 7244 : 7243);
        });
    }
    public static String readCareer(Activity activity, Uri uri) throws Exception { return readBounded(activity, uri, 8388608); }
    public static void writeCareer(Activity activity, Uri uri, String text) throws Exception { writeBounded(activity, uri, text, 8388608); }
    public static String read(Activity activity, Uri uri) throws Exception { return readBounded(activity, uri, LIMIT); }
    private static String readBounded(Activity activity, Uri uri, int limit) throws Exception {
        try (InputStream stream = activity.getContentResolver().openInputStream(uri);
             ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[4096];
            int count;
            while ((count = stream.read(buffer)) != -1) {
                if (bytes.size() + count > limit) throw new IllegalArgumentException("Document exceeds size limit");
                bytes.write(buffer, 0, count);
            }
            return StandardCharsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(bytes.toByteArray())).toString();
        }
    }
    public static void write(Activity activity, Uri uri, String text) throws Exception { writeBounded(activity, uri, text, LIMIT); }
    private static void writeBounded(Activity activity, Uri uri, String text, int limit) throws Exception {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        if (bytes.length > limit) throw new IllegalArgumentException("Document exceeds size limit");
        try (OutputStream stream = activity.getContentResolver().openOutputStream(uri, "wt")) {
            stream.write(bytes);
        }
    }
}

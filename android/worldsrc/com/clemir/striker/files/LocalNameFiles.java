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
    public static String read(Activity activity, Uri uri) throws Exception {
        try (InputStream stream = activity.getContentResolver().openInputStream(uri);
             ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[4096];
            int count;
            while ((count = stream.read(buffer)) != -1) {
                if (bytes.size() + count > LIMIT) throw new IllegalArgumentException("Name pack exceeds 256 KiB");
                bytes.write(buffer, 0, count);
            }
            return StandardCharsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(bytes.toByteArray())).toString();
        }
    }
    public static void write(Activity activity, Uri uri, String text) throws Exception {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        if (bytes.length > LIMIT) throw new IllegalArgumentException("Name pack exceeds 256 KiB");
        try (OutputStream stream = activity.getContentResolver().openOutputStream(uri, "wt")) {
            stream.write(bytes);
        }
    }
}

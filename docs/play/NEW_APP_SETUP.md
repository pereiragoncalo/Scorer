# Create Scorer World in Google Play Console

Owner confirmed that no app exists yet. This is new enrollment, not an upload-key replacement.

## Console app creation

Choose **Create app** and enter:

- App name: **Scorer World**.
- Default language: **English (United States), en-US**.
- App or game: **Game**.
- Free or paid: **Free**.
- Developer contact: **goncalo@clemir.com**.

Review the declarations shown by Console before accepting them. Create only World;
the legacy Free edition is not part of this launch. The Android package is
`com.clemir.scorerworld`, established when the first bundle is uploaded.

## Signing preparation on the owner's computer

Use Play App Signing with a Google-generated app signing key. Keep the separate
upload key under the owner's control. Do not send its password or private key in chat.
With Python and the JDK installed, from the Scorer repository run:

```sh
python3 tools/play/create_upload_key.py --keystore ~/scorer-signing/scorer-upload.p12
```

This prompts for a new password twice without echo. It refuses an existing path.
Back up the private keystore and password securely in separate storage. Alias:
`scorer-upload`. If a suitable unregistered upload key already exists, use it instead
of generating another. The public certificate can be shared; the private key cannot.

## First release

Use **Internal testing** first. The intended public version is **1.0** and versionCode
**1030000**. The existing QA APK uses DEBUG signing and is not the release bundle.
The AAB still needs production configuration, signing and verification as described
in SIGNING_AND_CONSOLE.md. Do not mark publication assertions as reviewed without evidence.

Use STORE_LISTING.md for the listing and DATA_SAFETY.md for the data inventory.
Complete the actual target audience (including minors), content rating, data safety,
app access (no login), no-ads declaration and free availability forms. Obtain actual
Android screenshots and confirm public policy accessibility. Follow the current
Console requirements for testing and production access; account verification alone
does not establish production eligibility.

Before installing the Play build over a DEBUG installation, export and verify career
recovery: the signatures differ, so ordinary in-place replacement will not work.

No app creation, bundle upload, signing-key enrollment or rollout has been performed
by this guide.

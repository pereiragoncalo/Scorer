Scorer Play internal uploader1.1 fixes the Google400 observed on owner bastion:
"Changes are sent for review automatically. The query parameter
changesNotSentForReview must not be set."

Only that incompatible optional parameter is omitted. ERROR_IF_IN_REVIEW and the
internal-only target remain, with no review-cancelling retry or production/listing/
tester changes. Existing service credential, upload key and signed1030003file stay
in place; original certificate/payload/version/SHA256 guards remain.

Owner live API connection,1030003signature checks, resumable upload and validation
passed. Final commit must be retried with this version; successful commit/device
availability have not yet been observed.24local cases cover the regression and
reusing a matching already-uploaded bundle. No Google credentials received or used
by this cloud/GitHub; private files stay on owner bastion.

Update ONLY the public program, then rerun --publish. No new key, account, AABbuild,
or repeated credential setup is required. Normal Google automatic review applies
to this explicitly authorized internal release; ongoing reviews are never cancelled.

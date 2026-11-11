Owner-side Scorer → Google Play INTERNAL uploader. No changes to the game/AAB.

Python stdlib + OpenSSL + fullJDK. One-time Google service-account authorization
is required, scoped only to Scorer's read/testing release permissions. Keys and
passwords remain on owner bastion. Google Cloud project creation/API enablement
are being performed by owner; no live credentials or API upload from this cloud.

Program pins the approved1030003 content and original upload certificate, performs
resumable uploads, validates the edit and commits only internal. Review safety
flags stay enabled; no production/listing/tester changes or automatic review
cancellation. Existing/newer-version/hash guards and local lock prevent mistakes.

23local scenarios pass across host/fullJDK fixtures. Live account connection and
first real Google API upload still require owner setup; see attached instructions.
Never upload the P12, its password, or service-account JSON to chat/GitHub.

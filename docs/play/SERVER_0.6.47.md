# Install World 0.6.47 server and final English policy

Run this entire block in the laptop's **root session** (`#`, after `su -`). It installs the reviewed source commit below, keeps the existing administrator credential/database and does not change either Cloudflare tunnel. The existing publicacao checkout is root-owned; the safe-directory exception is scoped to this exact command/path. Stop on any error.

```bash
bash -e <<'SH'
git -c safe.directory=/home/clemir/scorer-publicacao-0646 -C /home/clemir/scorer-publicacao-0646 fetch --depth 1 origin 19c13b10d51e9dc49f4bbd70f34f66b82cb50ffc
git -c safe.directory=/home/clemir/scorer-publicacao-0646 -C /home/clemir/scorer-publicacao-0646 worktree add --detach /home/clemir/scorer-world-0647-19c13b1 19c13b10d51e9dc49f4bbd70f34f66b82cb50ffc
bash /home/clemir/scorer-world-0647-19c13b1/server/install_online.sh
python3 /home/clemir/scorer-world-0647-19c13b1/server/install_public_policy.py
curl --fail https://stats.clemir.com/health
scorer_policy_page="$(mktemp)"
trap 'rm -f "$scorer_policy_page"' EXIT
curl --fail --silent --show-error https://stats.clemir.com/privacy -o "$scorer_policy_page"
python3 - "$scorer_policy_page" <<'PYCODE'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text()
assert 'lang="en"' in text and 'lang="pt-PT"' not in text
assert 'data-publication-status="published"' in text
assert 'DRAFT UNDER REVIEW' not in text
assert 'Scorer World Privacy Policy' in text and 'Privacy requests and suspension' in text
print('Final English World policy is live.')
PYCODE
curl --fail --silent --show-error --output /dev/null https://stats.clemir.com/terms
curl --fail --silent --show-error --output /dev/null https://stats.clemir.com/delete
printf '\nWorld public-page checks passed.\n'
SH
```

If this fresh worktree directory already exists, do not delete it or reset it blindly; check its commit and the prior command's error before retrying. Do not use global `safe.directory=*`, change repository ownership or expose the administrator environment file.

Then install the matching World 0.6.47 APK (debug QA, not Play production signing), use **Privacy > Privacy rights**, and verify an actual test request reaches the new **Privacy requests** section at `/admin`. Collection pauses immediately, even offline; admin Grant keeps it paused. Only an explicit requester withdrawal resumes counting on the next opening after server confirmation. A public case reference is safe to use with support; never send its secret token. This operator test does not publish a football record.

The cloud prepared and locally tested these files. It has no SSH connection to the laptop; running this block is the deployment step. Google Play signing, actual Android/Play testing/screenshots and Console forms remain separate.

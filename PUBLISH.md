# Publishing the prepared Git commit

Destination: **`dimkadimon/No3InLine`**. A new repository is to be public; an existing repository keeps its visibility, branch history and unrelated files. The paper is prepared for arXiv-style typesetting; nothing here submits it to arXiv.

A `.bundle` distributed alongside the paper contains the source tree **and the actual local commit**, without credentials. To publish it from a machine where you control the GitHub login:

```sh
git clone -b main No3InLine-R4.bundle No3InLine
cd No3InLine
gh auth login --hostname github.com --web      # skip if already signed in as dimkadimon
python3 scripts/publish.py                     # authenticated inspection; no remote writes
python3 scripts/publish.py --apply             # publish and read back the remote commit SHA
```

The script uses the GitHub CLI credential helper; it does not require a token on the command line or a token file. `git clone` from a bundle sets `origin` to a local filename. After a successful publication, optionally reset it for future work: `git remote set-url origin https://github.com/dimkadimon/No3InLine.git`, then `git fetch origin`. If an existing repository was merged, check out the published default branch before making subsequent edits.

**Safeguards.** A 404 without authentication does not prove a repository does not exist. The script first authenticates and checks the repository through the API. If the owner is authenticated and the name is absent, `gh repo create --public` requests an empty public repository. If the target exists, the script does not change its visibility. It checks out the existing default branch in a disposable clone and merges the release (even when the histories were originally unrelated). It does not choose between conflicting file versions, remove unrelated files, force-push, or turn off branch protection. On a conflict or rejected push, use a reviewed merge or pull request instead. An identical branch tip is confirmed with `git ls-remote` after a successful push.

Keep access tokens out of the repository, URLs, chat, and shell commands. Use a credential manager or the browser login.

The repository is public. R3 uses the annotated tag `review-r3`. The earlier R2 manuscript is at `review-r2-2026-11-19`, and the exact replay kit is pinned separately to data commit `e19b8a1b689eba392c7d26ec3733e88db566dc0e`. Verify tag targets before creating a release. Never force-push a branch, overwrite a published tag, or replace an existing release asset silently. A GitHub working release is not author sign-off, peer review, a DOI or an arXiv submission.

## R4 branch and tag

For a checkout of the verified R4 bundle, `main` and the annotated `review-r4` tag identify the same commit. On a machine with an authorized GitHub account, a safe fast-forward publication of both refs is:

```sh
gh auth setup-git --hostname github.com
url=https://github.com/dimkadimon/No3InLine.git
git fetch --no-tags "$url" refs/heads/main && git merge-base --is-ancestor FETCH_HEAD main && git push --atomic "$url" refs/heads/main:refs/heads/main refs/tags/review-r4:refs/tags/review-r4
git ls-remote "$url" refs/heads/main 'refs/tags/review-r4^{}'
```

Compare both returned SHAs with `git rev-parse 'review-r4^{commit}'`. Stop on divergence, conflicting tag or branch protection; do not force a push. Previous annotated tags and release assets are kept intact. For the separate arXiv step use the [submission sheet](paper/arxiv-submission.md), not the bundle.

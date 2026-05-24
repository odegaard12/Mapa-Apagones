# Public pages truthfulness refresh v0.10.7.6

## Problem fixed

The public distributor pages were technically based on repository data, but their wording could be misleading.

Issues fixed:

- The public changelog could show a newer entry after older historical entries.
- The coverage page could make "100% with hint" look like "100% verified".
- The coverage page did not clearly explain that confidence counts may count distributor entries, not unique zones.
- The reliability page looked like an old audit page rather than current criteria plus historical audit context.

## Changes

- Reordered public changelog with a new top entry.
- Clarified distributor coverage wording.
- Clarified that `regional_default` is orientation, not municipal verification.
- Clarified that `verified_partial` is partial/source-backed and not exclusive.
- Added a public pages truthfulness guard.
- Integrated that guard into `post_merge_validate.sh`.

## Static deployment note

These pages are static files under `frontend/public/` and are deployed by Cloudflare Pages from the repository.

The backend/API data may come from the Raspberry Pi, but these public HTML pages only change after the repository is updated and Cloudflare Pages deploys the new build.

## Safety

No distributor hints are imported.

No CUPS, addresses, exact coordinates, customer data, private grid inventory, raw external API responses, secrets, backups or logs are added.

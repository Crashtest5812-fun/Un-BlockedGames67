# Crashtest Games

## Game catalog

Games are listed in the `games` array in `index.html`. Keep the name, category,
game-page path or HTTPS URL, and optional image or emoji in sync when adding a
game. When both image and emoji are null, the card displays its gradient artwork
without an icon. Search matches game names and categories. The menu keeps the
five most recently opened games in that browser for quick access.

Run the catalog checks before publishing:

```sh
python scripts/validate_catalog.py
```

The check verifies game and app paths, local image files, and catalog fields.
External image URLs are syntax-checked; their availability depends on the
external host.

## License

Original code and documentation authored by Adrian Virrueta are released under
the MIT License; see [`LICENSE`](./LICENSE). This does not cover third-party
games, files in `Assets/Games/`, or third-party artwork, images, fonts,
libraries, or other materials. Those remain subject to their respective
licenses and permissions. This software license is separate from the site's
Terms of Service, which govern use of the website.

## Supabase ratings setup

The initial ratings schema is in [`supabase/schema.sql`](./supabase/schema.sql).
To enable it:

1. Create a Supabase project and run that SQL in the project's SQL Editor.
2. Enable anonymous sign-ins in the Supabase Auth provider settings. Anonymous
   sessions use the `authenticated` database role, so each session can create
   and update only its own rating. Signed-in users can use the same ratings.
3. The current site is configured with this project's URL and publishable key
   in `index.html`. The key is intended for browser use; never put a secret or
   `service_role` key in the site.

Ratings are keyed by each game's catalog `href`. Individual ratings are private
to their owner; the `game_rating_summary` view exposes only each game's average
and rating count. The game browser loads community averages and lets guests
create or update their own rating. Anonymous sessions persist in the same
browser; clearing browser storage loses access to that guest identity.

## Before release

- Review the Terms of Service and Confidentiality Policy with the site owner.
- Confirm the school Google Form's access, email-collection, and verification
  settings; the website cannot inspect or verify the form's configuration.
- Check the version, policy effective dates, contact details, and permissions
  for third-party games and media.
- Test the deployed site on desktop and mobile, including keyboard navigation,
  the policy dialog, the menu, game and app links, and audio controls.
- Check external images and other hosted assets manually; the catalog check
  only validates external image URL syntax.
# Un-BlockedGames67

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
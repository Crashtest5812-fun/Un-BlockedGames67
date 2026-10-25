# Un-BlockedGames67

## Game catalog

Games are listed in the `games` array in `index.html`. Each game also needs a
matching description in the `gameDescriptions` map. Keep the name, category,
game-page path, and image or emoji fallback in sync when adding a game.

Run the catalog checks before publishing:

```sh
python scripts/validate_catalog.py
```

The check verifies game and app paths, local image files, catalog fields, and
descriptions. External image URLs are syntax-checked; their availability depends
on the external host.
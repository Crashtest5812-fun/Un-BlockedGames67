# Un-BlockedGames67

## Game catalog

Games are listed in the `games` array in `index.html`. Keep the name, category,
game-page path, and image or emoji fallback in sync when adding a game. Search
matches game names and categories. The menu keeps the five most recently opened
games in that browser for quick access.

Run the catalog checks before publishing:

```sh
python scripts/validate_catalog.py
```

The check verifies game and app paths, local image files, and catalog fields.
External image URLs are syntax-checked; their availability depends on the
external host.
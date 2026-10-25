import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
GAME_DATA_PATTERN = re.compile(r"const games = (\[.*?\]);\s+const gameDescriptions", re.S)
ALLOWED_CATEGORIES = {"Sports", "Racing", "Arcade", "Puzzle", "Casual", "Other"}


def local_file(reference):
    path = (ROOT / unquote(reference)).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {reference}")
    return path


def main():
    content = INDEX.read_text(encoding="utf-8")
    match = GAME_DATA_PATTERN.search(content)
    if not match:
        raise ValueError("Could not find the game catalog in index.html")

    games = json.loads(match.group(1))
    errors = []
    names = set()
    hrefs = set()
    external_images = 0

    for game in games:
        name = game.get("name")
        href = game.get("href")
        image = game.get("image")
        category = game.get("category")

        if not isinstance(name, str) or not name.strip():
            errors.append("Game has no name")
            continue
        if name in names:
            errors.append(f"{name}: duplicate game name")
        names.add(name)

        if not isinstance(href, str) or not href:
            errors.append(f"{name}: missing game link")
        elif href in hrefs:
            errors.append(f"{name}: duplicate game link {href}")
        else:
            hrefs.add(href)
            try:
                if not local_file(href).is_file():
                    errors.append(f"{name}: game file does not exist: {href}")
            except ValueError as error:
                errors.append(f"{name}: {error}")

        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{name}: invalid category {category!r}")

        if image:
            parsed_image = urlparse(image)
            if parsed_image.scheme:
                if parsed_image.scheme not in {"http", "https"} or not parsed_image.netloc:
                    errors.append(f"{name}: invalid image URL: {image}")
                else:
                    external_images += 1
            else:
                try:
                    if not local_file(image).is_file():
                        errors.append(f"{name}: local image does not exist: {image}")
                except ValueError as error:
                    errors.append(f"{name}: {error}")
        elif not isinstance(game.get("emoji"), str) or not game["emoji"]:
            errors.append(f"{name}: needs an image or an emoji fallback")

        if not isinstance(game.get("artStart"), str) or not isinstance(game.get("artEnd"), str):
            errors.append(f"{name}: missing card artwork colors")

    descriptions = re.search(r"const gameDescriptions = new Map\(\[(.*?)\]\);", content, re.S)
    if not descriptions:
        errors.append("Could not find game descriptions")
    else:
        description_names = set(re.findall(r'\["([^"]+)",\s*"([^"]+)"\]', descriptions.group(1)))
        described_names = {name for name, _ in description_names}
        missing_descriptions = names - described_names
        extra_descriptions = described_names - names
        errors.extend(f"{name}: missing description" for name in sorted(missing_descriptions))
        errors.extend(f"{name}: description has no matching game" for name in sorted(extra_descriptions))

    app_links = re.findall(r'href="(Assets/Apps/[^"]+)"', content)
    for href in app_links:
        try:
            if not local_file(href).is_file():
                errors.append(f"App file does not exist: {href}")
        except ValueError as error:
            errors.append(str(error))

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Catalog valid: {len(games)} games, {len(app_links)} app links, "
        f"{external_images} external image URLs."
    )
    print("External image URLs are syntax-checked only; their availability depends on the host.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

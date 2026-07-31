import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path


def directory_name(category_name: str) -> str:
    return re.sub(r"_\d+$", "", category_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("copy", "move"), default="copy")
    args = parser.parse_args()

    dataset = json.loads(args.annotations.read_text(encoding="utf-8"))
    categories = {category["id"]: category["name"] for category in dataset["categories"]}
    image_categories = defaultdict(set)
    for annotation in dataset["annotations"]:
        category_id = annotation["category_id"]
        if category_id not in categories:
            raise ValueError(f"Неизвестный category_id: {category_id}")
        image_categories[annotation["image_id"]].add(directory_name(categories[category_id]))

    destination_images = args.output_dir / "images"
    destination_annotations = args.output_dir / "annotations"
    destination_images.mkdir(parents=True, exist_ok=True)
    destination_annotations.mkdir(parents=True, exist_ok=True)

    for image in dataset["images"]:
        filename = Path(image["file_name"]).name
        source = args.images_dir / filename
        if not source.is_file():
            raise FileNotFoundError(f"Не найдено изображение: {source}")
        names = sorted(image_categories[image["id"]])
        folder = "_".join(names) if names else "unlabeled"
        destination = destination_images / folder / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        if args.mode == "copy":
            shutil.copy2(source, destination)
        else:
            shutil.move(source, destination)
        image["file_name"] = destination.relative_to(args.output_dir).as_posix()

    output_path = destination_annotations / "updated_annotations.json"
    output_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()

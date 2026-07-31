import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    annotations_path = args.annotations or args.dataset_dir / "annotations" / "updated_annotations.json"
    dataset = json.loads(annotations_path.read_text(encoding="utf-8"))
    class_ids = {category["id"]: index for index, category in enumerate(sorted(dataset["categories"], key=lambda item: item["id"]))}
    annotations_by_image = defaultdict(list)
    for annotation in dataset["annotations"]:
        annotations_by_image[annotation["image_id"]].append(annotation)

    for image in dataset["images"]:
        source = args.dataset_dir / image["file_name"]
        target = args.output_dir / image["file_name"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        lines = []
        for annotation in annotations_by_image[image["id"]]:
            x, y, width, height = annotation["bbox"]
            left = max(0, x)
            top = max(0, y)
            right = min(image["width"], x + width)
            bottom = min(image["height"], y + height)
            if right <= left or bottom <= top:
                continue
            center_x = (left + right) / 2 / image["width"]
            center_y = (top + bottom) / 2 / image["height"]
            normalized_width = (right - left) / image["width"]
            normalized_height = (bottom - top) / image["height"]
            values = [center_x, center_y, normalized_width, normalized_height]
            lines.append(f"{class_ids[annotation['category_id']]} " + " ".join(f"{value:.6f}" for value in values))
        target.with_suffix(".txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

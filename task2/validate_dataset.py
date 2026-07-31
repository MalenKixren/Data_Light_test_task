import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    annotations_path = args.annotations or args.dataset_dir / "annotations" / "updated_annotations.json"
    report_path = args.report or args.dataset_dir / "dataset_report.json"
    dataset = json.loads(annotations_path.read_text(encoding="utf-8"))
    image_ids = {image["id"] for image in dataset["images"]}
    category_ids = {category["id"] for category in dataset["categories"]}
    annotated_image_ids = Counter()
    errors = []

    for image in dataset["images"]:
        image_path = args.dataset_dir / image["file_name"]
        if not image_path.is_file():
            errors.append({"type": "missing_image_file", "image_id": image["id"], "file_name": image["file_name"]})

    for annotation in dataset["annotations"]:
        image_id = annotation["image_id"]
        category_id = annotation["category_id"]
        if image_id not in image_ids:
            errors.append({"type": "unknown_image_id", "annotation_id": annotation.get("id"), "image_id": image_id})
        else:
            annotated_image_ids[image_id] += 1
        if category_id not in category_ids:
            errors.append({"type": "unknown_category_id", "annotation_id": annotation.get("id"), "category_id": category_id})

    report = {
        "images_total": len(dataset["images"]),
        "annotations_total": len(dataset["annotations"]),
        "categories_total": len(dataset["categories"]),
        "empty_images_total": len(image_ids - set(annotated_image_ids)),
        "errors_total": len(errors),
        "errors": errors,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

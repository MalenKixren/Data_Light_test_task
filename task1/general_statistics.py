import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


FIGURE_TAGS = {"box", "polygon", "points"}


def xml_files(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob("annotations*.xml") if not path.stem.endswith("_modified"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    args = parser.parse_args()

    images = []
    figure_count = 0
    annotated_count = 0

    for xml_path in xml_files(args.input_dir):
        root = ET.parse(xml_path).getroot()
        for image in root.findall("image"):
            figures = [element for element in image if element.tag in FIGURE_TAGS]
            images.append(
                {
                    "name": image.get("name", ""),
                    "width": int(float(image.get("width", 0))),
                    "height": int(float(image.get("height", 0))),
                }
            )
            figure_count += len(figures)
            annotated_count += bool(figures)

    if not images:
        raise SystemExit("В XML-файлах не найдены элементы image")

    areas = [image["width"] * image["height"] for image in images]
    smallest_area = min(areas)
    largest_area = max(areas)
    smallest = next(image for image in images if image["width"] * image["height"] == smallest_area)
    largest = next(image for image in images if image["width"] * image["height"] == largest_area)
    result = {
        "images_total": len(images),
        "images_annotated": annotated_count,
        "images_unannotated": len(images) - annotated_count,
        "figures_total": figure_count,
        "smallest_image": {"count": areas.count(smallest_area), **smallest},
        "largest_image": {"count": areas.count(largest_area), **largest},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

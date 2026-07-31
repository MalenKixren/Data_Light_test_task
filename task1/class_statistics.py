import argparse
import json
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


FIGURE_TAGS = {"box", "polygon", "points"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    args = parser.parse_args()

    counts = Counter()
    for xml_path in sorted(args.input_dir.glob("annotations*.xml")):
        if xml_path.stem.endswith("_modified"):
            continue
        root = ET.parse(xml_path).getroot()
        for image in root.findall("image"):
            for figure in image:
                if figure.tag in FIGURE_TAGS:
                    counts[figure.get("label", "<without_label>")] += 1

    print(json.dumps(dict(sorted(counts.items())), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

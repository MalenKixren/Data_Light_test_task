import argparse
from pathlib import Path, PureWindowsPath
import xml.etree.ElementTree as ET


def normalized_name(value: str) -> str:
    filename = PureWindowsPath(value).name
    return f"{Path(filename).stem}.png"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for xml_path in sorted(args.input_dir.glob("annotations*.xml")):
        if xml_path.stem.endswith("_modified"):
            continue
        tree = ET.parse(xml_path)
        root = tree.getroot()
        images = root.findall("image")
        identifiers = [image.get("id", "") for image in images]
        for image, identifier in zip(images, reversed(identifiers)):
            image.set("id", identifier)
            image.set("name", normalized_name(image.get("name", "")))
        ET.indent(tree, space="  ")
        output_path = args.output_dir / f"{xml_path.stem}_modified.xml"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(output_path)


if __name__ == "__main__":
    main()

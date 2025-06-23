import os
import json
import argparse

BASE_OUT = "/valohai/outputs/colmap_processed_dataset"
META_PATH = "/valohai/outputs/valohai.metadata.jsonl"


def main(dataset_name, version_name):
    lines = []
    for root, _, files in os.walk(BASE_OUT):
        for fn in files:
            # ruta relativa desde /valohai/outputs
            rel = os.path.relpath(os.path.join(
                root, fn), "/valohai/outputs")
            lines.append({
                "file": rel,
                "metadata": {
                    # si el dataset no existía, se crea
                    "valohai.dataset-versions": [
                        f"dataset://{dataset_name}/{version_name}"
                    ]
                }
            })

    with open(META_PATH, "w") as out:
        for entry in lines:
            out.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Valohai metadata for a dataset.")
    parser.add_argument("--dataset_name", required=True,
                        help="Name of the dataset.")
    parser.add_argument("--version_name", required=True,
                        help="Version name of the dataset.")
    parser.add_argument("--directory_basename", required=True,
                        help="path to the directory containing the dataset files")
    args = parser.parse_args()

    main(args.dataset_name, args.version_name)

def group_records_by_image(records: list[dict]) -> dict:
    from collections import defaultdict

    result = defaultdict(lambda: {
        "time": None,
        "location": None,
        "objects": set(),
        "relations": []
    })

    for row in records:
        img_id = row["img"]["image_id"]
        result[img_id]["time"] = row["t"]
        result[img_id]["location"] = row["loc"]

        if row["obj"]:
            result[img_id]["objects"].add(row["obj"]["label"])

        if row.get("r"):
            src = row["r"][0].get("label")
            rel = row["r"][1]
            tgt = row["r"][2].get("label")
            if src and tgt:
                result[img_id]["relations"].append({
                    "source": src,
                    "relation": rel,
                    "target": tgt
                })

    for img_id in result:
        result[img_id]["objects"] = sorted(list(result[img_id]["objects"]))

    return dict(result)

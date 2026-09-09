import json
import re
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/chart-api.schema.json").read_text())


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def validate_document(document):
    jsonschema.Draft202012Validator(SCHEMA).validate(document)
    parsed = urlparse(document["api"]["base_url"])
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("invalid URL or embedded credentials")
    for endpoint in ("kline", "trend", "realtime", "batch_realtime"):
        if endpoint not in document["api"]:
            continue
        parser = document["response"].get(endpoint, {})
        if not parser.get("field_mapping") and not parser.get("parser"):
            raise ValueError(f"missing response parser: {endpoint}")
    for key, value in document["api"].get("headers", {}).items():
        if re.search(r"authorization|cookie|api[-_]?key|token|secret", key, re.I) and value:
            raise ValueError(f"do not publish credentials in header {key}")
    text = yaml.safe_dump(document)
    if re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_|-----BEGIN .*PRIVATE KEY-----", text):
        raise ValueError("potential secret detected")


def main():
    identifiers = set()
    count = 0
    for directory in ("providers", "examples"):
        for path in sorted((ROOT / directory).rglob("*")):
            if path.suffix not in (".yaml", ".yml"):
                continue
            if path.is_symlink() or path.stat().st_size > 1024 * 1024:
                raise ValueError(f"invalid file: {path}")
            document = yaml.load(path.read_text(), Loader=UniqueLoader)
            validate_document(document)
            if document["id"] in identifiers:
                raise ValueError(f"duplicate ID: {document['id']}")
            identifiers.add(document["id"])
            if directory == "providers":
                if path.parent.name != document["id"] or path.name != "config.yaml":
                    raise ValueError("expected providers/<id>/config.yaml")
                if not document.get("supported_markets"):
                    raise ValueError("published providers must declare supported_markets")
            count += 1
            print(f"OK {path.relative_to(ROOT)}")
    if not count:
        raise ValueError("no configurations validated")


if __name__ == "__main__":
    main()

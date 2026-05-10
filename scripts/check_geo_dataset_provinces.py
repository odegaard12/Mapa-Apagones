#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "frontend" / "public" / "data"

PROVINCE_KEYS = [
    "province",
    "prov_name",
    "prov_name_local",
    "province_name",
    "provincia",
    "PROVINCIA",
    "NPRO",
    "name_prov",
]

MUNICIPIO_KEYS = [
    "municipio",
    "mun_name",
    "mun_name_local",
    "name",
    "name_es",
    "nombre",
    "NOMBRE",
    "Texto",
    "texto",
    "label",
    "LAU_NAME",
    "lau_name",
    "NAMEUNIT",
    "nameunit",
]

ALLOWED_PROVINCES = {
    "galicia": {"a_coruna", "la_coruna", "lugo", "ourense", "orense", "pontevedra"},
    "asturias": {"asturias"},
    "cantabria": {"cantabria"},
    "castilla_leon": {"avila", "burgos", "leon", "palencia", "salamanca", "segovia", "soria", "valladolid", "zamora"},
    "aragon": {"huesca", "teruel", "zaragoza"},
    "madrid": {"madrid"},
    "navarra": {"navarra"},
    "la_rioja": {"la_rioja"},
    "murcia": {"murcia"},
    "ceuta": {"ceuta"},
    "melilla": {"melilla"},
    "comunitat_valenciana": {"alicante", "alacant", "castellon", "castello", "valencia", "valencia_valencia"},
    "illes_balears": {"illes_balears", "islas_baleares", "baleares"},
    "canarias": {"las_palmas", "santa_cruz_de_tenerife"},
    "euskadi": {"araba", "alava", "araba_alava", "bizkaia", "vizcaya", "gipuzkoa", "guipuzcoa"},
    "extremadura": {"badajoz", "caceres"},
    "castilla_la_mancha": {"albacete", "ciudad_real", "cuenca", "guadalajara", "toledo"},
    "andalucia": {"almeria", "cadiz", "cordoba", "granada", "huelva", "jaen", "malaga", "sevilla"},
    "catalunya": {"barcelona", "girona", "gerona", "lleida", "lerida", "tarragona"},
}


def slug(value: Any = "") -> str:
    text = (
        unicodedata.normalize("NFD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def first_prop(props: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = props.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def dataset_id_from_path(path: Path) -> str:
    return path.name.replace("_municipios.geojson", "")


def main() -> int:
    files = sorted(
        path for path in DATA_DIR.glob("*_municipios.geojson")
        if path.name != "toda_espana_municipios.geojson"
    )

    if not files:
        print("ERROR: no hay datasets *_municipios.geojson")
        return 1

    errors: list[str] = []

    for path in files:
        dataset_id = dataset_id_from_path(path)
        allowed = ALLOWED_PROVINCES.get(dataset_id)

        if not allowed:
            errors.append(f"{path.relative_to(ROOT)}: dataset sin lista de provincias permitidas")
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        features = data.get("features") or []

        for index, feature in enumerate(features):
            props = feature.get("properties") or {}
            municipio = first_prop(props, MUNICIPIO_KEYS) or f"feature#{index}"
            province = first_prop(props, PROVINCE_KEYS)

            if not province:
                errors.append(
                    f"{path.relative_to(ROOT)}: {municipio}: falta provincia"
                )
                continue

            province_slug = slug(province)

            if province_slug not in allowed:
                errors.append(
                    f"{path.relative_to(ROOT)}: {municipio}: provincia no permitida "
                    f"'{province}' para dataset '{dataset_id}'"
                )

    if errors:
        print("ERROR: datasets geográficos con provincias fuera de su ámbito:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"OK geo dataset provinces: {len(files)} datasets revisados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

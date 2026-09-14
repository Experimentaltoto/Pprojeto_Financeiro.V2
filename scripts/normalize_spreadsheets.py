"""CLI para normalização atômica das planilhas financeiras."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finance_normalizer.errors import ImportValidationError
from finance_normalizer.normalizer import normalize_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Padroniza uma planilha financeira para CSV canônico.")
    parser.add_argument("input", type=Path, help="arquivo .xlsx ou .xls")
    parser.add_argument("output", type=Path, help="CSV normalizado de destino")
    parser.add_argument("--source", choices=("auto", "stone", "bank", "tiny"), default="auto")
    parser.add_argument("--category-map", type=Path, help="JSON {categoria_da_origem: categoria_padronizada}")
    args = parser.parse_args()
    try:
        category_map = json.loads(args.category_map.read_text(encoding="utf-8")) if args.category_map else None
        if category_map is not None and not isinstance(category_map, dict):
            raise ValueError("o mapa de categorias deve ser um objeto JSON")
        count = normalize_file(args.input, args.output, args.source, category_map)
    except (ImportValidationError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2
    print(f"OK: {count} registros normalizados em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

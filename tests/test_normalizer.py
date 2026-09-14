import csv
import sys
import unittest
from pathlib import Path

from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from finance_normalizer.errors import ImportValidationError
from finance_normalizer.normalizer import PENDING_CATEGORY, normalize_file


def _write_xlsx(path: Path, rows: list[list[object]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    for row in rows:
        sheet.append(row)
    workbook.save(path)


class NormalizerTests(unittest.TestCase):
    def test_stone_normalizes_brazilian_money_and_preserves_fees(self):
        with self.subTest("stone"):
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as directory:
                source, output = Path(directory) / "stone.xlsx", Path(directory) / "out.csv"
                _write_xlsx(source, [
                    ["STONECODE", "DATA DA VENDA", "VALOR BRUTO", "VALOR LIQUIDO", "DESCONTO DE MDR", "DESCONTO DE ANTECIPACAO", "DESCONTO UNIFICADO", "ULTIMO STATUS", "PRODUTO", "STONE ID"],
                    ["x", "01/09/2026 13:15", "1.234,50", "1.200,00", "-20,00", "0,00", "-14,50", "Aprovada", "Credito", "sale-1"],
                ])
                self.assertEqual(normalize_file(source, output), 1)
                with output.open(encoding="utf-8", newline="") as handle:
                    row = next(csv.DictReader(handle))
                self.assertEqual((row["gross_amount"], row["net_amount"], row["fee_amount"]), ("1234.50", "1200.00", "34.50"))
                self.assertEqual(row["event_at"], "2026-09-01T13:15")

    def test_invalid_file_is_atomic_and_keeps_existing_output(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "bad.xlsx", Path(directory) / "out.csv"
            output.write_text("previous-output", encoding="utf-8")
            _write_xlsx(source, [["STONECODE", "DATA DA VENDA"], ["x", "01/09/2026 13:15"]])
            with self.assertRaises(ImportValidationError):
                normalize_file(source, output)
            self.assertEqual(output.read_text(encoding="utf-8"), "previous-output")

    def test_bank_keeps_candidates_and_marks_unmapped_category_pending(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "bank.xlsx", Path(directory) / "out.csv"
            _write_xlsx(source, [
                ["metadado"], [], ["Data", "Lançamento", "Razão Social", "Valor (R$)", "Saldo (R$)"],
                ["31/08/2026", "SALDO ANTERIOR", "", "", "100,00"],
                ["01/09/2026", "PIX recebido", "Cliente", "10,25", "110,25"],
                ["01/09/2026", "PIX recebido", "Cliente", "10,25", "120,50"],
            ])
            normalize_file(source, output)
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["record_type"], "bank_balance")
            self.assertEqual(rows[1]["category_normalized"], PENDING_CATEGORY)
            self.assertEqual(rows[1]["candidate_duplicate_key"], rows[2]["candidate_duplicate_key"])

    def test_bank_category_map_is_explicit(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "bank.xlsx", Path(directory) / "out.csv"
            _write_xlsx(source, [["Data", "Lançamento", "Valor (R$)"], ["01/09/2026", "Tarifa bancária", "-2,50"]])
            normalize_file(source, output, category_map={"tarifa bancaria": "Tarifas, juros e receitas financeiras"})
            with output.open(encoding="utf-8", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["category_normalized"], "Tarifas, juros e receitas financeiras")

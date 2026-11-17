"""CLI: uv run python -m Back_end.site_cms.modules.metas.geografia.import_cli ..."""
import argparse
import json

from Back_end.site_cms.modules.metas.geografia.parser import read_records, audit_records


def main() -> None:
    p = argparse.ArgumentParser(description="Importação integral de monitoramento territorial das Metas")
    p.add_argument("--file", required=True)
    p.add_argument("--source", choices=["planilha", "json", "smae"], default="planilha")
    p.add_argument("--apply", action="store_true", help="Grava no PostgreSQL; omitido executa apenas auditoria sem DB")
    p.add_argument("--dry-run-db", action="store_true", help="Simula upsert no PostgreSQL com rollback")
    args = p.parse_args()
    rows = read_records(args.file, source=args.source)
    audit = audit_records(rows)
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    if args.apply or args.dry_run_db:
        from Back_end.site_cms.modules.metas.geografia.service import import_rows
        outcome = import_rows(rows, dry_run=not args.apply)
        print("UPSERT:", json.dumps(outcome, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

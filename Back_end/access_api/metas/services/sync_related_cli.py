import json

from Back_end.access_api.metas.services.related_snapshot_service import (
    sync_related_snapshots,
)


def main() -> None:
    result = sync_related_snapshots()
    print(
        json.dumps(
            {
                "received": result.received,
                "created": result.created,
                "updated": result.updated,
                "unchanged": result.unchanged,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

import json

from Back_end.site_cms.modules.metas.smae_bridge import (
    sync_cms_meta_snapshots_from_local,
)


def main() -> None:
    print(
        "[CMS METAS] Aplicando snapshot "
        "do SMAE já sincronizado localmente..."
    )

    result = (
        sync_cms_meta_snapshots_from_local()
    )

    print(
        "\n=== Snapshot SMAE aplicado ==="
    )
    print(
        json.dumps(
            {
                "processed": result[
                    "processed"
                ],
                "changed_fields": result[
                    "changed_fields"
                ],
                "added_fields": result[
                    "added_fields"
                ],
                "conflicts": result[
                    "conflicts"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

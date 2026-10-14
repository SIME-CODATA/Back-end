from Back_end.access_api.metas.services.query_service import list_metas


def main():
    print("Buscando metas no PostgreSQL...")

    metas = list_metas()

    print(f"Metas encontradas localmente: {len(metas)}")

    if metas:
        primeira_meta = metas[0]

        print()
        print("Primeira meta local:")
        print(f"ID local: {primeira_meta.id}")
        print(f"ID SMAE: {primeira_meta.smae_id}")
        print(f"Código: {primeira_meta.codigo}")
        print(f"Título: {primeira_meta.titulo}")


if __name__ == "__main__":
    main()
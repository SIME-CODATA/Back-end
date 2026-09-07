from Back_end.smae.services.meta_service import fetch_metas


def main():
    print("Conectando ao SMAE...")

    metas = fetch_metas()

    print(f"Metas encontradas: {len(metas)}")

    if metas:
        primeira_meta = metas[0]

        print()
        print("Primeira meta:")
        print(f"ID SMAE: {primeira_meta.get('id')}")
        print(f"Código: {primeira_meta.get('codigo')}")
        print(f"Título: {primeira_meta.get('titulo')}")


if __name__ == "__main__":
    main()
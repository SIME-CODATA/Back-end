from Back_end.access_api.metas.services.sync_service import sync_metas


def main():
    print("Sincronizando metas com o SMAE...")

    result = sync_metas()

    print()
    print("Sincronização concluída.")
    print(f"Recebidas do SMAE: {result.received}")
    print(f"Inseridas: {result.inserted}")
    print(f"Atualizadas: {result.updated}")
    print(f"Sem alterações: {result.unchanged}")


if __name__ == "__main__":
    main()
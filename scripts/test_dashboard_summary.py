from Back_end.access_api.metas.services.dashboard_service import get_dashboard_summary


def main():
    print("\n=== Dashboard Summary ===\n")

    summary = get_dashboard_summary()

    print(f"Total de metas: {summary['total_metas']}")
    print(f"Total de temas: {summary['total_temas']}")
    print(f"Metas ativas: {summary['metas_ativas']}")
    print(f"Última sincronização: {summary['ultima_sincronizacao']}")
    print("\nMetas por eixo:")

    for eixo, quantidade in summary["metas_por_eixo"].items():
        print(f"- {eixo}: {quantidade}")


if __name__ == "__main__":
    main()
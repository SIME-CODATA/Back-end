import os


TRUE_VALUES = {
    "1",
    "true",
    "yes",
    "on",
    "sim",
}


def institutional_email_required() -> bool:
    """Indica se o ambiente exige e-mail institucional."""

    value = os.getenv(
        "ENFORCE_INSTITUTIONAL_EMAIL",
        "false",
    )

    return value.strip().lower() in TRUE_VALUES


def allowed_email_domains() -> set[str]:
    """Retorna os domínios institucionais permitidos."""

    raw_domains = os.getenv(
        "ALLOWED_EMAIL_DOMAINS",
        "prefeitura.sp.gov.br",
    )

    return {
        domain.strip().lower().lstrip("@")
        for domain in raw_domains.split(",")
        if domain.strip()
    }


def normalize_email(email: str) -> str:
    """Normaliza e valida a estrutura mínima de um e-mail."""

    normalized = email.strip().lower()

    if (
        not normalized
        or normalized.count("@") != 1
    ):
        raise ValueError(
            "Informe um e-mail válido."
        )

    local_part, domain = normalized.rsplit(
        "@",
        1,
    )

    if not local_part or not domain:
        raise ValueError(
            "Informe um e-mail válido."
        )

    return normalized


def is_institutional_email(
    email: str,
) -> bool:
    """Verifica se o e-mail pertence a um domínio permitido."""

    try:
        normalized = normalize_email(email)
    except ValueError:
        return False

    domain = normalized.rsplit(
        "@",
        1,
    )[1]

    return domain in allowed_email_domains()


def validate_allowed_email(
    email: str,
) -> str:
    """
    Normaliza o e-mail e, quando habilitado no ambiente,
    exige que ele pertença a um domínio institucional.
    """

    normalized = normalize_email(email)

    if not institutional_email_required():
        return normalized

    domain = normalized.rsplit(
        "@",
        1,
    )[1]

    allowed_domains = allowed_email_domains()

    if domain not in allowed_domains:
        readable_domains = ", ".join(
            f"@{item}"
            for item in sorted(allowed_domains)
        )

        raise ValueError(
            "Utilize um e-mail institucional permitido: "
            f"{readable_domains}."
        )

    return normalized

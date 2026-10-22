def canonical_meta_code(value: object) -> str:
    """
    Normaliza a identidade da Meta usada pelo CMS.

    A API antiga usa 01..09 e 10..132.
    O SMAE usa códigos como 001, 023, 132.

    No CMS usamos:
        001 -> 01
        004 -> 04
        056 -> 56
        132 -> 132
    """

    raw = str(value or "").strip()

    if not raw:
        return ""

    if raw.isdigit():
        number = int(raw)

        if number < 10:
            return str(number).zfill(2)

        return str(number)

    return raw

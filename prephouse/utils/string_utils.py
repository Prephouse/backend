def get_name_abbreviation(name: str, concise: bool = True) -> str:
    match len(components := name.split()):
        case 0 | 1:
            res = name
        case 2:
            res = f"{components[0]} {components[-1][0]}."
        case _ if concise:
            res = f"{components[0]} {components[1]} {components[-1][0]}."
        case _:
            res = f"{' '.join(components[:-1])} {components[-1][0]}."

    return res  # noqa: R504

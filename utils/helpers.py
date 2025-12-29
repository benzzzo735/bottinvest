def to_float(val):
    if val is None:
        return 0.0
    val = str(val).strip()
    if val == "":
        return 0.0
    return float(val.replace(",", "."))

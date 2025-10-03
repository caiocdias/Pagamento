def read_float(prompt: str, min_=None, max_=None):
    while True:
        s = input(prompt).strip().replace(',', '.')
        try:
            x = float(s)
        except ValueError:
            print("Valor inválido. Tente de novo (ex.: 12.34 ou 12,34).")
            continue

        if min_ is not None and x < min_:
            print(f"O valor deve ser ≥ {min_}.")
            continue
        if max_ is not None and x > max_:
            print(f"O valor deve ser ≤ {max_}.")
            continue
        return x
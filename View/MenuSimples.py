class MenuSimples:
    def __init__(self, title: str, options: list[str]):
        if not options:
            raise ValueError("Forneça ao menos uma opção.")
        self.title = title
        self.options = [str(o) for o in options]

    def show(self, include_exit: bool = True) -> None:
        if self.title:
            print(f"\n=== {self.title} ===")
        for i, label in enumerate(self.options, start=1):
            print(f"{i}- {label}")
        if include_exit:
            print("0) Sair")

    def choose(self, include_exit: bool = True, prompt: str = "Selecione: ") -> int | None:
        self.show(include_exit=include_exit)
        while True:
            raw = input(prompt).strip()
            if not raw.isdigit() and not (raw.startswith("-") and raw[1:].isdigit()):
                print("Digite um número válido.")
                continue
            n = int(raw)

            if include_exit and n == 0:
                return None
            if 1 <= n <= len(self.options):
                return n - 1  # índice 0-based
            print(f"Escolha um número entre 1 e {len(self.options)}" + (" ou 0 para sair." if include_exit else "."))

if __name__ == "__main__":
    usuarios = ["Ana", "Bruno", "Carlos", "Dora"]
    menu = MenuSimples("Selecionar usuário", usuarios)
    idx = menu.choose(include_exit=True)
    if idx is None:
        print("Cancelado.")
    else:
        print(f"Você escolheu: #{idx} -> {usuarios[idx]}")

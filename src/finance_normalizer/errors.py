class ImportValidationError(ValueError):
    """Erro crítico que invalida o arquivo inteiro antes de qualquer saída."""

    def __init__(self, filename: str, reason: str, action: str):
        self.filename = filename
        self.reason = reason
        self.action = action
        super().__init__(f"{filename}: {reason}. Ação necessária: {action}")

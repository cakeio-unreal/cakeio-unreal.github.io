class ErrorCode:
    def __init__(self, code_value, linked_policy=None, extra_context=None) -> None:
        self.code_value = code_value
        self.linked_policy = linked_policy
        self.extra_context = extra_context

    def has_policy(self) -> bool:
        return self.linked_policy is not None
    
class FunctionErrorMap:
    def __init__(self, func_name: str, error_codes: list[ErrorCode]) -> None:
        self.func_name = func_name
        self.error_codes = error_codes

class ClassErrorMap:
    def __init__(self, typename: str, func_map: list[FunctionErrorMap]) -> None:
        self.typename = typename
        self.func_map = func_map
from collections.abc import Sequence

from gofra.exceptions import GofraError
from gofra.parser.functions.function import Function
from gofra.parser.operators import Operator

from .types import GofraType


class TypecheckInvalidOperatorArgumentTypeError(GofraError):
    def __init__(
        self,
        *args: object,
        expected_type: GofraType,
        actual_type: GofraType,
        operator: Operator,
    ) -> None:
        super().__init__(*args)
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.operator = operator

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Expected {self.expected_type.name} but got {self.actual_type.name}
 for '{self.operator.token.text}' at {self.operator.token.location}

Did you miss the types?"""


class TypecheckInvalidFunctionArgumentTypeError(GofraError):
    def __init__(
        self,
        *args: object,
        expected_type: GofraType,
        actual_type: GofraType,
        function: Function,
    ) -> None:
        super().__init__(*args)
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.function = function

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Expected {self.expected_type.name} but got {self.actual_type.name}
 for function '{self.function.name}' at {self.function.location}

Did you miss the types?"""


class TypecheckInvalidBinaryMathArithmeticsError(GofraError):
    def __init__(
        self,
        *args: object,
        actual_lhs_type: GofraType,
        actual_rhs_type: GofraType,
        operator: Operator,
    ) -> None:
        super().__init__(*args)
        self.actual_lhs_type = actual_lhs_type
        self.actual_rhs_type = actual_rhs_type
        self.operator = operator

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Binary math operator '{self.operator.token.text}' at {self.operator.token.location} expected both {GofraType.INTEGER.name} operands, 
but got {self.actual_lhs_type.name} on the left and {self.actual_rhs_type.name} on the right.

Expected contract: [{GofraType.INTEGER.name}, {GofraType.INTEGER.name}]
Actual contract: [{self.actual_lhs_type.name}, {self.actual_rhs_type.name}]

Pointer arithmetics disallowed within binary math operators!
Please use desired pointer-arithmetics safe operators!

Did you miss the types?"""


class TypecheckInvalidPointerArithmeticsError(GofraError):
    def __init__(
        self,
        *args: object,
        actual_lhs_type: GofraType,
        actual_rhs_type: GofraType,
        operator: Operator,
    ) -> None:
        super().__init__(*args)
        self.actual_lhs_type = actual_lhs_type
        self.actual_rhs_type = actual_rhs_type
        self.operator = operator

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Invalid pointer arithmetics for operator '{self.operator.token.text}' at {self.operator.token.location}

Expected contract: [{GofraType.POINTER.name}, {GofraType.INTEGER.name}]
Actual contract: [{self.actual_lhs_type.name}, {self.actual_rhs_type.name}]

Did you miss the types?"""


class TypecheckFunctionTypeContractOutViolatedError(GofraError):
    def __init__(
        self,
        *args: object,
        function: Function,
        type_stack: list[GofraType],
    ) -> None:
        super().__init__(*args)
        self.function = function
        self.type_stack = type_stack

    def __repr__(self) -> str:
        return f"""Type safety check error!

Function `{self.function.name}` at {self.function.location} has type contract out {self.function.type_contract_out}

But actual stack at the end is: {self.type_stack}"""


class TypecheckNotEnoughOperatorArgumentsError(GofraError):
    def __init__(
        self,
        *args: object,
        types_on_stack: Sequence[GofraType],
        required_args: int,
        operator: Operator,
    ) -> None:
        super().__init__(*args)
        self.types_on_stack = types_on_stack
        self.required_args = required_args
        self.operator = operator

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Expected {self.required_args} arguments on stack but got {len(self.types_on_stack)}
 for '{self.operator.token.text}' at {self.operator.token.location}

Did you miss some arguments?"""


class TypecheckNotEnoughFunctionArgumentsError(GofraError):
    def __init__(
        self,
        *args: object,
        types_on_stack: Sequence[GofraType],
        function: Function,
        callee_function: Function,
        called_from_operator: Operator,
    ) -> None:
        super().__init__(*args)
        self.types_on_stack = types_on_stack
        self.function = function
        self.callee_function = callee_function
        self.called_from_operator = called_from_operator

    def __repr__(self) -> str:
        return f"""Type safety check failed!

Expected {len(self.function.type_contract_in)} arguments on stack but got {len(self.types_on_stack)}
For function '{self.function.name}' defined at {self.function.location}
Called from function `{self.callee_function.name}` with `{self.called_from_operator.token.text}` at `{self.called_from_operator.token.location}`

Function type contract in: {self.function.type_contract_in}
But types on stack is: {self.types_on_stack}

Did you miss some arguments?"""


class TypecheckBlockStackMismatchError(GofraError):
    def __init__(
        self,
        *args: object,
        operator_begin: Operator,
        operator_end: Operator,
        stack_before_block: Sequence[GofraType],
        stack_after_block: Sequence[GofraType],
    ) -> None:
        super().__init__(*args)
        self.operator_begin = operator_begin
        self.operator_end = operator_end
        self.stack_before_block = stack_before_block
        self.stack_after_block = stack_after_block

    def __repr__(self) -> str:
        return f"""Stack mismatch!

Expected that `{self.operator_begin.token.text}` block at {self.operator_begin.token.location} will not modify stack state!
(Block ends with `{self.operator_end.token.text}` at {self.operator_end.token.location})

Before block stack types was: {self.stack_before_block}
After block stack types become: {self.stack_after_block}

Blocks should not modify stack state.
Please ensure that stacks are same!"""

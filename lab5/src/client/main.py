import grpc
from google.protobuf.message_factory import GetMessageClass
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
from google.protobuf.descriptor_pool import DescriptorPool

SERVER_ADDRESS = "127.0.0.1:50051"


channel = grpc.insecure_channel(SERVER_ADDRESS)
reflection_db = ProtoReflectionDescriptorDatabase(channel)
desc_pool = DescriptorPool(reflection_db)

# services
service_desc = desc_pool.FindServiceByName("calculator.Calculator")

# methods
add_desc = service_desc.FindMethodByName("Add")
subtract_desc = service_desc.FindMethodByName("Subtract")
multiply_desc = service_desc.FindMethodByName("Multiply")
max_desc = service_desc.FindMethodByName("Max")
min_desc = service_desc.FindMethodByName("Min")
batch_arithmetic_op_desc = service_desc.FindMethodByName("BatchArithmeticOp")

# messages
arithmetic_op_args = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.ArithmeticOpArguments"))
arithmetic_op_result = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.ArithmeticOpResult"))
sequence_op_args = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.SequenceOpArguments"))
batch_op_args = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.BatchOpArguments"))
batch_arithmetic_op_request = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.BatchArithmeticOpRequest"))
batch_arithmetic_op_result = GetMessageClass(desc_pool.FindMessageTypeByName("calculator.BatchArithmeticOpResult"))

# enums
operation_enum = desc_pool.FindEnumTypeByName("calculator.Operation")
enums = {value.number: value.name for value in operation_enum.values}


def add(a: int, b: int) -> int:
    method_name = f"/{service_desc.full_name}/{add_desc.name}"
    call = channel.unary_unary(method_name)
    request = arithmetic_op_args(a=a, b=b)
    result = call(request=request.SerializeToString())
    return arithmetic_op_result.FromString(result).res


def subtract(a: int, b: int) -> int:
    method_name = f"/{service_desc.full_name}/{subtract_desc.name}"
    call = channel.unary_unary(method_name)
    request = arithmetic_op_args(a=a, b=b)
    result = call(request=request.SerializeToString())
    return arithmetic_op_result.FromString(result).res


def multiply(a: int, b: int) -> int:
    method_name = f"/{service_desc.full_name}/{multiply_desc.name}"
    call = channel.unary_unary(method_name)
    request = arithmetic_op_args(a=a, b=b)
    result = call(request=request.SerializeToString())
    return arithmetic_op_result.FromString(result).res


def max_(args: list) -> int:
    method_name = f"/{service_desc.full_name}/{max_desc.name}"
    call = channel.unary_unary(method_name)
    request = sequence_op_args(args=args)
    result = call(request=request.SerializeToString())
    return arithmetic_op_result.FromString(result).res


def min_(args: list) -> int:
    method_name = f"/{service_desc.full_name}/{min_desc.name}"
    call = channel.unary_unary(method_name)
    request = sequence_op_args(args=args)
    result = call(request=request.SerializeToString())
    return arithmetic_op_result.FromString(result).res


def batch_arithmetic_op(ops: list[tuple[int, int, str]]) -> list[int]:
    method_name = f"/{service_desc.full_name}/{batch_arithmetic_op_desc.name}"
    call = channel.unary_unary(method_name)
    request = batch_arithmetic_op_request(ops=[batch_op_args(arg1=arg1, arg2=arg2, op=op) for arg1, arg2, op in ops])
    result = call(request=request.SerializeToString())
    return [r.res for r in batch_arithmetic_op_result.FromString(result).results]


print("Add:", add(3, 2))
print("Subtract:", subtract(3, 2))
print("Multiply:", multiply(3, 2))
print("Max:", max_([3, 2, 1]))
print("Min:", min_([3, 2, 1]))
print("Batch:", batch_arithmetic_op([(1, 2, "ADD"), (1, 2, "SUBTRACT"), (1, 2, "MULTIPLY")]))


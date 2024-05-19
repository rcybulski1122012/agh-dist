package sr.grpc.server;

import sr.grpc.gen.CalculatorGrpc;

public class CalculatorImpl extends CalculatorGrpc.CalculatorImplBase {
    @Override
    public void add(sr.grpc.gen.ArithmeticOpArguments request,
                    io.grpc.stub.StreamObserver<sr.grpc.gen.ArithmeticOpResult> responseObserver) {
        int result = request.getA() + request.getB();
        responseObserver.onNext(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(result).build());
        responseObserver.onCompleted();
    }

    @Override
    public void subtract(sr.grpc.gen.ArithmeticOpArguments request,
                         io.grpc.stub.StreamObserver<sr.grpc.gen.ArithmeticOpResult> responseObserver) {
        int result = request.getA() - request.getB();
        responseObserver.onNext(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(result).build());
        responseObserver.onCompleted();
    }

    @Override
    public void multiply(sr.grpc.gen.ArithmeticOpArguments request,
                         io.grpc.stub.StreamObserver<sr.grpc.gen.ArithmeticOpResult> responseObserver) {
        int result = request.getA() * request.getB();
        responseObserver.onNext(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(result).build());
        responseObserver.onCompleted();
    }

    @Override
    public void max(sr.grpc.gen.SequenceOpArguments request,
                    io.grpc.stub.StreamObserver<sr.grpc.gen.ArithmeticOpResult> responseObserver) {
        int max = Integer.MIN_VALUE;
        for (int i : request.getArgsList()) {
            if (i > max) {
                max = i;
            }
        }
        responseObserver.onNext(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(max).build());
        responseObserver.onCompleted();
    }

    @Override
    public void min(sr.grpc.gen.SequenceOpArguments request,
                    io.grpc.stub.StreamObserver<sr.grpc.gen.ArithmeticOpResult> responseObserver) {
        int min = Integer.MAX_VALUE;
        for (int i : request.getArgsList()) {
            if (i < min) {
                min = i;
            }
        }
        responseObserver.onNext(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(min).build());
        responseObserver.onCompleted();
    }

    @Override
    public void batchArithmeticOp(sr.grpc.gen.BatchArithmeticOpRequest request,
                                  io.grpc.stub.StreamObserver<sr.grpc.gen.BatchArithmeticOpResult> responseObserver) {
        sr.grpc.gen.BatchArithmeticOpResult.Builder resultBuilder = sr.grpc.gen.BatchArithmeticOpResult.newBuilder();
        for (sr.grpc.gen.BatchOpArguments args : request.getOpsList()) {
            int result = 0;
            switch (args.getOp()) {
                case ADD:
                    result = args.getArg1() + args.getArg2();
                    break;
                case SUBTRACT:
                    result = args.getArg1() - args.getArg2();
                    break;
                case MULTIPLY:
                    result = args.getArg1() * args.getArg2();
                    break;
            }
            resultBuilder.addResults(sr.grpc.gen.ArithmeticOpResult.newBuilder().setRes(result).build());
        }
        responseObserver.onNext(resultBuilder.build());
        responseObserver.onCompleted();
    }
}

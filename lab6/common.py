from enum import StrEnum


class ExaminationType(StrEnum):
    KNEE = "knee"
    HIP = "hip"
    ELBOW = "elbow"


HOST = "localhost"
REQUEST_EXCHANGE_NAME = "request-exchange"
RESPONSE_EXCHANGE_NAME = "response-exchange"

QUEUE_NAMES = {
    ExaminationType.KNEE: "knee-queue",
    ExaminationType.HIP: "hip-queue",
    ExaminationType.ELBOW: "elbow-queue"
}

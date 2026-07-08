from fastapi import Depends

from vision.adapter.outbound.resource_datapters.yolo.local_face_dataset_adapter import LocalFaceDatasetAdapter
from vision.app.ports.input.face_recognition_use_case import FaceRecognitionUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.use_cases.face_recognition_interactor import FaceRecognitionInteractor


def get_face_dataset_adapter() -> FaceDatasetPort:
    return LocalFaceDatasetAdapter()


def get_face_recognition_use_case(
    dataset_port: FaceDatasetPort = Depends(get_face_dataset_adapter),
) -> FaceRecognitionUseCase:
    return FaceRecognitionInteractor(dataset_port=dataset_port)

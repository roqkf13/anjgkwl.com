from fastapi import Depends

from star_craft.adapter.outbound.resource_datapters.yolo.local_face_dataset_adapter import LocalFaceDatasetAdapter
from star_craft.app.ports.input.face_recognition_use_case import FaceRecognitionUseCase
from star_craft.app.ports.output.face_dataset_port import FaceDatasetPort
from star_craft.app.use_cases.face_recognition_interactor import FaceRecognitionInteractor


def get_face_dataset_adapter() -> FaceDatasetPort:
    return LocalFaceDatasetAdapter()


def get_face_recognition_use_case(
    dataset_port: FaceDatasetPort = Depends(get_face_dataset_adapter),
) -> FaceRecognitionUseCase:
    return FaceRecognitionInteractor(dataset_port=dataset_port)

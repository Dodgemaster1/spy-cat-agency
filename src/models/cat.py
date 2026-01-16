from src.models.base import BaseEntityModel


class CreateSpyCatModel(BaseEntityModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class SpyCatModel(CreateSpyCatModel):
    id: int


class UpdateSpyCatModel(BaseEntityModel):
    id: int
    salary: float

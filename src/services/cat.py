import httpx

from src.models.cat import CreateSpyCatModel, SpyCatModel, UpdateSpyCatModel
from src.repository.cat import SpyCatRepository


class SpyCatService:
    def __init__(self, repository: SpyCatRepository) -> None:
        self._repository = repository
        self._breeds_cache: set[str] | None = None

    def _get_breeds(self) -> set[str]:
        if self._breeds_cache is not None:
            return self._breeds_cache

        try:
            response = httpx.get("https://api.thecatapi.com/v1/breeds")
            response.raise_for_status()
            breeds_data = response.json()
            self._breeds_cache = {b["name"] for b in breeds_data}
            return self._breeds_cache
        except Exception as e:
            # Fallback or strict fail?
            # If we strictly need to validate, we should probably fail.
            # But relying on external API for every request without fallback might be brittle.
            # I will clear cache if exception occurs so we retry next time, but for now re-raise.
            raise ValueError("Failed to fetch breeds for validation") from e

    def _validate_breed(self, breed: str) -> None:
        breeds = self._get_breeds()
        if breed not in breeds:
            msg = f"Breed '{breed}' is invalid."
            raise ValueError(msg)

    def create_cat(self, cat: CreateSpyCatModel) -> SpyCatModel:
        self._validate_breed(cat.breed)
        return self._repository.create(cat)

    def read_cat(self, cat_id: int) -> SpyCatModel | None:
        return self._repository.read(cat_id)

    def read_all_cats(self) -> list[SpyCatModel]:
        return self._repository.read_all()

    def update_cat(self, cat: UpdateSpyCatModel) -> SpyCatModel | None:
        return self._repository.update(cat)

    def delete_cat(self, cat_id: int) -> None:
        if not self._repository.delete(cat_id):

            raise ValueError("Cat not found")

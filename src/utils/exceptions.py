class TaskNotFoundError(Exception):
    def __init__(self, id_: int) -> None:
        self.id_ = id_
        super().__init__(f"Task with id {id_} not found")


class TaskRepositoryError(Exception): ...


class LlmServiceError(Exception): ...

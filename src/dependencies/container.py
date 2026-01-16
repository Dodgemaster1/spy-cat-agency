from dishka import make_async_container, make_container
from dishka.integrations.fastapi import FastapiProvider

from src.dependencies.db_provider import SyncDBProvider
from src.dependencies.repository_provider import RepositoryProvider
from src.dependencies.service_provider import ServiceProvider

providers = (
    FastapiProvider(),
    ServiceProvider(),
    RepositoryProvider(),
    SyncDBProvider(),
)

async_container = make_async_container(*providers)
sync_container = make_container(*providers)

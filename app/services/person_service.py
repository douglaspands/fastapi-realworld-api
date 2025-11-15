from app.infra.context import IContext
from app.models.person_model import Person as PersonModel
from app.repositories import person_repository
from app.resources.person_resource import (
    CreatePerson,
    Person,
    UpdatePerson,
    UpdatePersonOptional,
)


async def get_all_persons(ctx: IContext) -> list[Person]:
    persons = await person_repository.get_all(ctx)
    return [Person(**person.__dict__) for person in persons]


async def get_person(ctx: IContext, *, person_id: int) -> Person:
    person = await person_repository.get(ctx, pk=person_id)
    return Person(**person.__dict__)


async def create_person(ctx: IContext, *, create_person: CreatePerson) -> Person:
    new_person = PersonModel(
        first_name=create_person.first_name, last_name=create_person.last_name
    )
    person = await person_repository.create(ctx, person=new_person)
    return Person(**person.__dict__)


async def update_person(
    ctx: IContext, *, person_id: int, update_person: UpdatePerson
) -> Person:
    values = update_person.model_dump()
    person = await person_repository.update(ctx, pk=person_id, **values)
    return Person(**person.__dict__)


async def update_person_optional(
    ctx: IContext, *, person_id: int, update_person: UpdatePersonOptional
) -> Person:
    values = update_person.model_dump(exclude_none=True)
    person = await person_repository.update(ctx, pk=person_id, **values)
    return Person(**person.__dict__)


async def delete_person(ctx: IContext, *, person_id: int):
    await person_repository.delete(ctx, pk=person_id)


__all__ = (
    "get_person",
    "get_all_persons",
    "create_person",
    "update_person",
    "update_person_optional",
    "delete_person",
)

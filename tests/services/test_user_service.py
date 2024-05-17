# from copy import copy
# from unittest.mock import AsyncMock, patch

# import pytest
# from faker import Faker
# from sqlalchemy.exc import IntegrityError, NoResultFound

# from server.core.database import SessionIO
# from server.models.user_model import People
# from server.services import user_service
# from tests.mocks.context_mock import ContextMock

# fake = Faker("pt_BR")
# Faker.seed(0)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_get_user_ok(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 1

#     # MOCK
#     user_mock = People(
#         id=user_id, first_name=fake.first_name(), last_name=fake.last_name()
#     )
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.get.return_value = user_mock

#     # WHEN
#     res = await user_service.get_user(context_mock, pk=user_id)

#     # THEN
#     assert res.id == user_id
#     assert res.first_name and isinstance(res.first_name, str)
#     assert res.last_name and isinstance(res.last_name, str)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_get_user_not_found(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 9999

#     # MOCK
#     error_message = "No row was found when one was required"
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.get.side_effect = NoResultFound(error_message)

#     # WHEN
#     with pytest.raises(NoResultFound) as exc_info:
#         await user_service.get_user(context_mock, pk=user_id)

#     # THEN
#     assert error_message in str(exc_info.value)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_all_user_ok(user_repository_mock: AsyncMock):
#     # MOCK
#     user_mock = [
#         People(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
#         for idx in range(10)
#     ]
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.get_all.return_value = user_mock

#     # WHEN
#     res = await user_service.all_user(context_mock)

#     # THEN
#     assert len(res) == len(user_mock)
#     for idx in range(len(user_mock)):
#         assert res[idx].id == user_mock[idx].id
#         assert res[idx].first_name == user_mock[idx].first_name
#         assert res[idx].last_name == user_mock[idx].last_name


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_create_user_ok(user_repository_mock: AsyncMock):
#     # GIVEN
#     create_user = CreatePeople(first_name=fake.first_name(), last_name=fake.last_name())

#     # MOCK
#     context_mock = ContextMock.context_session_mock()

#     async def create_mock(session: SessionIO, user: People):
#         user.id = 1

#     user_repository_mock.create = create_mock

#     # WHEN
#     user = await user_service.create_user(context_mock, create_user=create_user)

#     # THEN
#     assert user.id and user.id == 1
#     assert user.first_name == create_user.first_name
#     assert user.last_name == create_user.last_name


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_create_user_error(user_repository_mock: AsyncMock):
#     # GIVEN
#     create_user = CreatePeople(first_name=fake.first_name(), last_name=fake.last_name())

#     # MOCK
#     error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.create.side_effect = IntegrityError(
#         orig=Exception(error_message), params={}, statement=""
#     )

#     # WHEN
#     with pytest.raises(IntegrityError) as exc_info:
#         await user_service.create_user(context_mock, create_user=create_user)

#     # THEN
#     assert error_message in str(exc_info.value)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_update_user_ok(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 1
#     update_user = UpdatePeople(first_name=fake.first_name(), last_name=fake.last_name())

#     # MOCK
#     context_mock = ContextMock.context_session_mock()

#     async def update_mock(session: SessionIO, pk: int, **values):
#         return People(id=pk, **values)

#     user_repository_mock.update = update_mock

#     # WHEN
#     user = await user_service.update_user(
#         context_mock, pk=user_id, update_user=update_user
#     )

#     # THEN
#     assert user.id == user_id
#     assert user.first_name == update_user.first_name
#     assert user.last_name == update_user.last_name


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_update_user_error(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 1
#     update_user = UpdatePeople(first_name=fake.first_name(), last_name=fake.last_name())

#     # MOCK
#     error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.update.side_effect = IntegrityError(
#         orig=Exception(error_message), params={}, statement=""
#     )

#     # WHEN
#     with pytest.raises(IntegrityError) as exc_info:
#         await user_service.update_user(
#             context_mock, pk=user_id, update_user=update_user
#         )

#     # THEN
#     assert error_message in str(exc_info.value)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_update_user_optional_ok(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 1
#     update_user = UpdatePeopleOptional(first_name=fake.first_name())  # type: ignore

#     # MOCK
#     context_mock = ContextMock.context_session_mock()
#     user_mock = People(
#         id=user_id,
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#     )

#     async def update_mock(session: SessionIO, pk: int, **values):
#         user = copy(user_mock)
#         for k, v in values.items():
#             setattr(user, k, v)
#         return user

#     user_repository_mock.update = update_mock

#     # WHEN
#     user = await user_service.update_user_optional(
#         context_mock, pk=user_id, update_user=update_user
#     )

#     # THEN
#     assert user.id == user_id
#     assert user.first_name != user_mock.first_name
#     assert user.first_name == update_user.first_name
#     assert user.last_name == user_mock.last_name


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_update_user_optional_error(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 999999
#     update_user = UpdatePeopleOptional(first_name=fake.first_name())  # type: ignore

#     # MOCK
#     error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.update.side_effect = IntegrityError(
#         orig=Exception(error_message), params={}, statement=""
#     )

#     # WHEN
#     with pytest.raises(IntegrityError) as exc_info:
#         await user_service.update_user_optional(
#             context_mock, pk=user_id, update_user=update_user
#         )

#     # THEN
#     assert error_message in str(exc_info.value)


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_delete_user_ok(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 1

#     # MOCK
#     context_mock = ContextMock.context_session_mock()

#     # WHEN
#     await user_service.delete_user(context_mock, pk=user_id)

#     # THEN
#     assert True


# @pytest.mark.asyncio
# @patch("server.services.user_service.user_repository", new_callable=AsyncMock)
# async def test_delete_user_error(user_repository_mock: AsyncMock):
#     # GIVEN
#     user_id = 999999

#     # MOCK
#     error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
#     context_mock = ContextMock.context_session_mock()
#     user_repository_mock.delete.side_effect = IntegrityError(
#         orig=Exception(error_message), params={}, statement=""
#     )

#     # WHEN
#     with pytest.raises(IntegrityError) as exc_info:
#         await user_service.delete_user(context_mock, pk=user_id)

#     # THEN
#     assert error_message in str(exc_info.value)

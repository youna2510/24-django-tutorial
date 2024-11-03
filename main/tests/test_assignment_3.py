# Create your tests here.
import random
import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def random_user_generator():
    from main.models import User

    return lambda idx: User(
        username=f"{uuid.uuid4()}",
        student_number=f"2021{str(random.randint(0, 9999)).zfill(4)}",
    )


@pytest.fixture
def random_study_generator():
    from main.models import Study

    return lambda idx, user: Study(
        name=f"스터디{idx}", description=f"스터디{idx} 설명", created_by=user
    )


@pytest.fixture
def users(random_user_generator):
    from main.models import User

    return User.objects.bulk_create(
        [random_user_generator(idx + 1) for idx in range(10)]
    )


@pytest.fixture
def studies(users, random_study_generator):
    from main.models import Study
    from main.models import StudyParticipation

    studies = Study.objects.bulk_create(
        [random_study_generator(idx + 1, random.choice(users)) for idx in range(10)]
    )

    for study in studies:
        participants = users[:]
        random.shuffle(participants)

        StudyParticipation.objects.bulk_create(
            StudyParticipation(study=study, user=participant)
            for participant in participants[: random.randint(2, len(users))]
        )

    return studies


@pytest.mark.django_db
def test_스터디_조회(client, random_user_generator, studies):
    from main.models import User

    new_user = User.objects.bulk_create([random_user_generator(9_000)])[0]
    study = random.choice(studies)

    client.force_login(user=new_user)
    res = client.get(
        f"/study/{study.id}/",
    )

    result = res.data

    for participation in study.studyparticipation_set.all():
        assert {
            "id": participation.id,
            "study": participation.study.id,
            "user": participation.user.id,
        } in result["studyparticipation_set"]


@pytest.mark.django_db
def test_스터디_참여_목록_조회(client, studies):
    from main.models import StudyParticipation

    random_user = random.choice(
        random.choice(studies).studyparticipation_set.all()
    ).user
    client.force_login(user=random_user)

    res = client.get(
        "/study-participation/",
    )

    result = res.data

    participation_list = StudyParticipation.objects.filter(user=random_user).all()

    assert len(participation_list) == len(result)

    for participation in participation_list:
        assert {
            "id": participation.id,
            "study": participation.study.id,
            "user": participation.user.id,
        } in result


@pytest.mark.django_db
def test_스터디_참여(client, random_user_generator, studies):
    from main.models import User, StudyParticipation

    new_user = User.objects.bulk_create([random_user_generator(9_000)])[0]
    study = random.choice(studies)

    client.force_login(user=new_user)
    res = client.post(
        "/study-participation/",
        data={
            "user": new_user.id,
            "study": study.id,
        },
    )

    result = res.data

    created_study_participation = StudyParticipation.objects.get(id=result["id"])

    assert result["study"] == created_study_participation.study.id
    assert result["user"] == created_study_participation.user.id


@pytest.mark.django_db
def test_다른_사람_스터디_참여(client, random_user_generator, studies):
    from main.models import User

    new_user, another_user = User.objects.bulk_create(
        [random_user_generator(9_000), random_user_generator(9_001)]
    )
    study = random.choice(studies)

    client.force_login(user=new_user)
    res = client.post(
        "/study-participation/",
        data={
            "user": another_user.id,
            "study": study.id,
        },
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_스터디_참여_삭제(client, studies):
    from main.models import StudyParticipation

    study = random.choice(studies)
    study_participation = random.choice(study.studyparticipation_set.all())
    user = study_participation.user

    client.force_login(user=user)
    client.delete(
        f"/study-participation/{study_participation.id}/",
    )

    with pytest.raises(StudyParticipation.DoesNotExist):
        StudyParticipation.objects.get(study=study.id, user=user.id)


@pytest.mark.django_db
def test_다른_사람_스터디_참여_삭제(client, random_user_generator, studies):
    study = random.choice(studies)

    study_participation = random.choice(study.studyparticipation_set.all())
    another_study_participation = random.choice(
        [
            s
            for s in study.studyparticipation_set.all()
            if s.id != study_participation.id
        ]
    )

    user = study_participation.user

    client.force_login(user=user)
    res = client.delete(
        f"/study-participation/{another_study_participation.id}/",
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND

# Create your tests here.
import json
import random

import pytest
from rest_framework.test import APIClient


MAJORS = [
    "컴퓨터공학",
    "전자공학",
    "기계공학",
    "산업공학",
    "화학공학",
    "건축학",
    "신소재공학",
    "항공우주공학",
    "생명공학",
    "환경공학",
]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def random_student_generator():
    from main.models import Student

    return lambda idx: Student(
        name=f"학생{idx}",
        student_number=f"2021{str(random.randint(0, 9999)).zfill(4)}",
        primary_major=random.choice(MAJORS),
    )


@pytest.fixture
def students(random_student_generator):
    from main.models import Student

    return Student.objects.bulk_create(
        [random_student_generator(idx + 1) for idx in range(10)]
    )


@pytest.mark.django_db
def test_학생_목록_조회(client, students):
    res = client.get(
        "/student",
    )

    result = res.data

    for student in students:
        assert {
            "id": student.id,
            "name": student.name,
            "student_number": student.student_number,
            "primary_major": student.primary_major,
        } in result


@pytest.mark.django_db
def test_학생_생성(client, random_student_generator):
    from main.models import Student

    student = random_student_generator(1)

    res = client.post(
        "/student",
        data={
            "name": student.name,
            "student_number": student.student_number,
            "primary_major": student.primary_major,
        },
    )

    result = res.data

    created_student = Student.objects.get(id=result["id"])

    assert student.name == created_student.name
    assert student.student_number == created_student.student_number
    assert student.primary_major == created_student.primary_major


@pytest.mark.django_db
def test_학생_조회(client, students):
    student = random.choice(students)

    res = client.get(
        f"/student/{student.id}",
    )

    result = res.data

    assert result["id"] == student.id
    assert result["name"] == student.name
    assert result["student_number"] == student.student_number
    assert result["primary_major"] == student.primary_major


@pytest.mark.django_db
def test_학생_수정(client, students):
    student = random.choice(students)
    new_name = "수정된 이름"

    client.patch(
        f"/student/{student.id}",
        headers={
            "Content-Type": "application/json",
        },
        data=json.dumps({"name": new_name}),
    )

    student.refresh_from_db()
    assert new_name == student.name


@pytest.mark.django_db
def test_학생_삭제(client, students):
    from main.models import Student

    student = random.choice(students)

    client.delete(
        f"/student/{student.id}",
    )

    with pytest.raises(Student.DoesNotExist):
        Student.objects.get(id=student.id)

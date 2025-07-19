import pytest
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from students.models import Course, Student
from model_bakery import baker
from django.conf import settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# проверка получения первого курса (retrieve-логика):
@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == course.id
    assert data['name'] == course.name


# проверка получения списка курсов (list-логика):
@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


# проверка фильтрации списка курсов по id:
@pytest.mark.django_db
def test_filter_id_course(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'id': courses[1].id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == courses[1].id


# проверка фильтрации списка курсов по name:
@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'name': courses[2].name})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == courses[2].name


# тест успешного создания курса:
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url,
                           data={'name': 'python'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


# тест успешного обновления курса:
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    response = client.patch(url, data={'name': 'python'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'python'


# тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    client.delete(url)
    response = client.get(url)
    data = response.json()
    assert response.status_code == 404
    assert course.id not in data


@pytest.mark.django_db
def test_max_students(client, course_factory, student_factory):
    max_students = settings.MAX_STUDENTS_PER_COURSE
    course = course_factory()
    students = student_factory(_quantity=20)
    for student in students:
        course.students.add(student)

    # Проверка добавления 21-го студента
    new_student = baker.make(Student)

    if max_students == 20:
        # Пытаемся добавить 21-го студента и ожидаем ошибку валидации
        course.students.add(new_student)
        with pytest.raises(ValidationError):
            course.full_clean()  # Вызов полной проверки на уровне модели
    else:
        # Если лимит студентов не 20, то добавление должно быть успешным
        course.students.add(new_student)
        course.full_clean()  # Пройти валидацию без ошибок
        assert course.students.count() == 20

import copy
import data
import sender_stand_request

MENSAJE_ERROR = ("Has introducido un nombre de usuario no válido. "
                 "El nombre solo puede contener letras del alfabeto latino, "
                 "la longitud debe ser de 2 a 15 caracteres.")

MENSAJE_FALTAN_PARAMETROS = "No se han aprobado todos los parámetros requeridos"


def get_user_body(first_name):
    body = copy.deepcopy(data.user_body)  # copia, para no alterar el original
    body["firstName"] = first_name
    return body


def positive_assert(first_name):
    body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(body)

    # Resultado esperado 1: 201 Created
    assert response.status_code == 201
    # Resultado esperado 2: authToken con un valor
    assert response.json()["authToken"] != ""
    # Resultado esperado 3: el usuario aparece en la tabla Users
    users_table = sender_stand_request.get_users_table()
    assert response.json()["authToken"] in users_table.text


def negative_assert(first_name):
    body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == MENSAJE_ERROR


def negative_assert_no_firstname(body):
    response = sender_stand_request.post_new_user(body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == MENSAJE_FALTAN_PARAMETROS


def negative_assert_code_400(body):
    response = sender_stand_request.post_new_user(body)

    assert response.status_code == 400


# Casos 1 y 2 de la lista de comprobación
def test_firstname_2_characters_success():
    positive_assert("Aa")


def test_firstname_15_characters_success():
    positive_assert("Aaaaaaaaaaaaaaa")


# Casos 3 a 7 de la lista de comprobación
def test_firstname_1_character_error():
    negative_assert("A")


def test_firstname_16_characters_error():
    negative_assert("Aaaaaaaaaaaaaaaa")


def test_firstname_with_space_error():
    negative_assert("A Aaa")


def test_firstname_special_characters_error():
    negative_assert("№%@")


def test_firstname_numbers_error():
    negative_assert("123")


# Caso 8: el parámetro firstName no se pasa en la solicitud
def test_create_user_no_first_name_error():
    body = get_user_body("Aa")
    del body["firstName"]
    negative_assert_no_firstname(body)


# Caso 9: se pasa un valor vacío en firstName
def test_create_user_empty_first_name_error():
    body = get_user_body("")
    negative_assert_no_firstname(body)


# Caso 10: se pasa un número en lugar de texto en firstName
def test_create_user_number_type_first_name_error():
    body = get_user_body(12)
    negative_assert_code_400(body)


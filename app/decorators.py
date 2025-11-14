from functools import wraps


def input_error(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Невалідні дані: перевірте введені дані"
        except IndexError:
            return "Недостатньо аргументів для виконання команди"
        except KeyError:
            return "Контакт/нотатка  з таким іменем не знайдена"
        except AttributeError:
            return "Помилка доступу до атрибута"
        except Exception:
            return "Сталася несподівана помилка. Спробуйте пізніше"

    return wrapper
import random
from django.conf import settings
from django.core.mail import send_mail


LEN_CODE = 5


def get_random_code():
    """Получить временный код из 4-ех цифр."""
    # return "".join(random.sample("0123456789", LEN_CODE))
    return "".join([random.randint(0, 9) for _ in range(LEN_CODE)])


def send_code_by_email(email, message):
    """Отправить код на электронную почту."""
    # message = f"Код: {code}"
    send_mail(
        subject="Временный код доступа",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return message

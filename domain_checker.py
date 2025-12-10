import dns.resolver
import dns.exception
import os


def check_domains(emails: list[str]):
    """
    Проверяет наличие MX-записей для списка email-адресов.
    """
    print(f"{'Email':<35} | {'Статус'}")
    print("-" * 75)

    for email in emails:
        status = ""
        try:
            if '@' not in email:
                raise ValueError("Некорректный формат")

            domain = email.split('@')[1]

            # Запрашиваем MX записи
            answers = dns.resolver.resolve(domain, 'MX')

            if answers:
                status = "✅ Домен валиден (MX found)"
            else:
                status = "⚠️ MX-записи отсутствуют или пусты"

        except (dns.resolver.NXDOMAIN):
            status = "❌ Домен отсутствует (NXDOMAIN)"
        except (dns.resolver.NoAnswer):
            status = "⚠️ MX-записи отсутствуют (NoAnswer)"
        except (dns.resolver.NoNameservers, dns.exception.Timeout):
            status = "⚠️ Ошибка DNS (Timeout/NoNameservers)"
        except ValueError:
            status = "🚫 Некорректный формат email"
        except Exception as e:
            status = f"❗ Ошибка: {str(e)}"

        print(f"{email:<35} | {status}")


if __name__ == "__main__":
    # 1. Сначала пытаемся найти файл emails.txt
    input_filename = "emails.txt"
    email_list = []

    if os.path.exists(input_filename):
        print(f"📂 Найден файл '{input_filename}'. Читаем адреса...")
        try:
            with open(input_filename, "r", encoding="utf-8") as f:
                # Читаем строки, убираем пробелы и пустые строки
                email_list = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")

    # 2. Если файла нет или он пуст, используем демо-список (Fallback)
    if not email_list:
        print(f"ℹ️ Файл '{input_filename}' не найден или пуст. Используем тестовый список.")
        email_list = [
            "test@gmail.com",  # Живой домен
            "admin@nonexistent-xyz.ru",  # Несуществующий
            "contact@yandex.ru",  # Живой домен
            "broken@example.com",  # Тестовый (зависит от настроек сети)
            "invalid-email-format"  # Ошибка формата
        ]

    print(f"Всего адресов для проверки: {len(email_list)}\n")
    check_domains(email_list)
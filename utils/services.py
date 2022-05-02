import os
from pandas import read_csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.db.utils import IntegrityError
from api.models import Category, Diagnosis


_category_columns = ["category_code", "category_title"]
_diagnosis_columns = [
    "category_code",
    "diagnosis_code",
    "full_code",
    "abbreviated_description",
    "full_description",
    "category_title",
]

_success_subject = "Data Injection Succes"
_failed_subject = "Data Injection Failed"


def _custom_message(name, status="success"):
    if status == "success":
        msg = f"Hello {name}, your data has been injected successfully"
        return msg
    else:
        msg = f"Hello {name}, your data injection was not successfully"
        return msg


class ProcessCSV:
    """
    class for injecting diagnosis data into database
    :params: file_object
    :params: csv_type
    """

    def __init__(self, file_object, csv_type="category"):
        self.file_object = file_object
        self.csv_type = csv_type

        if csv_type == "category":
            self._columns = _category_columns
        else:
            self._columns = _diagnosis_columns

    def inject_category(self):
        df = read_csv(self.file_object, names=self._columns)
        df.dropna(subset="category_code", inplace=True)
        data = df.drop_duplicates(
            subset=["category_code"],
            keep="first",
        )

        injection_set = [
            Category(
                category_code=row.category_code,
                category_title=row.category_title,
            )
            for row in data.itertuples()
        ]

        try:
            Category.objects.bulk_create(injection_set)
        except IntegrityError as e:
            pass

    def inject_diagnosis(self):
        df = read_csv(self.file_object, names=self._columns)
        df.dropna(subset="full_code", inplace=True)
        data = df.drop_duplicates(subset=["full_code"], keep="first")

        injection_set = list()

        for _index, row in data.iterrows():
            try:
                category_id = Category.objects.get(
                    category_code=row["category_code"],
                )
            except Category.DoesNotExist:
                continue

            injection_set.append(
                Diagnosis(
                    diagnosis_code=row["diagnosis_code"],
                    abbreviated_desc=row["abbreviated_description"],
                    category=category_id,
                    full_desc=row["full_description"],
                )
            )

        Diagnosis.objects.bulk_create(injection_set)


class Messaging:
    @staticmethod
    def send_mail(email, status="success"):

        name = email.split("@")[0]

        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

        if status == "success":
            success_message = Mail(
                from_email=os.environ.get("EMAIL_HOST_USER"),
                to_emails=email,
                subject=_success_subject,
                plain_text_content=_custom_message(name=name, status=status),
            )

            response = sg.send(success_message)
            print({"status_code": response.status_code, "body": response.body})

        else:
            failure_message = Mail(
                from_email=os.environ.get("EMAIL_HOST_USER"),
                to_emails=email,
                subject=_failed_subject,
                plain_text_content=_custom_message(name=name, status=status),
            )

            response = sg.send(failure_message)
            print({"status_code": response.status_code, "body": response.body})


class Operations(ProcessCSV, Messaging):
    def __init__(
        self,
        file_object,
        email,
        status="success",
        csv_type="category",
    ):
        self.email = email
        self.status = status
        super().__init__(file_object, csv_type)

    def service(self):
        try:
            if self.csv_type == "category":
                self.inject_category()
            else:
                self.inject_diagnosis()

            self.send_mail(email=self.email, status=self.status)
        except Exception as e:
            print(e)
            self.send_mail(email=self.email, status="failed")

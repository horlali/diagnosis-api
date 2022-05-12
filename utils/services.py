import os
from pandas import read_csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from api.models import Category, Diagnosis


CATEGORY_COLUMNS = ["category_code", "category_title"]
DIAGNOSIS_COLUMNS = [
    "category_code",
    "diagnosis_code",
    "full_code",
    "abbreviated_description",
    "full_description",
    "category_title",
]

_SUCCESS_SUBJECT = "Data Injection Success"
_FAILED_SUBJECT = "Data Injection Failed"


def _custom_message(name, status="success"):
    """
    Returns a custom string base on operations status

    Parameters
    ----------
        `name`: Name of user the message is meant for.
        `status`: Status of operation, defaults to success if not provided

    """
    if status == "success":
        msg = (
            f"Hello {name}, \n"
            f"Your data has been injected successfully \n"
            f"Best, Regards"
        )
        return msg
    else:
        msg = (
            f"Hello {name}, \n"
            f"Your data injection was not successfully \n"
            f"Best, Regards"
        )
        return msg


class ProcessCSV:
    """
    Class for injecting data into database table

    Parameters
    ----------
        `file_object`: uploaded csv file loaded as an object
        `csv_type`: record type of the csv, category or diagnosis, \
            defaults to category if not provided

    Methods
    -------
        `inject_category`: inject data into category table
        `inject_diagnosis`: inject data into diagnosis table
    """

    def __init__(self, file_object, csv_type="category"):
        self.file_object = file_object
        self.csv_type = csv_type

        if csv_type == "category":
            self._columns = CATEGORY_COLUMNS
        else:
            self._columns = DIAGNOSIS_COLUMNS

    def inject_category(self):
        df = read_csv(self.file_object, names=self._columns)
        df.dropna(subset="category_code", inplace=True)
        data = df.drop_duplicates(
            subset=["category_code"],
            keep="first",
        )

        print("Started collecting category data for injection")
        injection_set = [
            Category(
                category_code=row.category_code,
                category_title=row.category_title,
            )
            for row in data.itertuples()
        ]

        print("Injection data into category table ")
        Category.objects.bulk_create(injection_set, ignore_conflicts=True)

        return str("Category Data Injection Done")

    def inject_diagnosis(self):
        df = read_csv(self.file_object, names=self._columns)
        df.dropna(subset="full_code", inplace=True)
        data = df.drop_duplicates(subset=["full_code"], keep="first")

        print("Started collecting diagnosis data for injection")
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

        print("Injection data into diagnosis table ")
        Diagnosis.objects.bulk_create(injection_set, ignore_conflicts=True)

        return str("Diagnosis Data Injection Done")


class Messaging:
    """
    Class for sending out messages about processing status

    Methods
    -------
        send_mail: sends email using sendgrids API
    """

    @staticmethod
    def send_mail(email, status="success"):
        """
        Sends report email to user after operations is done

        Parameters
        ----------
            email: email to which message will be sent to
            status: specifies which email to send, \
                defaults to success if not provided
        """
        name = email.split("@")[0]

        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

        if status == "success":
            print("Started sending success message")
            success_message = Mail(
                from_email=os.environ.get("EMAIL_HOST_USER"),
                to_emails=email,
                subject=_SUCCESS_SUBJECT,
                plain_text_content=_custom_message(name=name, status=status),
            )

            response = sg.send(success_message)
            print({"status_code": response.status_code, "body": response.body})

        else:
            print("Started sending failure message")
            failure_message = Mail(
                from_email=os.environ.get("EMAIL_HOST_USER"),
                to_emails=email,
                subject=_FAILED_SUBJECT,
                plain_text_content=_custom_message(name=name, status=status),
            )

            response = sg.send(failure_message)
            print({"status_code": response.status_code, "body": response.body})

        return str("Messaging Done!")


class Operations(ProcessCSV, Messaging):
    """
    class for processing uploaded csv files.

    Parameters
    ----------
    All parameters of inherited classes `ProcessCSV` and `Messaging` applies
    """

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
            print("Starting Data Injection")
            if self.csv_type == "category":
                self.inject_category()
            else:
                self.inject_diagnosis()

            print("Finished Data Injection, Start Sending Success mail")
            self.send_mail(email=self.email, status=self.status)
        except Exception as e:
            print(e)
            print(
                "Something went wrong while sending Success Email, \
                    resort to failure message"
            )
            self.send_mail(email=self.email, status="failed")

        return str("Service Done!")

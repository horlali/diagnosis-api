from django.db import models


class Category(models.Model):
    category_code = models.CharField("Category Code", max_length=8, unique=True)
    category_title = models.CharField("Category Title", max_length=128)
    created_at = models.DateField("Created On", auto_now_add=True)
    updated_at = models.DateField("Updated On", auto_now=True)

    class Meta:
        ordering = ["category_code"]

    def __str__(self):
        return self.category_title


class Diagnosis(models.Model):
    ICD_TYPES = [
        ("ICD_9", "ICD_9"),
        ("ICD_10", "ICD_10"),
        ("ICD_11", "ICD_11"),
    ]

    icd_type = models.CharField(
        max_length=12, choices=ICD_TYPES, default=ICD_TYPES[1][0]
    )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    diagnosis_code = models.CharField("Diagnosis Code", max_length=8, blank=True)
    abbreviated_desc = models.CharField("Abreviated Description", max_length=256)
    full_desc = models.TextField("Full Description", max_length=512)
    created_at = models.DateField("Created At", auto_now_add=True)
    updated_at = models.DateField("Updated At", auto_now=True)

    @property
    def full_code(self):
        return f"{self.category.category_code}{self.diagnosis_code if self.diagnosis_code else ''}"

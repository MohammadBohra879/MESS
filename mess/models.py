from django.db import models


# -------------------------
# User Model
# -------------------------
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact_no = models.BigIntegerField()
    password = models.CharField(max_length=50)
    create_date = models.DateField()
    update_date = models.DateField(null=True, blank=True)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return self.name


# -------------------------
# Equipment Model
# -------------------------
class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=50)
    available_status = models.CharField(max_length=50)
    equipment_img = models.ImageField(upload_to='equipment/')
    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='equipment'
    )
    create_date = models.DateField()
    update_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.equipment_name


# -------------------------
# Request Model
# -------------------------
class Request(models.Model):
    req_id = models.AutoField(primary_key=True)
    req_date = models.DateField()
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    update_date = models.DateField(null=True, blank=True)

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests_made'
    )

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests_received'
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Request {self.req_id} - {self.status}"


# -------------------------
# Rating Model
# -------------------------
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    score = models.FloatField()
    feedback = models.CharField(max_length=1000)
    rating_date = models.DateField()

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Rating {self.score}"

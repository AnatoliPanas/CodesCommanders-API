from django.db import models
from django.utils import timezone


from applications.orders.choices.order_status import OrderStatus
from applications.orders.managers.order import SoftDeleteManager
from applications.users.models.user import User


class Order(models.Model):
    title = models.CharField(max_length=90, db_index=True)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=36, choices=OrderStatus.choices(), default=OrderStatus.CREATED.name)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def delete(self, *arg, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])


    class Meta:
        db_table = "order"
        constraints = [
            models.UniqueConstraint(fields=[
                'title',
                'status',
                'is_deleted'
            ],
                name='unique_orders_title_desc_status_not_deleted')
        ]

    def __str__(self):
        return self.title

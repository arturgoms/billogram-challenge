from commons.models.audit import AuditModel
from commons.models.uuid import UUIDModel


class Model(AuditModel, UUIDModel):
    """
    Base model with audit fields and UUID primary key support.
    """

    class Meta:
        abstract = True

from tortoise import fields, Model


class EndpointState(Model):
    """
    Модель статуса
    """
    id = fields.IntField(primary_key=True)
    endpoint_id = fields.ForeignKeyField('models.Client')
    client_id = fields.ForeignKeyField('models.Endpoint')
    state_name = fields.CharField(max_length=50)
    state_reason = fields.CharField(max_length=50)
    state_start = fields.BigIntField()
    state_end = fields.BigIntField(null=True)
    state_id = fields.CharField(max_length=250)
    group_id = fields.CharField(max_length=250)
    reason_group = fields.CharField(max_length=50, null=True)
    info = fields.JSONField(null=True)

    class Meta:
        table = 'endpoint_states'


class Client(Model):
    """
    Модель клиента
    """
    id = fields.IntField(primary_key=True)
    client_name = fields.CharField(max_length=250)

    class Meta:
        table = 'clients'

    def __str__(self) -> str:
        return self.client_name


class Endpoint(Model):
    """
    Модель энд поинта
    """
    id = fields.IntField(primary_key=True)
    endpoint_name = fields.CharField(max_length=250)

    class Meta:
        table = 'endpoints'

    def __str__(self) -> str:
        return self.endpoint_name

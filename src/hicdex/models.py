from enum import Enum, IntEnum

from tortoise import Model, fields

# on mint token, holder
# on_swap new, cancel_swap, collect


class SwapStatus(IntEnum):
    ACTIVE = 0
    FINISHED = 1
    CANCELED = 2


class Holder(Model):
    address = fields.CharField(36, pk=True)


class Token(Model):
    id = fields.BigIntField(pk=True)
    creator = fields.ForeignKeyField('models.Holder', 'tokens')
    # tags = fields.ManyToManyField('models.Tag', related_name='tokens', through='token_tag')
    title = fields.TextField()
    description = fields.TextField()
    artifact_uri = fields.TextField()
    thumbnail_uri = fields.TextField()
    mime = fields.TextField()
    royalties = fields.BigIntField()
    supply = fields.BigIntField()
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


class Tag(Model):
    id = fields.BigIntField(pk=True)
    tag = fields.CharField(255)


class TokenTag(Model):
    token = fields.ForeignKeyField("models.Token", "tokens_tag", null=False)
    tag = fields.ForeignKeyField("models.Tag", "tags_token", null=False)

    class Meta:
        table = 'token_tag'


# class TokenHolder(Model):
#     holder = fields.ForeignKeyField("models.Holder", "holders_token", null=False)
#     token = fields.ForeignKeyField("models.Token", "token_holders", null=False)
#     quantity = fields.BigIntField(default=0)

#     class Meta:
#         table = 'token_holder'


class Swap(Model):
    id = fields.BigIntField(pk=True)
    creator = fields.ForeignKeyField('models.Holder', 'swaps')
    token = fields.ForeignKeyField('models.Token', 'swaps')
    price = fields.BigIntField()
    amount = fields.BigIntField()
    amount_left = fields.BigIntField()
    level = fields.BigIntField()
    status = fields.IntEnumField(SwapStatus)
    timestamp = fields.DatetimeField()


class Trade(Model):
    id = fields.BigIntField(pk=True)
    token = fields.ForeignKeyField('models.Token', 'trades')
    swap = fields.ForeignKeyField('models.Swap', 'trades')
    seller = fields.ForeignKeyField('models.Holder', 'sales')
    buyer = fields.ForeignKeyField('models.Holder', 'purchases')
    amount = fields.BigIntField()
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()

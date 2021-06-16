from enum import Enum, IntEnum

from tortoise import Model, fields


class SwapStatus(IntEnum):
    ACTIVE = 0
    FINISHED = 1
    CANCELED = 2


class ShareholderStatus(str, Enum):
    unspecified = "unspecified"
    core_participant = "core_participant"
    benefactor = "benefactor"


class Holder(Model):
    address = fields.CharField(36, pk=True)
    name = fields.TextField(default='')
    metadata_file = fields.TextField(default='')
    metadata = fields.JSONField(default={})
    hdao_balance = fields.BigIntField(default=0)
    is_split = fields.BooleanField(default=False)


class SplitContract(Model):
    contract = fields.ForeignKeyField('models.Holder', 'shares', index=True)
    administrator = fields.CharField(36)
    total_shares = fields.BigIntField()


class Shareholder(Model):
    split_contract = fields.ForeignKeyField('models.SplitContract', 'shareholder', index=True)
    holder = fields.ForeignKeyField('models.Holder', 'shareholder', index=True)
    shares = fields.BigIntField()
    holder_type = fields.CharEnumField(ShareholderStatus, default=ShareholderStatus.unspecified)


class Token(Model):
    id = fields.BigIntField(pk=True)
    creator = fields.ForeignKeyField('models.Holder', 'tokens', index=True)
    title = fields.TextField()
    description = fields.TextField()
    artifact_uri = fields.TextField()
    display_uri = fields.TextField()
    thumbnail_uri = fields.TextField()
    metadata = fields.TextField()
    extra = fields.JSONField(default={})
    mime = fields.TextField()
    royalties = fields.BigIntField()
    supply = fields.BigIntField()
    hdao_balance = fields.BigIntField(default=0)

    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


class Tag(Model):
    id = fields.BigIntField(pk=True)
    tag = fields.CharField(255)


class TokenTag(Model):
    token = fields.ForeignKeyField("models.Token", "token_tags", null=False, index=True)
    tag = fields.ForeignKeyField("models.Tag", "tag_tokens", null=False, index=True)

    class Meta:
        table = 'token_tag'


class TokenHolder(Model):
    holder = fields.ForeignKeyField("models.Holder", "holders_token", null=False, index=True)
    token = fields.ForeignKeyField("models.Token", "token_holders", null=False, index=True)
    quantity = fields.BigIntField(default=0)

    class Meta:
        table = 'token_holder'


class Swap(Model):
    id = fields.BigIntField(pk=True)
    creator = fields.ForeignKeyField('models.Holder', 'swaps', index=True)
    token = fields.ForeignKeyField('models.Token', 'swaps', index=True)
    price = fields.BigIntField()
    amount = fields.BigIntField()
    amount_left = fields.BigIntField()
    status = fields.IntEnumField(SwapStatus)

    level = fields.BigIntField()
    timestamp = fields.DatetimeField()


class Trade(Model):
    id = fields.BigIntField(pk=True)
    token = fields.ForeignKeyField('models.Token', 'trades', index=True)
    swap = fields.ForeignKeyField('models.Swap', 'trades', index=True)
    seller = fields.ForeignKeyField('models.Holder', 'sales', index=True)
    buyer = fields.ForeignKeyField('models.Holder', 'purchases', index=True)
    amount = fields.BigIntField()

    level = fields.BigIntField()
    timestamp = fields.DatetimeField()

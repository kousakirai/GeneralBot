from GBot.models import model

modelname = model.Guild


class Guild:
    def __init__(self, guild_id):
        self.guild_id = guild_id

    def get(self):
        rest = modelname.objects.filter(
            id=self.guild_id
            ).first()
        return rest

    def set(self, **kwargs):
        rest = modelname.objects.filter(
            id=self.guild_id
            ).update_one(**kwargs)
        return rest

    def delete(self):
        rest = modelname.objects.filter(
            id=self.guild_id
            ).first().delete()
        return rest

    @classmethod
    def create(cls, *, guild_id):
        rest = modelname(
            id=guild_id
            )
        rest.save()
        return rest

    @classmethod
    def get_all(cls):
        return modelname.objects.all()

    @classmethod
    def delete_all(cls):
        for guild in modelname.objects.all():
            guild.delete()
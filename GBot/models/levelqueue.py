from GBot.models import model

modelname = model.LevelQueue


class LevelQueue:
    def __init__(self, user_id):
        self.user_id = user_id

    def get(self):
        rest = modelname.objects.filter(
            id=self.user_id
            ).first()
        return rest

    def set(self, **kwargs):
        rest = modelname.objects.filter(
            id=self.user_id
            ).update_one(**kwargs)
        return rest

    def delete(self):
        rest = modelname.objects.filter(
            id=self.user_id
            ).first().delete()
        return rest

    @classmethod
    def create(cls, *, user_id):
        rest = modelname(
            id=user_id
            )
        rest.save()
        return rest

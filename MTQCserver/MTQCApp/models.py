from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=64, null=False)
    verified = models.BooleanField(default=True)
    rol = models.IntegerField(null=True)

    def __str__(self) -> str:
        return 'User id: {0}. email: {1}'.format(self.id, self.email)

    def get_projects(self):
        return list(Project.objects.filter(user=self)) + list(map(lambda ps: ps.project, ShareProject.objects.filter(user=self)))


class Verification(models.Model):
    token = models.CharField(primary_key=True, max_length=64, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    verified = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=100, null=False)
    path = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_allowed_users(self):
        return list(map(lambda us: us.user, ShareProject.objects.filter(project=self)))

    def add_allowed_user(self, user: User):
        ShareProject(user=user, project=self).save()


class ShareProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('user', 'project',)


'''
class File(models.Model):
    name = models.CharField(max_length=100, null=False)
    path = models.CharField(max_length=100, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
'''

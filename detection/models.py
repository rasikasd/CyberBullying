from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)


def __str__(self):
        return self.name

class Bullycomments(models.Model):
    comment_data = models.TextField()
    author = models.CharField(max_length=100)
    source = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    vid = models.ForeignKey(Profile, on_delete=models.CASCADE)

    

    def __str__(self):
        return  '%s %s' % (self.vid, self.comment_data)


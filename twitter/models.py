from django.db import models
from django.contrib.auth.models import User #importamos de django el modelo de user(integrado por django)
from django.utils import timezone #importando zona horaria

class Profile(models.Model):
    #oneToOne hace mencion a la clase User integrada en django de esta manera extendemos la clase para poder agregarle otros campos
    user = models.OneToOneField(User, on_delete=models.CASCADE) #CASCADE HACE REFERENCIA ASI EN CASO SE ETLIMINA EL REGISTRO SE ELIMINA ODOS LOS QUE DEPENDAN DE ESTE (HIJOS)
    bio = models.CharField(default="Hola, twitter", max_length=100)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return f"Perfil de {self.user.username}"


    def following(self):
        user_ids = RelationShip.objects.filter(from_user=self.user)\
                                    .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = RelationShip.objects.filter(to_user=self.user)\
                                    .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
        
    
    
    
    

class Post(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')

    class Meta:  #sirve para agregar informacion que no sea un campo en la base de datos
        ordering = ['-timestamp']

    def __str__(self):
        return self.content

    def num_likes(self):
        return self.liked.all().count()
    
  
class RelationShip(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}" #usuario sigue a tal usuario


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"









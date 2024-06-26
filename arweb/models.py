from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
        name            = models.CharField(max_length=255)
        product_id      = models.CharField(max_length=20, unique=True, blank=False)
        desc            = models.TextField(blank=True)
        created_at      = models.DateTimeField(auto_now_add=True)
        updated_at      = models.DateTimeField(auto_now=True)
        picture         = models.ImageField(upload_to='product/', null=True, blank=True)

        def __str__(self):
                return self.name
        def preview_name(self):
                return self.name[:40] + '...' if len(self.name) > 40 else self.name
        def preview_desc(self):
                return self.desc[:40] + '...' if len(self.desc) > 40 else self.desc
        def get_steps(self):
                steps = list(self.step_set.all())
                return steps
        def get_components(self):
                all_components = set()
                for step in self.get_steps():
                        all_components.update(step.components.all())
                return all_components
        
        steps                   = property(get_steps)
        components     = property(get_components)

class Step(models.Model):
        product             = models.ForeignKey(Product, on_delete=models.CASCADE)
        title               = models.CharField(max_length=250)
        order               = models.IntegerField(null=False, validators=[MinValueValidator(1)])
        instruction         = models.TextField(blank=True)
        components          = models.ManyToManyField('Component', blank=True, related_name='step_components')
        picture             = models.ImageField(upload_to='step_hint/', null=True, blank=True)


        def __str__(self):
                return self.title
    
class Component(models.Model):
        name                    = models.CharField(max_length=250)
        component_id            = models.CharField(max_length=15, unique=True)
        created_at              = models.DateTimeField(auto_now_add=True)
        updated_at              = models.DateTimeField(auto_now=True)
        is_active               = models.BooleanField(default=True)
        picture                 = models.ImageField(upload_to='component_pictures/', null=True, blank=True)

        def __str__(self):
                return self.name
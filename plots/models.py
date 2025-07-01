from django.db import models
from django.utils import timezone

# Updating project section

class Project(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    
    
    price_range_min = models.CharField(max_length=50)
    price_range_max = models.CharField(max_length=50)
    master_plan_image = models.ImageField(upload_to="project_images/", null=True, blank=True)
    payment_plan_image = models.ImageField(upload_to="project_images/", null=True, blank=True)
    
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    address = models.CharField(max_length=255)
    map_embed_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='project_videos/')

class ProjectOverviewRow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='overview_rows')
    plot_name = models.CharField(max_length=100)
    price_range = models.CharField(max_length=100)
    area_size = models.CharField(max_length=100)

class ProjectDescriptionSection(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='description_sections')
    heading = models.CharField(max_length=255)
    
class ProjectDescriptionPoint(models.Model):
    section = models.ForeignKey(ProjectDescriptionSection, on_delete=models.CASCADE, related_name='points')
    point = models.TextField()

class ProjectFeatureGroup(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feature_groups')
    group_title = models.CharField(max_length=255)  # e.g., "Plot Features", "Nearby Facilities"


class ProjectFeaturePoint(models.Model):
    group = models.ForeignKey(ProjectFeatureGroup, on_delete=models.CASCADE, related_name='points')
    point = models.CharField(max_length=255)  # e.g., "Electricity", "Security Staff"


class ProjectPlotType(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='plot_types')
    type_name = models.CharField(max_length=255)  # e.g., "Residential Plots", "Commercial (Block A)"
    price_range = models.CharField(max_length=100)  # e.g., "PKR 38.99 Lakh to 4.22 Crore"
    area_size = models.CharField(max_length=100)  # e.g., "5 - 20 Marla"
class Plot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="plots")
    plot_number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    size = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    image = models.ImageField(upload_to="plots/")
    class Meta:
        unique_together = ('project', 'plot_number')  # unique key for a project...

    def __str__(self):
        return f"{self.plot_number} - {self.title}"


# class Booking(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
#     cnic = models.CharField(max_length=15)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     booking_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.plot}"


class UserBooking(models.Model):
    PLAN_TYPE_CHOICES = [
        ('project', 'Project'),
        ('other_plot', 'Other Plot'),
    ]

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    reference_id = models.IntegerField()
    ptype = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    plot_number = models.CharField(max_length=100, blank=False, null=False)

    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    coupon = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.ptype} ({self.size})"


class Video(models.Model):
    title = models.CharField(max_length=255) 
    video = models.FileField(upload_to="videos/")

    def __str__(self):
        return self.title


class FloatingVideo(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="floating_videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # Intallments
# class InstallmentPlan(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='installments')
#     size = models.CharField(max_length=100)  # e.g., "3 marla", "2 kanal 4 marla"
#     total_payment = models.DecimalField(max_digits=12, decimal_places=2)
#     advance = models.DecimalField(max_digits=12, decimal_places=2)
#     remaining = models.DecimalField(max_digits=12, decimal_places=2)
#     installment = models.IntegerField()

#     def __str__(self):
#         return f"{self.project.name} - {self.size}"

class InstallmentPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('project', 'Project'),
        ('other_plot', 'Other Plot'),
    ]

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    reference_id = models.IntegerField()  # ID of Project or OtherPlot

    size = models.CharField(max_length=100)
    total_payment = models.CharField(max_length=100)  
    advance = models.CharField(max_length=100)
    remaining = models.CharField(max_length=100)
    installments = models.TextField()
    
    ptype = models.CharField(max_length=100, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_plan_type_display()} - {self.size}"






# plots details
# models.py
class PlotDetail(models.Model):
    plot = models.OneToOneField(Plot, on_delete=models.CASCADE)
    overview = models.JSONField()
    description = models.TextField()
    map_embed_url = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

class PlotImage(models.Model):
    plot_detail = models.ForeignKey(PlotDetail, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="plot_images/")

class PlotVideo(models.Model):
    plot_detail = models.ForeignKey(PlotDetail, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to="plot_videos/")




# other plots
class OtherPlot(models.Model):
    location = models.CharField(max_length=255)
    map_embed_url = models.URLField(max_length=1000) # Google Maps iframe URL
    image = models.ImageField(upload_to="other_plot_images/")
    video = models.FileField(upload_to="other_plot_videos/", blank=True, null=True)
    description = models.TextField()
    overview = models.TextField()
    available = models.BooleanField(default=True)
    price = models.CharField(max_length=50)
    plot_size = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location
    
class OtherPlotImage(models.Model):
    plot = models.ForeignKey(OtherPlot, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='other_plots/images/')

    def __str__(self):
        return f"Image for {self.plot.id}"


class OtherPlotVideo(models.Model):
    plot = models.ForeignKey(OtherPlot, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='other_plots/videos/')

    def __str__(self):
        return f"Video for {self.plot.id}"


# dealers

class Dealer(models.Model):
    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=20, unique=True)
    coupon_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.coupon_id}"
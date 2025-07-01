

from django.contrib import admin
from django.utils.html import format_html
from .models import Dealer
from .models import OtherPlot
from .models import (
   Plot, Project, ProjectImage, ProjectVideo, 
    ProjectOverviewRow, ProjectDescriptionSection, ProjectDescriptionPoint , UserBooking
)

admin.site.register(Plot)

admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(ProjectVideo)
admin.site.register(ProjectOverviewRow)
admin.site.register(ProjectDescriptionSection)
admin.site.register(ProjectDescriptionPoint)

admin.site.register(UserBooking)
admin.site.register(Dealer)
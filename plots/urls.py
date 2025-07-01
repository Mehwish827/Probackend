from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InstallmentPlanViewSet, get_installment_plans
from .views import submit_booking
# from .views import get_bookings
from rest_framework.routers import DefaultRouter
from .views import PlotDetailViewSet, PlotImageViewSet, PlotVideoViewSet , create_project
from django.urls import path, include
from . import views
from .views import OtherPlotListCreateAPIView
from .views import OtherPlotDetailAPIView

from .views import (
    # Project APIs
    project_list,
    project_detail,
    delete_project_by_name,
    delete_user_booking,
    get_dealers,
    delete_dealer,

    # Plot APIs
    get_all_plots,
    get_plots_by_project,
    add_plot,
    delete_plot,
    
    project_detail,
    delete_installment,

    # Booking APIs
    # book_plot,
    # get_bookings,
    # remove_booking,

    # Video APIs
    upload_video,
    video_list,
    delete_video_by_title,

    # Floating video
    get_floating_video,
    upload_floating_video,
    OtherPlotViewSet,

    # project detail
    OtherPlotDetailAPIView,
    OtherPlotImageListView,
    OtherPlotVideoListView,



    ProjectViewSet,
    ProjectImageViewSet,
    ProjectVideoViewSet,
    ProjectOverviewRowViewSet,
    ProjectDescriptionSectionViewSet
)
router = DefaultRouter()
router.register(r'plot-details', PlotDetailViewSet, basename='plot-detail')
router.register(r'plot-images', PlotImageViewSet, basename='plot-image')
router.register(r'plot-videos', PlotVideoViewSet, basename='plot-video')
router.register(r'installment-plans', InstallmentPlanViewSet)
router.register(r'other-plots', OtherPlotViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-images', ProjectImageViewSet)
router.register(r'project-videos', ProjectVideoViewSet)
router.register(r'project-overview-rows', ProjectOverviewRowViewSet)
router.register(r'project-description-sections', ProjectDescriptionSectionViewSet)

urlpatterns = router.urls
urlpatterns = [
    # Project APIs
    path("projects/", project_list, name="project-list"),
    path('project/<int:project_id>/', project_detail, name='project-detail'),
    path("delete-project/", delete_project_by_name, name="delete-project"),

    # Plot APIs
    path("add-plot/", add_plot, name="add-plot"),
    path("get-plots/", get_all_plots, name="get-all-plots"),
    path("get-plots/<str:project_name>/", get_plots_by_project, name="get-plots-by-project"),
    path("delete-plot/", delete_plot, name="delete-plot"),
    

    # # Booking APIs
    # path("book-plot/", book_plot, name="book-plot"),
    # path("get-bookings/", get_bookings),
    # path("remove-booking/", remove_booking, name="remove-booking"),

    # Video APIs
    path("upload-video/", upload_video, name="upload-video"),
    path("videos/", video_list, name="video-list"),
    path("delete-video/", delete_video_by_title, name="delete-video"),

    # Floating Video
    path("floating-video/", get_floating_video, name="floating-video"),
    path("upload-floating-video/", upload_floating_video, name="upload-floating-video"),

   
    path('get-installment-plans/<int:project_id>/', get_installment_plans, name='get_installment_plans'),

    path('submit-booking/', submit_booking, name='submit-booking'),
    path("delete-installment/", delete_installment, name="delete_installment"),
    path('delete-installment/', views.delete_installment),
    # path('get-bookings/', get_bookings),
    path("delete-plot/", views.delete_plot, name="delete_plot"),

    path('user-bookings/', views.get_user_bookings, name='user-bookings'),
  
    path("projects/", create_project),



    
    path('', include(router.urls)),
    path('project-detail/<int:project_id>/', project_detail, name='project-detail'),
    path('delete-other-plot/', views.delete_other_plot, name='delete-other-plot'),
    path("other-plots/<int:pk>/", OtherPlotDetailAPIView.as_view()),
    path("other-plot-image/", OtherPlotImageListView.as_view()),
    path("other-plot-video/", OtherPlotVideoListView.as_view()),
    path("delete-user-booking/", delete_user_booking),
    
    path('dealers/', get_dealers, name='get-dealers'),
    
    path('delete-dealer/<int:dealer_id>/', delete_dealer, name='delete-dealer'),
    

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

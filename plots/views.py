from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import OtherPlot, OtherPlotImage, OtherPlotVideo
from .serializers import OtherPlotSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from .models import (
    UserBooking, Plot, Project, Video, FloatingVideo, 
    InstallmentPlan, PlotDetail, PlotImage, PlotVideo ,
    Project, ProjectImage, ProjectVideo, ProjectOverviewRow, ProjectDescriptionSection , ProjectDescriptionPoint,
    ProjectFeatureGroup, ProjectFeaturePoint, ProjectPlotType
    
)
from rest_framework import generics
from .models import Dealer
from .serializers import DealerSerializer
from .serializers import OtherPlotSerializer, OtherPlotImageSerializer, OtherPlotVideoSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import (
    UserBookingSerializer, PlotSerializer, ProjectSerializer,
    VideoSerializer, FloatingVideoSerializer,
    InstallmentPlanSerializer, PlotDetailSerializer,
    PlotImageSerializer, PlotVideoSerializer ,
    ProjectSerializer, ProjectImageSerializer, ProjectVideoSerializer,
    ProjectOverviewRowSerializer, ProjectDescriptionSectionSerializer
)

# --- Project List (GET + POST)
# @api_view(['GET', 'POST'])
# @parser_classes([MultiPartParser, FormParser])
# def project_list(request):
#     if request.method == 'GET':
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True, context={"request": request})
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
import json

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # First: Save the base project
        project_serializer = ProjectSerializer(data=request.data)
        if not project_serializer.is_valid():
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project = project_serializer.save()

        # ✅ Parse JSON nested fields
        overview_rows = json.loads(request.data.get("overview_rows", "[]"))
        description_sections = json.loads(request.data.get("description_sections", "[]"))
        feature_groups = json.loads(request.data.get("feature_groups", "[]"))
        plot_types = json.loads(request.data.get("plot_types", "[]"))

        # ✅ Save overview rows
        for row in overview_rows:
            ProjectOverviewRow.objects.create(project=project, **row)

        # ✅ Save description sections and their points
        for section in description_sections:
            sec_obj = ProjectDescriptionSection.objects.create(project=project, heading=section["heading"])
            for point in section.get("points", []):
                ProjectDescriptionPoint.objects.create(section=sec_obj, point=point)

        # ✅ Save feature groups and their points
        for group in feature_groups:
            fg = ProjectFeatureGroup.objects.create(project=project, group_title=group["group_title"])
            for point in group.get("points", []):
                ProjectFeaturePoint.objects.create(group=fg, point=point)

        # ✅ Save plot types
        for pt in plot_types:
            ProjectPlotType.objects.create(project=project, **pt)

        # ✅ Save uploaded images
        for img in request.FILES.getlist("images"):
            ProjectImage.objects.create(project=project, image=img)

        # ✅ Save uploaded videos
        for vid in request.FILES.getlist("videos"):
            ProjectVideo.objects.create(project=project, video=vid)

        return Response(ProjectSerializer(project, context={"request": request}).data, status=status.HTTP_201_CREATED)

# --- Add Plot to a Project
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_plot(request):
    project_name = request.data.get('project_name')
    plot_number = request.data.get('plot_number')
    size = request.data.get('size')
    image = request.data.get('image')

    if not project_name:
        return Response({"error": "Project name is required"}, status=400)

    try:
        project = Project.objects.get(name=project_name)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

    plot = Plot(project=project, plot_number=plot_number, size=size, image=image)
    plot.save()
    return Response({"message": "Plot added successfully"}, status=201)


# --- Get all plots
@api_view(['GET'])
def get_all_plots(request):
    plots = Plot.objects.all()
    serializer = PlotSerializer(plots, many=True, context={"request": request})
    return Response(serializer.data)


# --- Get plots by project name
@api_view(['GET'])
def get_plots_by_project(request, project_name):
    try:
        project = Project.objects.get(name=project_name)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

    plots = Plot.objects.filter(project=project)
    serializer = PlotSerializer(plots, many=True, context={"request": request})
    return Response(serializer.data)


# --- Remove a plot by number
@api_view(['POST'])
def delete_plot(request):
    plot_number = request.data.get("plot_number")
    if not plot_number:
        return Response({"error": "Plot number is required"}, status=400)

    try:
        plot = Plot.objects.get(plot_number=plot_number)
        plot.delete()
        return Response({"message": "Plot deleted"})
    except Plot.DoesNotExist:
        return Response({"error": "Plot not found"}, status=404)



# --- Upload a regular video
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# --- List all regular videos
@api_view(['GET', 'POST'])
def video_list(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True, context={"request": request})
    return Response(serializer.data)


# --- Get floating video
@api_view(['GET', 'POST'])
def get_floating_video(request):
    try:
        video = FloatingVideo.objects.last()
        return Response({'video': video.video.url if video else None})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# --- Upload new floating video
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_floating_video(request):
    serializer = FloatingVideoSerializer(data=request.data)
    if serializer.is_valid():
        FloatingVideo.objects.all().delete()
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# --- Delete video by title
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def delete_video_by_title(request):
    title = request.data.get("title")
    if not title:
        return Response({"error": "Title is required"}, status=400)

    try:
        video = Video.objects.get(title=title)
        video.delete()
        return Response({"message": f"Video titled '{title}' deleted successfully"})
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)


# --- Delete project by name
@api_view(['POST'])
def delete_project_by_name(request):
    name = request.data.get('name')
    if not name:
        return Response({'error': 'Project name is required'}, status=400)
    projects = Project.objects.filter(name=name)
    if not projects.exists():
        return Response({'error': 'No project found with that name'}, status=status.HTTP_404_NOT_FOUND)

    deleted_count = projects.delete()[0]
    return Response({'message': f'{deleted_count} project(s) deleted successfully'})



# --- Get project detail
@api_view(['GET'])
def project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    # installment plan
# @api_view(['POST'])
# @parser_classes([JSONParser])
# def add_installment_plan(request):
#     serializer = InstallmentPlanSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)


class InstallmentPlanViewSet(viewsets.ModelViewSet):
    queryset = InstallmentPlan.objects.all().order_by('-created_at')
    serializer_class = InstallmentPlanSerializer
@api_view(['GET'])
def get_installment_plans(request, project_id):
    plans = InstallmentPlan.objects.filter(project__id=project_id)
    serializer = InstallmentPlanSerializer(plans, many=True)
    return Response(serializer.data)
# booking
@api_view(['GET', 'POST'])
def submit_booking(request):
    if request.method == 'GET':
        return Response({"message": "Booking submission endpoint. Use POST to submit."})

    if request.method == 'POST':
        data = request.data
        # Validate required fields
        required_fields = ['plan_type', 'reference_id', 'ptype', 'size', 'name', 'cnic', 'phone','plot_number']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        from .models import UserBooking  # Make sure this model exists
        booking = UserBooking.objects.create(
            plan_type=data['plan_type'],
            reference_id=data['reference_id'],
            ptype=data['ptype'],
            size=data['size'],
            name=data['name'],
            cnic=data['cnic'],
            phone=data['phone'],
            plot_number=data['plot_number'],
            email=data.get('email', ""),
            coupon=data.get('coupon', "")
            
            
        )
        return Response({"message": "Booking submitted successfully."}, status=status.HTTP_201_CREATED)
    


@api_view(["GET", "POST"])
@csrf_exempt  # ✅ csrf_exempt comes after api_view
def get_user_bookings(request):
    bookings = UserBooking.objects.all().order_by('-id')
    serializer = UserBookingSerializer(bookings, many=True)
    return Response(serializer.data)
# till here
@api_view(["GET", "POST"])
@csrf_exempt 
def delete_installment(request):
    if request.method == "GET":
        return Response({"message": "Send a POST request to delete an installment plan."})

    if request.method == "POST":
        plan_type = request.data.get("plan_type")
        reference_id = request.data.get("reference_id")
        plot_size = request.data.get("plot_size", "").strip()

        print("🔥 Deleting Installment Plan With:")
        print("➡️ plan_type:", plan_type)
        print("➡️ reference_id:", reference_id)
        print("➡️ plot_size:", plot_size)

        if not plan_type or reference_id is None or not plot_size:
            return Response(
                {"message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Print all possible matches for debugging
            matching = InstallmentPlan.objects.filter(
                plan_type=plan_type,
                reference_id=reference_id
            )
            print("📦 All matching plans:", list(matching.values("size", "plan_type", "reference_id")))

            installment = matching.filter(size__iexact=plot_size).first()

            if not installment:
                return Response(
                    {
                        "message": "Installment plan not found.",
                        "debug": {
                            "plan_type": plan_type,
                            "reference_id": reference_id,
                            "plot_size": plot_size,
                            "available_sizes": list(matching.values_list("size", flat=True)),
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            installment.delete()
            return Response({"message": "✅ Installment plan deleted successfully."})

        except Exception as e:
            return Response(
                {"message": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# --- Plot Details: ViewSets for DRF Router (Admin Use) ---
class PlotDetailViewSet(viewsets.ModelViewSet):
    queryset = PlotDetail.objects.all()
    serializer_class = PlotDetailSerializer

class PlotImageViewSet(viewsets.ModelViewSet):
    queryset = PlotImage.objects.all()
    serializer_class = PlotImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        plot_detail_id = request.data.get("plot_detail")
        images = request.FILES.getlist("image")

        if not plot_detail_id or not images:
            return Response({"error": "plot_detail and image(s) required."}, status=status.HTTP_400_BAD_REQUEST)

        created_objects = []

        for img in images:
            serializer = self.get_serializer(data={"plot_detail": plot_detail_id, "image": img})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            created_objects.append(serializer.data)

        return Response({"message": "Images uploaded", "data": created_objects}, status=status.HTTP_201_CREATED)

class PlotVideoViewSet(viewsets.ModelViewSet):
    queryset = PlotVideo.objects.all()
    serializer_class = PlotVideoSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        plot_detail_id = request.data.get("plot_detail")
        videos = request.FILES.getlist("video")

        if not plot_detail_id or not videos:
            return Response({"error": "plot_detail and video(s) required."}, status=status.HTTP_400_BAD_REQUEST)

        created_objects = []

        for vid in videos:
            serializer = self.get_serializer(data={"plot_detail": plot_detail_id, "video": vid})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            created_objects.append(serializer.data)

        return Response({"message": "Videos uploaded", "data": created_objects}, status=status.HTTP_201_CREATED)


    # delet plot
@api_view(["POST"])
def delete_plot(request):
    project_name = request.data.get("project_name")
    plot_number = request.data.get("plot_number")

    if not project_name or not plot_number:
        return Response({"error": "Missing required fields."}, status=400)

    deleted, _ = Plot.objects.filter(project__name=project_name, plot_number=plot_number).delete()

    if deleted:
        return Response({"message": f"{deleted} plot(s) deleted successfully."})
    else:
        return Response({"error": "No plot found matching the criteria."}, status=404)
    






# project upadated section

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer

class ProjectVideoViewSet(viewsets.ModelViewSet):
    queryset = ProjectVideo.objects.all()
    serializer_class = ProjectVideoSerializer

class ProjectOverviewRowViewSet(viewsets.ModelViewSet):
    queryset = ProjectOverviewRow.objects.all()
    serializer_class = ProjectOverviewRowSerializer

class ProjectDescriptionSectionViewSet(viewsets.ModelViewSet):
    queryset = ProjectDescriptionSection.objects.all()
    serializer_class = ProjectDescriptionSectionSerializer

# views.py
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



class OtherPlotViewSet(viewsets.ModelViewSet):
    queryset = OtherPlot.objects.all()
    serializer_class = OtherPlotSerializer

class OtherPlotListCreateAPIView(APIView):
    def get(self, request):
        plots = OtherPlot.objects.all()
        serializer = OtherPlotSerializer(plots, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        plot = OtherPlot.objects.create(
            location=data.get("location"),
            map_embed_url=data.get("map_embed_url"),
            description=data.get("description"),
            overview=data.get("overview"),
            available=data.get("available") == "true",
            price=data.get("price"),
            plot_size=data.get("plot_size"),
        )

        # Handle multiple images
        images = request.FILES.getlist("images")
        for img in images:
            OtherPlotImage.objects.create(plot=plot, image=img)

        # Handle multiple videos
        videos = request.FILES.getlist("videos")
        for vid in videos:
            OtherPlotVideo.objects.create(plot=plot, video=vid)

        serializer = OtherPlotSerializer(plot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



   
#    delete plot

@api_view(['POST'])
def delete_other_plot(request):
    plot_id = request.data.get("id")
    
    if not plot_id:
        return Response({"error": "Plot ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        plot = OtherPlot.objects.get(id=plot_id)
        plot.delete()
        return Response({"message": "Plot deleted successfully."}, status=status.HTTP_200_OK)
    except OtherPlot.DoesNotExist:
        return Response({"error": "Plot not found."}, status=status.HTTP_404_NOT_FOUND)
    

class OtherPlotViewSet(viewsets.ModelViewSet):
    queryset = OtherPlot.objects.all()
    serializer_class = OtherPlotSerializer
    parser_classes = [MultiPartParser, FormParser]

class OtherPlotImageListView(ListAPIView):
    serializer_class = OtherPlotImageSerializer

    def get_queryset(self):
        plot_id = self.request.query_params.get("plot_id")
        return OtherPlotImage.objects.filter(other_plot_id=plot_id)

class OtherPlotVideoListView(ListAPIView):
    serializer_class = OtherPlotVideoSerializer

    def get_queryset(self):
        plot_id = self.request.query_params.get("plot_id")
        return OtherPlotVideo.objects.filter(other_plot_id=plot_id)
    
class OtherPlotDetailAPIView(RetrieveAPIView):
    queryset = OtherPlot.objects.all()
    serializer_class = OtherPlotSerializer


# delete booking

@api_view(["DELETE"])
def delete_user_booking(request):
    cnic = request.data.get("cnic")
    reference_id = request.data.get("reference_id")
    plan_type = request.data.get("plan_type")

    if not (cnic and reference_id and plan_type):
        return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = UserBooking.objects.get(cnic=cnic, reference_id=reference_id, plan_type=plan_type)
        booking.delete()
        return Response({"message": "Booking deleted successfully."}, status=status.HTTP_200_OK)
    except UserBooking.DoesNotExist:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_dealers(request):
    dealers = Dealer.objects.all().order_by('-id')
    serializer = DealerSerializer(dealers, many=True)
    return Response(serializer.data)


# delete

@api_view(['DELETE'])
def delete_dealer(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        dealer.delete()
        return Response({"message": "Dealer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Dealer.DoesNotExist:
        return Response({"error": "Dealer not found."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'POST'])
def create_dealer(request):
    if request.method == 'GET':
        return Response({"message": "Send a POST request to create a dealer."})
    
    serializer = DealerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_project_by_name(request):
    name = request.data.get('name')
    if not name:
        return Response({'error': 'Project name is required'}, status=400)
    
    projects = Project.objects.filter(name=name)
    if not projects.exists():
        return Response({'error': 'No project found with that name'}, status=404)

    deleted_count = projects.delete()[0]
    return Response({'message': f'{deleted_count} project(s) deleted successfully'})
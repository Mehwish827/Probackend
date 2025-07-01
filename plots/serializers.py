from rest_framework import serializers
from .models import  Plot,  Video, FloatingVideo
from .models import InstallmentPlan
from .models import Dealer
from .models import Plot, PlotDetail, PlotImage, PlotVideo
from .models import OtherPlot , OtherPlotImage, OtherPlotVideo


from .models import (
    Project, ProjectImage, ProjectVideo, 
    ProjectOverviewRow, ProjectDescriptionSection, ProjectDescriptionPoint , ProjectFeatureGroup,
    ProjectFeaturePoint,
    ProjectPlotType,UserBooking,

)

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVideo
        fields = ['id', 'video']

class ProjectOverviewRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOverviewRow
        fields = ['id', 'plot_name', 'price_range', 'area_size']

class ProjectDescriptionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDescriptionPoint
        fields = ['id', 'point']

class ProjectDescriptionSectionSerializer(serializers.ModelSerializer):
    points = ProjectDescriptionPointSerializer(many=True)

    class Meta:
        model = ProjectDescriptionSection
        fields = ['id', 'heading', 'points']

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        section = ProjectDescriptionSection.objects.create(**validated_data)
        for point_data in points_data:
            ProjectDescriptionPoint.objects.create(section=section, **point_data)
        return section
    
class ProjectFeaturePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFeaturePoint
        fields = ['id', 'point']


class ProjectFeatureGroupSerializer(serializers.ModelSerializer):
    points = ProjectFeaturePointSerializer(many=True)

    class Meta:
        model = ProjectFeatureGroup
        fields = ['id', 'group_title', 'points']
class ProjectPlotTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlotType
        fields = ['id', 'type_name', 'price_range', 'area_size']


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, required=False)
    videos = ProjectVideoSerializer(many=True, required=False)
    overview_rows = ProjectOverviewRowSerializer(many=True, required=False)
    description_sections = ProjectDescriptionSectionSerializer(many=True, required=False)
    feature_groups = ProjectFeatureGroupSerializer(many=True, required=False)
    plot_types = ProjectPlotTypeSerializer(many=True, required=False)

    # Explicitly add the image fields for upload
    master_plan_image = serializers.ImageField(required=False, allow_null=True)
    payment_plan_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data
        images_data = validated_data.pop('images', [])
        videos_data = validated_data.pop('videos', [])
        overview_rows_data = validated_data.pop('overview_rows', [])
        description_sections_data = validated_data.pop('description_sections', [])
        feature_groups_data = validated_data.pop('feature_groups', [])
        plot_types_data = validated_data.pop('plot_types', [])

        # Create project (including master_plan_image and payment_plan_image)
        project = Project.objects.create(**validated_data)

        # Create nested: images
        for image in images_data:
            ProjectImage.objects.create(project=project, **image)

        # Create nested: videos
        for video in videos_data:
            ProjectVideo.objects.create(project=project, **video)

        # Create nested: overview rows
        for row in overview_rows_data:
            ProjectOverviewRow.objects.create(project=project, **row)

        # Create nested: description sections and points
        for section in description_sections_data:
            points = section.pop('points', [])
            section_obj = ProjectDescriptionSection.objects.create(project=project, **section)
            for point in points:
                ProjectDescriptionPoint.objects.create(section=section_obj, **point)

        # Create nested: feature groups and points
        for group in feature_groups_data:
            points = group.pop('points', [])
            group_obj = ProjectFeatureGroup.objects.create(project=project, **group)
            for point in points:
                ProjectFeaturePoint.objects.create(group=group_obj, **point)

        # Create nested: plot types
        for plot in plot_types_data:
            ProjectPlotType.objects.create(project=project, **plot)

        return project




class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'
       
        

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class FloatingVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatingVideo
        fields = '__all__'
class InstallmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPlan
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    installments = InstallmentPlanSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'




# class BookingSerializer(serializers.ModelSerializer):
#     plot = PlotSerializer()
#     project = serializers.SerializerMethodField()
    
    
#     class Meta:
#         model = Booking
#         fields = '__all__'
#     def get_project(self, obj):
#         if obj.plot and obj.plot.project:
#             return {
#                 "name": obj.plot.project.name
#             }
#         return None


class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBooking
        fields = '__all__'


# plots details

# serializers.py

class PlotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotImage
        fields = '__all__'

class PlotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotVideo
        fields = '__all__'

class PlotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotDetail
        fields = '__all__'
class OtherPlotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPlotImage
        fields = ['id', 'image']

class OtherPlotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPlotVideo
        fields = ['id', 'video']


# other plots
class OtherPlotSerializer(serializers.ModelSerializer):
    images = OtherPlotImageSerializer(many=True, read_only=True)
    videos = OtherPlotVideoSerializer(many=True, read_only=True)
    class Meta:
        model = OtherPlot
        fields = "__all__"

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'
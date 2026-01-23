import django_filters
from .models import Course

class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search by Title')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains', label='Category')
    level = django_filters.ChoiceFilter(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], label='Level')
    rating = django_filters.RangeFilter(label="Rating Range")  # Filter courses by rating range
    # price=django_filters.RangeFilter(label="price-range")
    class Meta:
        model = Course
        fields = ['title', 'category', 'level', 'rating']

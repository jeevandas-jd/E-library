from django.contrib import admin
from .models import StudyMaterial

class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'semester')  # Display fields in the list view
    search_fields = ('title', 'subject')             # Add search capability
    list_filter = ('semester', 'subject')            # Add filters for easier management
    ordering = ('semester', 'subject')               # Order by semester and subject

admin.site.register(StudyMaterial, StudyMaterialAdmin)

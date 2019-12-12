from django.contrib import admin

# Register your models here.
from .models import Flow

class FlowAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "user", "topic", "direction", "state"]
	search_fields = ["user"]

	# list_filter = ["price", "sale_price"]
	# list_editable = ["sale_price"]
	class Meta:
		model = Flow

admin.site.register(Flow, FlowAdmin)
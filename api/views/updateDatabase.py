import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def update_database_name(request):
    new_db_name = request.data.get("database_name")

    if not new_db_name:
        return Response({"error": "Database name is required"}, status=400)

    # Get the correct settings.py file path
    settings_file = settings.__file__

    try:
        with open(settings_file, "r") as file:
            lines = file.readlines()

        with open(settings_file, "w") as file:
            for line in lines:
                if '"NAME":' in line:
                    file.write(f'        "NAME": "{new_db_name}",\n')
                else:
                    file.write(line)

        return Response({"message": "Database name updated successfully. Restart the server to apply changes."})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

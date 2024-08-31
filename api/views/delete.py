import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Api


def delete_function_from_file(app_name, name):
    file_path = os.path.join(settings.BASE_DIR, app_name, 'generated_apis', f"{name}.py")
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"{file_path} deleted."
    return f"{file_path} does not exist."


def remove_from_urls_file(app_name, name):
    urls_path = os.path.join(settings.BASE_DIR, app_name, 'urls.py')
    import_statement = f"from .generated_apis.{name} import {name}"
    urlpattern_entry = f"path('{name}/', {name}),"  # Adjust this pattern as needed

    with open(urls_path, 'r+') as f:
        content = f.readlines()
        
        # Remove the import statement
        content = [line for line in content if line.strip() != import_statement]
        
        # Remove the urlpattern entry
        content = [line for line in content if urlpattern_entry not in line.strip()]
        
        # Move back to the beginning of the file and write the changes
        f.seek(0)
        f.truncate()
        f.writelines(content)


@api_view(['DELETE'])
def delete_api(request):
    try:
        name = request.data.get('name').strip()

        if not name:
            return Response({'error': 'name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the API exists in the database
        try:
            api_to_delete = Api.objects.get(name=name)
        except Api.DoesNotExist:
            return Response({'error': 'API with this name does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Remove the API from the database
        api_to_delete.delete()

        # Delete the generated function file
        delete_message = delete_function_from_file("api", name)

        # Update the urls.py file to remove the API import and urlpattern
        remove_from_urls_file("api", name)

        return Response({'message': f"API '{name}' deleted successfully. {delete_message}"})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

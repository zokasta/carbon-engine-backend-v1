import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Api  # Import your Api model

def generate_api_function_content(method, name):
    lines = [
        "from rest_framework.decorators import api_view",
        "from rest_framework.response import Response",
        "",
        f"@api_view(['{method.upper()}'])",
        f"def {name}(request):",
        "    # Your logic here",
        "    return Response({'status': True, 'message': 'API working correctly'})",
    ]
    function_content = "\n".join(lines)
    return function_content

def write_to_file(app_name, file_name, file_content):
    app_directory = os.path.join(settings.BASE_DIR, app_name, 'generated_apis')
    if not os.path.exists(app_directory):
        os.makedirs(app_directory)
    file_path = os.path.join(app_directory, file_name)
    with open(file_path, 'w') as f:
        f.write(file_content)
    return file_path

def update_urls_file(app_name, url, name):
    urls_path = os.path.join(settings.BASE_DIR, app_name, 'urls.py')
    import_statement = f"from .generated_apis.{name} import {name}"
    urlpattern_entry = f"    path('{url.lstrip('/')}', {name}),"
    
    with open(urls_path, 'r+') as f:
        content = f.readlines()
        # Insert the import statement at the top
        if import_statement + "\n" not in content:
            content.insert(0, import_statement + "\n")
        # Find the `urlpatterns` list and insert the new entry
        for i, line in enumerate(content):
            if 'urlpatterns' in line:
                content.insert(i + 1, urlpattern_entry + "\n")
                break
        # Move back to the beginning of the file and write the changes
        f.seek(0)
        f.writelines(content)

@api_view(['POST'])
def create_api(request):
    try:
        method = request.data.get('method').strip().lower()
        url = request.data.get('url').strip()
        name = request.data.get('name').strip()
        
        if not all([method, url, name]):
            return Response({'error': 'method, url, and name are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if URL already exists in the database
        if Api.objects.filter(url=url).exists():
            return Response({'error': 'API with this URL already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the API to the database
        new_api = Api(url=url, method=method)
        new_api.save()
        
        # Generate the API function content
        function_content = generate_api_function_content(method, name)
        
        # Write the function to a new file in the generated_apis folder
        file_name = f"{name}.py"
        app_name = "api"  # Replace with your app's name
        file_path = write_to_file(app_name, file_name, function_content)
        
        # Update the urls.py file to include the new API
        update_urls_file(app_name, url, name)
        
        return Response({'message': f"API '{name}' created successfully, added to database, saved in '{file_path}', and added to urls.py!"})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

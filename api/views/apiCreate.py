import os
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

def parse_structure(structure):
    input_node = structure[0]
    output_node = structure[1]

    input_mapping = {}
    for var, details in input_node['structure'].items():
        input_mapping[var] = {
            'target': details['target'],
            'location': details['location']
        }

    return input_mapping, output_node['id']

def generate_function_content(input_mapping, output_node_id, file, format_structure):
    lines = [
        "import re",
        "from rest_framework.decorators import api_view",
        "from rest_framework.response import Response",
    ]

    lines.append("") 
    lines.append(f"@api_view(['POST'])")
    lines.append(f"def {file}(request):")

    output_node_structure = next(
        (node for node in format_structure if node['id'] == output_node_id), 
        None
    )
    
    if output_node_structure:
        output_mapping = output_node_structure['structure']
    else:
        output_mapping = {}

    # Process input mappings
    for var, mapping in input_mapping.items():
        lines.append(f"    {var} = request.data.get('{var}')")

    # Build response data based on output node structure
    response_data = []
    for output_key, output_value in output_mapping.items():
        # Find the input variable that corresponds to the output key
        input_var = next(
            (var for var, mapping in input_mapping.items() if mapping['location'] == output_key),
            None
        )
        if input_var:
            response_data.append(f"'{output_key}': {input_var}")

    # Build the response line
    response_line = "    return Response({ " + ", ".join(response_data) + " })"
    lines.append(response_line)
    
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

@api_view(['POST'])
def api_generator(request):
    try:
        file_name = request.data.get('file', 'generated_api') + '.py'
        format_structure = request.data.get('format')

        if not format_structure:
            return Response({'error': 'format structure is required.'}, status=status.HTTP_400_BAD_REQUEST)

        input_mapping, output_node_id = parse_structure(format_structure)

        function_content = generate_function_content(input_mapping, output_node_id, request.data.get('file', "generated_api"), format_structure)

        app_name = "api"  # Replace with your app's name
        file_path = write_to_file(app_name, file_name, function_content)

        return Response({'message': f"API file '{file_name}' created successfully in '{file_path}'!"})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

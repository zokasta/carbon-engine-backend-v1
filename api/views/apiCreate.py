import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

def parse_structure(structure):
    if not isinstance(structure, list) or len(structure) < 2:
        raise ValueError("Invalid format structure. Ensure there is at least one input and one output node.")

    input_node = structure[0]
    output_node = structure[1]

    input_mapping = {}
    for var, details in input_node.get('structure', {}).items():
        if 'fields' in details:
            input_mapping[var] = details['fields']
        else:
            input_mapping[var] = [{
                'target': details.get('target', 'none'),
                'location': details.get('location', 'none')
            }]
    
    return input_mapping, output_node.get('id', 'output_node')

def generate_function_content(input_mapping, output_node_id, file, format_structure):
    lines = [
        "import re",
        "from rest_framework.decorators import api_view",
        "from rest_framework.response import Response",
        "",
        f"@api_view(['POST'])",
        f"def {file}(request):"
    ]

    # Process input mappings
    for var in input_mapping:
        lines.append(f"    {var} = request.data.get('{var}')")

    # Extract the output node structure
    output_node_structure = next(
        (node for node in format_structure if node['id'] == output_node_id), 
        None
    )
    
    output_mapping = output_node_structure.get('structure', {}) if output_node_structure else {}

    # Build response data based on input and output mapping
    response_data = []
    for var, mappings in input_mapping.items():
        for mapping in mappings:
            if mapping['target'] != 'none':
                response_data.append(f"'{mapping['location']}': {var}")

    # Build the response line
    if response_data:
        response_line = "    return Response({ " + ", ".join(response_data) + " })"
    else:
        response_line = "    return Response({})"

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
            return Response({'error': 'Format structure is required.'}, status=status.HTTP_400_BAD_REQUEST)

        input_mapping, output_node_id = parse_structure(format_structure)

        function_content = generate_function_content(input_mapping, output_node_id, request.data.get('file', "generated_api"), format_structure)

        app_name = "api"  # Replace with your app's name
        file_path = write_to_file(app_name, file_name, function_content)

        return Response({'message': f"API file '{file_name}' created successfully in '{file_path}'!"})

    except ValueError as ve:
        return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

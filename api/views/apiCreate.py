import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin


def add_tabs(input_list, num_tabs):
    tab_prefix = "\t" * num_tabs
    return [tab_prefix + item for item in input_list]


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):  # If item is a list, recursively flatten
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)  # Otherwise, add directly
    return flat_list

def generate_function_content(elements :list, edges, file, type):
    result = []
    imports_lines=[]
    title_lines = []
    variable_lines = []
    output_lines = []
    
    imports_lines = [
        "from rest_framework.decorators import api_view",
        "from rest_framework.response import Response",
        "from rest_framework import status",
        "from ..plugin.load_plugin import load_plugin",
        "",
    ]
    
    result.append(imports_lines)

    title_lines = [f"@api_view(['{str(type).upper()}'])", f"def {file}(request):"]
    result.append(title_lines)
    
    input_nodes = []
    for element in elements:
        if element['type'] == "input_node":
            input_nodes.append(element)
            
    # input_nodes = next(
    #     (node for node in elements if node["type"] == "input_node"), None
    # )
    # output_nodes = next(
    #     (node for node in elements if node["type"] == "output_node"), None
    # )

    # Process input mappings
    for inputs in input_nodes:
        for node in inputs['nodes']:
            variable_lines.append(
                f"{node['display_name']} = request.data.get('{node['display_name']}')"
            )

    result.append(add_tabs(variable_lines,1))
    # return str(result)
    
    
  
    response_data = []
    for edge in edges: 
        
        for element in elements:
            if element['element_id'] == edge['source_id']:
                for node in element['nodes']:
                    if node['node_id'] == edge['source_node_id']:
                        source = node
                        return str(source)
            if element['element_id'] == edge['target_id']:
                for node in element['nodes']:
                    if node['node_id'] == edge['target_node_id']:
                        target = node
        
        
        if source and target:
            return str(source)
            response_data.append(f"{source['display_name']}:{target['display_name']}")
            break
        else:
            return Response({'error':'source or target not found'})


    # Build the response line
    if response_data:
        response_line = "return Response({ " + ", ".join(response_data) + " })"
    else:
        response_line = "return Response({'default':'this is default output'})"

    output_lines.append(response_line)

    result.append(add_tabs(output_lines,1))
    result = flatten_list(result)
    function_content = "\n".join(result)
    return function_content


def write_to_file(app_name, file_name, file_content):
    app_directory = os.path.join(settings.BASE_DIR, app_name, "generated_apis")

    if not os.path.exists(app_directory):
        os.makedirs(app_directory)

    file_path = os.path.join(app_directory, file_name)

    with open(file_path, "w") as f:
        f.write(file_content)

    return file_path


@api_view(["POST"])
def api_generator(request):
    try:
        file_name = request.data.get("file", "generated_api") + ".py"
        elements = request.data.get("elements")
        edges = request.data.get("edges")
        type = request.data.get("type")

        if not elements:
            return Response(
                {"error": "Elements not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # if not edges:
        #     return Response(
        #         {"error": "Nodes not found"}, status=status.HTTP_400_BAD_REQUEST
        #     )

        if not type:
            return Response(
                {"error": "Type not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        function_content = generate_function_content(elements, edges, request.data.get('filename'), type)
        # function_content = str(elements)
        app_name = "api"  # Replace with your app's name
        file_path = write_to_file(app_name, file_name, function_content)

        return Response(
            {
                "message": f"API file '{file_name}' created successfully in '{file_path}'!"
            }
        )

    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

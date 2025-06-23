"""
This tool is used to install libraries.
"""


def install_libraries(library_name: str):
    """
    Install a library with a specific version.
    """
    print(f"Installing {library_name}")
    return f"successfully installed {library_name}"


def get_install_libraries_tool() -> dict[str, any]:
    """
    Get the install libraries tool.
    """
    return {
        "type": "function",
        "function": {
            "name": "install_libraries",
            "description": "Install a library with a specific version.",
            "parameters": {
                "type": "object",
                "properties": {
                    "library_name": {
                        "type": "string",
                        "description": "The name of the library to install.",
                    }
                },
                "required": ["library_name"],
            },
        },
    }

# Maya_PBRTXT_Import

## Overview
`Maya_PBRTXT_Import` is a Python script for Autodesk Maya developed with the assistance of Chat GPT. It facilitates the import and automatic setup of PBR (Physically-Based Rendering) textures into Maya, aiming to streamline the shader creation process. This script automates the tedious process of manually connecting texture files to the appropriate shader attributes, making it a handy tool for quick setups in PBR workflows.

**Note**: This script is not fully developed and should be considered a prototype intended for temporary use. It was developed to demonstrate the capabilities and assist in automating certain tasks within Maya but is not intended for production use without further development and testing.


## Features
- **File Selection UI**: Allows users to interactively select PBR texture files from Maya's `sourceimages` directory via a user-friendly graphical interface.
- **Automatic Shader Creation**: Automatically creates an `aiStandardSurface` shader and connects the imported texture files to their respective shader attributes based on the PBR workflow.
- **Support for Various Texture Types**: Handles various types of textures such as albedo, normal, roughness, metallic, and others, including support for displacement and vector displacement maps.
- **UDIM Support**: The script detects and supports UDIM-tagged textures to accommodate multiple UV tiles.
- **Color Space Management**: Automatically sets the correct color space for different types of textures to ensure the materials render accurately.

## Installation
1. Download the `Maya_PBRTXT_Import.py` file.
2. Move the script into your Maya scripts directory.

## Usage
1. In Maya's Script Editor, click on the `Source Script` button, navigate to the saved script, select it, and open it. This action will load the script and automatically display the "Create PBR Shader Network" dialog.
2. Use the "PBR filename" button to browse and select the PBR texture file you want to import.
3. Click "Create PBR Shader Network" to automatically create and connect the shaders.

## Requirements
- Autodesk Maya (The script has been tested on Maya 2024 but should be compatible with other versions that support Python scripting and Arnold renderer.)
- Arnold Renderer must be set as the current renderer in Maya.

## License
This project is available under the MIT License. See the LICENSE file for more info.

## Contributing
Contributions to `Maya_PBRTXT_Import` are welcome! Feel free to fork the repository and submit pull requests.

## Support
If you encounter any problems or have any suggestions, please open an issue on the GitHub repository page.

---

We hope this tool makes your PBR texturing workflow in Maya easier and more efficient!

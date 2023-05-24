Title: Jupyter Notebook to Jekyll-Compatible Markdown Converter

Description: This script converts a Jupyter Notebook file to a Jekyll-compatible Markdown file, embedding images found in the original .ipynb file.

Usage:

1. Import required libraries:
   - os, shutil, argparse, and re.

2. Create the `ConvertorMarkDown4Jekyll` class. During initialization, the following instance variables are set:
   - file: Jupyter Notebook file to be converted.
   - file_md: Name of the converted Markdown file.
   - file_md_with_image: Name of the converted Markdown file containing embedded images.
   - file_html: Name of the intermediate HTML file during conversion.
   - image_data: A list to store image data from the original file.
   - layout, title, categories, tags: Metadata for the Jekyll Markdown file.

3. Define class methods:
   - nbconvertHTML(): Convert the Notebook file to an HTML file using `jupyter nbconvert`.
   - nbconvertMarkdown(): Convert the Notebook file to a Markdown file using `jupyter nbconvert`.
   - removeFiles(): Remove additional files created during conversion (e.g., image folders).
   - imageDataFromHtml(): Extract image data from the intermediate HTML file.
   - embeddingImageToMarkdown(): Embed images from the original file into the converted Markdown file.
   - embeddingImageToMarkdown_re(): Same as above, but utilizes regular expressions.
   - removeHTML(): Remove the intermediate HTML file.
   - removeMarkdown(): Remove the original Markdown file (without embedded images).
   - run(): Executes all necessary methods in the correct order.

4. Define main() function:
   - Use argparse to parse command line arguments for the file to be converted and the Jekyll metadata (layout, title, categories, and tags).
   - Create an instance of the `ConvertorMarkDown4Jekyll` class with the specified file.
   - Set the corresponding metadata parameters for the instance.
   - Run the conversion using the run() method.

Example:

Place the script in the desired directory and call the script with the appropriate command line arguments. 

```bash
python convert_ipynb_to_jekyll_md.py -f my_jupyter_notebook.ipynb -l post -t "My Jupyter Notebook Post" -c "Category1 Category2" -g "Tag1 Tag2"
```

This command will convert the `my_jupyter_notebook.ipynb` file to a Jekyll-compatible Markdown file with the layout set as `post`, title set as `My Jupyter Notebook Post`, categories set as `Category1` and `Category2`, and tags set as `Tag1` and `Tag2`. The resulting Markdown file will contain embedded images from the original Jupyter Notebook.

import os
import shutil
import argparse
import re

class ConvertorMarkDown4Jekyll:
    def __init__(self, file):
        self.file = file
        self.file_md = ""
        self.file_md_with_image = ""
        self.file_html = ""
        self.image_data = []
        
        self.layout = "single"
        self.title = ""
        self.categories = ""
        self.tags = []

    def nbconvertHTML(self):
        os.system("jupyter nbconvert --to html " + self.file)
        self.file_html = os.path.splitext(self.file)[0] + ".html"
    
    def nbconvertMarkdown(self):
        os.system("jupyter nbconvert --to markdown " + self.file)
        self.file_md = os.path.splitext(self.file)[0] + ".md"
        self.file_md_with_image = os.path.splitext(self.file)[0] + "_with_image.md"
    
    def removeFiles(self):
        dir_files = os.path.splitext(self.file)[0] + "_files"
        if os.path.isdir(dir_files):
            shutil.rmtree(dir_files)
    
    def imageDataFromHtml(self):
        with open(self.file_html, 'r', encoding='utf-8', errors='ignore') as f:
            line = None
            while line != '':
                line = f.readline()
                if "data:image/png;base64" in line and "background: url" not in line:
                    self.image_data.append(line)        
        return self.image_data
    
    def embeddingImageToMarkdown(self):
        with open(self.file_md, 'r', encoding='utf-8', errors='ignore') as f:
            line = None
            with open(self.file_md_with_image, 'w', encoding='utf-8', errors='ignore') as f2:
                post_info = f"---\nlayout: {self.layout}\ntitle : {self.title}\ncategories: {self.categories}\n"
                f2.write(post_info)
                
                post_tags = f"tags: {self.tags}\n---\n\n\n".replace("'", "")
                f2.write(post_tags)
                
                while line != '':
                    line = f.readline()
                    if len(self.image_data) == 0:
                        f2.write(line)
                    elif "![png]" in line:
                        line = "<p>"+ self.image_data.pop(0)+' alt="image.png"></p>'
                        f2.write(line)
                    elif "![image.png]" in line:
                        line = self.image_data.pop(0)
                        f2.write(line)
                    else:
                        f2.write(line)
                        
    def embeddingImageToMarkdown_re(self):
        with open(self.file_md, 'r', encoding='utf-8', errors='ignore') as f:
            line = None
            bracket = False
            with open(self.file_md_with_image, 'w', encoding='utf-8', errors='ignore') as f2:
                post_info = f"---\nlayout: {self.layout}\ntitle : {self.title}\ncategories: {self.categories}\n"
                f2.write(post_info)
                
                post_tags = f"tags: {self.tags}\n---\n\n\n".replace("'", "")
                f2.write(post_tags)
                
                while line != '':
                    line = f.readline()
                    
                    if re.match(r'^(```)(.*)$', line):
                        bracket = not bracket
                    
                    if len(self.image_data) == 0:
                        f2.write(line)
                    elif re.match(r'^!\[(.*)\]\((.*)\)$', line):
                        line = self.image_data.pop(0)
                        if not re.match(r'^(.*)<\/p>$', line):
                            line = "<p>" + line[:-1] + ' alt="image.png"></p>'
                            f2.write(line)                            
                        else:
                            f2.write(line)
                                                        
                    elif re.match(r'^(#+) (.*)$', line):
                        if bracket:
                            pass
                        else:
                            count_hash = len(line.split(' ')[0])
                            for _ in range(7-count_hash):
                                f2.write('<br>')
                            f2.write('\n\n')
                            f2.write(line)                            
                    else:
                        f2.write(line)
                           
    def removeHTML(self):
        if os.path.exists(self.file_html):
            os.remove(self.file_html)
            
    def removeMarkdown(self):
        if os.path.exists(self.file_md):
            os.remove(self.file_md)
            
    def run(self):
        self.nbconvertHTML()
        self.nbconvertMarkdown()
        self.removeFiles()
        self.imageDataFromHtml()        
        # self.embeddingImageToMarkdown()
        self.embeddingImageToMarkdown_re()
        self.removeHTML()
        self.removeMarkdown()
        
    def main():
        parser = argparse.ArgumentParser(description='Convert a Jupyter Notebook to a Jekyll-compatible Markdown file.')
        parser.add_argument('file', help='The Jupyter Notebook file that needs to be converted.')
        parser.add_argument('-l', '--layout', default='single', help='The layout for the Jekyll Markdown file.')
        parser.add_argument('-t','--title', required=True, help='The title for the Jekyll Markdown file.')
        parser.add_argument('-c','--categories', required=True, help='The categories for the Jekyll Markdown file.')
        parser.add_argument('-g','--tags', required=True, help='The tags for the Jekyll Markdown file.')
        
        args = parser.parse_args()
        
        converter = ConvertorMarkDown4Jekyll(args.file)
        converter.layout = args.layout
        converter.title = args.title
        converter.categories = args.categories
        converter.tags = args.tags.split(',')
        converter.run()
        
if __name__ == "__main__":
    ConvertorMarkDown4Jekyll.main()
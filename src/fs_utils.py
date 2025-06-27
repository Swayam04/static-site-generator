from pathlib import Path
import shutil
import os
from md_to_html import markdown_to_html_node
from md_parser import extract_title
    

def generate_pages(dir_path_content : str, template_path : str, dest_dir_path : str, basepath : str) -> None:
    md_file_dir = Path(dir_path_content)
    template_html_file_path = Path(template_path)
    generated_html_dir_path = Path(dest_dir_path)
    
    validate_paths(md_file_dir, template_html_file_path)
    print(f"Generating pages from {md_file_dir} to {generated_html_dir_path} using {template_path}")
    generate_pages_recursive(md_file_dir, template_html_file_path, generated_html_dir_path, basepath)
    
    
def generate_pages_recursive(md_path : Path, template_path : Path, dest_path : Path, basepath : str) -> None:
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {dest_path}: {e}")
        
        template_html = template_path.read_text()
        html_ext = ".html"
            
        for item in md_path.iterdir():
            dest_item = dest_path / item.name
            
            if item.is_dir():
                generate_pages_recursive(item, template_path, dest_item, basepath)
            elif item.is_file():
                if item.suffix != ".md":
                    continue
                md_content = item.read_text()
                html_content = markdown_to_html_node(md_content).to_html()
                title = extract_title(md_content)
                
                final_html = (
                    template_html
                    .replace("{{ Title }}", title)
                    .replace("{{ Content }}", html_content)
                    .replace('href="/', f'href="{basepath}') 
                    .replace('src="/', f'src="{basepath}')
                )
                dest_item = dest_item.with_suffix(html_ext)
                dest_item.write_text(final_html)
        

def validate_paths(md_file : Path, template_html_file : Path) -> None:
    if not md_file.is_dir():
        raise Exception(f"{md_file} is not a valid directory")

    if not template_html_file.is_file() or template_html_file.suffix.lower() != '.html':
        raise Exception(f"{template_html_file} is not a valid HTML file path")


def copy_to_destination(source_path : str, destination_path : str) -> None:
    source_dir = Path(source_path)
    destination_dir = Path(destination_path)
    
    validate_directory_paths(source_dir, destination_dir)
    clear_directory(destination_dir)
    copy_directory_contents(source_dir, destination_dir)
    

def copy_directory_contents(source_dir : Path, destination_dir : Path) -> None:
    print(f"--- Starting copy from '{source_dir}' to '{destination_dir}' ---")
    
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        print(f"Directory processed: {source_dir} -> {destination_dir}")
    except OSError as e:
        print(f"Error creating directory {destination_dir}: {e}")
        return
    
    for item in source_dir.iterdir():
        dest_item = destination_dir / item.name
        
        if item.is_dir():
            copy_directory_contents(item, dest_item)
        elif item.is_file():
            try:
                shutil.copy2(item, dest_item)
                print(f"  Copied file: {item} -> {dest_item}")
            except OSError as e:
                print(f"  Error copying file to {dest_item}: {e}")



def validate_directory_paths(source_path : Path, destination_path : Path) -> None:
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source path is not a valid directory: {source_path}")

    if destination_path.exists() and not destination_path.is_dir():
        raise NotADirectoryError(f"Destination path exists but is not a directory: {destination_path}")
        
    

def clear_directory(dir_path : Path) -> None:
    print(f"--- Starting clearing contents of '{dir_path}' ---")
    
    for current_path, dir_names, file_names in os.walk(dir_path, topdown=False):
        
        for file_name in file_names:
            file_path = Path(current_path, file_name)
            try:
                file_path.unlink()
                print(f"Deleted File: {file_path}")
            except OSError as e:
                print(f"Error deleting file: {file_path} - {e}")
        
        for dir_name in dir_names:
            nested_dir_path = Path(current_path, dir_name)
            try:
                nested_dir_path.rmdir()
                print(f"Deleted directory: {nested_dir_path}")
            except OSError as e:
                print(f"Error deleting directory: {nested_dir_path} - {e}")
        
    print(f"--- Cleared all contents of '{dir_path}' ---")            
        
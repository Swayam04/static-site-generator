from pathlib import Path
import shutil
import os

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
        
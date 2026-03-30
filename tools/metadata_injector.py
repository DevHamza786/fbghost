import os
import subprocess
import random
import hashlib
import string

def strip_metadata(input_file, output_file):
    """Strips all original metadata from the MP4 file."""
    cmd = [
        'ffmpeg', '-i', input_file,
        '-map_metadata', '-1',
        '-c:v', 'copy', '-c:a', 'copy',
        output_file, '-y'
    ]
    subprocess.run(cmd, check=True)

def inject_fingerprint(file_path):
    """Injects a unique byte at the end of the file to change MD5 and act as a digital fingerprint."""
    with open(file_path, 'ab') as f:
        # Append a random string of 16-32 bytes at the end
        unique_bytes = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(16, 32))).encode()
        f.write(b'\x00' + unique_bytes) # Add a null byte to signal end of standard atoms

def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def set_iphone_properties(input_file, output_file):
    """
    Sets file properties to mimic iPhone 15 Pro Max.
    In a real scenario, we'd use -metadata for specific tags like orientation, model, etc.
    """
    # Common iPhone 15 Pro Max metadata tags (mimicry)
    tags = {
        "com.apple.quicktime.make": "Apple",
        "com.apple.quicktime.model": "iPhone 15 Pro Max",
        "com.apple.quicktime.software": "17.4.1",
        "com.apple.quicktime.creationdate": "2024-03-30T10:15:33-0500",
        "location": "+40.7128-074.0060/", # US Coordinates (NYC)
    }
    
    metadata_args = []
    for k, v in tags.items():
        metadata_args.extend(['-metadata', f'{k}={v}'])
        
    cmd = [
        'ffmpeg', '-i', input_file,
        *metadata_args,
        '-c', 'copy',
        output_file, '-y'
    ]
    subprocess.run(cmd, check=True)

def process_video(input_path, output_directory):
    """Main function to perform all integrity operations."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]
    
    # Step 1: Strip existing metadata
    stripped_path = os.path.join(output_directory, f"{base_name}_stripped.mp4")
    strip_metadata(input_path, stripped_path)
    
    # Step 2: Set iPhone mimicry properties
    mimic_path = os.path.join(output_directory, f"{base_name}_mimic.mp4")
    set_iphone_properties(stripped_path, mimic_path)
    
    # Step 3: Inject Fingerprint (change MD5)
    inject_fingerprint(mimic_path)
    
    # Cleanup intermediate
    if os.path.exists(stripped_path):
        os.remove(stripped_path)
        
    # Return path and hash
    final_path = os.path.join(output_directory, f"{base_name}_clean.mp4")
    os.rename(mimic_path, final_path)
    
    final_hash = get_md5(final_path)
    return final_path, final_hash

if __name__ == "__main__":
    # Test stub (requires an input.mp4 in the same dir)
    import sys
    if len(sys.argv) > 1:
        p, h = process_video(sys.argv[1], "processed_assets")
        print(f"Processed: {p}\nMD5: {h}")
    else:
        print("Usage: python metadata_injector.py [input_file.mp4]")

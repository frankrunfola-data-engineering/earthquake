def validate_path( path):
    if not path or not isinstance(path, str):
        raise ValueError("Path \"{path}\" must be a non-empty string path.")
import os

def get_files_info(working_directory, directory=None):
    try:
        target_directory = directory or "."

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(os.path.join(working_directory, target_directory))

        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'

        entries = os.listdir(abs_target_dir)
        info_lines = []

        for entry in entries:
            entry_path = os.path.join(abs_target_dir, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                size = os.path.getsize(entry_path)
            except Exception as e:
                return f"Error: Could not get size for '{entry}': {e}"
            info_lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(info_lines)

    except Exception as e:
        return f"Error: {e}"

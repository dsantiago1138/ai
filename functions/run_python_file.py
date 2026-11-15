import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]

        if args:
            command.extend(args)
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_string = ''

        if result.returncode != 0:
            output_string += f'Process exited with code {result.returncode}\n'
        
        if not result.stdout and not result.stderr:
            output_string += f'No output produced'
        else:
            if result.stdout:
                output_string += f'STDOUT: {result.stdout}\n'
            if result.stderr:
                output_string += f'STDERR: {result.stderr}'

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
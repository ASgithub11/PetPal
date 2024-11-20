import concurrent.futures
import subprocess

# Function to run a Python script
def run_script(script):
    subprocess.run(['python', script])

if __name__ == "__main__":
    scripts = ['app.py', 'authentication.py', 'config.py', 'models.py', 'schemaadoption.py', 'schemafavorite.py', 'schemapet.py', 'schemauser.py', 'seed_pets.py', 'validation.py']  # List of Python scripts

    # ThreadPoolExecutor to run the scripts concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")


def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n🚀 Running {script_name}...\n")
    subprocess.run(["python", script_path])


def main():
    run_script("extractor.py")        # Generate v1 memos
    run_script("agent_generator.py")  # Generate v1 agent specs
    run_script("patch_engine.py")     # Generate v2 memos
    run_script("agent_generator.py")  # Generate v2 agent specs

    print("\n🎉 FULL PIPELINE EXECUTED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
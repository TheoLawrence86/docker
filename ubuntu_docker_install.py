import subprocess
import sys

def run_command(command, error_message="An error occurred"):
    """ Run shell commands with error handling """
    try:
        result = subprocess.run(command, check=True, shell=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e.stderr}")
        sys.exit(1)

def install_packages():
    print("Installing necessary packages...")
    run_command("sudo apt install apt-transport-https ca-certificates curl software-properties-common -y",
                "Failed to install prerequisites")

def setup_docker_repository():
    print("Adding Docker's official GPG key and setting up the repository...")
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
                "Failed to add GPG key")
    run_command(
        "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
        "Failed to add Docker repository")

def install_docker():
    print("Installing Docker Engine...")
    run_command("sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io -y",
                "Failed to install Docker")

def install_docker_compose(version="1.29.2"):
    print("Installing Docker Compose...")
    run_command(f"sudo curl -L \"https://github.com/docker/compose/releases/download/{version}/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
                "Failed to download Docker Compose")
    run_command("sudo chmod +x /usr/local/bin/docker-compose",
                "Failed to set Docker Compose permissions")

def configure_user():
    print("Adding user to the Docker group...")
    run_command("sudo usermod -aG docker ${USER}",
                "Failed to add user to Docker group")
    print("Please log out and log back in for this to take effect.")

def main():
    print("Updating and preparing the system...")
    run_command("sudo apt update && sudo apt upgrade -y",
                "System update failed")
    install_packages()
    setup_docker_repository()
    install_docker()
    install_docker_compose()
    configure_user()
    print("Docker has been installed and configured successfully!")

if __name__ == "__main__":
    main()

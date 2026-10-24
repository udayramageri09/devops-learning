from pathlib import Path
import docker

IMAGE = "devops-ex05-apparmor:lab"
PROFILE = "devops-lab-profile"


def main():
    client = docker.from_env()
    client.ping()

    options = client.info().get("SecurityOptions", [])
    supported = any("name=apparmor" in str(x) for x in options)
    print("Docker security options:", options)
    print("Docker AppArmor support:", supported)

    folder = Path(__file__).resolve().parent
    print("Building Exercise 05 image...")
    client.images.build(path=str(folder), tag=IMAGE, rm=True)

    if not supported:
        print("SKIPPED: Custom AppArmor attachment is unavailable.")
        print("Running an ordinary Docker SDK container check instead.")

    container = None
    try:
        kwargs = {
            "image": IMAGE,
            "command": ["python", "-c", "print('Docker SDK check passed')"],
            "detach": True,
            "network_disabled": True,
        }

        if supported:
            kwargs["security_opt"] = [f"apparmor={PROFILE}"]

        container = client.containers.create(**kwargs)
        details = client.api.inspect_container(container.id)
        configured = details["HostConfig"].get("SecurityOpt") or []
        print("Configured security options:", configured)

        if supported and f"apparmor={PROFILE}" not in configured:
            raise RuntimeError("AppArmor profile request missing")

        container.start()
        result = container.wait(timeout=30)
        print("Container exit code:", result["StatusCode"])
        print("Container output:", container.logs().decode().strip())

        if result["StatusCode"] != 0:
            raise RuntimeError("Docker SDK container check failed")

        if supported:
            print("Profile requested; enforcement requires separate testing.")
        else:
            print("PASS: Docker SDK baseline test.")
            print("NOT VERIFIED: Custom AppArmor enforcement.")

    finally:
        if container is not None:
            container.remove(force=True)
            print("Temporary Exercise 05 container removed.")


if __name__ == "__main__":
    main()

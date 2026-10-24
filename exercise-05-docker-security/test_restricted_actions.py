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

    if not supported:
        print("NOTICE: Running baseline tests without AppArmor.")
        print("NOTICE: These results do not demonstrate enforcement.")

    container = None
    try:
        kwargs = {
            "image": IMAGE,
            "detach": True,
            "network_disabled": True,
        }

        if supported:
            kwargs["security_opt"] = [f"apparmor={PROFILE}"]

        container = client.containers.run(**kwargs)
        print("Temporary container:", container.short_id)

        details = client.api.inspect_container(container.id)
        configured = details["HostConfig"].get("SecurityOpt") or []
        print("Configured security options:", configured)

        if supported and f"apparmor={PROFILE}" not in configured:
            raise RuntimeError("AppArmor profile request missing")

        tests = [
            ("Read /etc/passwd", ["cat", "/etc/passwd"]),
            ("Execute /bin/bash", ["/bin/bash", "-c", "echo BASH_EXECUTED"]),
        ]

        for description, command in tests:
            result = container.exec_run(command)
            output = result.output.decode(errors="replace").strip()

            print(f"\n=== {description} ===")
            print("Command:", command)
            print("Exit code:", result.exit_code)
            print("Output:", output[:300] if output else "<empty>")

            if supported:
                if result.exit_code != 0:
                    print("Command failed; investigate whether AppArmor caused it.")
                else:
                    print("Command succeeded; no restriction demonstrated.")
            else:
                print("BASELINE ONLY: AppArmor enforcement not tested.")

        print("\nRestricted-action test execution completed.")

    finally:
        if container is not None:
            container.remove(force=True)
            print("Temporary Exercise 05 container removed.")


if __name__ == "__main__":
    main()

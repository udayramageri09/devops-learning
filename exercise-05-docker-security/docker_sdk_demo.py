
import docker

client = docker.from_env()

print("Docker server version:", client.version()["Version"])

print("\nExisting containers:")
for existing in client.containers.list(all=True):
    print(existing.name, "-", existing.status)

print("\nCreating a temporary security lab container...")

container = None

try:
    container = client.containers.run(
        "alpine:3.20",
        command=["sh", "-c", "echo Docker SDK container executed successfully"],
        detach=True,
        remove=False,
    )

    result = container.wait()

    print("Exit code:", result["StatusCode"])
    print("Container output:", container.logs().decode().strip())

    if result["StatusCode"] != 0:
        raise RuntimeError("Container command failed")

finally:
    if container is not None:
        container.remove(force=True)
        print("Temporary container removed successfully.")

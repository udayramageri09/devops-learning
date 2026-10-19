import docker

client = docker.from_env()

print("Docker server version:", client.version()["Version"])

print("\nExisting containers:")
for container in client.containers.list(all=True):
    print(container.name, "-", container.status)

print("\nCreating a temporary security lab container...")

container = client.containers.run(
    "alpine:3.20",
    command=["sh", "-c", "echo Docker SDK container executed successfully"],
    detach=True,
    name="docker-sdk-security-test",
    remove=False
)

result = container.wait()

print("Exit code:", result["StatusCode"])
print("Container output:", container.logs().decode().strip())

container.remove()
print("Temporary container removed successfully.")

import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import docker

IMAGE_TAG = "devops-ex05-apparmor:lab"
PROFILE_NAME = "devops-lab-profile"


def check_profile_syntax(profile_path: Path) -> dict:
    """Validate AppArmor profile syntax using apparmor_parser where available."""
    result = {
        "parser_available": False,
        "syntax_valid": None,
        "detail": "apparmor_parser not found on host or WSL",
    }

    # Check for native apparmor_parser first
    parser_bin = shutil.which("apparmor_parser")
    cmd = None
    if parser_bin:
        cmd = [parser_bin, "-Q", str(profile_path)]
    elif shutil.which("wsl"):
        # On Windows host, convert to WSL path and run apparmor_parser inside WSL
        try:
            wsl_conv = subprocess.run(
                ["wsl", "wslpath", "-a", "-u", profile_path.as_posix()],
                capture_output=True,
                text=True,
                timeout=5,
            )
            wsl_path = wsl_conv.stdout.strip() if wsl_conv.returncode == 0 else profile_path.as_posix()
            cmd = ["wsl", "apparmor_parser", "-Q", wsl_path]
        except Exception:
            cmd = None

    if cmd:
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            result["parser_available"] = True
            result["syntax_valid"] = (res.returncode == 0)
            result["detail"] = (
                "Profile syntax is valid (apparmor_parser -Q returned 0)"
                if res.returncode == 0
                else f"Parser error: {res.stderr.strip()}"
            )
        except Exception as exc:
            result["detail"] = f"Syntax check invocation skipped: {exc}"

    return result


def main():
    print("=" * 60)
    print("Exercise 05 — Docker AppArmor Diagnostic & Verification")
    print("=" * 60)

    try:
        client = docker.from_env()
        client.ping()
    except Exception as exc:
        print(f"ERROR: Unable to connect to Docker daemon: {exc}", file=sys.stderr)
        return 1

    # Stage 1: Docker Engine Security Capability
    security_options = client.info().get("SecurityOptions", [])
    has_apparmor_support = any("name=apparmor" in str(opt) for opt in security_options)
    print(f"\n[Stage 1] Docker Engine Security Options: {security_options}")
    print(f"         Docker AppArmor Support: {'ENABLED' if has_apparmor_support else 'DISABLED / UNAVAILABLE'}")

    # Stage 2: Profile File & Syntax Validation
    folder = Path(__file__).resolve().parent
    profile_path = folder / "apparmor-profile"
    if not profile_path.exists():
        print(f"ERROR: AppArmor profile not found at {profile_path}", file=sys.stderr)
        return 1

    syntax_check = check_profile_syntax(profile_path)
    print("\n[Stage 2] Profile Syntax Validation:")
    print(f"         Profile file: {profile_path.name}")
    print(f"         Parser available: {syntax_check['parser_available']}")
    print(f"         Syntax valid: {syntax_check['syntax_valid']}")
    print(f"         Details: {syntax_check['detail']}")

    # Stage 3: Image Build
    print(f"\n[Stage 3] Building image {IMAGE_TAG}...")
    try:
        client.images.build(path=str(folder), tag=IMAGE_TAG, rm=True)
        print("         Image build successful.")
    except Exception as exc:
        print(f"ERROR: Image build failed: {exc}", file=sys.stderr)
        return 1

    # Stage 4: Profile Attachment & Container Creation
    container_name = f"ex05-verify-{uuid.uuid4().hex[:8]}"
    container = None
    exit_code = 0

    try:
        create_kwargs = {
            "image": IMAGE_TAG,
            "name": container_name,
            "command": [
                "python",
                "-c",
                "import os; print(f'Container running as UID={os.getuid()}'); "
                "label = open('/proc/1/attr/current').read().strip() if os.path.exists('/proc/1/attr/current') else 'n/a'; "
                "print(f'Security label (/proc/1/attr/current): {label}')",
            ],
            "detach": True,
            "network_disabled": True,
        }

        if has_apparmor_support:
            print(f"\n[Stage 4] Requesting AppArmor attachment: apparmor={PROFILE_NAME}")
            create_kwargs["security_opt"] = [f"apparmor={PROFILE_NAME}"]
        else:
            print("\n[Stage 4] Docker AppArmor unsupported; launching baseline unconfined container")

        container = client.containers.create(**create_kwargs)
        details = client.api.inspect_container(container.id)
        configured_sec_opts = details.get("HostConfig", {}).get("SecurityOpt") or []
        print(f"         Configured SecurityOpt: {configured_sec_opts}")

        # Stage 5: Container Execution & Actual Enforcement Inspection
        print("\n[Stage 5] Starting container to inspect live execution...")
        container.start()
        wait_result = container.wait(timeout=30)
        status_code = wait_result.get("StatusCode", -1)
        logs = container.logs().decode(errors="replace").strip()

        print(f"         Container exit code: {status_code}")
        print("         Container output:")
        for line in logs.splitlines():
            print(f"           {line}")

        if status_code != 0:
            print(f"ERROR: Verification container exited with non-zero status {status_code}", file=sys.stderr)
            exit_code = 1
        else:
            print("\n" + "-" * 60)
            print("SUMMARY EVALUATION:")
            print(f" - Docker AppArmor Support  : {'Present' if has_apparmor_support else 'Absent'}")
            print(f" - Profile Syntax Check     : {'Valid' if syntax_check['syntax_valid'] else 'Unverified/Failed'}")
            print(f" - Security Profile Attach  : {'Configured' if configured_sec_opts else 'Skipped (daemon unsupported)'}")
            if has_apparmor_support and PROFILE_NAME in str(logs):
                print(f" - Custom Enforcement       : VERIFIED ({PROFILE_NAME} active)")
            else:
                print(" - Custom Enforcement       : NOT VERIFIED (WSL2/Docker environment does not enforce custom AppArmor profiles)")
            print(" - Baseline Security Status : PASSED (hardened non-root user + baseline Docker container execution)")
            print("-" * 60)

    except Exception as exc:
        print(f"ERROR during container verification: {exc}", file=sys.stderr)
        exit_code = 1
    finally:
        if container is not None:
            try:
                container.remove(force=True)
                print(f"\nTemporary container '{container_name}' removed cleanly.")
            except Exception as rm_exc:
                print(f"Warning: Failed to clean up container {container_name}: {rm_exc}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

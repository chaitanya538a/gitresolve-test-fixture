import shutil
import tempfile
import traceback
from pathlib import Path

from sandbox import runner
from sandbox.models import ExecutionRequest

req = ExecutionRequest(
    execution_id="diag-1",
    repo_url="https://github.com/chaitanya538a/gitresolve-test-fixture",
    commit_sha="5983b2084d3cf2fc8a4d9d5522d595ed78a1ccea",
    command=["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"],
)

ws = Path(tempfile.mkdtemp(prefix="diag_"))
try:
    repo = runner._checkout(req, ws, False)
    print("checkout ok:", repo)
    result = runner._run(runner._docker_run_args("gitresolve-diag", repo, req.command), 30)
    print("docker run:", result.returncode, result.stdout.strip(), result.stderr.strip())
except BaseException:
    traceback.print_exc()
finally:
    runner._run(["docker", "rm", "-f", "gitresolve-diag"], 30)
    shutil.rmtree(ws, onexc=runner._force_remove)

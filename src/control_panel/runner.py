from dataclasses import dataclass
import subprocess
import threading


@dataclass(frozen=True)
class ProcessResult:
    return_code: int


class CommandRunner:
    def __init__(self, project_root, emit, finished):
        self.project_root = project_root
        self.emit = emit
        self.finished = finished
        self._thread = None

    @property
    def running(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self, command):
        if self.running:
            raise RuntimeError("Ya hay un proceso en ejecución.")
        self._thread = threading.Thread(
            target=self._run,
            args=(tuple(command),),
            daemon=True,
        )
        self._thread.start()

    def _run(self, command):
        try:
            process = subprocess.Popen(
                command,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            for line in process.stdout:
                self.emit(line)
            return_code = process.wait()
        except Exception as error:
            self.emit(f"ERROR iniciando proceso: {error}\n")
            return_code = 1
        self.finished(ProcessResult(return_code=return_code))


from datetime import datetime
from queue import Empty, Queue
import sys
import tkinter as tk
from tkinter import messagebox

from src.control_panel.actions import PROJECT_ROOT, build_actions
from src.control_panel.runner import CommandRunner
from src.control_panel.theme import (
    BLACK,
    BACKGROUND_ALPHA,
    CONSOLE_BG,
    CONSOLE_ERROR,
    CONSOLE_SUCCESS,
    CONSOLE_WARNING,
    DISABLED_BG,
    PANEL_BG,
    TITLE_FONT,
    TITLE_LETTER_COLORS,
    UI_FONT,
    WINDOW_ALPHA,
    WINDOW_TRANSPARENT_COLOR,
    WINDOW_TOPMOST,
    WHITE,
    register_private_fonts,
    lighten_hex,
)
from src.control_panel.workflow import WorkflowState


class ControlPanelApp:
    def __init__(self, root, backdrop=None):
        self.root = root
        self.backdrop = backdrop
        self.actions = build_actions()
        self.workflow = WorkflowState(len(self.actions))
        self.root.title("Yu-Gi-Oh DB · Panel operativo")
        self.root.geometry("980x720")
        self.root.minsize(820, 620)
        self.root.configure(bg=PANEL_BG)
        self.root.attributes("-alpha", WINDOW_ALPHA)
        self.root.attributes("-topmost", WINDOW_TOPMOST)
        if sys.platform == "win32":
            self.root.attributes("-transparentcolor", WINDOW_TRANSPARENT_COLOR)
        self.events = Queue()
        self.buttons = []
        self.active_action = None
        self.active_index = None
        self.status = tk.StringVar(value="Paso 1 preparado")
        self.runner = CommandRunner(
            PROJECT_ROOT, self._queue_output, self._queue_finished
        )
        self._build_ui()
        self._apply_workflow_state()
        if self.backdrop is not None:
            self.root.bind("<Configure>", self._sync_backdrop)
            self.root.protocol("WM_DELETE_WINDOW", self._close_windows)
            self.root.after_idle(self._sync_backdrop)
        self.root.after(100, self._drain_events)

    def _build_ui(self):
        container = tk.Frame(self.root, bg=PANEL_BG, padx=22, pady=18)
        container.pack(fill="both", expand=True)

        title_frame = tk.Frame(container, bg=PANEL_BG)
        title_frame.pack(anchor="w")
        tk.Label(
            title_frame,
            text="Panel operativo ",
            bg=PANEL_BG,
            fg=WHITE,
            font=(TITLE_FONT, 22, "bold"),
        ).pack(side="left")
        for index, character in enumerate("MySQL + ETL"):
            tk.Label(
                title_frame,
                text=character,
                bg=PANEL_BG,
                fg=TITLE_LETTER_COLORS[index % len(TITLE_LETTER_COLORS)],
                font=(TITLE_FONT, 22, "bold"),
            ).pack(side="left")
        tk.Label(
            container,
            text="Un ciclo guiado: schema → validación → snapshots → backup → tests.",
            bg=PANEL_BG,
            fg=WHITE,
            font=(UI_FONT, 11),
        ).pack(anchor="w", pady=(2, 14))

        actions_frame = tk.Frame(container, bg=PANEL_BG)
        actions_frame.pack(fill="x")
        actions_frame.columnconfigure((0, 1), weight=1)

        for index, action in enumerate(self.actions):
            card = tk.Frame(actions_frame, bg=PANEL_BG, padx=7, pady=7)
            card.grid(row=index // 2, column=index % 2, sticky="nsew", padx=5, pady=5)
            if action.primary:
                tk.Label(
                    card,
                    text="Si no reset db -> Pulsar. ",
                    bg=PANEL_BG,
                    fg=action.color,
                    font=(UI_FONT, 9, "bold"),
                ).pack(anchor="w", pady=(0, 4))
            button = tk.Button(
                card,
                text=action.label,
                bg=action.color,
                fg=WHITE,
                activebackground=action.color,
                activeforeground=WHITE,
                disabledforeground="#ded9d5",
                font=(
                    TITLE_FONT if action.primary else UI_FONT,
                    13 if action.primary else 11,
                    "bold",
                ),
                relief="solid",
                bd=1,
                highlightbackground=BLACK,
                highlightcolor=BLACK,
                cursor="hand2",
                command=lambda selected=action, selected_index=index: self._run_action(
                    selected_index, selected
                ),
            )
            button.pack(fill="x", ipady=13 if action.primary else 8)
            button.bind(
                "<Enter>",
                lambda _event, selected=button, selected_index=index: self._on_button_enter(selected, selected_index),
            )
            button.bind(
                "<Leave>",
                lambda _event, selected=button, selected_index=index: self._on_button_leave(selected, selected_index),
            )
            tk.Label(
                card,
                text=action.description,
                bg=PANEL_BG,
                fg=WHITE,
                font=(UI_FONT, 9),
                wraplength=410,
                justify="left",
            ).pack(anchor="w", pady=(5, 0))
            self.buttons.append(button)

        status_frame = tk.Frame(container, bg=PANEL_BG)
        status_frame.pack(fill="x", pady=(14, 6))
        tk.Label(
            status_frame,
            textvariable=self.status,
            bg=PANEL_BG,
            fg=WHITE,
            font=(UI_FONT, 10, "bold"),
        ).pack(side="left")
        tk.Button(
            status_frame,
            text="Limpiar consola",
            command=self._clear_log,
            bg=WHITE,
            fg=BLACK,
            font=(UI_FONT, 9, "bold"),
            relief="solid",
            bd=1,
        ).pack(side="right")

        console_border = tk.Frame(container, bg=BLACK, padx=1, pady=1)
        console_border.pack(fill="both", expand=True)
        self.log = tk.Text(
            console_border,
            height=17,
            bg=CONSOLE_BG,
            fg=WHITE,
            insertbackground=WHITE,
            font=(UI_FONT, 10),
            wrap="word",
            state="disabled",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.log.pack(fill="both", expand=True)
        self.log.tag_configure("warning", foreground=CONSOLE_WARNING)
        self.log.tag_configure("error", foreground=CONSOLE_ERROR)
        self.log.tag_configure("success", foreground=CONSOLE_SUCCESS)

    def _run_action(self, index, action):
        if not self.workflow.is_enabled(index) and not action.primary:
            return
        if self.runner.running:
            messagebox.showinfo(
                "Proceso activo", "Espera a que termine el proceso actual."
            )
            return
        if action.destructive and not messagebox.askyesno(
            "Confirmar reset",
            "Se hará backup del histórico y se recrearán las tablas madre. ¿Continuar?",
            icon="warning",
        ):
            return

        self.active_action = action
        self.active_index = index
        self._disable_all_actions()
        suffix = " · guarda snapshot" if action.stores_snapshot else ""
        self.status.set(f"Ejecutando: {action.label}{suffix}")
        self._append_log(
            f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] {action.label}\n"
            f"> {' '.join(action.command)}\n"
        )
        try:
            self.runner.start(action.command)
        except Exception as error:
            self._append_log(f"ERROR: {error}\n")
            self.active_action = None
            self.active_index = None
            self._apply_workflow_state()

    def _queue_output(self, text):
        self.events.put(("output", text))

    def _queue_finished(self, result):
        self.events.put(("finished", result))

    def _drain_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "output":
                    self._append_log(payload)
                else:
                    self._finish_action(payload.return_code)
        except Empty:
            pass
        self.root.after(100, self._drain_events)

    def _finish_action(self, return_code):
        label = self.active_action.label if self.active_action else "Proceso"
        index = self.active_index
        succeeded = return_code == 0
        is_routine_shortcut = (
            self.active_action.primary and index != self.workflow.current_index
        )
        if succeeded:
            if is_routine_shortcut:
                next_index = self.workflow.current_index
                self.status.set("Carga API completada · acción recomendada disponible")
                self._append_log(
                    "\nCarga rutinaria completada. No es necesario ejecutar los pasos 4–6.\n"
                )
            else:
                next_index = self.workflow.complete(index, True)
            if is_routine_shortcut:
                pass
            elif next_index == 0 and index == len(self.actions) - 1:
                self.status.set("Ciclo completado · paso 1 preparado")
                self._append_log(
                    "\nCiclo completado. Los pasos 2–6 vuelven a bloquearse.\n"
                )
            else:
                self.status.set(f"Completado: {label} · paso {next_index + 1} liberado")
                self._append_log("\nProceso completado correctamente.\n")
        else:
            if not is_routine_shortcut:
                self.workflow.complete(index, False)
            self.status.set(f"Error ({return_code}): {label} · repite el paso")
            self._append_log(f"\nProceso finalizado con código {return_code}.\n")
        self.active_action = None
        self.active_index = None
        self._apply_workflow_state()

    def _apply_workflow_state(self):
        for index, button in enumerate(self.buttons):
            enabled = self.workflow.is_enabled(index) or self.actions[index].primary
            button.configure(
                state="normal" if enabled else "disabled",
                bg=self.actions[index].color if enabled else DISABLED_BG,
                cursor="hand2" if enabled else "arrow",
            )

    def _disable_all_actions(self):
        for button in self.buttons:
            button.configure(state="disabled", bg=DISABLED_BG, cursor="arrow")

    def _on_button_enter(self, button, index):
        if str(button.cget("state")) != "disabled":
            button.configure(bg=lighten_hex(self.actions[index].color))

    def _on_button_leave(self, button, index):
        enabled = (
            str(button.cget("state")) != "disabled"
            and (self.workflow.is_enabled(index) or self.actions[index].primary)
        )
        button.configure(bg=self.actions[index].color if enabled else DISABLED_BG)

    def _append_log(self, text):
        self.log.configure(state="normal")
        for line in text.splitlines(keepends=True):
            tag = classify_console_line(line)
            self.log.insert("end", line, (tag,) if tag else ())
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _sync_backdrop(self, _event=None):
        if self.backdrop is None or not self.root.winfo_exists():
            return
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        self.backdrop.geometry(f"{width}x{height}+{x}+{y}")
        self.backdrop.lower(self.root)
        self.root.lift()

    def _close_windows(self):
        if self.backdrop is not None and self.backdrop.winfo_exists():
            self.backdrop.destroy()
        else:
            self.root.destroy()


def main():
    register_private_fonts(PROJECT_ROOT)
    backdrop = tk.Tk()
    backdrop.configure(bg=BLACK)
    backdrop.overrideredirect(True)
    backdrop.attributes("-alpha", BACKGROUND_ALPHA)
    backdrop.attributes("-topmost", WINDOW_TOPMOST)

    overlay = tk.Toplevel(backdrop)
    ControlPanelApp(overlay, backdrop=backdrop)
    backdrop.mainloop()


def classify_console_line(line):
    normalized = line.casefold()
    if any(token in normalized for token in ("traceback", "exception", "crash", "error", "failed", "fallido")):
        return "error"
    if any(token in normalized for token in ("warning", "advertencia", "warn")):
        return "warning"
    if any(
        token in normalized
        for token in (
            "completado", "correctamente", "restaurado", "guardado", "procesado",
            "prepared", "success", "status: completed",
        )
    ):
        return "success"
    return None

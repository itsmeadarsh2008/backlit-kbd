"""Background notification blinking manager."""

from __future__ import annotations

import threading
from dataclasses import dataclass

from .controller import BacklitKeyboardController
from .errors import NotificationAlreadyRunningError


@dataclass(slots=True)
class _BlinkWorker:
    stop_event: threading.Event
    thread: threading.Thread


class NotificationBlinker:
    """Manage one or more named background blink notification workers."""

    def __init__(self, controller: BacklitKeyboardController) -> None:
        self._controller = controller
        self._workers: dict[str, _BlinkWorker] = {}
        self._lock = threading.Lock()

    def start(
        self,
        name: str,
        *,
        count: int = 3,
        on_ms: int = 150,
        off_ms: int = 150,
        level_percent: float = 100.0,
        restore: bool = True,
    ) -> None:
        """Start a named background blink notification task."""
        with self._lock:
            if name in self._workers and self._workers[name].thread.is_alive():
                raise NotificationAlreadyRunningError(
                    f"Notification worker {name!r} is already running"
                )

            stop_event = threading.Event()
            thread = threading.Thread(
                target=self._run_worker,
                kwargs={
                    "name": name,
                    "stop_event": stop_event,
                    "count": count,
                    "on_ms": on_ms,
                    "off_ms": off_ms,
                    "level_percent": level_percent,
                    "restore": restore,
                },
                name=f"backlit-notification-{name}",
                daemon=True,
            )
            self._workers[name] = _BlinkWorker(stop_event=stop_event, thread=thread)
            thread.start()

    def stop(self, name: str, *, wait: bool = True, timeout: float | None = 2.0) -> None:
        """Stop a named worker if it exists."""
        worker = None
        with self._lock:
            worker = self._workers.get(name)
            if worker is None:
                return
            worker.stop_event.set()

        if wait:
            worker.thread.join(timeout=timeout)

        with self._lock:
            current = self._workers.get(name)
            if current is worker:
                self._workers.pop(name, None)

    def stop_all(self, *, wait: bool = True, timeout: float | None = 2.0) -> None:
        """Stop all active notification workers."""
        with self._lock:
            names = list(self._workers.keys())
        for name in names:
            self.stop(name, wait=wait, timeout=timeout)

    def active(self) -> list[str]:
        """Return currently active worker names."""
        with self._lock:
            active_names = [
                name for name, worker in self._workers.items() if worker.thread.is_alive()
            ]
        return sorted(active_names)

    def _run_worker(
        self,
        *,
        name: str,
        stop_event: threading.Event,
        count: int,
        on_ms: int,
        off_ms: int,
        level_percent: float,
        restore: bool,
    ) -> None:
        try:
            self._controller.blink(
                count,
                on_ms=on_ms,
                off_ms=off_ms,
                level_percent=level_percent,
                restore=restore,
                stop_event=stop_event,
            )
        finally:
            with self._lock:
                self._workers.pop(name, None)

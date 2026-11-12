import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY
from Back_end.smae_scheduler.state import SmaeSchedulerState


def _label(text: str) -> rx.Component:
    return rx.text(
        text,
        color=TEXT_PRIMARY,
        font_family=FONT_FAMILY_PRIMARY,
        font_size="0.74rem",
        font_weight="600",
    )


def _status_badge(status=None, label=None) -> rx.Component:
    current = status if status is not None else SmaeSchedulerState.last_status
    current_label = label if label is not None else SmaeSchedulerState.last_status_label

    return rx.badge(
        current_label,
        variant="soft",
        color_scheme=rx.cond(
            current == "success",
            "green",
            rx.cond(
                current == "failed",
                "red",
                rx.cond(current == "busy", "orange", "gray"),
            ),
        ),
    )


def _run_row(item) -> rx.Component:
    return rx.box(
        rx.grid(
            rx.vstack(
                rx.text(item["source"], color=TEXT_PRIMARY, font_weight="700", font_size="0.76rem"),
                rx.text(item["started_at"], color=TEXT_SECONDARY, font_size="0.67rem"),
                spacing="1",
                align="start",
            ),
            _status_badge(item["status"], item["status_label"]),
            rx.text(item["finished_at"], color=TEXT_SECONDARY, font_size="0.7rem"),
            rx.text(item["message"], color=TEXT_SECONDARY, font_size="0.7rem"),
            columns={"initial": "1", "md": "4"},
            spacing="3",
            align_items="center",
            width="100%",
        ),
        padding="0.75rem 0",
        border_bottom=f"1px solid {BORDER}",
        width="100%",
    )


def scheduler_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "INTEGRAÇÃO SMAE",
                color="#1281AA",
                font_size="0.72rem",
                font_weight="700",
                letter_spacing="0.08em",
            ),
            rx.heading(
                "Agendamento automático",
                size="7",
                color=TEXT_PRIMARY,
                font_family=FONT_FAMILY_SECUNDARY,
            ),
            rx.text(
                "Agenda a mesma sincronização completa já usada pelo botão manual do painel.",
                color=TEXT_SECONDARY,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.84rem",
            ),
            spacing="2",
            align="start",
        ),
        rx.cond(
            SmaeSchedulerState.scheduler_error_message != "",
            rx.callout(
                SmaeSchedulerState.scheduler_error_message,
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
            rx.box(),
        ),
        rx.cond(
            SmaeSchedulerState.scheduler_success_message != "",
            rx.callout(
                SmaeSchedulerState.scheduler_success_message,
                icon="circle_check",
                color_scheme="green",
                width="100%",
            ),
            rx.box(),
        ),
        rx.cond(
            SmaeSchedulerState.loading,
            rx.center(rx.spinner(size="3"), min_height="300px", width="100%"),
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading("Configuração", size="4", color=TEXT_PRIMARY),
                                rx.text(
                                    "Timezone fixo: America/Sao_Paulo",
                                    color=TEXT_SECONDARY,
                                    font_size="0.7rem",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.hstack(
                                rx.text("Ativo", color=TEXT_PRIMARY, font_size="0.78rem", font_weight="600"),
                                rx.switch(
                                    checked=SmaeSchedulerState.enabled,
                                    on_change=SmaeSchedulerState.set_enabled,
                                    disabled=~SmaeSchedulerState.can_manage_schedule,
                                ),
                                spacing="2",
                                align="center",
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.grid(
                            rx.vstack(
                                _label("Frequência"),
                                rx.select.root(
                                    rx.select.trigger(width="100%"),
                                    rx.select.content(
                                        rx.select.item("Uma vez por dia", value="daily"),
                                        rx.select.item("Por intervalo", value="interval"),
                                        position="popper",
                                    ),
                                    value=SmaeSchedulerState.mode,
                                    on_change=SmaeSchedulerState.set_mode,
                                    disabled=~SmaeSchedulerState.can_manage_schedule,
                                ),
                                spacing="1",
                                width="100%",
                            ),
                            rx.cond(
                                SmaeSchedulerState.mode == "daily",
                                rx.vstack(
                                    _label("Horário diário"),
                                    rx.input(
                                        type="time",
                                        value=SmaeSchedulerState.daily_time,
                                        on_change=SmaeSchedulerState.set_daily_time,
                                        disabled=~SmaeSchedulerState.can_manage_schedule,
                                        width="100%",
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                rx.vstack(
                                    _label("Intervalo em minutos"),
                                    rx.input(
                                        type="number",
                                        min="60",
                                        step="30",
                                        value=SmaeSchedulerState.interval_minutes,
                                        on_change=SmaeSchedulerState.set_interval_minutes,
                                        disabled=~SmaeSchedulerState.can_manage_schedule,
                                        width="100%",
                                    ),
                                    rx.text(
                                        "Mínimo: 60 minutos.",
                                        color=TEXT_SECONDARY,
                                        font_size="0.66rem",
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                            ),
                            columns={"initial": "1", "md": "2"},
                            spacing="3",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button(
                                rx.icon(tag="save", size=14),
                                "Salvar agendamento",
                                variant="outline",
                                on_click=SmaeSchedulerState.save_schedule,
                                loading=SmaeSchedulerState.saving,
                                disabled=~SmaeSchedulerState.can_manage_schedule,
                            ),
                            rx.spacer(),
                            rx.button(
                                rx.icon(tag="refresh_cw", size=14),
                                "Sincronizar agora",
                                background="#272361",
                                color="white",
                                on_click=SmaeSchedulerState.run_now,
                                loading=SmaeSchedulerState.running,
                                disabled=~SmaeSchedulerState.can_manage_schedule,
                            ),
                            width="100%",
                            align="center",
                            wrap="wrap",
                        ),
                        spacing="4",
                        width="100%",
                        align="stretch",
                    ),
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="12px",
                    padding="1.2rem",
                    width="100%",
                ),
                rx.grid(
                    rx.box(
                        rx.vstack(
                            rx.text("ÚLTIMA EXECUÇÃO", color=TEXT_SECONDARY, font_size="0.66rem", font_weight="700"),
                            rx.text(SmaeSchedulerState.last_run, color=TEXT_PRIMARY, font_weight="700"),
                            _status_badge(),
                            spacing="2",
                            align="start",
                        ),
                        background=SURFACE,
                        border=f"1px solid {BORDER}",
                        border_radius="10px",
                        padding="1rem",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("PRÓXIMA EXECUÇÃO", color=TEXT_SECONDARY, font_size="0.66rem", font_weight="700"),
                            rx.text(SmaeSchedulerState.next_run, color=TEXT_PRIMARY, font_weight="700"),
                            spacing="2",
                            align="start",
                        ),
                        background=SURFACE,
                        border=f"1px solid {BORDER}",
                        border_radius="10px",
                        padding="1rem",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("HEARTBEAT DO WORKER", color=TEXT_SECONDARY, font_size="0.66rem", font_weight="700"),
                            rx.text(SmaeSchedulerState.worker_heartbeat, color=TEXT_PRIMARY, font_weight="700"),
                            spacing="2",
                            align="start",
                        ),
                        background=SURFACE,
                        border=f"1px solid {BORDER}",
                        border_radius="10px",
                        padding="1rem",
                    ),
                    columns={"initial": "1", "md": "3"},
                    spacing="3",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("Últimas execuções", size="4", color=TEXT_PRIMARY),
                        rx.cond(
                            SmaeSchedulerState.last_message != "",
                            rx.text(
                                SmaeSchedulerState.last_message,
                                color=TEXT_SECONDARY,
                                font_size="0.72rem",
                            ),
                            rx.box(),
                        ),
                        rx.cond(
                            SmaeSchedulerState.runs.length() == 0,
                            rx.text(
                                "Nenhuma execução registrada ainda.",
                                color=TEXT_SECONDARY,
                                font_size="0.75rem",
                            ),
                            rx.vstack(
                                rx.foreach(SmaeSchedulerState.runs, _run_row),
                                spacing="0",
                                width="100%",
                                align="stretch",
                            ),
                        ),
                        spacing="3",
                        width="100%",
                        align="stretch",
                    ),
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="12px",
                    padding="1rem",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                align="stretch",
            ),
        ),
        spacing="5",
        width="100%",
        max_width="1150px",
        margin="0 auto",
        padding_bottom="5rem",
        align="stretch",
    )


def smae_scheduler_page() -> rx.Component:
    return admin_layout(scheduler_content())

import reflex as rx


# ============================================================
# CSS DE IMPRESSÃO
# ============================================================

PRINT_CSS = """
/* ==========================================================
   PREVIEW
   ========================================================== */

.meta-print-shell {
    min-height: 100vh;
    background: #eef1f5;
    padding: 24px;
    box-sizing: border-box;
}

.meta-print-document {
    width: 210mm;
    max-width: calc(100vw - 48px);

    margin: 0 auto;

    background: #ffffff;
    color: #17213c;

    box-sizing: border-box;

    padding: 14mm;

    box-shadow:
        0 10px 35px
        rgba(18, 30, 55, 0.15);
}

.meta-print-document,
.meta-print-document * {
    box-sizing: border-box;

    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

.print-toolbar {
    width: 210mm;
    max-width: calc(100vw - 48px);

    margin: 0 auto 16px auto;
}

.print-section {
    break-inside: avoid;
    page-break-inside: avoid;
}

.print-allow-break {
    break-inside: auto;
    page-break-inside: auto;
}

.print-card {
    break-inside: avoid;
    page-break-inside: avoid;
}

.print-page-break {
    break-before: page;
    page-break-before: always;
}


/* ==========================================================
   IMPRESSÃO
   ========================================================== */

@page {
    size: A4 portrait;
    margin: 12mm;
}

@media print {

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;

        background: #ffffff !important;

        overflow: visible !important;

        height: auto !important;
        min-height: auto !important;
    }

    .print-toolbar {
        display: none !important;
    }

    .meta-print-shell {
        width: auto !important;
        min-height: auto !important;

        margin: 0 !important;
        padding: 0 !important;

        background: #ffffff !important;

        overflow: visible !important;
    }

    .meta-print-document {
        width: 100% !important;
        max-width: none !important;

        margin: 0 !important;
        padding: 0 !important;

        box-shadow: none !important;

        border: none !important;

        overflow: visible !important;
    }

    .print-section {
        break-inside: avoid;
        page-break-inside: avoid;
    }

    .print-allow-break {
        break-inside: auto;
        page-break-inside: auto;
    }

    .print-card {
        break-inside: avoid;
        page-break-inside: avoid;
    }
}


/* ==========================================================
   TELAS PEQUENAS
   ========================================================== */

@media screen and (max-width: 900px) {

    .meta-print-shell {
        padding: 12px;
    }

    .meta-print-document {
        width: 100%;
        max-width: 100%;

        padding: 20px;
    }

    .print-toolbar {
        width: 100%;
        max-width: 100%;
    }
}
"""


# ============================================================
# COMPONENTE
# ============================================================

def meta_print_styles() -> rx.Component:
    """Insere o CSS específico da versão imprimível."""

    return rx.el.style(
        PRINT_CSS
    )
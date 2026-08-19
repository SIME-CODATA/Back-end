import reflex as rx

config = rx.Config(
    app_name="Back_end",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
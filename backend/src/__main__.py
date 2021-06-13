import uvicorn

from app.app import create_app

app = create_app()

uvicorn.run(app, use_colors=True, port=8000)

import uvicorn
from app.app import create_app
from rich.console import COLOR_SYSTEMS, Console


app = create_app()
console = Console(color_system="windows")
console.print('Dev link: http://localhost:8000/', style='bold blue')
uvicorn.run(app, use_colors=True, port=8000, host='0.0.0.0')

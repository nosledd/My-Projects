"""Launch the local browser interface from the project root."""
import os
from pathlib import Path
from automation.interface.web import serve

serve(
    Path(__file__).parent,
    host=os.getenv("AUTOMATION_HOST", "127.0.0.1"),
    port=int(os.getenv("PORT", "8080")),
)

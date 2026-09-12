"""Launch the local browser interface from the project root."""
from pathlib import Path
from automation.interface.web import serve

serve(Path(__file__).parent)

from fasthtml.common import fast_app, serve

from config import fast_config
from app.routes import router

# Create the FastHTML app
app, rt = fast_app(**fast_config)

# All of the logic is in the router
router(rt)

# Only run the server if this file is executed directly
if __name__ == "__main__":
    serve()

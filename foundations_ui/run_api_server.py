from foundations_rest_api.global_state import app_manager
from foundations.global_state import deployment_manager

app = app_manager.app()
app.run(port=37722)
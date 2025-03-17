# """
# app/__init__.py
# """ 

# # ---- app.py ----
# from flask import Flask
# from app.controller.trend_analyzer_controller import openserve_bp

# app = Flask(__name__)
# app.register_blueprint(openserve_bp)


from app.controller.agent_controller import app as app

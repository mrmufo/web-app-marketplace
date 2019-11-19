from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers  # This import is at the bottom to avoid circular dependencies.


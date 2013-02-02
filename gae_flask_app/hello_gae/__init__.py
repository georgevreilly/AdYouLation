from flask import Blueprint
 
hello_gae = Blueprint('hello_gae', __name__)
 
import handlers

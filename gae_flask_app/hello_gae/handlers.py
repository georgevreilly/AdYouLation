from ..hello_gae import hello_gae
from flask import render_template 

@hello_gae.route('/')
def hello_gae():
    return render_template("base.html")

from flask import render_template, request, Blueprint


CONFIGURATOR_BLUEPRINTS = []

configurator_page = Blueprint('configurator_page', __name__, static_folder='static', template_folder='templates')
CONFIGURATOR_BLUEPRINTS.append(configurator_page)
@configurator_page.route("/configurator/", methods=['POST', 'GET'])
@configurator_page.route("/configurator", methods=['POST', 'GET'])
def configurator():
    if request.method == 'POST':
        pass
    else:
        return render_template("configurator.html")
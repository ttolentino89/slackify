from slackify import Flask, FlackBlueprint, reply_text


bp = FlackBlueprint('slack_blueprint', __name__, url_prefix='/integrations')


@bp.command
def hello():
    return reply_text('Hello from a Blueprint!')



app = Flask(__name__)

app.register_blueprint(bp)
print(app.view_functions.keys())
print(app.url_map)
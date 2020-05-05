from slackify import Flack, FlackBlueprint, reply_text


bp = FlackBlueprint('slack_blueprint', __name__)


@bp.command
def hello():
    return reply_text('Hello from a Blueprint!')



app = Flack(__name__)

app.register_blueprint(bp, url_prefix='/integrations')
print(app.view_functions.keys())
print(app.url_map)
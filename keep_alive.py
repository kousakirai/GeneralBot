from sanic import Sanic
from sanic.response import text
from threading import Thread
app = Sanic('Discordbot')


@app.route('/')
async def main(request):
    return text('Alive')


def keep_run():
    app.run(host="0.0.0.0", port=8080)
    server = Thread(target=keep_run)
    server.start()


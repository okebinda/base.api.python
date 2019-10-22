from app.api_admin import create_app
from app.Config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run(host='127.0.0.1')

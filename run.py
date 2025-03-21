from server import create_app
from config import Config
from waitress import serve

app=create_app()

if __name__ == "__main__":

    if Config.DEBUG == 'True':
        app.run(debug=Config.DEBUG, port=Config.PORT)
    
    else:
        serve(app, host='0.0.0.0', port=Config.PORT)
    
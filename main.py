#imports
from Website import init_application

web_app = init_application()
if __name__ == '__main__':
    web_app.run(debug=True)
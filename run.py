from webapi import create_app

application = create_app(__name__)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)

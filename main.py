"""Creates a Flask web application and runs it in debug mode."""
from website import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

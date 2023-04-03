from website import create_app

app = create_app() # defined in website/__init__.py

if __name__ == '__main__':
    app.run(debug=True)
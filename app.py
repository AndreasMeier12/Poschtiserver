from flask import Flask, render_template
from . import db
from . import create_app

app = create_app()


@app.route('/')
def main():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()

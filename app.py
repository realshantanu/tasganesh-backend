from waitress import serve
import multiprocessing
from core import create_app,db

mode = 'prod'

app = create_app()

with app.app_context():
    # db.reflect()
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    if (mode == 'dev'):
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host="0.0.0.0", port=8080, threads=multiprocessing.cpu_count())

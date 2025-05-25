from main import *

@app.route('/')
def index():
    return render_template('list_post.html')
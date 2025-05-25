from main import *

@app.route('/')
def index():
    return render_template('list_post.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

    return render_template('auth/login.html')
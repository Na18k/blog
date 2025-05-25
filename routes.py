from main import *

@app.route('/')
def index():
    return render_template('list_post.html')

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Tira os espaços e coloca tudo em minúscula
        username = name.strip().lower()

        status, err = db.register_user(
            username=username,
            name=name,
            email=email,
            password=password
        )

        if status:
            return redirect(url_for('index'))
        
        return redirect(url_for('register_user'))

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        status, user_id = db.login_user(
            email=email,
            password=password
        )

        if status:
            session['userID'] = user_id
            return redirect(url_for('index'))
        
        # return redirect(url_for('login'))

    return render_template('auth/login.html')
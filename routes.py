from main import *

@app.route('/')
def index():
    return render_template('posts_index.html')

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

        status, user_id = db_user.login_user(
            email=email,
            password=password
        )

        if status:
            session['userID'] = user_id
            return redirect(url_for('index'))
        
        # return redirect(url_for('login'))

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    if session['userID']:
        session.pop('userID', None)

        return redirect(url_for('index'))

    else:
        return redirect(url_for('login'))


# Posts +------------------------------------------------>
@app.route('/post/register', methods=['GET', 'POST'])
def post_register():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        visibility = request.form.get('visibility')

        db_post.insert_post(
            user_id=session.get('userID'),
            title=title,
            content=content,
            visibility=visibility
        )

        # Com base no tipo de visualidade é mostrado uma mensagem diferente
        if visibility == 'private':
            flash('Post salvo como privado!')
        
        elif visibility == 'public':
            flash('Post publicado com sucesso!')

        # Retorna para a página inicial
        return redirect(url_for('index'))

    return render_template('post/register.html')
from main import *

@app.route('/')
def index():
    # Obtém o número da página da query string, padrão é 1
    page = request.args.get('page', default=1, type=int)
    per_page = 20

    # Busca os posts públicos paginados
    posts_data = db_post.get_list_posts(page=page, per_page=per_page, db_user=db_user)

    return render_template(
        'posts_index.html',
        posts=posts_data['posts'],
        page=posts_data['page'],
        per_page=posts_data['per_page'],
        total_pages=posts_data['total_pages'],
        total_posts=posts_data['total_posts']
    )


@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Tira os espaços e coloca tudo em minúscula
        username = name.strip().lower()

        status, err = db_user.register_user(
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

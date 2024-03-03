from app import create_app
from app.utils import db

# Crie a aplicação Flask
app = create_app()

# Crie o contexto da aplicação
ctx = app.app_context()
ctx.push()

# Inicialize o banco de dados
db.create_all()

# Pop do contexto da aplicação
ctx.pop()

print("db created.")
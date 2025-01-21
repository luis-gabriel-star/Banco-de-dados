from flask import Flask, request, jsonify
from models import db, Item

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    db.create_all()

def create_demo_data():
    if not Item.query.first():
        items = [
            Item(name="Camiseta", description="Camiseta de algodão, confortável e estilosa."),
            Item(name="Calça", description="Calça jeans de alta qualidade, ajuste perfeito."),
            Item(name="Tênis", description="Tênis esportivo, ideal para corridas e atividades físicas."),
            Item(name="Mochila", description="Mochila de viagem resistente e com diversos compartimentos."),
            Item(name="Óculos de Sol", description="Óculos de sol modernos, proteção UV garantida.")
        ]
        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Dados fictícios adicionados!")

def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

def setup_database():
    create_tables()
    create_demo_data()

with app.app_context():
    setup_database()

@app.route('/api/items', methods=['GET'])
def list_items():
    return get_items()

@app.route('/api/items/<int:item_id>', methods=['GET'])
def single_item(item_id):
    return get_item(item_id)

@app.route('/api/items', methods=['POST'])
def add_item():
    return create_item()

if __name__ == '__main__':
    app.run(debug=True)

from typing import List

import flask

app = flask.Flask(__name__)


class Vector3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def to_json(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}


class Item:
    id = 0
    position: Vector3 = Vector3(0, 0, 0)
    size: Vector3 = Vector3(0, 0, 0)

    def __init__(self, id: int, position: Vector3, size: Vector3):
        self.id = id
        self.position = position
        self.size = size

    def to_json(self):
        return {'Id': self.id, 'Position': self.position.to_json(), 'Size': self.size.to_json()},


@app.route("/api/item")
def items():
    return flask.jsonify(Store.get_instance().to_json())
    pass


@app.route("/api/item/<int:id>")
def item(id: int):
    return flask.jsonify(Store.get_instance().items[id].to_json())
    pass


@app.route("/")
def home():
    return flask.render_template("index.html", items=flask.json.dumps(Store.get_instance().to_json()))
class Store:
    items: List[Item] = None

    @staticmethod
    def get_instance():
        store = getattr(flask.g, "_store", None)

        if store is None:
            store = flask.g._store = Store()

        return store

    def __init__(self):
        self.items = [
            Item(0, Vector3(0, 0, 0), Vector3(1, 1, 1)),
            Item(1, Vector3(1, 1, 0), Vector3(1, 1, 1)),
            Item(2, Vector3(0, 0, 3), Vector3(1, 1, 1)),
        ]

    def to_json(self):
        return {
            "Items": [item.to_json() for item in self.items]
        }


if __name__ == "__main__":
    app.run(port=8085)

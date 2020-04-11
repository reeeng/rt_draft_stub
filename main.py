import json
from typing import List

import flask

app = flask.Flask(__name__)
store = None


class Vector3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def to_json(self):
        return dict(x=self.x, y=self.y, z=self.z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Item:
    id = 0
    position: Vector3 = Vector3(0, 0, 0)
    rotation: Vector3 = Vector3(0, 0, 0)
    type = 0

    def __init__(self, id: int, position: Vector3, rotation: Vector3, type: int):
        self.id = id
        self.position = position
        self.rotation = rotation
        self.type = type

    def to_json(self):
        return dict(id=self.id, position=self.position.to_json(), rotation=self.rotation.to_json(), type=self.type)

    def __repr__(self):
        return f"(id: {self.id}, position: {self.position}, rotation: {self.rotation}, type: {self.type})"


@app.route("/api/item")
def items():
    return flask.jsonify(Store.get_instance().to_json())


@app.route("/api/item/<int:id>")
def item(id: int):
    return flask.jsonify(Store.get_instance().items[id].to_json())


@app.route("/")
def home():
    return flask.render_template("index.html", items=flask.json.dumps(Store.get_instance().to_json()))


@app.route("/update", methods=["POST"])
def update():
    rawItems = json.loads(flask.request.form["items"])
    rawItems = rawItems["items"] if rawItems else None

    if not rawItems:
        return flask.redirect("/")

    newItems = []

    for rawItem in rawItems:
        # rawItem = rawItem[0]
        position = rawItem.get("position")
        rotation = rawItem.get("rotation")
        newItem = Item(rawItem.get("id"), Vector3(position.get("x"), position.get("y"), position.get("z")),
                       Vector3(rotation.get("x"), rotation.get("y"), rotation.get("z")), rawItem.get("type"))
        newItems.append(newItem)

    Store.get_instance().items = newItems
    return flask.redirect("/")


class Store:
    items: List[Item] = None

    @staticmethod
    def get_instance():
        global store
        if store is None:
            store = Store()
        return store

    def __init__(self):
        self.items = [
            Item(0, Vector3(0, 0, 0), Vector3(0, -90, 0), 1),
            Item(1, Vector3(0, 0, 2), Vector3(0, -90, 0), 1),
            Item(2, Vector3(2, 0, 0), Vector3(0, 180, 0), 2),
            Item(3, Vector3(0, 0, 4), Vector3(0, 0, 0), 1),
        ]

    def to_json(self):
        return dict(items=list(map(lambda item: item.to_json(), self.items)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

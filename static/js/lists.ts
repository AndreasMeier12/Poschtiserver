let model: ShoppingList[] = []
const DELETE = 'delete';
const CREATE = 'create';
const ORIGIN = 'server';

class ShoppingList {
    id: number;
    name: string;

    constructor(id: number, name: string) {
        this.id = id;
        this.name = name;
    }


}


function createList() {


}

function getMaxId() {
    return model.map(x => x.id).reduce(function (a, b) {
        return Math.max(a, b);
    }, 0);
}

function deleteList(list: ShoppingList) {
    const payload = {}


}

function displayList(list: ShoppingList) {
}

function redraw() {
}

function getFromServer() {
    fetch('', {}).then(
        response => {
            model = JSON.parse(response.toString());
        }
    )


}

function setUp() {
    getFromServer();
    redraw();
}

function handleListSubmit() {
    const element = (<HTMLInputElement>document.getElementById("inputname"));
    const name: string =  element.value;
    element.value = ""
    const id = getMaxId() + 1;
    model.push(new ShoppingList(id, name))


}
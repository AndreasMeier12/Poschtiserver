let model: ShoppingList[] = []

const ORIGIN = 'server';






enum CommandType {
    DELETE = 'delete',
    CREATE = 'create',

}

class ShoppingList {
    id: number;
    name: string;

    constructor(id: number, name: string) {
        this.id = id;
        this.name = name;
    }


}

class ListCommand {
    list: ShoppingList
    type: CommandType
    origin: string

    constructor(list: ShoppingList, type: CommandType) {
        this.list = list;
        this.type = type;
        origin = ORIGIN;
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
    const table = <HTMLTableElement>(document.getElementById('listbody'));
    for (const a of model) {
        const row = table.insertRow(-1)
        const nameCell = row.insertCell(0)
        const deleteCell = row.insertCell(1)
        const deleteButton = document.createElement('input');
        deleteButton.type = "button";
        deleteButton.value = "🗑";
        deleteButton.addEventListener("click", handleDelete(a.id))
        nameCell.innerText = a.name
        deleteCell.appendChild(deleteButton)
    }


}

function handleDelete(a: number) {
    return function asdf() {
        const payload = {'id': a, 'origin': ORIGIN}
        const response = fetch(window.location.href, {
            method: 'DELETE', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        }).then()
    }
}


function getFromServer() {
    fetch('', {}).then(
        response => {
            model = JSON.parse(response.toString());
        }
    )


}

function setUp() {
    const rows = Array.prototype.slice.call( (<HTMLTableElement>document.getElementById('liststable')).rows);
    for (const row of rows){
        const id = row.id.toString()
        if (id.includes("shopping-list-")) {
            const idString = id.replace('shopping-list-', '')
            const numId: number = +idString;

            const button = document.getElementById("delete-" + numId)
            button.addEventListener("click", handleDelete(numId))
        }

    }


}


function send_list(a: ShoppingList) {
    console.log("send list")
    const command = new ListCommand(a, CommandType.CREATE)
    const body = JSON.stringify(command)
    fetch('/auth/lists/api', {method: 'POST', body: body})

}

function handleListSubmit() {
    const element = (<HTMLInputElement>document.getElementById("inputname"));
    const name: string = element.value;
    element.value = ""
    const id = getMaxId() + 1;
    const list = new ShoppingList(id, name);
    model.push(list)
    send_list(list)


}

window.addEventListener("DOMContentLoaded", setUp)

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
function handleDelete(a: number){
   return function asdf (){
       console.log( `List ${a} delete`)
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
    getFromServer();
    redraw();
}

function handleListSubmit() {
    const element = (<HTMLInputElement>document.getElementById("inputname"));
    const name: string = element.value;
    element.value = ""
    const id = getMaxId() + 1;
    model.push(new ShoppingList(id, name))


}
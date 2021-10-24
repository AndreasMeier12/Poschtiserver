let model : ShopItem[] = []
const LISTID = 1

class ShopItem {
    id: number;
    listId: number;
    name: string;
    shop: string;
    quantity: string;
    done: boolean;

    constructor(id: number, listId: number, name: string, shop: string, quantity: string, done: boolean){
        this.id = id;
        this.listId = listId;
        this.name = name;
        this.shop = shop;
        this.quantity = quantity;
        this.done = done;

}



}

function checkDone(a: number){
    console.log("check done");
}

function getMaxId() : number{
return  model.map(x => x.id).reduce(function(a, b) {
    return Math.max(a, b);
}, 0);
}


function create(){
    const itemId : number = getMaxId() + 1
    const name : string = document.getElementById("inputname").value
    const quantity = document.getElementById("inputquantity").value
    const shop = document.getElementById("inputshop").value
    const done = false
    const newItem = new ShopItem(itemId, LISTID, name, shop, quantity, done)
    model.push(newItem)
    addToList(newItem)
}


function addToList(a: ShopItem){
    const table = <HTMLTableElement>document.getElementById("listtable");
    const row = table.insertRow(-1)
    row.id = "row"+ a.id.toString()
    const name = row.insertCell(0)
    name.innerHTML = a.name;
    row.insertCell(1).innerHTML=a.quantity
    row.insertCell(2).innerHTML=a.shop
    if (a.done){
        name.innerHTML = "<S>" + name.innerHTML + "</S>>"
    }
    const btn = document.createElement('input');
    btn.type = 'button';
    btn.value = "✅";
    row.insertCell(3).appendChild(btn)
    const deleteButton = document.createElement('input');
    deleteButton.type = "button";
    deleteButton.value = "🗑";
    row.insertCell(4).appendChild(deleteButton)



}



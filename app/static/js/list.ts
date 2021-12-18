const ORIGIN = 'server'

function setUp() {
    const rows = Array.prototype.slice.call((<HTMLTableElement>document.getElementById('listtable')).rows);
    for (const row of rows) {
        const id = row.id.toString()
        if (id.includes("shopping-item-")) {

            const idString = id.replace('shopping-item-', '')

            const button = document.getElementById("delete-" + idString)
            button.addEventListener("click", handleDelete(idString))

            const checkButton = document.getElementById("check-" + idString)
            let doneness: boolean = false

            if (row.dataset.done == "1"){
                doneness = true
            }

            checkButton.addEventListener("click", handleCheck(idString, doneness))
        }

    }
}

function handleDelete(a: string) {
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
function handleCheck(a: string, done: boolean){
    console.log(a, done)
        return function asdf() {
        const payload = {'id': a, 'origin': ORIGIN, 'done': !done}
        const response = fetch(window.location.href, {
            method: 'PATCH', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        }).then()
    }
}




window.addEventListener("DOMContentLoaded", setUp)

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
            const name = row.dataset.name
            const shop = row.dataset.shop
            const quantity = row.dataset.quantity

            checkButton.addEventListener("click", handleCheck(idString, doneness, name, shop, quantity))
        }
    document.getElementById("button-clear-done").addEventListener("click", clearDone)

    }
}


function clearDone() {
    const rows = Array.prototype.slice.call((<HTMLTableElement>document.getElementById('listtable')).rows);
    const doneItems: Array<String> = []

    for (const row of rows) {
        const id = row.id.toString()
        if (id.includes("shopping-item-")) {
            if (row.dataset.done == "1") {
                const idString = id.replace('shopping-item-', '')

                doneItems.push(idString)
            }
        }


    }
    const response = fetch(window.location.href, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(doneItems)
    }).then(response => {
            window.location.href = response.url
        }
    )
}

function handleDelete(a: string) {
    return function asdf() {
        const payload = [a]
        const response = fetch(window.location.href, {
            method: 'DELETE', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
    }).then(response => {
            window.location.href = response.url
        }
    )

    }
}

function handleCheck(a: string, done: boolean, name: string, shop: string, quantity: string) {
    console.log(a, done)
    return function asdf() {
        const payload = {
            'id': a,
            'origin': ORIGIN,
            'done': !done,
            'name': name,
            'shop': shop,
            'quantity': quantity
        }
        const response = fetch(window.location.href, {
            method: 'PATCH', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        }).then(response => {
                window.location.href = response.url
            }
        )
    }
}




window.addEventListener("DOMContentLoaded", setUp)

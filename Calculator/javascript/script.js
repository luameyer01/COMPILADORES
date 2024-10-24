async function calcular() {
    let resultado = 0;

    const response = await fetch('/analizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            expresion: expresion,
        }),
    });

    const data = await response.json();

    // Crear el HTML para el árbol
    const treeContainer = document.querySelector('#tree-container');
    const treeHTML = crearArbolHTML(data.arbol);
    treeContainer.innerHTML = treeHTML;

    try {
        resultado = eval(expresion);
        ans = resultado;
        document.querySelector('.result').innerText = resultado;
    } catch (error) {
        document.querySelector('.result').innerText = "Error en la expresión";
    }
}

// Función que convierte el árbol recibido en HTML jerárquico
function crearNodo(valor, tipo) {
    let nodo = document.createElement('div');
    nodo.innerText = valor;
    if (tipo === 'operator') {
        nodo.classList.add('operator');
    } else {
        nodo.classList.add('operand');
    }
    return nodo;
}

// Asume que 'arbol' es un array de objetos con los nodos del árbol
arbol.forEach(nodo => {
    let tipoNodo = (nodo.tipo === 'OPERADOR') ? 'operator' : 'operand';
    let nuevoNodo = crearNodo(nodo.valor, tipoNodo);
    // Aquí añades el nodo al DOM
});

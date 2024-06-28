console.log("funcoes");

function valorPtBr(valor){
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
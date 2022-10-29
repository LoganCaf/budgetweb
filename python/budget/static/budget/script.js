function addRow(name,values){
    const newRow = document.createElement("tr");
    const newCell1 = document.createElement('td');
    const newCell1In = document.createElement('input');
    const newCell2 = document.createElement('td');
    const newCell2In = document.createElement('input');
    const newCell3 = document.createElement('td');
    const newCell3In = document.createElement('input');
    const newCellName = document.createElement('td');
    const newAtribute = document.createAttribute("id");
    const newAtributeCell = document.createAttribute("class");
    newAtributeCell.value = 'cell';
    newCellName.textContent = name;
    newCell1In.value = values[0];
    newCell1In.setAttributeNode(newAtributeCell.cloneNode());
    newCell2In.value = values[1];
    newCell2In.setAttributeNode(newAtributeCell.cloneNode());
    newCell3In.value = values[2];
    newCell3In.setAttributeNode(newAtributeCell.cloneNode());
    newCell1.appendChild(newCell1In);
    newCell2.appendChild(newCell2In);
    newCell3.appendChild(newCell3In);
    newRow.appendChild(newCellName);
    newRow.appendChild(newCell1);
    newRow.appendChild(newCell2);
    newRow.appendChild(newCell3);
    newAtribute.value = name;
    newRow.setAttributeNode(newAtribute);
    document.getElementById('table1').appendChild(newRow); 
}
function addRowClick(){
    console.log(categories);
    const name = document.getElementById('input1').value;
    if (name !== ''){
        collumns[name] = [0,0,0];
        addRow(name,[0,0,0]);
    }
    
}

let collumns = {'Fun':[20,5,50],'Food':[30,27,3],'Computer':[10,0,300]};
for(let i = 0; i < Object.keys(collumns).length; i++) {
    addRow(Object.keys(collumns)[i],collumns[Object.keys(collumns)[i]]);
}

document.getElementById('button1').onclick = addRowClick;


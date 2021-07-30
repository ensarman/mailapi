// get the specified parent element from given TAgName
const find_parent = (parent, element) =>{
  if (element.tagName !=  parent ){
    return find_parent(parent, element.parentElement);
  }
  else{
     return element;
  }
}
import React, {useState, useEffect} from 'react';
import Table from './Table';
import Form from './Form';
import axios from 'axios';

function MyApp() {
  const [characters, setCharacters] = useState([]);  

  function removeOneCharacter (index) {
    // console.log("<<"+index)
      makeDeleteCall(characters[index].id).then( result => {
        if (result.status === 204)
           setCharacters(characters.filter((character, i) => {
           return i !== index
      }));
      });
    }

  
    function updateList(person) { 
      makePostCall(person).then( result => {
      if (result.status === 201)
        setCharacters([...characters, result.data] );
      });
      
   }

// function updateList(person) {
//   setCharacters([...characters, person]);
// }
async function makePostCall(person){
  try {
     const response = await axios.post('http://localhost:5000/users', person);
     console.log(response)
     return response;
  }
  catch (error) {
     console.log(error);
     return false;
  }
}  

async function makeDeleteCall(person){
  try {
     const response = await axios.delete('http://localhost:5000/users/'+ person);
     console.log(response)
     return response;
  }
  catch (error) {
     console.log(error);
     return false;
  }
}  
async function fetchAll(){
  try {
     const response = await axios.get('http://localhost:5000/users');
     return response.data.users_list;     
  }
  catch (error){
     //We're not handling errors. Just logging into the console.
     console.log(error); 
     return false;         
  }
}

useEffect(() => {
  fetchAll().then( result => {
     if (result)
        setCharacters(result);
   });
}, [] );

  return (
    <div className="container">
      <Table characterData={characters} removeCharacter={removeOneCharacter} />
      <Form handleSubmit={updateList} />


    </div>
  )


}


export default MyApp;
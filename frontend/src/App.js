import { useState } from "react";
import './App.css';

function App() {
  const [url, setUrl] = useState("");
  const [shortUrl,setShortUrl]=useState("")
  const handleSubmit = () => {
    

    var link = 'http://127.0.0.1:8000/save_url';
  fetch(link,{
      method:'POST',
      headers:{
        'Accept':'application/json',
        'Content-Type':'application/json'
      },
      body:JSON.stringify({"url":url})
    }).then((response)=>{
      if(response.ok){
        console.log("Created user")
      }
      return response.json();
    }).then((data)=>{
      setShortUrl(data["shortened_url"])
    })
    
  };

  return (
    <div className="App">
      <header className="App-header">
         <div>
          <label>Enter URL: </label>
          <input type='text' value={url} onChange={(e)=>setUrl(e.target.value)} /><br/>

          <button onClick={handleSubmit}>Submit</button><br></br>

          <span>Shortened URL: </span><span id='shortUrl'>{shortUrl}</span>
         </div>
      </header>
    </div>
  );
}

export default App;

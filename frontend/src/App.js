import { useState } from "react";
import './App.css';

function App() {
  const [url, setUrl] = useState("");
  const [shortUrl,setShortUrl]=useState("");
  const [allUrls,setAllUrls]=useState([])
  const handleSubmit = () => {
    
    if(url.length===0){
      return {"msg":"URL is mandaotry"}
    }
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
      console.log(data)
      setShortUrl(data["shortened_url"])
      console.log(data['all_urls'])
      const urlsArray = Object.entries(data.all_urls).map(([original, shortened]) => ({
        original_url: original,
        shortened_url: shortened
      }));
      console.log(urlsArray)
      setAllUrls(urlsArray);
    })
    
  };

  return (
    <div className="h-[100vh] w-[100%]">
      <div className="flex justify-center items-center h-[40%]">
              <div className="text-2xl font-thin">Shorten your URL for work, personal use and anything.....</div>
      </div>
      <div className="flex flex-col justify-center items-center ">
        
        <div className="flex w-[100%] justify-center">
           <input type='text' className="w-[50%] border border-gray-400 rounded-sm p-5" value={url} onChange={(e)=>{setUrl(e.target.value)}} placeholder="Enter URL:"></input>
      
        <button onClick={handleSubmit} className="bg-black text-white rounded-sm p-5 w-[10%]">Shorten</button>
        </div>
       
      </div>

<div className="flex flex-col w-[90%] justify-center mt-10 overflow-x-auto mx-auto">
  <div className="w-full text-center font-bold mb-2">Previous Links</div>
  <table className="table-fixed border-collapse border border-gray-400 w-full">
    <thead>
      <tr>
        <th className="border border-gray-400 px-4 py-2 w-3/5 text-left">Original</th>
        <th className="border border-gray-400 px-4 py-2 w-2/5 text-left">Shortened</th>
      </tr>
    </thead>
    <tbody>
      {allUrls.map((item, index) => (
        <tr key={index}>
          <td className="border border-gray-400 px-4 py-2 w-3/5 overflow-hidden whitespace-nowrap truncate">
            {item.original_url}
          </td>
          <td className="border border-gray-400 px-4 py-2 w-2/5 overflow-hidden whitespace-nowrap truncate">
            {item.shortened_url}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>


    </div>
  );
}

export default App;

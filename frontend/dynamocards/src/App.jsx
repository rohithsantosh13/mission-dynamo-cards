import React, {useState} from 'react'
import axios from 'axios'

function App(){
    const [youtubeLink, setYoutubeLink] = useState("");
    const [responseData, setResponseData] = useState(null);

    const handlerLinkChange = (event) => {
        setYoutubeLink(event.target.value);
    };

    const sendLink = async() =>
    {
        try{
            const response = await axios.post("http://127.0.0.1:8000/analyze_video",{youtube_link: youtubeLink});
            setResponseData(response.data);
        }
        catch(error){
            console.log(error);
        }
    };

    return (
        <div className = "App">
            <h1>
                Youtube link to Flashcards Generator
            </h1>
        <input
            type='text'
            placeholder="Paste Youtube link Here"
            value  = {youtubeLink}
            onChange={handlerLinkChange}
        />
        <button onClick={sendLink}>
            Generate FlashCards
        </button>
        {responseData && (
            <div>
                <h2> Response Data: </h2>
                <p>
                    {JSON.stringify(responseData,null,2)}
                </p>
            </div>
        )}
        </div>
    )
}
export default App;
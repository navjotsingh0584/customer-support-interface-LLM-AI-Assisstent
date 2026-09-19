import { useState } from "react";


function ChatInput({
    setMessages,
    setThinking,
    sessionId,
    refreshSessions
}) {


    const [text, setText] = useState("");

    const [file, setFile] = useState(null);

    const [preview, setPreview] = useState(null);





    async function uploadFile(){


        if(!file)
            return null;


        const token =
        localStorage.getItem("token");



        const formData =
        new FormData();



        formData.append(
            "file",
            file
        );


        formData.append(
            "session_id",
            sessionId
        );



        try{


            const response =
            await fetch(

                "http://127.0.0.1:8000/upload",

                {

                    method:"POST",

                    headers:{

                        "Authorization":
                        `Bearer ${token}`

                    },

                    body:formData

                }

            );




            if(!response.ok){


                console.log(
                    "Upload failed",
                    response.status
                );


                return null;

            }




            const data =
            await response.json();


            return data;



        }

        catch(error){


            console.log(
                "UPLOAD ERROR",
                error
            );


            return null;

        }


    }









    async function send(){



        if(
            !text.trim()
            &&
            !file
        )
        return;





        const msg =
        text;




        setText("");



        let uploadedFile=null;



        if(file){


            uploadedFile =
            await uploadFile();



            setFile(null);

            setPreview(null);


        }








        let displayMessage =
        msg;





        if(uploadedFile){


            displayMessage +=
            `\n\n📎 Uploaded: ${file?.name}`;

        }







        setMessages(old=>[


            ...old,


            {

                role:"user",

                message:displayMessage

            }


        ]);






        setThinking(true);





        const token =
        localStorage.getItem("token");







        try{



            const response =
            await fetch(

                "http://127.0.0.1:8000/chat/stream",

                {

                    method:"POST",


                    headers:{


                        "Content-Type":"application/json",


                        "Authorization":
                        `Bearer ${token}`


                    },



                    body:JSON.stringify({


                        message:msg,


                        session_id:sessionId


                    })


                }

            );







            if(!response.ok){


                console.log(
                    "Chat error:",
                    response.status
                );


                setThinking(false);

                return;

            }







            const reader =
            response.body.getReader();



            const decoder =
            new TextDecoder();



            let bot="";






            setMessages(old=>[


                ...old,


                {

                    role:"assistant",

                    message:""

                }


            ]);







            while(true){



                const {

                    done,

                    value

                }=await reader.read();





                if(done)

                    break;







                const chunk =
                decoder.decode(value);




                bot += chunk;







                setMessages(old=>{



                    let copy=[...old];



                    copy[
                        copy.length-1
                    ]={


                        role:"assistant",


                        message:bot


                    };




                    return copy;


                });




            }







            setThinking(false);








            setTimeout(()=>{


                if(refreshSessions){

                    refreshSessions();

                }


            },2000);






        }



        catch(error){



            console.log(

                "STREAM ERROR:",

                error

            );



            setThinking(false);



        }





    }









    return (


        <div className="chat-input">






            <label
                className="upload-button"
            >

                📎



                <input

                    type="file"

                    hidden



                    onChange={

                        (e)=>{


                            const selectedFile =
                            e.target.files[0];



                            setFile(selectedFile);





                            if(

                                selectedFile &&

                                selectedFile.type.startsWith("image/")

                            ){


                                setPreview(

                                    URL.createObjectURL(
                                        selectedFile
                                    )

                                );


                            }

                            else{


                                setPreview(null);


                            }


                        }

                    }


                />


            </label>







            {

                file &&


                <div className="file-chip">



                    {

                        preview &&


                        <img

                            src={preview}

                            className="preview-image"

                            alt="preview"

                        />


                    }





                    <span>

                        {file.name}

                    </span>





                    <button

                        type="button"

                        onClick={()=>{


                            setFile(null);

                            setPreview(null);


                        }}


                    >

                        ✕

                    </button>





                </div>


            }








            <input



                value={text}



                placeholder="Ask HAL anything..."



                onChange={

                    e=>

                    setText(
                        e.target.value
                    )

                }



                onKeyDown={(e)=>{



                    if(

                        e.key==="Enter"

                        &&

                        !e.shiftKey

                    ){


                        e.preventDefault();


                        send();


                    }


                }}



            />







            <button

                type="button"

                onClick={send}

            >

                ➤

            </button>






        </div>


    );


}



export default ChatInput;
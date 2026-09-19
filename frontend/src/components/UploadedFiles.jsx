import { useEffect, useState } from "react";
import "./../App.css";


function UploadedFiles({ sessionId }) {


    const [files, setFiles] = useState([]);




    async function loadFiles(){


        if(!sessionId){

            setFiles([]);

            return;

        }



        const token =
        localStorage.getItem("token");



        try{


            const res = await fetch(

                `http://127.0.0.1:8000/api/uploads/${sessionId}`,

                {

                    headers:{

                        Authorization:
                        `Bearer ${token}`

                    }

                }

            );



            if(res.ok){


                const data =
                await res.json();


                setFiles(data);


            }


        }


        catch(error){


            console.log(
                "FILES LOAD ERROR",
                error
            );


            setFiles([]);


        }



    }






    useEffect(()=>{


        loadFiles();


    },[sessionId]);









    function getIcon(type){


        if(type==="image")

            return "🖼️";



        if(type==="pdf")

            return "📄";



        if(
            type==="table" ||
            type==="csv" ||
            type==="xlsx"
        )

            return "📊";



        return "📁";


    }







    if(files.length===0)

        return null;









    return (


        <div className="uploaded-panel">


            <h3>

                📂 Uploaded Files

            </h3>





            <div className="file-grid">



            {

                files.map((file,index)=>(


                    <div

                    className="file-card"

                    key={index}

                    >




                        <div className="file-image">



                        {

                            file.file_type==="image"
                            &&
                            file.stored_filename

                            ?

                            <img

                            src={
                            `http://127.0.0.1:8000/uploads/${file.stored_filename}`
                            }

                            alt={file.filename}

                            />

                            :


                            <span>

                            {
                                getIcon(
                                file.file_type
                                )
                            }

                            </span>


                        }



                        </div>






                        <div className="file-info">


                            <strong>

                                {file.filename}

                            </strong>



                            <small>

                                {file.file_type}

                            </small>



                            {

                            file.created_at &&

                            <small>

                            {
                                new Date(
                                file.created_at
                                )
                                .toLocaleDateString()
                            }

                            </small>


                            }



                        </div>





                    </div>



                ))

            }


            </div>



        </div>


    );



}


export default UploadedFiles;
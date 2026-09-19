const API_URL = "http://localhost:8000";


export async function uploadFile(
    sessionId,
    file
){

    const formData = new FormData();

    formData.append(
        "session_id",
        sessionId
    );

    formData.append(
        "file",
        file
    );


    const response = await fetch(
        `${API_URL}/upload`,
        {
            method:"POST",
            body:formData,
            credentials:"include"
        }
    );


    return await response.json();
}



export async function sendMessage(
    sessionId,
    message
){

    const response = await fetch(
        `${API_URL}/chat`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                session_id:sessionId,
                message:message

            }),

            credentials:"include"
        }
    );


    return await response.json();
}

export async function getUploadedFiles(sessionId){

    const token =
    localStorage.getItem("token");


    const response =
    await fetch(
        `${API_URL}/api/sessions/${sessionId}/files`,
        {
            headers:{
                Authorization:
                `Bearer ${token}`
            }
        }
    );


    if(!response.ok){
        return [];
    }


    return await response.json();

}
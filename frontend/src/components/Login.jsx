import { useState } from "react";
import "./../App.css";


function Login({ onLogin }) {


const [username,setUsername] = useState("");
const [password,setPassword] = useState("");

const [error,setError] = useState("");

const [loading,setLoading] = useState(false);





async function submit(e){

e.preventDefault();


setError("");



// ----------------------
// FIELD VALIDATION
// ----------------------

if(!username && !password){

setError(
"Username and password are required"
);

return;

}


if(!username){

setError(
"Username is required"
);

return;

}


if(!password){

setError(
"Password is required"
);

return;

}



setLoading(true);



const formData = new FormData();


formData.append(
"username",
username
);


formData.append(
"password",
password
);





try{


const res = await fetch(

"http://127.0.0.1:8000/login",

{
method:"POST",
body:formData
}

);




let data;


try{

data = await res.json();

}

catch{

data = {};

}




// ----------------------
// SUCCESS
// ----------------------

if(res.ok){


localStorage.setItem(

"token",

data.access_token

);



onLogin(

data.access_token

);



}

else{


// ----------------------
// WRONG LOGIN
// ----------------------

if(
res.status === 401 ||
res.status === 400
){


setError(
"Incorrect username or password"
);


}

else{


setError(
data.detail || "Login failed"
);


}



}



}

catch(err){


setError(
"Unable to connect to server"
);


}



setLoading(false);



}







return (

<div className="login-page">


<div className="login-glow"></div>



<form

className="login-card"

onSubmit={submit}

>




<div className="logo">

🤖

</div>




<h1>

HAL

</h1>



<p>

AI Customer Support Assistant

</p>







<input


placeholder="Username"


value={username}


onChange={
e=>setUsername(e.target.value)
}


/>







<input


type="password"


placeholder="Password"


value={password}


onChange={
e=>setPassword(e.target.value)
}


/>









{
error &&

<div className="error">

{error}

</div>

}









<button

disabled={loading}

>


{

loading

?

"Signing in..."

:

"Login"

}


</button>





</form>



</div>

)



}


export default Login;
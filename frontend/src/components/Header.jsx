function Header({logout}){

return (

<div className="header">

<h2>
HAL Support Bot
</h2>


<button 
className="logout-btn"
onClick={logout}
>
Logout
</button>


</div>

)

}


export default Header;
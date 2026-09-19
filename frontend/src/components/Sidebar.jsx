import { useState } from "react";
import "./../App.css";
import UploadedFiles from "./UploadedFiles";


function Sidebar({
    sessions,
    newChat,
    openSession,
    deleteChat,
    sessionId
}) {

    const [collapsed, setCollapsed] = useState(false);


    return (

        <div className={collapsed ? "sidebar collapsed" : "sidebar"}>


            <div className="sidebar-top">


                <button
                    className="collapse-btn"
                    onClick={() => setCollapsed(!collapsed)}
                >
                    ☰
                </button>


                {!collapsed && (
                    <h2>
                        HAL
                    </h2>
                )}


            </div>





            <button
                className="new-chat-btn"
                onClick={newChat}
            >

                {
                    collapsed
                        ? "+"
                        : "+ New Chat"
                }

            </button>






            {!collapsed && (

                <div className="sidebar-heading">

                    Chats

                </div>

            )}







            <div className="history">


                {
                    sessions.map((chat, index) => (


                        <div

                            key={chat.session_id}

                            className="chat-item"

                            onClick={() =>
                                openSession(chat.session_id)
                            }

                        >



                            <div className="chat-info">


                                <div className="chat-icon">

                                    ✈

                                </div>





                                {

                                    !collapsed &&

                                    <div className="chat-text">


                                        <span>

                                            {
                                                chat.title ||
                                                "New Conversation"
                                            }

                                        </span>



                                        <small>

                                            #{index + 1}

                                        </small>


                                    </div>

                                }



                            </div>






                            {

                                !collapsed &&


                                <button

                                    className="delete-btn"


                                    onClick={(e) => {


                                        e.stopPropagation();


                                        deleteChat(
                                            chat.session_id
                                        );


                                    }}

                                >

                                    🗑


                                </button>

                            }



                        </div>


                    ))

                }


            </div>







            {
                !collapsed && sessionId &&

                <UploadedFiles
                    sessionId={sessionId}
                />

            }




        </div>

    );

}


export default Sidebar;
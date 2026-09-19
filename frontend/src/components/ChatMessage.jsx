import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


function VisionCard({ vision }) {

  if (!vision) return null;


  return (
    <div className="vision-card">

      <div className="vision-title">
        🖼️ Image Analysis
      </div>


      <div className="vision-item">
        📂 <b>File</b>
        <br />
        1. {extractLine(vision, "Filename")}
      </div>



      <div className="vision-item">
        🔍 <b>Type</b>
        <br />
        2. {extractLine(vision, "Image Type")}
      </div>



      <div className="vision-item">
        ⚙️ <b>Technical Analysis</b>
        <br />

        <div className="vision-text">
          {extractLine(
            vision,
            "Analysis"
          )}
        </div>

      </div>


    </div>
  );
}



function extractLine(text, key) {

  if (!text) return "";


  const index = text.indexOf(key);


  if (index === -1)
    return text;



  return text
    .substring(index + key.length)
    .replace(":", "")
    .trim()
    .split("\n\n")[0];

}



function ChatMessage({
  role,
  message,
  vision_context
}) {


  return (

    <div
      className={
        role === "user"
          ? "message user"
          : "message bot"
      }
    >


      {
        role !== "user" && vision_context && (

          <VisionCard
            vision={vision_context}
          />

        )
      }



      <ReactMarkdown
        remarkPlugins={[
          remarkGfm
        ]}
      >

        {message}

      </ReactMarkdown>



    </div>

  );
}



export default ChatMessage;
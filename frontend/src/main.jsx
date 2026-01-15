import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)



/*


create the screen

create template for title + value box + refresh button

times n for how many sensors you want


payload_temp formatter that holds current_temp - get_temp()

payload_humid formatter that holds current_humid - get_humid()


response_temp-> sends payload to blueOS then 200 OK response
response_humid -> sends payload to blueOS then 200 OK response
LOG the 200 response

create a script that install all the dependencies and runs the frontend server

*/
import {StrictMode} from "react";
import {createRoot} from "react-dom/client";
import App from "./App.jsx";
import "./index.scss";

//import * as bootstrap from "bootstrap";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <App/>
    </StrictMode>,
);

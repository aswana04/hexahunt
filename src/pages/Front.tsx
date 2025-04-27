import React from "react";
import { motion } from "framer-motion";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import hexcentLogo from "./hexcent.png"; // Ensure the logo is correct
import "./front.css";

const App: React.FC = () => {
    const navigate = useNavigate();
    const handleButtonClick = () => {
        navigate("/Form");
        console.log("Button clicked! Navigating to job search...");
      };
return (
<div className="about-us-container">
{/* Logo */}
<motion.img
src={hexcentLogo}
alt="Hexcent Logo"
className="hexcent-logo"
initial={{ opacity: 0, y: -20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 1 }}
/>

{/* Main Content */}
<motion.div
className="content"
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 1, delay: 0.5 }}
>
<h1 className="title">Welcome to Hexcent Job Portal</h1>
<p className="description">
Let your resume speak — we’ll match you with jobs that truly fit your skills.</p>
<button className="cta-button" onClick={handleButtonClick}>Find Your Job</button>
</motion.div>
</div>
);
};

export default App;
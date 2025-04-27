import React from "react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./pages/form"; // Form Page
import job from "./pages/Job"; // Job Page


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} /> {/* This is your form page */}
        <Route path="/job" element={<job />} /> {/* This is your job listing page */}
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);

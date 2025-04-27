import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Form from "./pages/form"; // Form Page
import App from "./pages/Front";
import Job from "./pages/Job"; // Job Page
import Course from "./pages/Course"; // Job Page
import AdminLogin from "./pages/AdminLogin";
import Admin from "./pages/Admin";
import Overview from "./pages/Overview";
import Loading from "./pages/Loading";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} /> {/* This is your form page */}
        <Route path="/job" element={<Job />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/form" element={<Form/>} />
        <Route path="/course" element={<Course />} /> {/* This is your job listing page */}
        <Route path="/AdminLogin" element={<AdminLogin />} />
        <Route path="/Overview" element={<Overview />} />
        <Route path="/Loading" element={<Loading />} />
        
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);

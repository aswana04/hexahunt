import React from "react";
import "./App.css";
import logo from "./hexcent.png";  // Importing the logo image

const App: React.FC = () => {
  return (
    <div className="page-container">
      {/* Animated Background Circles */}
      <ul className="circles">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ul>

      {/* Header Section */}
      <header className="header">
        <div className="logo">
          <img src={logo} alt="Logo" className="logo-icon" /> {/* Using imported logo */}
          <h2>Hexahunt</h2>
        </div>
        <button className="home-button">🏠</button> {/* Home emoji button */}
      </header>

      {/* Main Content Container */}
      <div className="app-container">
        {/* Unified Form Container */}
        <div className="form-container">
          <h3>Submit Your Information</h3>
          
          {/* Resume Upload Field */}
          <label htmlFor="resume-upload" className="upload-box">
            <div className="upload-icon">📄</div>
            <p>Drag & Drop or Click to Upload Your Resume</p>
          </label>
          <input type="file" id="resume-upload" className="file-input" />

          {/* Location Preference Field */}
          <div className="additional-fields">
            <label htmlFor="location">Preferred Location:</label>
            <input
              type="text"
              id="location"
              name="location"
              className="input-field"
              placeholder="Enter your preferred location"
            />
          </div>

          {/* Salary Expectations Field */}
          <div className="additional-fields">
            <label htmlFor="salary">Salary Expectations:</label>
            <input
              type="text"
              id="salary"
              name="salary"
              className="input-field"
              placeholder="Enter your expected salary"
            />
          </div>

          {/* Submit Button */}
          <button className="submit-btn">Submit</button>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">© 2025 Hexcent. All rights reserved.</footer>
    </div>
  );
};

export default App;

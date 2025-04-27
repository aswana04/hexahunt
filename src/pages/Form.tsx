import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./form.css";
import logo from "./hexcent.png";
import { Menu } from "lucide-react";

const Form: React.FC = () => {
  const [location, setLocation] = useState("");
  const [job, setJob] = useState("");
  const [resume, setResume] = useState<File | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  const [errors, setErrors] = useState({
    location: "",
    job: "",
    resume: "",
  });

  const navigate = useNavigate();

  const handleLocationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setLocation(value);

    // Clear error when a valid location is selected
    if (value) {
      setErrors((prev) => ({ ...prev, location: "" }));
    }
  };

  const handleJobChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setJob(value);

    if (value && !/^[a-zA-Z\s]*$/.test(value)) {
      setErrors((prev) => ({ ...prev, job: "Only letters are allowed." }));
    } else {
      setErrors((prev) => ({ ...prev, job: "" }));
    }
  };

  const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setResume(e.target.files[0]);
      setErrors((prev) => ({ ...prev, resume: "" }));
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!resume) {
      setErrors((prev) => ({ ...prev, resume: "Please upload your resume." }));
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("location", location);
    formData.append("job", job);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response data from backend:", data);

      if (data.success) {
        console.log("Upload successful:", data.message);
        navigate("/job", { state: { jobs: data.matching_jobs } });
      } else {
        console.error("Upload failed:", data.message);
      }
    } catch (error) {
      console.error("Error uploading data:", error);
    }
  };

  const parseResume = async (file: File): Promise<string[]> => {
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await fetch("http://localhost:5000/parse", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend Response:", data);

      if (data.success && data.unmatched_keywords && data.unmatched_keywords.length > 0) {
        return data.unmatched_keywords;
      } else {
        console.log("No keywords found in the resume.");
        return [];
      }
    } catch (err) {
      console.error("Error during resume parsing:", err);
      return [];
    }
  };

  const handleCourseLinkClick = async (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();

    if (!resume) {
      setErrors((prev) => ({
        ...prev,
        resume: "Please upload your resume before proceeding.",
      }));
      return;
    }

    try {
      const keywords = await parseResume(resume);
      console.log("Keywords from resume:", keywords);

      if (keywords.length > 0) {
        navigate("/course", { state: { keywords } });
      } else {
        setErrors((prev) => ({
          ...prev,
          resume: "No keywords found in the resume.",
        }));
      }
    } catch (error) {
      console.error("Error parsing resume:", error);
      setErrors((prev) => ({
        ...prev,
        resume: "An error occurred while processing the resume.",
      }));
    }
  };

  return (
    <div className="page-container">
      <ul className="circles">
        <li></li><li></li><li></li><li></li><li></li>
        <li></li><li></li><li></li><li></li><li></li>
      </ul>

      <header className="header">
        <div className="logo">
          <img src={logo} alt="Logo" className="logo-icon" />
        </div>

        <section className="content">
          <h2 className="wave-text">HEXAHUNT</h2>
          <h2 className="wave-text">HEXAHUNT</h2>
        </section>

        <div className="menu-container">
          <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)}>
            <Menu size={24} />
          </button>

          {menuOpen && (
            <div className="dropdown-menu">
              <button className="dropdown-item" onClick={() => navigate("/AdminLogin")}>
                Admin Login
              </button>
              <button className="dropdown-item" onClick={() => navigate("/")}>
                Exit
              </button>
            </div>
          )}
        </div>
      </header>

      <div className="content-container">
        <p className="cursor">Explore Opportunities with Hexcent!</p>

        <div className="form-container">
          <h3>Submit Your Resume</h3>
          <form onSubmit={handleSubmit}>
            {/* Resume Upload */}
            <label htmlFor="resume-upload" className="upload-box">
              <div className="upload-icon">📄</div>
              <p>Click to Upload Your Resume</p>
            </label>
            <input
              type="file"
              id="resume-upload"
              className="file-input"
              onChange={handleResumeUpload}
              accept=".pdf,.doc,.docx"
            />
            {resume && <p className="file-name">Selected File: {resume.name}</p>}
            {errors.resume && <p className="error-message">{errors.resume}</p>}

            {/* Location Dropdown */}
            <div className="input-field-container">
              <label htmlFor="location">Preferred Location (optional):</label>
              <select
                id="location"
                className="input-field"
                value={location}
                onChange={handleLocationChange}
              >
                <option value="">Select a Location</option>
                <option value="calicut">Calicut</option>
                <option value="mumbai">Mumbai</option>
                <option value="bangalore">Bangalore</option>
                <option value="chennai">Chennai</option>
                <option value="hyderabad">Hyderabad</option>
                <option value="kochi">Kochi</option>
                <option value="trivandrum">Trivandrum</option>
              </select>
              {errors.location && <p className="error-message">{errors.location}</p>}
            </div>

            {/* Job Expectations Input */}
            <div className="input-field-container">
              <label htmlFor="job">Job Expectations (optional):</label>
              <input
                type="text"
                id="job"
                className="input-field"
                value={job}
                onChange={handleJobChange}
                placeholder="Enter your expected job"
              />
              {errors.job && <p className="error-message">{errors.job}</p>}
            </div>

            {/* Link to course */}
            <div className="link-container">
              <Link
                to="/course"
                className="help-link"
                onClick={handleCourseLinkClick}
              >
                Looking for new courses?
              </Link>
            </div>

            {/* Submit Button */}
            <button type="submit" className="submit-btn">
              Submit
            </button>
          </form>
        </div>
      </div>

      <footer className="footer">© 2025 Hexcent. All rights reserved.</footer>
    </div>
  );
};

export default Form;

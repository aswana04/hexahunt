import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";  // Correct import
import { FaArrowLeft } from "react-icons/fa"; // For the back icon
import "./course.css";

// Mock data to simulate course recommendations
const courseRecommendations = [
  { id: 1, keyword: "React for Beginners", provider: "Hexcent", location: "Online" },
  { id: 2, keyword: "Data Science with Python", provider: "Hexcent", location: "Online" },
  { id: 3, keyword: "UX/UI Design Fundamentals", provider: "Hexcent", location: "Online" },
  { id: 4, keyword: "Product Management Masterclass", provider: "Hexcent", location: "Online" },
  { id: 5, keyword: "Full Stack Web Development", provider: "Hexcent", location: "Online" },
];

const Course = () => {
  const [courses, setCourses] = useState(courseRecommendations);
  const navigate = useNavigate(); // Initialize the navigate function

  useEffect(() => {
    setCourses((prevCourses) => [...prevCourses].sort((a, b) => a.keyword.localeCompare(b.keyword)));
  }, []);

  const handleBackClick = () => {
    navigate("/form"); // Navigates to the form page
  };

  const handleWebsiteClick = () => {
    window.open("https://hexcent.in/course.html", "_blank"); // Opens the website in a new tab
  };

  return (
    <div className="app-container">
      {/* Animated Background */}
      <div className="area">
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
      </div>

      {/* Header Section */}
      <header className="app-header">
        <h1>Course Recommendations</h1>
        <div className="back-icon" onClick={handleBackClick}>
          <FaArrowLeft size={30} color="#fff" />
        </div>
      </header>

      {/* Course List Section with Scroll */}
      <main className="course-list" style={{ maxHeight: '500px', overflowY: 'auto' }}>
        {courses.map((course) => (
          <div className="course-card" key={course.id}>
            <h2>{course.keyword}</h2> {/* Replaced title with keyword */}
            <p className="provider">{course.provider}</p>
            <p className="location">{course.location}</p>
            {/* Removed the skills part */}
      
          </div>
        ))}
      </main>

      <div className="website-button">
        <button onClick={handleWebsiteClick} className="go-to-website-btn">Go to Website</button>
      </div>
    </div>
  );
};

export default Course;

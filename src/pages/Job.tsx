import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import "./job.css";

interface Job {
  title: string;
  company?: string;
  location?: string;
  skills?: string[];
  link?: string; // <-- Added link inside Job
}

const Job = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const rawJobs = location.state?.jobs || [];
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    console.log("Navigated with jobs:", rawJobs);

    const formattedJobs: Job[] = rawJobs.map((item: any) => ({
      title: item.Title || "Untitled Job",
      company: item.Company || "Unknown Company",
      location: item.Location || "Not specified",
      skills: typeof item.Skills === "string"
        ? item.Skills.split(",").map((s: string) => s.trim())
        : [],
      link: item.Link || "", // <-- Extract link from each job
    }));

    setJobs(
      formattedJobs.sort((a, b) => a.title.localeCompare(b.title))
    );
  }, [rawJobs]);

  const handleBackClick = () => {
    navigate("/form");
  };

  return (
    <div className="app-container">
      <div className="area">
        <ul className="circles">
          <li></li><li></li><li></li><li></li><li></li>
          <li></li><li></li><li></li><li></li><li></li>
        </ul>
      </div>

      <header className="app-header">
        <h1>Job Recommendations</h1>
        <div className="back-icon" onClick={handleBackClick}>
          <FaArrowLeft size={30} color="#fff" />
        </div>
      </header>

      <main className="job-list">
        {jobs.length === 0 ? (
          <p className="no-jobs">No matching jobs found.</p>
        ) : (
          jobs.map((job, index) => (
            <div className="job-card" key={index}>
              <h2>{job.title}</h2>
              <p className="company">{job.company}</p>
              <p className="location">{job.location}</p>
              <p className="skills">
                <strong>Skills:</strong>{" "}
                {Array.isArray(job.skills) && job.skills.length > 0
                  ? job.skills.join(", ")
                  : "Not specified"}
              </p>
              {/* NEW: Display link if available */}
              {job.link && (
        <p className="link">
          <strong>Link:</strong>{" "}
        <a href={job.link} target="_blank" rel="noopener noreferrer"><strong>Apply Now</strong></a>
        </p>
        )}

            </div>
          ))
        )}
      </main>
    </div>
  );
};

export default Job;

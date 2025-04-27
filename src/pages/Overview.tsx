import React, { useEffect, useState, useCallback } from 'react';
import './Overview.css';
import { useNavigate } from 'react-router-dom';

interface Job {
  'Job Number': number;
  'Title': string;
  'Company': string;
  'Skills': string;
  'Link': string;
}

const Overview: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1); // Start with page 1

  const navigate = useNavigate();

  // Function to fetch jobs from the Flask backend
  const fetchJobs = useCallback(() => {
    if (loading) return; // Prevent multiple requests at the same time

    setLoading(true); // Set loading state to true

    // Adjust URL to include the current page number in query parameters
    fetch(`http://localhost:5000/fetch_job_list?page=${page}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          setJobs((prevJobs) => [...prevJobs, ...data]);  // Append new jobs to the list
          setPage((prevPage) => prevPage + 1);  // Increment the page for the next fetch
        }
      })
      .catch((error) => console.error('Error fetching jobs:', error))
      .finally(() => setLoading(false));  // Set loading state to false once request is complete
  }, [loading, page]);

  // Detect when the user has scrolled to the bottom of the page
  const handleScroll = () => {
    const bottom = window.innerHeight + document.documentElement.scrollTop === document.documentElement.offsetHeight;
    if (bottom && !loading) {
      fetchJobs();  // Trigger fetching jobs when at the bottom
    }
  };

  useEffect(() => {
    fetchJobs(); // Initial fetch of jobs
    window.addEventListener('scroll', handleScroll); // Listen for scroll events

    return () => {
      window.removeEventListener('scroll', handleScroll); // Clean up the scroll event listener
    };
  }, [fetchJobs]);

  return (
    <div className="overview-wrapper">
      <div className="overview-dashboard">
        <button
          className="back-button"
          onClick={() => navigate('/admin')} // Navigate to admin page
        >
          ⇐
        </button>

        <h1>Web Scraping Overview</h1>
        <div className="job-cards-container">
          {jobs.length === 0 ? (
            <p>No jobs found or data is still loading.</p>
          ) : (
            jobs.map((job) => (
              <div key={job['Job Number']} className="job-card">
                <h2>{job.Title}</h2>
                <p>{job.Company}</p>
                <p>Skills: {job.Skills}</p>
                <a href={job.Link} target="_blank" rel="noopener noreferrer">
                  Apply Here
                </a>
              </div>
            ))
          )}
        </div>
        {loading && <p>Loading more jobs...</p>} {/* Show loading text */}
        <div className="pagination-info">
          <p>Page: {page}</p> {/* Display current page number */}
        </div>
      </div>
    </div>
  );
};

export default Overview;

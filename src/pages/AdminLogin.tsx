import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./AdminLogin.css";

const AdminLogin = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Hook for navigation

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === "admin@gmail.com" && password === "admin1234") {
      console.log("Login successful");
      navigate("/admin"); // Redirect to admin page
  } else {
      console.log("Invalid username or password");
      // Show an error message to the user
  }
  };

  return (      
    <div>{/* Back button */}
      <button className="back-button" onClick={() => navigate("/Form")}>
        ← Back
      </button>


      <div className="container">
      <div className="top"></div>
      <div className="center">
        <h2>Please Sign In</h2>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>
      </div>
      <div className="bottom"></div>
    </div>
    </div>
  );
};

export default AdminLogin;

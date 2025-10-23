import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

export default function ShortenForm({ getAccessToken, setShortUrl }) {
  const [longUrl, setLongUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { loginWithRedirect } = useAuth0();

  const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

  // Validate URL
  const isValidUrl = (url) => {
    try {
      const parsed = new URL(url);
      return parsed.protocol === "http:" || parsed.protocol === "https:";
    } catch {
      return false;
    }
  };

  // Update error state whenever longUrl changes
  useEffect(() => {
    if (!longUrl) {
      setError("");
    } else if (!isValidUrl(longUrl)) {
      setError("Please enter a valid URL (http or https).");
    } else {
      setError("");
    }
  }, [longUrl]);

  const handleShorten = async () => {
    setLoading(true);
    try {
      const token = await getAccessToken();

      const response = await axios.post(
        `${backendUrl}/shorten`,
        { long_url: longUrl },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShortUrl(response.data.short_url);
      setLongUrl(""); // clear input
    } catch (err) {
        // Token expired or invalid
      if (err.response && err.response.status === 401) {
        console.warn("⚠️ Token expired or invalid, reauthenticating...");
        await loginWithRedirect(); // or handle silently if desired
      } else {
        console.error(err);
        setError("Error shortening URL. Try again.");
      }
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <input
        style={{ ...styles.input, borderColor: error ? "#f44336" : "#ccc" }}
        type="text"
        placeholder="Enter long URL"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
      />
      <button
        style={{ ...styles.button, background: isValidUrl(longUrl) ? "#1976d2" : "#ccc", cursor: isValidUrl(longUrl) ? "pointer" : "not-allowed" }}
        onClick={handleShorten}
        disabled={!isValidUrl(longUrl) || loading}
      >
        {loading ? "Shortening..." : "Shorten"}
      </button>
      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "0.5rem",
    marginBottom: "1rem",
    marginTop: "1rem"
  },
  input: {
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    width: "300px",
    borderRadius: "4px",
    border: "1px solid #ccc"
  },
  button: {
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "none",
    color: "white",
    transition: "background 0.2s",
  },
  error: {
    color: "#f44336",
    fontSize: "0.9rem",
    marginTop: "0.2rem"
  }
};

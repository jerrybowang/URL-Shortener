import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import { commonStyles } from "../styles/commonStyles";

export default function ShortenForm({ getAccessToken, setShortUrl }) {
  const [longUrl, setLongUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { isAuthenticated, loginWithRedirect } = useAuth0();

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

  // Update error when URL changes
  useEffect(() => {
    if (!longUrl) setError("");
    else if (!isValidUrl(longUrl)) setError("Please enter a valid URL (http or https).");
    else setError("");
  }, [longUrl]);

  const handleShorten = async () => {
    setLoading(true);
    try {
      let headers = { "Content-Type": "application/json" };
      if (isAuthenticated && getAccessToken) {
        try {
          const token = await getAccessToken();
          headers.Authorization = `Bearer ${token}`;
        } catch (err) {
          console.warn("⚠️ Could not get access token, reauthenticating...");
          await loginWithRedirect();
          return;
        }
      }

      const response = await axios.post(
        `${backendUrl}/shorten`,
        { long_url: longUrl },
        { headers }
      );

      setShortUrl(response.data.short_url);
      setLongUrl(""); // clear input
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        setError("You need to log in to shorten URLs with customization.");
      } else {
        setError("Error shortening URL. Try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={commonStyles.container}>
      <input
        style={{
          ...commonStyles.input,
          borderColor: error ? "#f44336" : "#ccc",
        }}
        type="text"
        placeholder="Enter long URL"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
      />

      <button
        style={{
          ...commonStyles.button,
          background: isValidUrl(longUrl) ? "#1976d2" : "#ccc",
          cursor: isValidUrl(longUrl) ? "pointer" : "not-allowed",
        }}
        onClick={handleShorten}
        disabled={!isValidUrl(longUrl) || loading}
      >
        {loading ? "Shortening..." : "Shorten"}
      </button>

      {error && <p style={commonStyles.error}>{error}</p>}
    </div>
  );
}
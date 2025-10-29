import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import { commonStyles } from "../styles/commonStyles";

export default function CustomShortenForm({ getAccessToken, setShortUrl }) {
  const [longUrl, setLongUrl] = useState("");
  const [alias, setAlias] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { user, loginWithRedirect } = useAuth0();

  const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

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

  const handleShorten = async (overwrite = false) => {
    setLoading(true);
    setError("");
    try {
      let token;
      try {
        token = await getAccessToken();
      } catch (authErr) {
        console.error("Auth0 token error", authErr);
        setError("Session expired. Please log in again.");
        loginWithRedirect();
        return;
      }

      const response = await axios.post(
        `${backendUrl}/shorten/custom`,
        { 
          long_url: longUrl, 
          custom_alias: alias,
          user_name: user.sub
        },
        {
          headers: { Authorization: `Bearer ${token}` },
          params: { overwrite },
        }
      );

      setShortUrl(response.data.short_url);
      setLongUrl("");
      setAlias("");
    } catch (err) {
      console.error(err);
      handleError(err);

    } finally {
      setLoading(false);
    }
  };

  const handleError = async (error) => {
    if (!error.response) {
      setError("Network error. Please check your connection.");
      return;
    }

    const { status, data, config } = error.response;
    const requestUrl = config.url || "";

    // Backend conflict (409)
    if (status === 409 && requestUrl.includes("/shorten")) {
      const detail = data?.detail;
      if (detail && typeof detail === "object" && detail.can_overwrite) {
        const confirmOverwrite = window.confirm(
          "You already own this alias. Do you want to overwrite the existing short link?"
        );
        if (confirmOverwrite) {
          await handleShorten(true);
          return;
        } else {
          setError("Alias already exists. Try another one.");
          return;
        }
      }
      setError("Alias already taken by another user.");
      return;
    }

    // Other backend errors
    if (requestUrl.includes("/shorten")) {
      setError(`Unexpected backend error (${status}): ${data?.detail || "Unknown"}`);
      return;
    }

    // Fallback
    setError(`Unexpected error (${status}) from ${requestUrl}`);
  };


  return (
    <div style={commonStyles.container}>
      <input
        style={{ ...commonStyles.input, borderColor: error ? "#f44336" : "#ccc" }}
        type="text"
        placeholder="Enter long URL"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
      />
      <input
        style={commonStyles.input}
        type="text"
        placeholder="Custom alias (optional)"
        value={alias}
        onChange={(e) => setAlias(e.target.value)}
      />
      <button
        style={{
          ...commonStyles.button,
          background: isValidUrl(longUrl) ? "#1976d2" : "#ccc",
        }}
        onClick={() => handleShorten(false)}
        disabled={!isValidUrl(longUrl) || loading}
      >
        {loading ? "Shortening..." : "Shorten"}
      </button>
      {error && <p style={commonStyles.error}>{error}</p>}
    </div>
  );
}

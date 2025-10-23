import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import AuthButtons from "./components/AuthButtons";
import ShortenForm from "./components/ShortenForm";
import CustomShortenForm from "./components/CustomShortenForm";
import ShortUrlDisplay from "./components/ShortUrlDisplay";

export default function App() {
  const { isAuthenticated, user, getAccessTokenSilently } = useAuth0();
  const [shortUrl, setShortUrl] = useState("");

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>✨ URL Shortener</h1>

      <AuthButtons />

      {isAuthenticated ? (
        <>
          <p>Welcome, <b>{user.name}</b>!</p>
          <CustomShortenForm
            getAccessToken={getAccessTokenSilently}
            setShortUrl={setShortUrl}
          />
          <ShortUrlDisplay shortUrl={shortUrl} />
        </>
      ) : (
        <>
          <p>You can shorten URLs without logging in 👇</p>
          <p>For Custom alias, please login</p>
          <ShortenForm setShortUrl={setShortUrl} />
          <ShortUrlDisplay shortUrl={shortUrl} />
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    textAlign: "center",
    marginTop: "5rem",
    padding: "2rem"
  },
  title: {
    fontSize: "2.5rem",
    marginBottom: "2rem",
    color: "#1976d2"
  }
};

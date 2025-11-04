import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import AuthButtons from "./components/AuthButtons";
import LinkAccountButton from "./components/LinkAccountButton";
import ShortenForm from "./components/ShortenForm";
import CustomShortenForm from "./components/CustomShortenForm";
import ShortUrlDisplay from "./components/ShortUrlDisplay";
import useAuth0AccountLink from "./hooks/useAuth0AccountLink";

export default function App() {
  const { isAuthenticated, user, getAccessTokenSilently, getIdTokenClaims, loginWithRedirect } =
    useAuth0();
  const [shortUrl, setShortUrl] = useState("");

  const { linkMessage, linkError } = useAuth0AccountLink({
    isAuthenticated,
    user,
    getIdTokenClaims,
    getAccessTokenSilently,
    loginWithRedirect,
  });

  useEffect(() => {
    if (!isAuthenticated && sessionStorage.getItem("auth0.linking_flag") != "true") {
      sessionStorage.removeItem("auth0.linking_flag");
      sessionStorage.removeItem("auth0.primary_sub");
    }
  }, [isAuthenticated]);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>✨ URL Shortener</h1>

      <AuthButtons />

      {linkMessage && <div style={{ color: "green" }}>{linkMessage}</div>}
      {linkError && <div style={{ color: "red" }}>{linkError}</div>}

      {isAuthenticated ? (
        <>
          <p>
            Welcome, <b>{user.name}</b>!
          </p>
          <LinkAccountButton />
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
    padding: "2rem",
  },
  title: {
    fontSize: "2.5rem",
    marginBottom: "2rem",
    color: "#1976d2",
  },
};

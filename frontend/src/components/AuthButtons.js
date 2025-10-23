import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

export default function AuthButtons() {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();

  if (!isAuthenticated) {
    return <button style={styles.button} onClick={() => loginWithRedirect()}>Log In</button>;
  }

  return (
    <button style={{ ...styles.button, background: "#f44336" }} onClick={() => logout({ returnTo: window.location.origin })}>
      Log Out
    </button>
  );
}

const styles = {
  button: {
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "none",
    cursor: "pointer",
    background: "#1976d2",
    color: "white",
    transition: "background 0.2s",
    marginBottom: "1rem"
  }
};

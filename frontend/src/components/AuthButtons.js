import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { commonStyles } from "../styles/commonStyles";

export default function AuthButtons() {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();

  const clearAuthLinkingState = () => {
    sessionStorage.removeItem("auth0.linking_flag");
    sessionStorage.removeItem("auth0.primary_sub");
  };

  if (!isAuthenticated) {
    return (
      <button
        style={commonStyles.button}
        onClick={() => {
          clearAuthLinkingState();
          loginWithRedirect();
        }}
      >
        Log In
      </button>
    );
  }

  return (
    <button
      style={{ ...commonStyles.button, background: "#f44336" }}
      onClick={() => {
        clearAuthLinkingState();
        logout({ returnTo: window.location.origin });
      }}
    >
      Log Out
    </button>
  );
}

import { useEffect, useState } from "react";
import axios from "axios";

export default function useAuth0AccountLink({
  isAuthenticated,
  user,
  getIdTokenClaims,
  getAccessTokenSilently,
  loginWithRedirect,
}) {
  const [linkMessage, setLinkMessage] = useState("");
  const [linkError, setLinkError] = useState("");

  useEffect(() => {
    if (!isAuthenticated || !user) return;

    // Initialize primary identity if missing
    const existingPrimary = sessionStorage.getItem("auth0.primary_sub");
    if (!existingPrimary) {
      sessionStorage.setItem("auth0.primary_sub", user.sub);
    }
  }, [isAuthenticated, user]);

  useEffect(() => {
    async function handleLinking() {
      if (!isAuthenticated || !user) return;

      const linkingFlag = sessionStorage.getItem("auth0.linking_flag");
      if (linkingFlag !== "true") return;

      const primarySub = sessionStorage.getItem("auth0.primary_sub");
      if (!primarySub) {
        setLinkError("Primary identity not found");
        return;
      }

      // Get current login identity (secondary)
      const claims = await getIdTokenClaims();
      const secondarySub = claims.sub;
      const [provider, secondary_user_id] = secondarySub.split("|");

      // Prevent infinite loop:
      if (secondarySub === primarySub) {
        sessionStorage.removeItem("auth0.linking_flag");
        setLinkError("Cannot link with the same identity");
        return;
      }

      const backendUrl =
        process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

      try {
        let token = await getAccessTokenSilently();
        const response = await axios.post(
          `${backendUrl}/api/link-account`,
          {
            primary_user_id: primarySub,
            secondary_user_id,
            provider,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );

        setLinkMessage(response.data.message || "Account linked successfully!");
        setLinkError("");

        // linking succeeded → force refresh
        await loginWithRedirect({
          appState: { afterLink: true },
        });

        // linking succeeded → update stored primary
        sessionStorage.setItem("auth0.primary_sub", primarySub);
      } catch (err) {
        const msg =
          err.response?.data?.message || err.message || "Linking failed";
        setLinkError(msg);
        setLinkMessage("");
      }

      // Always clear linking flag
      sessionStorage.removeItem("auth0.linking_flag");
    }

    handleLinking();
  }, [isAuthenticated, user, getIdTokenClaims]);

  return { linkMessage, linkError };
}

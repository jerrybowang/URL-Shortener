import { useAuth0 } from "@auth0/auth0-react";
import { commonStyles } from "../styles/commonStyles";

export default function LinkAccountButton() {
  const { loginWithRedirect, isAuthenticated } = useAuth0();

  if (!isAuthenticated) return null;

  const linkAccount = () => {
    sessionStorage.setItem("auth0.linking_flag", "true");

    loginWithRedirect({
      authorizationParams: {
        prompt: "login",
        screen_hint: "signup",
        max_age: 0,
      },
      appState: { linking: true },
    });
  };

  return (
    <button style={commonStyles.button} onClick={linkAccount}>
      Add another login method
    </button>
  );
}

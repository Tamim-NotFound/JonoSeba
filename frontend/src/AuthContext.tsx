import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getMyProfile,
  loginCitizen,
  type LoginPayload,
  type UserProfile,
} from "./api/auth";

interface AuthContextValue {
  user: UserProfile | null;
  loading: boolean;
  signIn: (payload: LoginPayload) => Promise<void>;
  signOut: () => void;
}

const TOKEN_STORAGE_KEY = "jonoseba-access-token";

const AuthContext = createContext<AuthContextValue | null>(
  null,
);

function readToken(): string | null {
  try {
    return sessionStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

function storeToken(token: string): void {
  sessionStorage.setItem(TOKEN_STORAGE_KEY, token);
}

function removeToken(): void {
  try {
    sessionStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch {
    // Continue clearing in-memory authentication.
  }
}

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [user, setUser] = useState<UserProfile | null>(
    null,
  );

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function restoreSession() {
      const token = readToken();

      if (!token) {
        if (!cancelled) {
          setLoading(false);
        }
        return;
      }

      try {
        const profile = await getMyProfile(token);

        if (!cancelled) {
          setUser(profile);
        }
      } catch {
        if (!cancelled) {
          removeToken();
          setUser(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void restoreSession();

    return () => {
      cancelled = true;
    };
  }, []);

  async function signIn(
    payload: LoginPayload,
  ): Promise<void> {
    const result = await loginCitizen(payload);

    if (
      result.token_type.toLowerCase() !== "bearer" ||
      !result.access_token
    ) {
      throw new Error("Unexpected authentication response.");
    }

    const profile = await getMyProfile(result.access_token);

    if (!profile.is_active) {
      throw new Error("Your account is not active.");
    }

    try {
      storeToken(result.access_token);
    } catch {
      throw new Error(
        "Browser session storage is unavailable. Please enable it to sign in.",
      );
    }

    setUser(profile);
  }

  function signOut(): void {
    removeToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within AuthProvider.",
    );
  }

  return context;
}
